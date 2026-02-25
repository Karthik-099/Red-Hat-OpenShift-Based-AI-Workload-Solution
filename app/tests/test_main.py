import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_readiness_check():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"

def test_predict_valid_input():
    payload = {"data": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "latency_ms" in response.json()

def test_predict_invalid_input():
    payload = {"data": [1.0, 2.0, 3.0]}
    response = client.post("/predict", json=payload)
    assert response.status_code == 400

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "inference_requests_total" in response.text
