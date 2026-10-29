from datetime import datetime
from typing import Literal

from pydantic import Field

from app.schemas.health import ApiSchema


class ReadinessIssue(ApiSchema):
    code: str
    severity: Literal["blocker", "warning", "info"]
    message: str
    affected_indicator_codes: list[str] = Field(default_factory=list)
    affected_signal_categories: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    next_action: str | None = None


class SourceStateSummary(ApiSchema):
    source_id: str | None
    source_name: str
    signal_category: str
    access_status: str
    connector_status: str
    latest_category_status: str
    latest_attempt_at: datetime | None
    latest_observed_at: datetime | None
    message: str
    latest_observation_ids: list[str] = Field(default_factory=list)


class AnalysisReadiness(ApiSchema):
    case_id: str
    status: Literal["ready", "qualified", "blocked"]
    checked_at: datetime
    information_cutoff_at: datetime
    blockers: list[ReadinessIssue]
    warnings: list[ReadinessIssue]
    ready_formula_codes: list[str]
    skipped_formula_codes: list[str]
    eligible_finding_rule_codes: list[str]
    skipped_finding_rule_codes: list[str]
    source_coverage: list[SourceStateSummary]
