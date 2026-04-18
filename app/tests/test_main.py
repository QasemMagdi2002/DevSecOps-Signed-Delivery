from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert "service" in body
    assert "environment" in body
    assert "message" in body
    assert "version" in body


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready() -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_config() -> None:
    response = client.get("/config")
    assert response.status_code == 200
    body = response.json()
    assert "app_name" in body
    assert "app_env" in body
    assert "app_message" in body


def test_secret_check() -> None:
    response = client.get("/secret-check")
    assert response.status_code == 200
    assert "secret_present" in response.json()


def test_cpu_endpoint_small_load() -> None:
    response = client.get("/cpu?iterations=1000")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_cpu_endpoint_invalid_large_load() -> None:
    response = client.get("/cpu?iterations=10000001")
    assert response.status_code == 200
    assert response.json()["status"] == "rejected"