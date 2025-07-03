"""
Unit tests for chatbot API
"""

from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_ask_text_valid():
    response = client.post("/ask-text/", json={
        "user_id": "user123",
        "message": "¿Cuál será el pronóstico de precipitación en Palmira la próxima semana?"
    })
    assert response.status_code == 200
    assert "response" in response.json()
    assert "user_id" in response.json()

def test_ask_text_missing_field():
    response = client.post("/ask-text/", json={
        "message": "¿Cuál es el clima en Popayán?"
    })
    assert response.status_code == 422  # user_id is required
