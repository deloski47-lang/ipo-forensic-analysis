from datetime import datetime
from typing import Literal

from pydantic import Field, field_validator

from app.schemas.health import ApiSchema

CaseStatus = Literal["identity_pending", "active", "archived"]
IdentityStatus = Literal["unresolved", "ambiguous", "confirmed", "out_of_scope", "rejected"]
ReadinessStatus = Literal["ready", "qualified", "blocked"]


class CreateCaseRequest(ApiSchema):
    entered_name: str = Field(min_length=2, max_length=200)
    title: str | None = Field(default=None, max_length=160)

    @field_validator("entered_name")
    @classmethod
    def trim_entered_name(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Enter an IPO or issuer name.")
        return value

    @field_validator("title")
    @classmethod
    def trim_title(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None


class UpdateCaseRequest(ApiSchema):
    title: str = Field(min_length=1, max_length=160)

    @field_validator("title")
    @classmethod
    def trim_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be blank.")
        return value


class CaseDetail(ApiSchema):
    case_id: str
    entered_name: str
    title: str
    case_status: CaseStatus
    identity_status: IdentityStatus
    issue: dict | None = None
    created_at: datetime
    updated_at: datetime
    last_activity_at: datetime
    latest_analysis_run_id: str | None
    latest_report_id: str | None
    case_changed_since_last_run: bool
    readiness_summary: ReadinessStatus | None
    warning_count: int = Field(ge=0)


class CaseSummary(ApiSchema):
    case_id: str
    entered_name: str
    title: str
    case_status: CaseStatus
    identity_status: IdentityStatus
    issue_display_name: str | None
    last_activity_at: datetime
    latest_analysis_run_id: str | None
    latest_report_id: str | None
    warning_count: int = Field(ge=0)


class CaseListResponse(ApiSchema):
    items: list[CaseSummary]
    total: int = Field(ge=0)
