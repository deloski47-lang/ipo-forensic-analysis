from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import EvidenceItem, IpoIssue, Issuer, ResearchCase
from app.schemas.cases import CaseDetail, CaseListResponse, CaseStatus, CaseSummary, CreateCaseRequest, UpdateCaseRequest
from app.schemas.identity import ConfirmIdentityRequest

router = APIRouter()


def as_detail(case: ResearchCase, db: Session | None = None) -> CaseDetail:
    issue = db.get(IpoIssue, case.issue_id) if db is not None and case.issue_id else None
    issuer = db.get(Issuer, issue.issuer_id) if db is not None and issue is not None else None
    issue_detail = ({
        "issueId": issue.id,
        "issuerLegalName": issuer.legal_name if issuer else None,
        "displayName": issue.display_name,
        "marketSegment": issue.market_segment,
        "openDate": issue.open_date,
        "closeDate": issue.close_date,
        "listingDate": issue.listing_date,
        "priceBandLow": issue.price_band_low,
        "priceBandHigh": issue.price_band_high,
        "issueSizeAmount": issue.issue_size_amount,
        "issueSizeUnit": issue.issue_size_unit,
    } if issue is not None else None)
    return CaseDetail(
        case_id=case.id,
        entered_name=case.entered_name,
        title=case.title,
        case_status=case.case_status,
        identity_status=case.identity_status,
        issue=issue_detail,
        created_at=case.created_at,
        updated_at=case.updated_at,
        last_activity_at=case.last_activity_at,
        latest_analysis_run_id=case.latest_analysis_run_id,
        latest_report_id=case.latest_report_id,
        case_changed_since_last_run=case.case_changed_since_last_run,
        readiness_summary=case.readiness_summary,
        warning_count=case.warning_count,
    )


def find_case(db: Session, case_id: str) -> ResearchCase:
    try:
        canonical_id = str(UUID(case_id))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Research case not found.") from exc
    case = db.get(ResearchCase, canonical_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Research case not found.")
    return case


@router.get("/cases", response_model=CaseListResponse)
def list_cases(
    status: CaseStatus | None = Query(default=None),
    db: Session = Depends(get_db),
) -> CaseListResponse:
    statement = select(ResearchCase)
    if status is not None:
        statement = statement.where(ResearchCase.case_status == status)
    statement = statement.order_by(ResearchCase.last_activity_at.desc(), ResearchCase.id.asc())
    cases = list(db.scalars(statement))
    return CaseListResponse(
        items=[
            CaseSummary(
                case_id=case.id,
                entered_name=case.entered_name,
                title=case.title,
                case_status=case.case_status,
                identity_status=case.identity_status,
                issue_display_name=None,
                last_activity_at=case.last_activity_at,
                latest_analysis_run_id=case.latest_analysis_run_id,
                latest_report_id=case.latest_report_id,
                warning_count=case.warning_count,
            )
            for case in cases
        ],
        total=len(cases),
    )


@router.post("/cases", response_model=CaseDetail, status_code=201)
def create_case(payload: CreateCaseRequest, db: Session = Depends(get_db)) -> CaseDetail:
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    case = ResearchCase(
        entered_name=payload.entered_name,
        title=(payload.title or payload.entered_name)[:160],
        case_status="identity_pending",
        identity_status="unresolved",
        created_at=now,
        updated_at=now,
        last_activity_at=now,
        case_changed_since_last_run=True,
        warning_count=0,
    )
    db.add(case)
    db.commit()
    db.refresh(case)
    return as_detail(case, db)


@router.get("/cases/{case_id}", response_model=CaseDetail)
def get_case(case_id: str, db: Session = Depends(get_db)) -> CaseDetail:
    return as_detail(find_case(db, case_id), db)


@router.patch("/cases/{case_id}", response_model=CaseDetail)
def update_case(case_id: str, payload: UpdateCaseRequest, db: Session = Depends(get_db)) -> CaseDetail:
    case = find_case(db, case_id)
    now = datetime.now(timezone.utc)
    case.title = payload.title
    case.updated_at = now
    case.last_activity_at = now
    case.case_changed_since_last_run = True
    db.commit()
    db.refresh(case)
    return as_detail(case)


@router.post("/cases/{case_id}/archive", response_model=CaseDetail)
def archive_case(case_id: str, db: Session = Depends(get_db)) -> CaseDetail:
    case = find_case(db, case_id)
    now = datetime.now(timezone.utc)
    case.case_status = "archived"
    case.updated_at = now
    case.last_activity_at = now
    db.commit()
    db.refresh(case)
    return as_detail(case)



@router.post("/cases/{case_id}/identity/confirm", response_model=CaseDetail)
def confirm_identity(case_id: str, payload: ConfirmIdentityRequest, db: Session = Depends(get_db)) -> CaseDetail:
    case = find_case(db, case_id)
    if payload.manual_issue is None:
        raise HTTPException(status_code=422, detail="A manual Mainboard issue is required in this build.")
    evidence_ids = payload.identity_evidence_ids
    found = set(db.scalars(
        select(EvidenceItem.id).where(EvidenceItem.case_id == case.id, EvidenceItem.id.in_(evidence_ids))
    ))
    if found != set(evidence_ids):
        raise HTTPException(status_code=422, detail="Every identity evidence item must belong to this research case.")
    manual = payload.manual_issue
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    issuer = Issuer(id=str(uuid4()), legal_name=manual.issuer_legal_name, created_at=now, updated_at=now)
    issue = IpoIssue(
        id=str(uuid4()), issuer_id=issuer.id, display_name=manual.display_name, market_segment="MAINBOARD",
        open_date=manual.open_date.isoformat() if manual.open_date else None,
        close_date=manual.close_date.isoformat() if manual.close_date else None,
        listing_date=manual.listing_date.isoformat() if manual.listing_date else None,
        price_band_low=manual.price_band_low, price_band_high=manual.price_band_high,
        issue_size_amount=manual.issue_size_amount, issue_size_unit=manual.issue_size_unit,
        created_at=now, updated_at=now,
    )
    case.issue_id = issue.id
    case.identity_status = "confirmed"
    case.case_status = "active"
    case.updated_at = now
    case.last_activity_at = now
    case.case_changed_since_last_run = True
    db.add(issuer)
    db.add(issue)
    db.commit()
    db.refresh(case)
    return as_detail(case, db)
