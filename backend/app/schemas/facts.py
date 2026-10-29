from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Literal
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from app.indicator_registry import is_registered_indicator
from app.schemas.health import ApiSchema


class CreateFactRequest(ApiSchema):
    indicator_code: str = Field(min_length=6, max_length=16)
    raw_value_text: str = Field(min_length=1, max_length=5000)
    value_numeric: str | None = None
    value_text: str | None = Field(default=None, max_length=5000)
    unit: str | None = Field(default=None, max_length=64)
    currency: str | None = Field(default=None, max_length=8)
    period_start: date | None = None
    period_end: date | None = None
    as_of_date: date | None = None
    evidence_id: str
    definition_note: str | None = Field(default=None, max_length=2000)

    @field_validator("indicator_code")
    @classmethod
    def validate_indicator(cls, value: str) -> str:
        value = value.strip().upper()
        if not is_registered_indicator(value):
            raise ValueError("Use an indicator ID defined in the IPO Indicator Catalogue.")
        return value

    @field_validator("raw_value_text")
    @classmethod
    def trim_raw_value(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Raw value text cannot be blank.")
        return value

    @field_validator("value_numeric")
    @classmethod
    def validate_decimal_string(cls, value: str | None) -> str | None:
        if value is None:
            return None
        try:
            parsed = Decimal(value)
        except InvalidOperation as exc:
            raise ValueError("Enter a decimal as a string.") from exc
        if not parsed.is_finite():
            raise ValueError("Numeric values must be finite.")
        return format(parsed, "f")

    @field_validator("evidence_id")
    @classmethod
    def validate_evidence_id(cls, value: str) -> str:
        try:
            return str(UUID(value))
        except ValueError as exc:
            raise ValueError("Evidence ID must be a UUID.") from exc

    @model_validator(mode="after")
    def validate_period(self):
        if self.period_start and self.period_end and self.period_start > self.period_end:
            raise ValueError("Period start cannot be after period end.")
        return self


class FactRecord(ApiSchema):
    fact_id: str
    case_id: str
    indicator_code: str
    raw_value_text: str
    value_numeric: str | None
    value_text: str | None
    unit: str | None
    currency: str | None
    period_start: date | None
    period_end: date | None
    as_of_date: date | None
    evidence_id: str
    entry_method: Literal["manual", "extracted_candidate", "imported", "connector", "derived"]
    review_status: Literal["candidate", "accepted", "rejected", "conflicted", "superseded"]
    definition_note: str | None
    recorded_at: str
    created_at: str
    reviewed_at: str | None
    review_rationale: str | None
    supersedes_fact_id: str | None


class FactListResponse(ApiSchema):
    items: list[FactRecord]
    total: int = Field(ge=0)


class ReviewFactRequest(ApiSchema):
    action: Literal["accept", "reject", "mark_conflicted", "supersede"]
    rationale: str | None = Field(default=None, max_length=2000)

    @model_validator(mode="after")
    def require_rationale_when_needed(self):
        if self.action in ("mark_conflicted", "supersede") and not (self.rationale and self.rationale.strip()):
            raise ValueError("A rationale is required for this review action.")
        return self
