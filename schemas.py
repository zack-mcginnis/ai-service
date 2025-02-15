from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ExampleBase(BaseModel):
    name: str

class ExampleCreate(ExampleBase):
    pass

class Example(ExampleBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 