from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_manual_fact_is_candidate_until_reviewed(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        case = client.post("/api/v1/cases", json={"enteredName": "Acme IPO"}).json()
        evidence = client.post(
            f"/api/v1/cases/{case['caseId']}/evidence",
            json={"evidenceKind": "manual_note", "title": "Restated financial statement"},
        ).json()
        response = client.post(f"/api/v1/cases/{case['caseId']}/facts", json={
            "indicatorCode": "FIN-01",
            "rawValueText": "Operating cash flow ₹125 crore",
            "valueNumeric": "125",
            "unit": "INR crore",
            "periodStart": "2025-04-01",
            "periodEnd": "2026-03-31",
            "evidenceId": evidence["evidenceId"],
            "definitionNote": "Raw reported value; period from cited document."
        })
        assert response.status_code == 201, response.text
        fact = response.json()
        assert fact["reviewStatus"] == "candidate"
        assert fact["valueNumeric"] == "125"
        accepted = client.post(
            f"/api/v1/cases/{case['caseId']}/facts/{fact['factId']}/review",
            json={"action": "accept", "rationale": "Checked against the linked statement."},
        )
        assert accepted.status_code == 200
        assert accepted.json()["reviewStatus"] == "accepted"


def test_fact_requires_registered_indicator_and_case_owned_evidence(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        case = client.post("/api/v1/cases", json={"enteredName": "Acme IPO"}).json()
        other = client.post("/api/v1/cases", json={"enteredName": "Other IPO"}).json()
        evidence = client.post(
            f"/api/v1/cases/{other['caseId']}/evidence",
            json={"evidenceKind": "manual_note", "title": "Other issuer statement"},
        ).json()
        payload = {"indicatorCode": "FIN-99", "rawValueText": "42", "evidenceId": evidence["evidenceId"]}
        invalid_code = client.post(f"/api/v1/cases/{case['caseId']}/facts", json=payload)
        assert invalid_code.status_code == 422
        payload["indicatorCode"] = "FIN-01"
        wrong_case = client.post(f"/api/v1/cases/{case['caseId']}/facts", json=payload)
        assert wrong_case.status_code == 422
