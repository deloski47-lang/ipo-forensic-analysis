from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_health_is_truthful_before_database_migration(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["apiVersion"] == "v1"
    assert body["status"] == "degraded"
    assert body["databaseStatus"] == "error"
    assert body["dataDirectoryStatus"] == "ok"
    assert body["timestamp"].endswith("Z") or "+" in body["timestamp"]


def test_startup_creates_local_directories(local_data_dir: Path) -> None:
    for name in ("evidence", "reports", "backups", "tmp", "logs"):
        assert (local_data_dir / name).is_dir()
