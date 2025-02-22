import httpx
from fastapi import HTTPException
import os
import json
import logging

logger = logging.getLogger(__name__)

async def query_ollama(input_text: str, model_name: str) -> str:
    """
    Query a local Ollama instance running Deepseek
    """
    ollama_url = os.getenv("OLLAMA_API_URL", "http://ollama:11434")
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:  # Increased timeout to 120 seconds
            logger.info(f"Sending request to Ollama API: {ollama_url}")
            
            response = await client.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": input_text,
                    "stream": False,
                    "options": {
                        "num_predict": 100,  # Limit response length
                        "temperature": 0.7   # Add some randomness but keep responses focused
                    }
                }
            )
            
            if response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail="Model not found. Please ensure the model is pulled and available."
                )
            
            if response.status_code != 200:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Ollama API error: {response.text}"
                )
            
            result = response.json()
            return result["response"]
            
    except httpx.TimeoutException:
        logger.error("Ollama API request timed out after 120 seconds")
        raise HTTPException(
            status_code=504,
            detail="Ollama API request timed out. The model might be overloaded or needs more resources."
        )
    except Exception as e:
        logger.error(f"Error querying Ollama: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) 