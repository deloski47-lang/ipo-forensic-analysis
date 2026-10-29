from datetime import datetime
from typing import Literal
from pydantic import Field, HttpUrl, field_validator

from app.schemas.health import ApiSchema

EvidenceKind = Literal["web_page", "manual_note", "manual_value", "document"]
EvidenceVerificationStatus = Literal["unverified", "reviewed", "conflicting", "rejected"]


class CreateEvidenceRequest(ApiSchema):
    evidence_kind: Literal["web_page", "manual_note", "manual_value"]
    title: str = Field(min_length=1, max_length=200)
    source_url: HttpUrl | None = None
    published_at: datetime | None = None
    notes: str | None = Field(default=None, max_length=10_000)

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Evidence title cannot be blank.")
        return value

    @field_validator("source_url")
    @classmethod
    def http_only(cls, value: HttpUrl | None) -> HttpUrl | None:
        if value is not None and value.scheme not in ("http", "https"):
            raise ValueError("Evidence URLs must use HTTP or HTTPS.")
        return value


class EvidenceItem(ApiSchema):
    evidence_id: str
    case_id: str
    source_id: str | None
    evidence_kind: EvidenceKind
    title: str
    source_url: str | None
    original_file_name: str | None
    mime_type: str | None
    size_bytes: int | None
    sha256: str | None
    published_at: datetime | None
    captured_at: datetime
    locator: str | None
    verification_status: EvidenceVerificationStatus
    notes: str | None
    download_url: str | None
    local_available: bool


class EvidenceListResponse(ApiSchema):
    items: list[EvidenceItem]
    total: int = Field(ge=0)
