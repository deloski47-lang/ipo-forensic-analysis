from pathlib import Path
from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import app


def test_scenario_preview_uses_decimal_and_never_invents_net_return(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        case = client.post("/api/v1/cases", json={"enteredName": "Acme IPO"}).json()
        response = client.post(f"/api/v1/cases/{case['caseId']}/scenarios/preview", json={
            "label": "Base case", "entryPrice": "100.00", "exitPrice": "125.50", "quantity": 10,
            "assumptionNote": "User-defined hypothetical listing price."
        })
        assert response.status_code == 200, response.text
        body = response.json()
        assert Decimal(body["grossReturnPct"]) == Decimal("25.5")
        assert Decimal(body["grossProfitAmount"]) == Decimal("255.00")
        assert body["netReturnPct"] is None
        assert "not a forecast" in body["limitationNote"]


def test_scenario_rejects_zero_entry_price_and_can_be_saved(local_data_dir: Path) -> None:
    with TestClient(app) as client:
        case = client.post("/api/v1/cases", json={"enteredName": "Acme IPO"}).json()
        invalid = client.post(f"/api/v1/cases/{case['caseId']}/scenarios/preview", json={
            "label": "Bad entry", "entryPrice": "0", "exitPrice": "100"
        })
        assert invalid.status_code == 422
        created = client.post(f"/api/v1/cases/{case['caseId']}/scenarios", json={
            "label": "Downside", "entryPrice": "100", "exitPrice": "80", "quantity": 5
        })
        assert created.status_code == 201, created.text
        assert client.get(f"/api/v1/cases/{case['caseId']}/scenarios").json()["total"] == 1
