import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app
from app.routes.ai import get_gemini_client

client = TestClient(app)

# Mock Gemini Response
mock_response = MagicMock()
mock_response.text = "Hello! I am your AI assistant. You spent ₹500 on Food."

@patch("google.genai.Client")
def test_ai_chat_mock(mock_genai):
    # Setup mock
    mock_instance = mock_genai.return_value
    mock_instance.models.generate_content.return_value = mock_response
    
    resp = client.post("/ai/chat", json={
        "message": "Tell me about my spending",
        "month": "4",
        "year": "2026"
    })
    
    assert resp.status_code == 200
    assert "Hello!" in resp.json()["response"]
    assert "Food" in resp.json()["response"]

@patch("app.routes.ai.get_gemini_client")
@patch("app.ocr_utils.extract_receipt_data")
def test_ocr_logic_mock(mock_extract, mock_gemini):
    # Setup mock for Gemini OCR
    mock_client = MagicMock()
    mock_gemini.return_value = (mock_client, None)
    mock_client.models.generate_content.return_value = MagicMock(text='{"amount": 1500.0, "description": "Starbucks"}')
    
    # 1. Test Local OCR Success
    mock_extract.return_value = {"amount": 500.0, "description": "Zomato"}
    resp = client.post("/ai/receipt", files={"file": ("r.jpg", b"fake", "image/jpeg")})
    assert resp.json()["description"] == "Zomato"
    
    # 2. Test Local OCR Failure -> Gemini Fallback
    mock_extract.side_effect = Exception("OCR Error")
    resp = client.post("/ai/receipt", files={"file": ("r.jpg", b"fake", "image/jpeg")})
    assert resp.json()["description"] == "Starbucks"
    assert resp.json()["method"] == "gemini_ai"
