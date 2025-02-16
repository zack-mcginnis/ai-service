import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from services.openai_service import query_openai
from services.anthropic_service import query_anthropic
from services.gemini_service import query_gemini
from services.ollama_service import query_ollama

pytestmark = pytest.mark.asyncio

@patch('services.openai_service.AsyncOpenAI')
async def test_openai_service(mock_openai):
    # Setup mock
    mock_client = AsyncMock()
    mock_openai.return_value = mock_client
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock(message=AsyncMock(content="Mocked OpenAI response"))]
    mock_client.chat.completions.create.return_value = mock_response

    response = await query_openai(
        input_text="Say 'Hello, Test!'",
        model_name="gpt-3.5-turbo"
    )
    
    assert response == "Mocked OpenAI response"
    mock_client.chat.completions.create.assert_called_once()

@patch('services.anthropic_service.AsyncAnthropic')
async def test_anthropic_service(mock_anthropic):
    # Setup mock
    mock_client = AsyncMock()
    mock_anthropic.return_value = mock_client
    mock_response = AsyncMock()
    mock_response.content = [AsyncMock(text="Mocked Anthropic response")]
    mock_client.messages.create.return_value = mock_response

    response = await query_anthropic(
        input_text="Say 'Hello, Test!'",
        model_name="claude-3-sonnet-20240229"
    )
    
    assert response == "Mocked Anthropic response"
    mock_client.messages.create.assert_called_once()

@patch('services.gemini_service.genai')
async def test_gemini_service(mock_genai):
    # Setup mock
    mock_model = AsyncMock()
    mock_response = AsyncMock()
    mock_response.text = "Mocked Gemini response"
    mock_model.generate_content.return_value = mock_response
    mock_genai.GenerativeModel.return_value = mock_model

    response = await query_gemini(
        input_text="Say 'Hello, Test!'",
        model_name="gemini-pro"
    )
    
    assert response == "Mocked Gemini response"
    mock_genai.GenerativeModel.assert_called_once_with("gemini-pro")

@patch('services.ollama_service.httpx.AsyncClient')
async def test_ollama_service(mock_client):
    # Setup mock
    mock_client_instance = AsyncMock()
    mock_client.return_value.__aenter__.return_value = mock_client_instance
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "Mocked Ollama response"}
    mock_client_instance.post.return_value = mock_response

    response = await query_ollama(
        input_text="Say 'Hello, Test!'",
        model_name="deepseek-coder:6.7b"
    )
    
    assert response == "Mocked Ollama response"
    mock_client_instance.post.assert_called_once() 