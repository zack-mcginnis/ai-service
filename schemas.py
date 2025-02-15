from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict
from enum import Enum

class ExampleBase(BaseModel):
    name: str

class ExampleCreate(ExampleBase):
    pass

class Example(ExampleBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Provider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"

class AIConfig(BaseModel):
    provider: Provider
    ai_model: str

class AIRequest(BaseModel):
    input: str
    config: AIConfig

class AIResponse(BaseModel):
    output: str 