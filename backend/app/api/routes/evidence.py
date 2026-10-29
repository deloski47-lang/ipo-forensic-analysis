from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.models import EvidenceItem as EvidenceModel, ResearchCase
from app.schemas.evidence import CreateEvidenceRequest, EvidenceItem, EvidenceListResponse
from app.schemas.evidence_review import ReviewEvidenceRequest

router = APIRouter()


def parse_uuid(value: str) -> str:
    try:
        return str(UUID(value))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Research resource not found.") from exc


def get_case(db: Session, case_id: str) -> ResearchCase:
    case = db.get(ResearchCase, parse_uuid(case_id))
    if case is None:
        raise HTTPException(status_code=404, detail="Research case not found.")
    return case


def get_evidence(db: Session, case_id: str, evidence_id: str) -> EvidenceModel:
    case = get_case(db, case_id)
    evidence = db.get(EvidenceModel, parse_uuid(evidence_id))
    if evidence is None or evidence.case_id != case.id:
        raise HTTPException(status_code=404, detail="Evidence item not found.")
    return evidence


def serialize(item: EvidenceModel) -> EvidenceItem:
    path = get_settings().data_dir / item.local_relative_path if item.local_relative_path else None
    local_available = bool(path and path.is_file())
    return EvidenceItem(
        evidence_id=item.id,
        case_id=item.case_id,
        source_id=None,
        evidence_kind=item.evidence_kind,
        title=item.title,
        source_url=item.source_url,
        original_file_name=item.original_file_name,
        mime_type=item.mime_type,
        size_bytes=item.size_bytes,
        sha256=item.sha256,
        published_at=item.published_at,
        captured_at=item.captured_at,
        locator=item.locator,
        verification_status=item.verification_status,
        notes=item.notes,
        download_url=f"/api/v1/cases/{item.case_id}/evidence/{item.id}/download" if local_available else None,
        local_available=local_available,
    )


@router.get("/cases/{case_id}/evidence", response_model=EvidenceListResponse)
def list_evidence(case_id: str, db: Session = Depends(get_db)) -> EvidenceListResponse:
    case = get_case(db, case_id)
    items = list(db.scalars(select(EvidenceModel).where(EvidenceModel.case_id == case.id).order_by(EvidenceModel.captured_at.desc())))
    return EvidenceListResponse(items=[serialize(item) for item in items], total=len(items))


@router.post("/cases/{case_id}/evidence", response_model=EvidenceItem, status_code=201)
def create_evidence(case_id: str, payload: CreateEvidenceRequest, db: Session = Depends(get_db)) -> EvidenceItem:
    case = get_case(db, case_id)
    if payload.evidence_kind == "web_page" and payload.source_url is None:
        raise HTTPException(status_code=422, detail="A web page evidence item requires a source URL.")
    now = datetime.now(timezone.utc)
    item = EvidenceModel(
        id=str(uuid4()),
        case_id=case.id,
        evidence_kind=payload.evidence_kind,
        title=payload.title,
        source_url=str(payload.source_url) if payload.source_url else None,
        original_file_name=None,
        mime_type=None,
        size_bytes=None,
        sha256=None,
        published_at=payload.published_at.isoformat().replace("+00:00", "Z") if payload.published_at else None,
        captured_at=now,
        locator=None,
        verification_status="unverified",
        notes=payload.notes,
        local_relative_path=None,
    )
    db.add(item)
    case.last_activity_at = now.isoformat().replace("+00:00", "Z")
    case.updated_at = case.last_activity_at
    case.case_changed_since_last_run = True
    db.commit()
    db.refresh(item)
    return serialize(item)


