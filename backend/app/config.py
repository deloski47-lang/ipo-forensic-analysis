from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path


def default_data_dir() -> Path:
    """Resolve the per-user app data directory without using the repository."""
    if sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA")
        base = Path(local_app_data) if local_app_data else Path.home() / "AppData" / "Local"
        return base / "IPOForensicAnalysis"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "IPOForensicAnalysis"
    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    base = Path(xdg_data_home) if xdg_data_home else Path.home() / ".local" / "share"
    return base / "ipo-forensic-analysis"


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    api_host: str
    api_port: int
    allowed_origins: tuple[str, ...]
    max_upload_bytes: int
    http_timeout_seconds: float
    log_level: str

    @property
    def database_path(self) -> Path:
        return self.data_dir / "ipo_forensic.sqlite3"

    def ensure_data_directories(self) -> None:
        """Create expected folders; SQLite schema initialization belongs to migrations."""
        for directory in (
            self.data_dir,
            self.data_dir / "evidence",
            self.data_dir / "reports",
            self.data_dir / "backups",
            self.data_dir / "tmp",
            self.data_dir / "logs",
        ):
            directory.mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    override = os.environ.get("IPOFA_DATA_DIR", "").strip()
    data_dir = Path(override).expanduser() if override else default_data_dir()
    origins_raw = os.environ.get(
        "IPOFA_ALLOWED_ORIGINS",
        "http://127.0.0.1:5173,http://localhost:5173"
    )
    origins = tuple(origin.strip() for origin in origins_raw.split(",") if origin.strip())
    try:
        api_port = int(os.environ.get("IPOFA_API_PORT", "8000"))
        max_upload_bytes = int(os.environ.get("IPOFA_MAX_UPLOAD_BYTES", "26214400"))
        http_timeout_seconds = float(os.environ.get("IPOFA_HTTP_TIMEOUT_SECONDS", "15"))
    except ValueError as exc:
        raise ValueError(
            "IPOFA_API_PORT, IPOFA_MAX_UPLOAD_BYTES and IPOFA_HTTP_TIMEOUT_SECONDS must be numeric."
        ) from exc
    if not 1 <= api_port <= 65535:
        raise ValueError("IPOFA_API_PORT must be between 1 and 65535.")
    if max_upload_bytes <= 0:
        raise ValueError("IPOFA_MAX_UPLOAD_BYTES must be positive.")
    if http_timeout_seconds <= 0:
        raise ValueError("IPOFA_HTTP_TIMEOUT_SECONDS must be positive.")
    return Settings(
        data_dir=data_dir,
        api_host=os.environ.get("IPOFA_API_HOST", "127.0.0.1"),
        api_port=api_port,
        allowed_origins=origins,
        max_upload_bytes=max_upload_bytes,
        http_timeout_seconds=http_timeout_seconds,
        log_level=os.environ.get("IPOFA_LOG_LEVEL", "INFO").upper()
    )
