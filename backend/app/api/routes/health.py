from datetime import datetime, timezone
import os

from fastapi import APIRouter

from app.config import get_settings
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Report API and local SQLite/data-directory readiness."""
    settings = get_settings()
    data_dir_ok = (
        settings.data_dir.is_dir()
        and os.access(settings.data_dir, os.R_OK | os.W_OK | os.X_OK)
    )
    database_ok = (
        settings.database_path.is_file()
        and os.access(settings.database_path, os.R_OK | os.W_OK)
    )
    return HealthResponse(
        status="ok" if data_dir_ok and database_ok else "degraded",
        app_version="0.1.0",
        api_version="v1",
        database_status="ok" if database_ok else "error",
        data_directory_status="ok" if data_dir_ok else "error",
        timestamp=datetime.now(timezone.utc)
    )
