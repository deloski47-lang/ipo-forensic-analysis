from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_manual_subscription_observation_is_candidate_and_preserves_timestamps(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        case = client.post("/api/v1/cases", json={"enteredName": "Acme IPO"}).json()
        evidence = client.post(
            f"/api/v1/cases/{case['caseId']}/evidence",
            json={"evidenceKind": "manual_note", "title": "Exchange subscription screenshot"},
        ).json()
        response = client.post(
            f"/api/v1/cases/{case['caseId']}/observations",
            json={
                "indicatorCode": "DEM-01",
                "signalCategory": "subscription_qib",
                "segment": "QIB",
                "rawValueText": "4.25x at 14:00 IST",
                "valueNumeric": "4.25",
                "unit": "multiple",
                "metricDefinition": "QIB subscription multiple as reported at 14:00 IST; denominator follows the cited source.",
                "observedAt": None,
                "retrievedAt": "2026-10-29T08:30:00Z",
                "evidenceId": evidence["evidenceId"],
                "definitionMetadata": {"sourceTimestampPresent": False},
            },
        )
        assert response.status_code == 201, response.text
        item = response.json()
        assert item["reviewStatus"] == "candidate"
        assert item["observedAt"] is None
        assert item["retrievedAt"] == "2026-10-29T08:30:00Z"
        assert item["valueNumeric"] == "4.25"
        reviewed = client.post(
            f"/api/v1/cases/{case['caseId']}/observations/{item['observationId']}/review",
            json={"action": "accept", "rationale": "Compared against the cited screenshot."},
        )
        assert reviewed.status_code == 200
        assert reviewed.json()["reviewStatus"] == "accepted"


def test_observation_requires_registered_indicator_and_case_owned_evidence(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        case = client.post("/api/v1/cases", json={"enteredName": "Acme IPO"}).json()
        other_case = client.post("/api/v1/cases", json={"enteredName": "Other IPO"}).json()
        evidence = client.post(
            f"/api/v1/cases/{other_case['caseId']}/evidence",
            json={"evidenceKind": "manual_note", "title": "Other evidence"},
        ).json()
        payload = {
            "indicatorCode": "NOT-A-CODE",
            "signalCategory": "gmp",
            "rawValueText": "₹15",
            "metricDefinition": "Unofficial GMP quote",
            "evidenceId": evidence["evidenceId"],
        }
        bad_code = client.post(f"/api/v1/cases/{case['caseId']}/observations", json=payload)
        assert bad_code.status_code == 422
        payload["indicatorCode"] = "GMP-01"
        wrong_case = client.post(f"/api/v1/cases/{case['caseId']}/observations", json=payload)
        assert wrong_case.status_code == 422