@router.post("/cases/{case_id}/evidence/files", response_model=EvidenceItem, status_code=201)
async def upload_pdf(
    case_id: str,
    file: UploadFile = File(...),
    title: str | None = Form(default=None, max_length=200),
    source_url: str | None = Form(default=None),
    published_at: datetime | None = Form(default=None),
    notes: str | None = Form(default=None, max_length=10_000),
    db: Session = Depends(get_db),
) -> EvidenceItem:
    case = get_case(db, case_id)
    if notes is not None and len(notes) > 10_000:
        raise HTTPException(status_code=422, detail="Notes must be 10,000 characters or fewer.")
    if source_url:
        from pydantic import TypeAdapter, HttpUrl, ValidationError
        try:
            parsed_url = TypeAdapter(HttpUrl).validate_python(source_url)
            if parsed_url.scheme not in ("http", "https"):
                raise ValueError("Only HTTP and HTTPS URLs are supported.")
        except (ValidationError, ValueError) as exc:
            raise HTTPException(status_code=422, detail="Source URL must be a valid HTTP or HTTPS URL.") from exc
    filename = Path(file.filename or "evidence.pdf").name
    if not filename.lower().endswith(".pdf") or file.content_type not in ("application/pdf", "application/octet-stream", None):
        raise HTTPException(status_code=415, detail="Only PDF evidence files are accepted.")
    settings = get_settings()
    evidence_id = str(uuid4())
    relative = Path("evidence") / case.id / evidence_id / "original.pdf"
    target = settings.data_dir / relative
    target.parent.mkdir(parents=True, exist_ok=False)
    digest = hashlib.sha256()
    size = 0
    try:
        with target.open("xb") as destination:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)
                if size > settings.max_upload_bytes:
                    raise HTTPException(status_code=413, detail="PDF exceeds the configured upload size limit.")
                digest.update(chunk)
                destination.write(chunk)
        if size == 0:
            raise HTTPException(status_code=422, detail="The uploaded PDF is empty.")
        with target.open("rb") as source:
            if source.read(5) != b"%PDF-":
                raise HTTPException(status_code=415, detail="The file does not have a valid PDF header.")
        now = datetime.now(timezone.utc)
        item = EvidenceModel(
            id=evidence_id, case_id=case.id, evidence_kind="uploaded_document",
            title=(title or filename).strip()[:200] or filename,
            source_url=source_url or None, original_file_name=filename, mime_type="application/pdf",
            size_bytes=size, sha256=digest.hexdigest(), published_at=published_at.isoformat().replace("+00:00", "Z") if published_at else None, captured_at=now.isoformat().replace("+00:00", "Z"),
            locator=None, verification_status="unverified", notes=notes,
            local_relative_path=relative.as_posix(),
        )
        db.add(item)
        case.last_activity_at = now.isoformat().replace("+00:00", "Z")
        case.updated_at = case.last_activity_at
        case.case_changed_since_last_run = True
        db.commit()
        db.refresh(item)
        return serialize(item)
    except Exception:
        db.rollback()
        target.unlink(missing_ok=True)
        try:
            target.parent.rmdir()
            target.parent.parent.rmdir()
        except OSError:
            pass
        raise
    finally:
        await file.close()


@router.get("/cases/{case_id}/evidence/{evidence_id}", response_model=EvidenceItem)
def get_evidence_detail(case_id: str, evidence_id: str, db: Session = Depends(get_db)) -> EvidenceItem:
    return serialize(get_evidence(db, case_id, evidence_id))


@router.get("/cases/{case_id}/evidence/{evidence_id}/download")
def download_evidence(case_id: str, evidence_id: str, db: Session = Depends(get_db)) -> FileResponse:
    item = get_evidence(db, case_id, evidence_id)
    if not item.local_relative_path:
        raise HTTPException(status_code=404, detail="This evidence item has no local file.")
    base = get_settings().data_dir.resolve()
    path = (base / item.local_relative_path).resolve()
    if base not in path.parents or not path.is_file():
        raise HTTPException(status_code=404, detail="The original evidence file is unavailable.")
    return FileResponse(path, media_type="application/pdf", filename=item.original_file_name or "evidence.pdf")



@router.post("/cases/{case_id}/evidence/{evidence_id}/review", response_model=EvidenceItem)
def review_evidence(
    case_id: str,
    evidence_id: str,
    payload: ReviewEvidenceRequest,
    db: Session = Depends(get_db),
) -> EvidenceItem:
    item = get_evidence(db, case_id, evidence_id)
    if payload.action == "verify":
        item.verification_status = "user_verified"
    elif payload.action == "mark_conflicted":
        if not payload.rationale or not payload.rationale.strip():
            raise HTTPException(status_code=422, detail="A rationale is required when marking evidence conflicted.")
        item.verification_status = "conflicting"
    else:
        item.verification_status = "rejected"
    if payload.rationale and payload.rationale.strip():
        item.notes = (item.notes + "\n\nReview: " if item.notes else "Review: ") + payload.rationale.strip()
    case = db.get(ResearchCase, item.case_id)
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    if case is not None:
        case.updated_at = now
        case.last_activity_at = now
        case.case_changed_since_last_run = True
    db.commit()
    db.refresh(item)
    return serialize(item)
