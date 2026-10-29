from datetime import datetime
from typing import Literal
from pydantic import Field

from app.schemas.health import ApiSchema


class CreateReportRequest(ApiSchema):
    analysis_run_id: str


class CreateReportExportRequest(ApiSchema):
    format: Literal["html", "docx"]


class ReportSection(ApiSchema):
    section_code: str
    heading: str
    body_markdown: str
    related_evidence_ids: list[str] = Field(default_factory=list)
    related_result_ids: list[str] = Field(default_factory=list)
    related_finding_ids: list[str] = Field(default_factory=list)
    status_note: str | None = None


class ReportArtifact(ApiSchema):
    artifact_id: str
    report_id: str
    format: Literal["html", "docx"]
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    size_bytes: int = Field(ge=0)
    created_at: datetime
    download_url: str


class ReportDetail(ApiSchema):
    report_id: str
    case_id: str
    analysis_run_id: str
    generated_at: datetime
    template_version: str
    report_snapshot_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    title: str
    issue_display_name: str
    information_cutoff_at: datetime
    sections: list[ReportSection]
    warnings: list[str]
    export_artifacts: list[ReportArtifact]


class ReportListResponse(ApiSchema):
    items: list[ReportDetail]
    total: int = Field(ge=0)
