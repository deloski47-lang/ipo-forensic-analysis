from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


def to_camel(value: str) -> str:
    head, *tail = value.split("_")
    return head + "".join(part[:1].upper() + part[1:] for part in tail)


class ApiSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid"
    )


class HealthResponse(ApiSchema):
    status: Literal["ok", "degraded"]
    app_version: str
    api_version: Literal["v1"]
    database_status: Literal["ok", "error"]
    data_directory_status: Literal["ok", "error"]
    timestamp: datetime
