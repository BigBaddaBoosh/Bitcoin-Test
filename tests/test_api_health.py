from fastapi.testclient import TestClient

from api.app import app


def test_health_endpoint_includes_user_constraints() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200

    payload = response.json()
    assert payload["provider"] == "openai"
    assert payload["exchange"] == "Binance AUS"
    assert payload["max_daily_loss_usd"] == 20.0
    assert payload["dashboard_enabled"] is True
