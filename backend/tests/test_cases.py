from pathlib import Path
from uuid import UUID

from fastapi.testclient import TestClient

from app.main import app


def test_create_case_persists_and_can_be_reopened(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        created = client.post("/api/v1/cases", json={"enteredName": "  Example Industries IPO  "})
        assert created.status_code == 201
        body = created.json()
        assert str(UUID(body["caseId"])) == body["caseId"]
        assert body["enteredName"] == "Example Industries IPO"
        assert body["title"] == "Example Industries IPO"
        assert body["caseStatus"] == "identity_pending"
        assert body["identityStatus"] == "unresolved"
        assert body["issue"] is None
        assert body["latestAnalysisRunId"] is None
        case_id = body["caseId"]

    with TestClient(app) as client:
        reopened = client.get(f"/api/v1/cases/{case_id}")
        assert reopened.status_code == 200
        assert reopened.json()["caseId"] == case_id
        listing = client.get("/api/v1/cases")
        assert listing.status_code == 200
        assert listing.json()["total"] == 1
        assert listing.json()["items"][0]["caseId"] == case_id


def test_case_create_rejects_unknown_fields_and_short_names(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        unknown = client.post("/api/v1/cases", json={"enteredName": "Acme IPO", "issueId": "untrusted"})
        short = client.post("/api/v1/cases", json={"enteredName": " "})
    assert unknown.status_code == 422
    assert unknown.json()["error"]["code"] == "VALIDATION_ERROR"
    assert short.status_code == 422


def test_case_can_be_renamed_and_archived_without_deletion(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        created = client.post("/api/v1/cases", json={"enteredName": "Acme IPO"})
        case_id = created.json()["caseId"]
        updated = client.patch(f"/api/v1/cases/{case_id}", json={"title": "Acme listing review"})
        assert updated.status_code == 200
        assert updated.json()["title"] == "Acme listing review"
        archived = client.post(f"/api/v1/cases/{case_id}/archive")
        assert archived.status_code == 200
        assert archived.json()["caseStatus"] == "archived"
        assert client.get(f"/api/v1/cases/{case_id}").status_code == 200
        assert client.get("/api/v1/cases?status=archived").json()["total"] == 1
