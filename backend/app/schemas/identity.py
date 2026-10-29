from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Literal
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from app.schemas.health import ApiSchema


class ManualIssueInput(ApiSchema):
    issuer_legal_name: str = Field(min_length=1, max_length=200)
    display_name: str = Field(min_length=1, max_length=200)
    market_segment: Literal["MAINBOARD"] = "MAINBOARD"
    open_date: date | None = None
    close_date: date | None = None
    listing_date: date | None = None
    price_band_low: str | None = None
    price_band_high: str | None = None
    issue_size_amount: str | None = None
    issue_size_unit: str | None = Field(default=None, max_length=32)

    @field_validator("issuer_legal_name", "display_name")
    @classmethod
    def trim_required_names(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This name cannot be blank.")
        return value

    @field_validator("price_band_low", "price_band_high", "issue_size_amount")
    @classmethod
    def validate_decimal_string(cls, value: str | None) -> str | None:
        if value is None:
            return None
        try:
            parsed = Decimal(value)
        except InvalidOperation as exc:
            raise ValueError("Enter a valid decimal string.") from exc
        if not parsed.is_finite() or parsed < 0:
            raise ValueError("Decimal values must be finite and non-negative.")
        return format(parsed, "f")


class ConfirmIdentityRequest(ApiSchema):
    candidate_id: str | None = None
    manual_issue: ManualIssueInput | None = None
    identity_evidence_ids: list[str] = Field(min_length=1, max_length=20)
    confirmation_note: str | None = Field(default=None, max_length=1000)

    @field_validator("identity_evidence_ids")
    @classmethod
    def validate_evidence_ids(cls, values: list[str]) -> list[str]:
        normalized = []
        for value in values:
            try:
                normalized.append(str(UUID(value)))
            except ValueError as exc:
                raise ValueError("Evidence IDs must be UUIDs.") from exc
        return normalized

    @model_validator(mode="after")
    def require_exactly_one_identity_source(self):
        if (self.candidate_id is None) == (self.manual_issue is None):
            raise ValueError("Provide exactly one of candidateId or manualIssue.")
        if self.candidate_id is not None:
            raise ValueError("This build supports manualIssue confirmation; no candidate discovery source is enabled.")
        return self


class IssueDetail(ApiSchema):
    issue_id: str
    issuer_legal_name: str
    display_name: str
    market_segment: Literal["MAINBOARD"]
    open_date: date | None
    close_date: date | None
    listing_date: date | None
    price_band_low: str | None
    price_band_high: str | None
    issue_size_amount: str | None
    issue_size_unit: str | None
