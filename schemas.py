from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class ExampleBase(BaseModel):
    name: str

class ExampleCreate(ExampleBase):
    pass

class Example(ExampleBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AIConfig(BaseModel):
    ai_model: str
    api: str

class AIRequest(BaseModel):
    input: str
    config: AIConfig

class AIResponse(BaseModel):
    output: str 