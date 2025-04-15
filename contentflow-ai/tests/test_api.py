"""
Pytest unit tests for ContentFlow AI FastAPI endpoints.
Covers expected, edge, and failure cases for all main routes.
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from src.api.main import app
from src.api.db import get_session
from src.api.models.core import Content, ContentType
import uuid

# Use an in-memory SQLite DB for tests
test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})

# Create tables before each test session
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    SQLModel.metadata.create_all(test_engine)

# Dependency override for DB session
def override_get_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)

# --- Content Extraction Endpoint Tests ---
from jose import jwt
import os
SECRET_KEY = os.environ.get("CFLOW_JWT_SECRET", "dev-secret-key")
ALGORITHM = "HS256"
def make_token(username="testuser", role="user", secret=SECRET_KEY):
    return jwt.encode({"sub": username, "role": role}, secret, algorithm=ALGORITHM)

def test_extract_content_expected():
    token = make_token()
    resp = client.post(
        "/content/extract",
        json={"url": "https://example.com", "type": "web"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "pending"
    assert "id" in data

def test_extract_content_missing_url():
    token = make_token()
    resp = client.post("/content/extract", json={"type": "web"}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 422

def test_extract_content_invalid_type():
    token = make_token()
    resp = client.post("/content/extract", json={"url": "https://example.com", "type": 123}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 422

def test_extract_content_unauthorized():
    resp = client.post("/content/extract", json={"url": "https://example.com", "type": "web"})
    assert resp.status_code in (401, 403)

# --- Content Listing Endpoint Tests ---
def test_list_content_items_empty():
    token = make_token()
    resp = client.get("/management/items", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json() == []

def test_list_content_items_after_insert():
    token = make_token()
    # Insert content
    client.post("/content/extract", json={"url": "https://example.com/2", "type": "web"}, headers={"Authorization": f"Bearer {token}"})
    resp = client.get("/management/items", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) >= 1
    assert any(item["source_url"] == "https://example.com/2" for item in items)

def test_list_content_items_unauthorized():
    resp = client.get("/management/items")
    assert resp.status_code in (401, 403)

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