from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import EvidenceItem, ResearchCase
from app.schemas.readiness import AnalysisReadiness, ReadinessIssue

router = APIRouter()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def get_case(db: Session, case_id: str) -> ResearchCase:
    case = db.get(ResearchCase, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Research case not found.")
    return case


@router.get("/cases/{case_id}/analysis/readiness", response_model=AnalysisReadiness)
def get_analysis_readiness(
    case_id: str,
    information_cutoff_at: datetime | None = Query(default=None),
    db: Session = Depends(get_db),
) -> AnalysisReadiness:
    case = get_case(db, case_id)
    checked_at = utc_now()
    cutoff = information_cutoff_at or checked_at
    evidence = list(db.scalars(select(EvidenceItem).where(EvidenceItem.case_id == case.id)))
    blockers: list[ReadinessIssue] = []
    warnings: list[ReadinessIssue] = []

    if case.identity_status != "confirmed" or not case.issue_id:
        blockers.append(ReadinessIssue(
            code="IPO_IDENTITY_UNCONFIRMED",
            severity="blocker",
            message="The exact Mainboard IPO identity has not been confirmed.",
            next_action="Add source evidence and confirm the exact Mainboard issue.",
        ))
    if not evidence:
        blockers.append(ReadinessIssue(
            code="NO_EVIDENCE_REGISTERED",
            severity="blocker",
            message="No evidence is registered for this case.",
            next_action="Add official offer documents or source-backed manual evidence.",
        ))
    elif not any(item.evidence_kind == "uploaded_document" for item in evidence):
        warnings.append(ReadinessIssue(
            code="NO_OFFER_DOCUMENT_UPLOADED",
            severity="warning",
            message="No local offer-document PDF is registered.",
            next_action="Upload the RHP/prospectus or another relevant PDF if available.",
        ))
    if not any(item.verification_status == "user_verified" for item in evidence):
        blockers.append(ReadinessIssue(
            code="NO_USER_VERIFIED_EVIDENCE",
            severity="blocker",
            message="Evidence exists, but none has been explicitly marked as reviewed.",
            next_action="Review evidence before using it as an accepted analytical input.",
        ))
    blockers.append(ReadinessIssue(
        code="FORMULA_REGISTRY_NOT_ENABLED",
        severity="blocker",
        message="The approved P0 formula register is not yet enabled; no financial metrics will be calculated.",
        next_action="Complete and test the formula registry before running financial analysis.",
    ))
    warnings.append(ReadinessIssue(
        code="SOURCE_CONNECTORS_NOT_ENABLED",
        severity="warning",
        message="No external source connectors are enabled. Source data must be supplied manually and cited.",
        next_action="Use manual evidence intake; do not interpret missing source data as zero.",
    ))
    status = "blocked" if blockers else ("qualified" if warnings else "ready")
    return AnalysisReadiness(
        case_id=case.id,
        status=status,
        checked_at=checked_at,
        information_cutoff_at=cutoff,
        blockers=blockers,
        warnings=warnings,
        ready_formula_codes=[],
        skipped_formula_codes=[],
        eligible_finding_rule_codes=[],
        skipped_finding_rule_codes=[],
        source_coverage=[],
    )
