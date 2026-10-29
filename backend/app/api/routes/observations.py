import json
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import EvidenceItem, MarketObservation, ResearchCase
from app.schemas.observations import (
    CreateObservationRequest, ObservationListResponse, ObservationRecord, ReviewObservationRequest
)

router = APIRouter()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def get_case(db: Session, case_id: str) -> ResearchCase:
    try:
        case_id = str(UUID(case_id))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Research case not found.") from exc
    case = db.get(ResearchCase, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Research case not found.")
    return case


def get_observation(db: Session, case_id: str, observation_id: str) -> MarketObservation:
    case = get_case(db, case_id)
    try:
        observation_id = str(UUID(observation_id))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Observation not found.") from exc
    observation = db.get(MarketObservation, observation_id)
    if observation is None or observation.case_id != case.id:
        raise HTTPException(status_code=404, detail="Observation not found.")
    return observation


def serialize(item: MarketObservation) -> ObservationRecord:
    return ObservationRecord(
        observation_id=item.id,
        case_id=item.case_id,
        indicator_code=item.indicator_code,
        signal_category=item.signal_category,
        segment=item.segment,
        raw_value_text=item.raw_value_text,
        value_numeric=item.value_numeric,
        value_text=item.value_text,
        unit=item.unit,
        currency=item.currency,
        metric_definition=item.metric_definition,
        observed_at=item.observed_at,
        published_at=item.published_at,
        retrieved_at=item.retrieved_at,
        recorded_at=item.recorded_at,
        source_id=item.source_id,
        acquisition_attempt_id=item.acquisition_attempt_id,
        evidence_id=item.evidence_id,
        entry_method=item.entry_method,
        review_status=item.review_status,
        definition_metadata=json.loads(item.definition_metadata_json),
        reviewed_at=item.reviewed_at,
        review_rationale=item.review_rationale,
        supersedes_observation_id=item.supersedes_observation_id,
    )


@router.get("/cases/{case_id}/observations", response_model=ObservationListResponse)
def list_observations(case_id: str, db: Session = Depends(get_db)) -> ObservationListResponse:
    case = get_case(db, case_id)
    rows = list(db.scalars(
        select(MarketObservation).where(MarketObservation.case_id == case.id).order_by(MarketObservation.recorded_at.desc())
    ))
    return ObservationListResponse(items=[serialize(row) for row in rows], total=len(rows))


@router.post("/cases/{case_id}/observations", response_model=ObservationRecord, status_code=201)
def create_observation(case_id: str, payload: CreateObservationRequest, db: Session = Depends(get_db)) -> ObservationRecord:
    case = get_case(db, case_id)
    evidence = db.get(EvidenceItem, payload.evidence_id)
    if evidence is None or evidence.case_id != case.id:
        raise HTTPException(status_code=422, detail="The evidence item must belong to this research case.")
    now = now_iso()
    item = MarketObservation(
        id=str(uuid4()), case_id=case.id, indicator_code=payload.indicator_code,
        signal_category=payload.signal_category, segment=payload.segment,
        raw_value_text=payload.raw_value_text, value_numeric=payload.value_numeric,
        value_text=payload.value_text, unit=payload.unit, currency=payload.currency,
        metric_definition=payload.metric_definition,
        observed_at=payload.observed_at.isoformat().replace("+00:00", "Z") if payload.observed_at else None,
        published_at=payload.published_at.isoformat().replace("+00:00", "Z") if payload.published_at else None,
        retrieved_at=payload.retrieved_at.isoformat().replace("+00:00", "Z") if payload.retrieved_at else None,
        recorded_at=now, source_id=None, acquisition_attempt_id=None, evidence_id=evidence.id,
        entry_method="manual", review_status="candidate",
        definition_metadata_json=json.dumps(payload.definition_metadata, sort_keys=True, separators=(",", ":")),
    )
    db.add(item)
    case.updated_at = now
    case.last_activity_at = now
    case.case_changed_since_last_run = True
    db.commit()
    db.refresh(item)
    return serialize(item)


@router.post("/cases/{case_id}/observations/{observation_id}/review", response_model=ObservationRecord)
def review_observation(
    case_id: str, observation_id: str, payload: ReviewObservationRequest, db: Session = Depends(get_db)
) -> ObservationRecord:
    item = get_observation(db, case_id, observation_id)
    item.review_status = {
        "accept": "accepted", "reject": "rejected",
        "mark_conflicted": "conflicted", "supersede": "superseded"
    }[payload.action]
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
