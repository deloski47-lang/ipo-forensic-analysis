from datetime import datetime
from typing import Literal
from pydantic import Field, model_validator

from app.schemas.health import ApiSchema


class BackupResponse(ApiSchema):
    backup_id: str
    created_at: datetime
    size_bytes: int = Field(ge=0)
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    case_count: int = Field(ge=0)
    evidence_file_count: int = Field(ge=0)
    download_url: str


class RestoreValidationResponse(ApiSchema):
    validation_id: str
    status: Literal["valid", "invalid", "incompatible"]
    case_count: int = Field(ge=0)
    evidence_file_count: int = Field(ge=0)
    warnings: list[str]
    errors: list[str]
    validated_at: datetime


class RestoreRequest(ApiSchema):
    validation_id: str
    confirmation_text: str

    @model_validator(mode="after")
    def exact_confirmation(self):
        if self.confirmation_text != "RESTORE":
            raise ValueError('confirmationText must exactly equal "RESTORE".')
        return self


class RestoreResponse(ApiSchema):
    status: Literal["completed", "failed"]
    restored_at: datetime | None
    safety_backup_id: str | None
    message: str
