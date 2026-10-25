from fastapi.testclient import TestClient
from app.model_api import app, metrics, API_TOKEN

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["model_loaded"] is True


def test_metrics_requires_token():
    response = client.get("/metrics")

    assert response.status_code == 422


def test_metrics_invalid_token():
    response = client.get(
        "/metrics",
        headers={"x-api-token": "token_incorrecto"}
    )

    assert response.status_code == 401


def test_metrics_counts_errors():
    errors_before = metrics["total_errors"]

    response = client.get("/ruta-inexistente-monitoring")

    assert response.status_code == 404
    assert metrics["total_errors"] == errors_before + 1


def test_metrics_returns_statistics():
    response = client.get(
        "/metrics",
        headers={"x-api-token": API_TOKEN}
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_requests" in data
    assert "total_errors" in data
    assert "total_predictions" in data
    assert "average_latency_ms" in data