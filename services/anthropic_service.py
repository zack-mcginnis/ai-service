from anthropic import AsyncAnthropic
from fastapi import HTTPException
import os

async def query_anthropic(input_text: str, model_name: str) -> str:
    """
    Query Anthropic's API
    """
    client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    try:
        message = await client.messages.create(
            model=model_name,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": input_text}
            ]
        )
        return message.content[0].text
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Anthropic API error: {str(e)}") 