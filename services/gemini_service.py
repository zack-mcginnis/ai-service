import google.generativeai as genai
from fastapi import HTTPException
import os
import asyncio

async def query_gemini(input_text: str, model_name: str) -> str:
    """
    Query Google's Gemini API
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    try:
        # Run in threadpool since Gemini's Python client is synchronous
        model = genai.GenerativeModel(model_name)
        response = await asyncio.to_thread(
            model.generate_content,
            input_text
        )
        return response.text
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}") 