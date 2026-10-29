from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Literal
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from app.indicator_registry import is_registered_indicator
from app.schemas.health import ApiSchema

SignalCategory = Literal[
    "issue_terms", "company_financials", "valuation", "subscription_qib",
    "subscription_nii", "subscription_retail", "gmp", "market_context", "company_events"
]
ReviewStatus = Literal["candidate", "accepted", "rejected", "conflicted", "superseded"]


class CreateObservationRequest(ApiSchema):
    indicator_code: str = Field(min_length=6, max_length=16)
    signal_category: SignalCategory
    segment: Literal["QIB", "NII", "RETAIL"] | None = None
    raw_value_text: str = Field(min_length=1, max_length=5000)
    value_numeric: str | None = None
    value_text: str | None = Field(default=None, max_length=5000)
    unit: str | None = Field(default=None, max_length=64)
    currency: str | None = Field(default=None, max_length=8)
    metric_definition: str = Field(min_length=1, max_length=2000)
    observed_at: datetime | None = None
    published_at: datetime | None = None
    retrieved_at: datetime | None = None
    source_id: str | None = None
    evidence_id: str
    definition_metadata: dict = Field(default_factory=dict)

    @field_validator("indicator_code")
    @classmethod
    def validate_indicator(cls, value: str) -> str:
        value = value.strip().upper()
        if not is_registered_indicator(value):
            raise ValueError("Use an indicator ID defined in the IPO Indicator Catalogue.")
        return value

    @field_validator("raw_value_text", "metric_definition")
    @classmethod
    def trim_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be blank.")
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
    def validate_segment(self):
        expected = {
            "subscription_qib": "QIB",
            "subscription_nii": "NII",
            "subscription_retail": "RETAIL",
        }.get(self.signal_category)
        if expected and self.segment not in (None, expected):
            raise ValueError(f"{self.signal_category} observations must use segment {expected}.")
        if self.source_id is not None:
            raise ValueError("Source registry is not enabled; link the observation through case evidence instead.")
        return self


class ObservationRecord(ApiSchema):
    observation_id: str
    case_id: str
    indicator_code: str
    signal_category: SignalCategory
    segment: Literal["QIB", "NII", "RETAIL"] | None
    raw_value_text: str
    value_numeric: str | None
    value_text: str | None
    unit: str | None
    currency: str | None
    metric_definition: str
    observed_at: datetime | None
    published_at: datetime | None
    retrieved_at: datetime | None
    recorded_at: datetime
    source_id: str | None
    acquisition_attempt_id: str | None
    evidence_id: str
    entry_method: Literal["manual", "extracted_candidate", "imported", "connector", "derived"]
    review_status: ReviewStatus
    definition_metadata: dict
    reviewed_at: datetime | None
    review_rationale: str | None
    supersedes_observation_id: str | None


class ObservationListResponse(ApiSchema):
    items: list[ObservationRecord]
    total: int = Field(ge=0)


class ReviewObservationRequest(ApiSchema):
    action: Literal["accept", "reject", "mark_conflicted", "supersede"]
    rationale: str | None = Field(default=None, max_length=2000)

    @model_validator(mode="after")
    def require_rationale_when_needed(self):
        if self.action in ("mark_conflicted", "supersede") and not (self.rationale and self.rationale.strip()):
            raise ValueError("A rationale is required for this review action.")
        return self
