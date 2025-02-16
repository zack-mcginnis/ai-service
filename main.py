from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db
from models import Base, Example
from schemas import ExampleCreate, Example as ExampleSchema, AIRequest, AIResponse, Provider
from services.openai_service import query_openai
from services.anthropic_service import query_anthropic
from services.gemini_service import query_gemini
from services.ollama_service import query_ollama

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="AI Service API")

@app.post("/examples/", response_model=ExampleSchema)
def create_example(example: ExampleCreate, db: Session = Depends(get_db)):
    db_example = Example(name=example.name)
    db.add(db_example)
    db.commit()
    db.refresh(db_example)
    return db_example

@app.get("/examples/", response_model=List[ExampleSchema])
def read_examples(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    examples = db.query(Example).offset(skip).limit(limit).all()
    return examples

@app.get("/examples/{example_id}", response_model=ExampleSchema)
def read_example(example_id: int, db: Session = Depends(get_db)):
    example = db.query(Example).filter(Example.id == example_id).first()
    if example is None:
        raise HTTPException(status_code=404, detail="Example not found")
    return example

@app.get("/generate")
async def generate(
    input: str,
    provider: str,
    ai_model: str
):
    supported_providers = ["openai", "anthropic", "gemini", "deepseek"]
    if provider not in supported_providers:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid provider. Supported providers are: {', '.join(supported_providers)}"
        )
        
    try:
        if provider == "openai":
            return {"output": await query_openai(input, ai_model)}
        elif provider == "anthropic":
            return {"output": await query_anthropic(input, ai_model)}
        elif provider == "gemini":
            return {"output": await query_gemini(input, ai_model)}
        elif provider == "deepseek":
            return {"output": await query_ollama(input, ai_model)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 