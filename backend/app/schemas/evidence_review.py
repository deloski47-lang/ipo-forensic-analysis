from pydantic import Field
from typing import Literal
from app.schemas.health import ApiSchema


class ReviewEvidenceRequest(ApiSchema):
    action: Literal["verify", "reject"]
    rationale: str | None = Field(default=None, max_length=2000)
