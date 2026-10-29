from datetime import datetime, timezone
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_analysis_run_snapshots_scenario_and_remains_immutable(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        case = client.post("/api/v1/cases", json={"enteredName": "Acme IPO"}).json()
        evidence = client.post(
            f"/api/v1/cases/{case['caseId']}/evidence",
            json={"evidenceKind": "manual_note", "title": "Offer terms"},
        ).json()
        client.post(
            f"/api/v1/cases/{case['caseId']}/evidence/{evidence['evidenceId']}/review",
            json={"action": "verify", "rationale": "Reviewed against the source document."},
        )
        identity = client.post(
            f"/api/v1/cases/{case['caseId']}/identity/confirm",
            json={
                "manualIssue": {
                    "issuerLegalName": "Acme Industries Limited",
                    "displayName": "Acme Industries IPO",
                    "marketSegment": "MAINBOARD",
                    "priceBandLow": "100",
                    "priceBandHigh": "110",
                },
                "identityEvidenceIds": [evidence["evidenceId"]],
            },
        )
        assert identity.status_code == 200, identity.text
        scenario = client.post(
            f"/api/v1/cases/{case['caseId']}/scenarios",
            json={"label": "Base", "entryPrice": "100", "exitPrice": "125", "quantity": 10},
        )
        assert scenario.status_code == 201, scenario.text
        run_response = client.post(
            f"/api/v1/cases/{case['caseId']}/analysis-runs",
            json={"informationCutoffAt": datetime.now(timezone.utc).isoformat()},
        )
        assert run_response.status_code == 201, run_response.text
        run = run_response.json()
        assert run["runStatus"] == "partial"
        assert run["results"][0]["indicatorCode"] == "RISK-03"
        assert run["results"][0]["valueDecimal"] == "25"
        run_id = run["analysisRunId"]
        snapshot_hash = run["inputSnapshotHash"]

        client.post(
            f"/api/v1/cases/{case['caseId']}/evidence",
            json={"evidenceKind": "manual_note", "title": "Added after run"},
        )
        reopened = client.get(f"/api/v1/cases/{case['caseId']}/analysis-runs/{run_id}")
        assert reopened.status_code == 200
        assert reopened.json()["inputSnapshotHash"] == snapshot_hash
        assert len(reopened.json()["results"]) == len(run["results"])


def test_analysis_run_is_blocked_without_confirmed_identity_or_scenario(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        case = client.post("/api/v1/cases", json={"enteredName": "Acme IPO"}).json()
        response = client.post(
            f"/api/v1/cases/{case['caseId']}/analysis-runs",
            json={"informationCutoffAt": datetime.now(timezone.utc).isoformat()},
        )
        assert response.status_code == 409
        assert "Confirm" in response.json()["error"]["message"]
