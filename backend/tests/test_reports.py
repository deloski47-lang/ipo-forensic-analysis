from datetime import datetime, timezone
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_report_snapshot_and_offline_exports(local_data_dir: Path) -> None:
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
        confirmed = client.post(
            f"/api/v1/cases/{case['caseId']}/identity/confirm",
            json={
                "manualIssue": {"issuerLegalName": "Acme Limited", "displayName": "Acme IPO", "marketSegment": "MAINBOARD"},
                "identityEvidenceIds": [evidence["evidenceId"]],
            },
        )
        assert confirmed.status_code == 200, confirmed.text
        scenario = client.post(
            f"/api/v1/cases/{case['caseId']}/scenarios",
            json={"label": "Base", "entryPrice": "100", "exitPrice": "120", "quantity": 5},
        )
        assert scenario.status_code == 201
        run = client.post(
            f"/api/v1/cases/{case['caseId']}/analysis-runs",
            json={"informationCutoffAt": datetime.now(timezone.utc).isoformat()},
        )
        assert run.status_code == 201, run.text
        created = client.post(
            f"/api/v1/cases/{case['caseId']}/reports",
            json={"analysisRunId": run.json()["analysisRunId"]},
        )
        assert created.status_code == 201, created.text
        report = created.json()
        assert len(report["reportSnapshotHash"]) == 64
        assert any(section["sectionCode"] == "scenario_results" for section in report["sections"])

        html_artifact = client.post(
            f"/api/v1/cases/{case['caseId']}/reports/{report['reportId']}/exports",
            json={"format": "html"},
        )
        assert html_artifact.status_code == 201, html_artifact.text
        html_download = client.get(html_artifact.json()["downloadUrl"])
        assert html_download.status_code == 200
        assert b"Acme IPO" in html_download.content

        docx_artifact = client.post(
            f"/api/v1/cases/{case['caseId']}/reports/{report['reportId']}/exports",
            json={"format": "docx"},
        )
        assert docx_artifact.status_code == 201, docx_artifact.text
        docx_download = client.get(docx_artifact.json()["downloadUrl"])
        assert docx_download.status_code == 200
        assert docx_download.content[:2] == b"PK"
