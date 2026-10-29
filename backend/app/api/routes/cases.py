from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import ResearchCase
from app.schemas.cases import CaseDetail, CaseListResponse, CaseStatus, CaseSummary, CreateCaseRequest, UpdateCaseRequest

router = APIRouter()


def as_detail(case: ResearchCase) -> CaseDetail:
    return CaseDetail(
        case_id=case.id,
        entered_name=case.entered_name,
        title=case.title,
        case_status=case.case_status,
        identity_status=case.identity_status,
        issue=None,
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
    now = datetime.now(timezone.utc)
    case = ResearchCase(
        entered_name=payload.entered_name,
        title=payload.title or payload.entered_name,
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
    return as_detail(case)


@router.get("/cases/{case_id}", response_model=CaseDetail)
def get_case(case_id: str, db: Session = Depends(get_db)) -> CaseDetail:
    return as_detail(find_case(db, case_id))


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
