import httpx
from typing import Dict
import json
import os
from fastapi import HTTPException

async def query_ai_api(input_text: str, model_name: str, api_url: str) -> str:
    """
    Send a query to an AI API following the OpenAI protocol
    """
    headers = {
        "Content-Type": "application/json",
    }
    
    # Add API key if exists in environment
    api_key = os.getenv("AI_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": input_text
            }
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                api_url,
                json=payload,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"AI API error: {response.text}"
                )
                
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="AI API request timed out")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"AI API request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 