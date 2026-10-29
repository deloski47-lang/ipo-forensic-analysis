from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.config import get_settings

settings = get_settings()
logging.basicConfig(level=getattr(logging, settings.log_level, logging.INFO))


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Phase 0 prepares local directories only. Database schema belongs to Alembic.
    get_settings().ensure_data_directories()
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


@app.get("/", include_in_schema=False)
def root_status() -> dict[str, str]:
    return {
        "name": "IPO Forensic Analysis Engine API",
        "apiVersion": "v1",
        "healthPath": "/api/v1/health"
    }
