from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_register_manual_evidence_and_list_it(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        case = client.post("/api/v1/cases", json={"enteredName": "Acme IPO"}).json()
        response = client.post(f"/api/v1/cases/{case['caseId']}/evidence", json={
            "evidenceKind": "manual_note", "title": "Registrar note", "notes": "Unverified user note"
        })
        assert response.status_code == 201
        item = response.json()
        assert item["evidenceKind"] == "manual_note"
        assert item["verificationStatus"] == "unverified"
        assert item["sha256"] is None
        listing = client.get(f"/api/v1/cases/{case['caseId']}/evidence")
        assert listing.status_code == 200
        assert listing.json()["total"] == 1
        assert listing.json()["items"][0]["evidenceId"] == item["evidenceId"]


def test_upload_pdf_keeps_original_and_hashes_it(local_data_dir: Path) -> None:
    pdf_bytes = b"%PDF-1.4\nminimal fixture"
    with TestClient(app) as client:
        case = client.post("/api/v1/cases", json={"enteredName": "Acme IPO"}).json()
        response = client.post(
            f"/api/v1/cases/{case['caseId']}/evidence/files",
            files={"file": ("fixture.pdf", pdf_bytes, "application/pdf")},
            data={"title": "Offer document"},
        )
        assert response.status_code == 201
        item = response.json()
        assert item["sha256"] is not None and len(item["sha256"]) == 64
        assert item["localAvailable"] is True
        download = client.get(item["downloadUrl"])
        assert download.status_code == 200
        assert download.content == pdf_bytes
