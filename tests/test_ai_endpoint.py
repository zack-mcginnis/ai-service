import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app
import os

client = TestClient(app)

@patch.dict(os.environ, {'OPENAI_API_KEY': 'mock-openai-key'})
@patch('services.openai_service.AsyncOpenAI')
def test_ai_generate_openai(mock_openai):
    # Setup mock
    mock_client = AsyncMock()
    mock_openai.return_value = mock_client
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock(message=AsyncMock(content="Mocked OpenAI response"))]
    mock_client.chat.completions.create.return_value = mock_response
    
    response = client.get(
        "/ai/generate",
        params={
            "input": "Say 'Hello, Test!'",
            "provider": "openai",
            "ai_model": "gpt-3.5-turbo"
        }
    )
    assert response.status_code == 200
    assert response.json()["output"] == "Mocked OpenAI response"

@patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'mock-anthropic-key'})
@patch('services.anthropic_service.AsyncAnthropic')
def test_ai_generate_anthropic(mock_anthropic):
    # Setup mock
    mock_client = AsyncMock()
    mock_anthropic.return_value = mock_client
    mock_response = AsyncMock()
    mock_response.content = [AsyncMock(text="Mocked Anthropic response")]
    mock_client.messages.create.return_value = mock_response
    
    response = client.get(
        "/ai/generate",
        params={
            "input": "Say 'Hello, Test!'",
            "provider": "anthropic",
            "ai_model": "claude-3-sonnet-20240229"
        }
    )
    assert response.status_code == 200
    assert response.json()["output"] == "Mocked Anthropic response"

@patch.dict(os.environ, {'GOOGLE_API_KEY': 'mock-google-key'})
@patch('services.gemini_service.genai')
def test_ai_generate_gemini(mock_genai):
    # Setup mock
    mock_model = AsyncMock()
    mock_response = AsyncMock()
    mock_response.text = "Mocked Gemini response"
    mock_model.generate_content.return_value = mock_response
    mock_genai.GenerativeModel.return_value = mock_model
    
    response = client.get(
        "/ai/generate",
        params={
            "input": "Say 'Hello, Test!'",
            "provider": "gemini",
            "ai_model": "gemini-pro"
        }
    )
    assert response.status_code == 200
    assert response.json()["output"] == "Mocked Gemini response"

def test_ai_generate_invalid_provider():
    response = client.get(
        "/ai/generate",
        params={
            "input": "test",
            "provider": "invalid",
            "ai_model": "test-model"
        }
    )
    assert response.status_code == 400
    assert "Invalid provider" in response.json()["detail"] 