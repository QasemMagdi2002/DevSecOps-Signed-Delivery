from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_and_config_smoke() -> None:
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"status": "ok"}

    config = client.get("/config")
    assert config.status_code == 200

    body = config.json()
    assert "app_name" in body
    assert "app_env" in body
    assert "app_message" in body