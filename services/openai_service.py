from openai import AsyncOpenAI
from fastapi import HTTPException
import os

async def query_openai(input_text: str, model_name: str) -> str:
    """
    Query OpenAI's API
    """
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    try:
        response = await client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": input_text}
            ]
        )
        return response.choices[0].message.content
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}") 