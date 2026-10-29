from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_backup_manifest_validation_and_restore_with_safety_backup(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        first = client.post("/api/v1/cases", json={"enteredName": "First IPO"}).json()
        backup_response = client.post("/api/v1/local-data/backups")
        assert backup_response.status_code == 201, backup_response.text
        backup = backup_response.json()
        assert len(backup["sha256"]) == 64
        archive = client.get(backup["downloadUrl"])
        assert archive.status_code == 200
        assert archive.content[:2] == b"PK"

        client.post("/api/v1/cases", json={"enteredName": "Second IPO"})
        validation_response = client.post(
            "/api/v1/local-data/restore/validate",
            files={"file": ("backup.zip", archive.content, "application/zip")},
        )
        assert validation_response.status_code == 201, validation_response.text
        validation = validation_response.json()
        assert validation["status"] == "valid"
        assert validation["caseCount"] == 1

        invalid_confirmation = client.post("/api/v1/local-data/restore", json={
            "validationId": validation["validationId"], "confirmationText": "yes"
        })
        assert invalid_confirmation.status_code == 422

        restored = client.post("/api/v1/local-data/restore", json={
            "validationId": validation["validationId"], "confirmationText": "RESTORE"
        })
        assert restored.status_code == 200, restored.text
        assert restored.json()["status"] == "completed"
        assert restored.json()["safetyBackupId"]

        listing = client.get("/api/v1/cases")
        assert listing.status_code == 200
        assert listing.json()["total"] == 1
        assert listing.json()["items"][0]["caseId"] == first["caseId"]


def test_restore_validation_rejects_non_zip_upload(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/local-data/restore/validate",
            files={"file": ("not-a-backup.zip", b"this is not a zip", "application/zip")},
        )
        assert response.status_code == 201
        assert response.json()["status"] == "invalid"
        assert response.json()["errors"]
