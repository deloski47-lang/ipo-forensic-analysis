from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_health_reports_migrated_local_database(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["apiVersion"] == "v1"
    assert body["status"] == "ok"
    assert body["databaseStatus"] == "ok"
    assert body["dataDirectoryStatus"] == "ok"
    assert body["timestamp"].endswith("Z") or "+" in body["timestamp"]
    assert (local_data_dir / "ipo_forensic.sqlite3").is_file()


def test_startup_creates_local_directories(local_data_dir: Path) -> None:
    for name in ("evidence", "reports", "backups", "tmp", "logs"):
        assert (local_data_dir / name).is_dir()
