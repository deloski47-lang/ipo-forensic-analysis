from decimal import Decimal, InvalidOperation
from typing import Literal
from pydantic import Field, field_validator

from app.schemas.health import ApiSchema


class CreateScenarioRequest(ApiSchema):
    label: str = Field(min_length=1, max_length=100)
    entry_price: str
    exit_price: str
    quantity: int | None = Field(default=None, ge=1)
    assumption_note: str | None = Field(default=None, max_length=2000)

    @field_validator("label")
    @classmethod
    def clean_label(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Scenario label cannot be blank.")
        return value

    @field_validator("entry_price")
    @classmethod
    def valid_entry(cls, value: str) -> str:
        parsed = parse_decimal(value)
        if parsed <= 0:
            raise ValueError("Entry price must be greater than zero.")
        return format(parsed, "f")

    @field_validator("exit_price")
    @classmethod
    def valid_exit(cls, value: str) -> str:
        parsed = parse_decimal(value)
        if parsed < 0:
            raise ValueError("Exit price cannot be negative.")
        return format(parsed, "f")


def parse_decimal(value: str) -> Decimal:
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError("Prices must be decimal strings, not binary floating-point values.") from exc
    if not parsed.is_finite():
        raise ValueError("Prices must be finite decimal values.")
    return parsed


class ScenarioDefinition(ApiSchema):
    scenario_id: str
    case_id: str
    label: str
    entry_price: str
    exit_price: str
    quantity: int | None
    assumption_note: str | None
    created_at: str
    updated_at: str


class ScenarioListResponse(ApiSchema):
    items: list[ScenarioDefinition]
    total: int = Field(ge=0)


class ScenarioPreview(ApiSchema):
    label: str
    entry_price: str
    exit_price: str
    quantity: int | None
    gross_return_pct: str
    gross_profit_amount: str | None
    net_return_pct: None = None
    calculation_status: Literal["calculated", "incomplete"]
    limitation_note: str
