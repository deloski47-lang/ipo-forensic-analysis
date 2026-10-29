from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_manual_identity_requires_case_owned_evidence(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        case = client.post("/api/v1/cases", json={"enteredName": "Acme IPO"}).json()
        evidence = client.post(
            f"/api/v1/cases/{case['caseId']}/evidence",
            json={"evidenceKind": "manual_note", "title": "Offer details"},
        ).json()
        client.post(f"/api/v1/cases/{case['caseId']}/evidence/{evidence['evidenceId']}/review", json={"action": "verify", "rationale": "Reviewed against the offer document."})
        response = client.post(
            f"/api/v1/cases/{case['caseId']}/identity/confirm",
            json={
                "manualIssue": {
                    "issuerLegalName": "Acme Industries Limited",
                    "displayName": "Acme Industries IPO",
                    "marketSegment": "MAINBOARD",
                    "priceBandLow": "100.00",
                    "priceBandHigh": "110.00",
                },
                "identityEvidenceIds": [evidence["evidenceId"]],
                "confirmationNote": "Manually compared against the offer document.",
            },
        )
        assert response.status_code == 200, response.text
        body = response.json()
        assert body["identityStatus"] == "confirmed"
        assert body["caseStatus"] == "active"
        assert body["issue"]["displayName"] == "Acme Industries IPO"
        assert body["issue"]["priceBandLow"] == "100.00"
        assert body["issue"]["listingDate"] is None


def test_identity_confirmation_rejects_evidence_from_another_case(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        first = client.post("/api/v1/cases", json={"enteredName": "First IPO"}).json()
        second = client.post("/api/v1/cases", json={"enteredName": "Second IPO"}).json()
        evidence = client.post(
            f"/api/v1/cases/{first['caseId']}/evidence",
            json={"evidenceKind": "manual_note", "title": "Not this issue"},
        ).json()
        response = client.post(
            f"/api/v1/cases/{second['caseId']}/identity/confirm",
            json={
                "manualIssue": {
                    "issuerLegalName": "Second Industries Limited",
                    "displayName": "Second Industries IPO",
                    "marketSegment": "MAINBOARD",
                },
                "identityEvidenceIds": [evidence["evidenceId"]],
            },
        )
        assert response.status_code == 422
