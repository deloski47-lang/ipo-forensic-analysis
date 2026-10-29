from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import EvidenceItem, FactRecord as FactModel, ResearchCase
from app.schemas.facts import CreateFactRequest, FactListResponse, FactRecord, ReviewFactRequest

router = APIRouter()


def get_case(db: Session, case_id: str) -> ResearchCase:
    try:
        case_id = str(UUID(case_id))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Research case not found.") from exc
    case = db.get(ResearchCase, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Research case not found.")
    return case


def get_fact(db: Session, case_id: str, fact_id: str) -> FactModel:
    case = get_case(db, case_id)
    try:
        fact_id = str(UUID(fact_id))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Fact record not found.") from exc
    item = db.get(FactModel, fact_id)
    if item is None or item.case_id != case.id:
        raise HTTPException(status_code=404, detail="Fact record not found.")
    return item


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def serialize(item: FactModel) -> FactRecord:
    return FactRecord(
        fact_id=item.id, case_id=item.case_id, indicator_code=item.indicator_code,
        raw_value_text=item.raw_value_text, value_numeric=item.value_numeric, value_text=item.value_text,
        unit=item.unit, currency=item.currency, period_start=item.period_start, period_end=item.period_end,
        as_of_date=item.as_of_date, evidence_id=item.evidence_id, entry_method=item.entry_method,
        review_status=item.review_status, definition_note=item.definition_note,
        recorded_at=item.recorded_at, created_at=item.created_at, reviewed_at=item.reviewed_at,
        review_rationale=item.review_rationale, supersedes_fact_id=item.supersedes_fact_id,
    )


@router.get("/cases/{case_id}/facts", response_model=FactListResponse)
def list_facts(case_id: str, db: Session = Depends(get_db)) -> FactListResponse:
    case = get_case(db, case_id)
    rows = list(db.scalars(select(FactModel).where(FactModel.case_id == case.id).order_by(FactModel.recorded_at.desc())))
    return FactListResponse(items=[serialize(row) for row in rows], total=len(rows))


@router.post("/cases/{case_id}/facts", response_model=FactRecord, status_code=201)
def create_fact(case_id: str, payload: CreateFactRequest, db: Session = Depends(get_db)) -> FactRecord:
    case = get_case(db, case_id)
    evidence = db.get(EvidenceItem, payload.evidence_id)
    if evidence is None or evidence.case_id != case.id:
        raise HTTPException(status_code=422, detail="The evidence item must belong to this research case.")
    now = now_iso()
    item = FactModel(
        id=str(uuid4()), case_id=case.id, indicator_code=payload.indicator_code,
        raw_value_text=payload.raw_value_text, value_numeric=payload.value_numeric, value_text=payload.value_text,
        unit=payload.unit, currency=payload.currency,
        period_start=payload.period_start.isoformat() if payload.period_start else None,
        period_end=payload.period_end.isoformat() if payload.period_end else None,
        as_of_date=payload.as_of_date.isoformat() if payload.as_of_date else None,
        evidence_id=evidence.id, entry_method="manual", review_status="candidate",
        definition_note=payload.definition_note, recorded_at=now, created_at=now,
    )
    db.add(item)
    case.updated_at = now
    case.last_activity_at = now
    case.case_changed_since_last_run = True
    db.commit()
    db.refresh(item)
    return serialize(item)


@router.post("/cases/{case_id}/facts/{fact_id}/review", response_model=FactRecord)
def review_fact(case_id: str, fact_id: str, payload: ReviewFactRequest, db: Session = Depends(get_db)) -> FactRecord:
    item = get_fact(db, case_id, fact_id)
    item.review_status = {"accept": "accepted", "reject": "rejected", "mark_conflicted": "conflicted", "supersede": "superseded"}[payload.action]
    item.reviewed_at = now_iso()
    item.review_rationale = payload.rationale.strip() if payload.rationale else None
    case = db.get(ResearchCase, item.case_id)
    if case:
        case.updated_at = item.reviewed_at
        case.last_activity_at = item.reviewed_at
        case.case_changed_since_last_run = True
    db.commit()
    db.refresh(item)
    return serialize(item)
