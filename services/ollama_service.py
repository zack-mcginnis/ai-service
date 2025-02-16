import httpx
from fastapi import HTTPException
import os
import json

async def query_ollama(input_text: str, model_name: str) -> str:
    """
    Query a local Ollama instance running Deepseek
    """
    ollama_url = os.getenv("OLLAMA_API_URL", "http://ollama:11434")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": input_text,
                    "stream": False
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Ollama API error: {response.text}"
                )
            
            result = response.json()
            return result["response"]
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ollama API request timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama API error: {str(e)}") 