"""
Pytest unit tests for ContentFlow AI FastAPI endpoints.
Covers expected, edge, and failure cases for all main routes.
"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

# --- Content Extraction Endpoint Tests ---
def test_extract_content_expected():
    resp = client.post("/content/extract", json={"url": "https://example.com", "type": "web"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "pending"
    assert "id" in data

def test_extract_content_missing_url():
    resp = client.post("/content/extract", json={"type": "web"})
    assert resp.status_code == 422

def test_extract_content_invalid_type():
    resp = client.post("/content/extract", json={"url": "https://example.com", "type": 123})
    assert resp.status_code == 422

# --- Content Processing Endpoint Tests ---
def test_process_content_expected():
    resp = client.post("/processing/run", json={"content_id": "abc", "operation": "summarize", "params": {}})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert "result" in data

def test_process_content_missing_content_id():
    resp = client.post("/processing/run", json={"operation": "summarize", "params": {}})
    assert resp.status_code == 422

# --- Content Management Endpoint Tests ---
def test_list_content_items_expected():
    resp = client.get("/management/items")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]
    assert "title" in data[0]

def test_list_content_items_empty(monkeypatch):
    from src.api.routes import management
    monkeypatch.setattr(management, "list_content_items", lambda: [])
    resp = client.get("/management/items")
    assert resp.status_code == 200
    assert resp.json() == []
