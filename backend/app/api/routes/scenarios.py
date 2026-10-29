from decimal import Decimal, localcontext
from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import ResearchCase, ScenarioDefinition as ScenarioModel
from app.schemas.scenarios import CreateScenarioRequest, ScenarioDefinition, ScenarioListResponse, ScenarioPreview

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


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def serialize(item: ScenarioModel) -> ScenarioDefinition:
    return ScenarioDefinition(
        scenario_id=item.id, case_id=item.case_id, label=item.label,
        entry_price=item.entry_price, exit_price=item.exit_price, quantity=item.quantity,
        assumption_note=item.assumption_note, created_at=item.created_at, updated_at=item.updated_at,
    )


def calculate(payload: CreateScenarioRequest) -> ScenarioPreview:
    entry = Decimal(payload.entry_price)
    exit_price = Decimal(payload.exit_price)
    with localcontext() as ctx:
        ctx.prec = 28
        gross_return = ((exit_price - entry) / entry) * Decimal("100")
        gross_profit = (exit_price - entry) * payload.quantity if payload.quantity is not None else None
    return ScenarioPreview(
        label=payload.label,
        entry_price=payload.entry_price,
        exit_price=payload.exit_price,
        quantity=payload.quantity,
        gross_return_pct=format(gross_return, "f"),
        gross_profit_amount=format(gross_profit, "f") if gross_profit is not None else None,
        net_return_pct=None,
        calculation_status="calculated",
        limitation_note="Gross scenario arithmetic only. This is a user-defined assumption, not a forecast. Brokerage, taxes, slippage and other costs are not included; net return is unknown.",
    )


@router.get("/cases/{case_id}/scenarios", response_model=ScenarioListResponse)
def list_scenarios(case_id: str, db: Session = Depends(get_db)) -> ScenarioListResponse:
    case = get_case(db, case_id)
    rows = list(db.scalars(select(ScenarioModel).where(ScenarioModel.case_id == case.id).order_by(ScenarioModel.created_at.desc())))
    return ScenarioListResponse(items=[serialize(row) for row in rows], total=len(rows))


@router.post("/cases/{case_id}/scenarios", response_model=ScenarioDefinition, status_code=201)
def create_scenario(case_id: str, payload: CreateScenarioRequest, db: Session = Depends(get_db)) -> ScenarioDefinition:
    case = get_case(db, case_id)
    now = now_iso()
    item = ScenarioModel(
        id=str(uuid4()), case_id=case.id, label=payload.label, entry_price=payload.entry_price,
        exit_price=payload.exit_price, quantity=payload.quantity, assumption_note=payload.assumption_note,
        created_at=now, updated_at=now,
    )
    db.add(item)
    case.updated_at = now
    case.last_activity_at = now
    case.case_changed_since_last_run = True
    db.commit()
    db.refresh(item)
    return serialize(item)


@router.post("/cases/{case_id}/scenarios/preview", response_model=ScenarioPreview)
def preview_scenario(case_id: str, payload: CreateScenarioRequest, db: Session = Depends(get_db)) -> ScenarioPreview:
    get_case(db, case_id)
    return calculate(payload)
