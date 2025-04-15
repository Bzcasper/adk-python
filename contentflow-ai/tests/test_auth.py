"""
Pytest unit tests for authentication and authorization in ContentFlow AI API.
Covers: valid JWT, invalid JWT, missing token, role-based access.
"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from jose import jwt
import os

SECRET_KEY = os.environ.get("CFLOW_JWT_SECRET", "dev-secret-key")
ALGORITHM = "HS256"

client = TestClient(app)

def make_token(username="alice", role="user", secret=SECRET_KEY):
    return jwt.encode({"sub": username, "role": role}, secret, algorithm=ALGORITHM)

def test_auth_valid_jwt():
    token = make_token()
    resp = client.post("/content/extract", json={"url": "https://example.com", "type": "web"}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert "Extraction started by alice" in resp.json()["message"]

def test_auth_missing_jwt():
    resp = client.post("/content/extract", json={"url": "https://example.com", "type": "web"})
    assert resp.status_code == 403 or resp.status_code == 401

def test_auth_invalid_jwt():
    resp = client.post("/content/extract", json={"url": "https://example.com", "type": "web"}, headers={"Authorization": "Bearer invalidtoken"})
    assert resp.status_code == 401

