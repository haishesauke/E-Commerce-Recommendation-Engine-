# tests/test_api.py
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_recommend_endpoint():
    r = client.get("/recommend/999999?n=5")
    assert r.status_code == 200
    json = r.json()
    assert "recommendations" in json
    assert isinstance(json["recommendations"], list)
