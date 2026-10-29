from contextlib import asynccontextmanager
import logging

from alembic import command
from alembic.config import Config
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone

from app.api.router import api_router
from app.config import get_settings

settings = get_settings()
logging.basicConfig(level=getattr(logging, settings.log_level, logging.INFO))


def to_camel(value: str) -> str:
    head, *tail = value.split("_")
    return head + "".join(part[:1].upper() + part[1:] for part in tail)


def run_migrations() -> None:
    """Apply checked-in Alembic migrations to the user's local database."""
    backend_dir = Path(__file__).resolve().parents[1]
    config = Config(str(backend_dir / "alembic.ini"))
    config.set_main_option("script_location", str(backend_dir / "alembic"))
    command.upgrade(config, "head")


@asynccontextmanager
async def lifespan(_: FastAPI):
    get_settings().ensure_data_directories()
    run_migrations()
    yield


app = FastAPI(
    title="IPO Forensic Analysis Engine API",
    description="Local-first API for evidence-driven Indian Mainboard IPO research.",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url=None,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.allowed_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["Accept", "Content-Type"]
)
app.include_router(api_router, prefix="/api/v1")


@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    request_id = str(uuid4())
    code = "NOT_FOUND" if exc.status_code == 404 else "INVALID_REQUEST"
    message = exc.detail if isinstance(exc.detail, str) else "The request could not be completed."
    return JSONResponse(
        status_code=exc.status_code,
        headers=exc.headers,
        content={
            "error": {"code": code, "message": message, "details": [], "requestId": request_id},
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    request_id = str(uuid4())
    details = []
    for error in exc.errors():
        location = [str(part) for part in error.get("loc", []) if part not in ("body", "query", "path")]
        details.append({
            "field": ".".join(to_camel(part) for part in location) or None,
            "issueCode": "required" if error.get("type") == "missing" else "invalid",
            "message": "This field is required." if error.get("type") == "missing" else "Check this field's value."
        })
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Review the highlighted fields and try again.",
                "details": details,
                "requestId": request_id
            },
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }
    )


@app.get("/", include_in_schema=False)
def root_status() -> dict[str, str]:
    return {
        "name": "IPO Forensic Analysis Engine API",
        "apiVersion": "v1",
        "healthPath": "/api/v1/health"
    }
