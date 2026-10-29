from datetime import datetime
from typing import Literal
from pydantic import Field, field_validator

from app.schemas.health import ApiSchema
from app.schemas.readiness import AnalysisReadiness

RunStatus = Literal["completed", "partial", "failed"]
CalculationStatus = Literal["calculated", "qualified", "skipped", "not_applicable", "invalid"]
FindingSeverity = Literal["info", "low", "medium", "high", "critical"]
FindingStatus = Literal["active", "unresolved", "not_run", "superseded"]


class CreateAnalysisRunRequest(ApiSchema):
    information_cutoff_at: datetime

    @field_validator("information_cutoff_at")
    @classmethod
    def normalize_cutoff(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("Information cutoff must include a timezone.")
        return value


class AnalysisResult(ApiSchema):
    result_id: str
    indicator_code: str
    calculation_status: CalculationStatus
    value_decimal: str | None
    value_text: str | None
    unit: str | None
    currency: str | None
    display_value: str | None
    formula_code: str | None
    formula_version: str | None
    input_fact_ids: list[str]
    input_observation_ids: list[str]
    evidence_ids: list[str]
    explanation: str
    reason: str | None


class FindingEvidenceLink(ApiSchema):
    evidence_id: str
    role: Literal["supports", "contradicts", "context"]
    note: str | None


class Finding(ApiSchema):
    finding_id: str
    rule_code: str
    rule_version: str
    finding_type: str
    severity: FindingSeverity
    status: FindingStatus
    title: str
    explanation: str
    limitation_note: str | None
    related_indicator_codes: list[str]
    input_fact_ids: list[str]
    input_observation_ids: list[str]
    evidence_links: list[FindingEvidenceLink]


class AnalysisRunDetail(ApiSchema):
    analysis_run_id: str
    case_id: str
    run_status: RunStatus
    information_cutoff_at: datetime
    started_at: datetime
    finished_at: datetime | None
    schema_version: str
    formula_set_version: str
    rule_set_version: str
    software_version: str
    input_snapshot_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    results: list[AnalysisResult]
    findings: list[Finding]
    readiness: AnalysisReadiness
    error_summary: str | None


class AnalysisRunSummary(ApiSchema):
    analysis_run_id: str
    case_id: str
    run_status: RunStatus
    information_cutoff_at: datetime
    started_at: datetime
    finished_at: datetime | None
    input_snapshot_hash: str


class AnalysisRunListResponse(ApiSchema):
    items: list[AnalysisRunSummary]
    total: int = Field(ge=0)
