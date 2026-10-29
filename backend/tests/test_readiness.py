from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_readiness_is_blocked_until_identity_and_formula_registry_are_ready(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        case = client.post("/api/v1/cases", json={"enteredName": "Acme IPO"}).json()
        response = client.get(f"/api/v1/cases/{case['caseId']}/analysis/readiness")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "blocked"
        codes = {item["code"] for item in body["blockers"]}
        assert "IPO_IDENTITY_UNCONFIRMED" in codes
        assert "NO_EVIDENCE_REGISTERED" in codes
        assert "FORMULA_REGISTRY_NOT_ENABLED" in codes
        assert body["readyFormulaCodes"] == []


def test_readiness_reflects_user_reviewed_evidence(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        case = client.post("/api/v1/cases", json={"enteredName": "Acme IPO"}).json()
        evidence = client.post(
            f"/api/v1/cases/{case['caseId']}/evidence",
            json={"evidenceKind": "manual_note", "title": "Offer details"},
        ).json()
        reviewed = client.post(
            f"/api/v1/cases/{case['caseId']}/evidence/{evidence['evidenceId']}/review",
            json={"action": "verify", "rationale": "Compared with the source document."},
        )
        assert reviewed.status_code == 200
        assert reviewed.json()["verificationStatus"] == "user_verified"
        readiness = client.get(f"/api/v1/cases/{case['caseId']}/analysis/readiness").json()
        codes = {item["code"] for item in readiness["blockers"]}
        assert "NO_EVIDENCE_REGISTERED" not in codes
        assert "NO_USER_VERIFIED_EVIDENCE" not in codes
        assert "FORMULA_REGISTRY_NOT_ENABLED" in codes
