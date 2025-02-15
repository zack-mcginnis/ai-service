from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db
from models import Base, Example
from schemas import ExampleCreate, Example as ExampleSchema, AIRequest, AIResponse, Provider
from services.openai_service import query_openai
from services.anthropic_service import query_anthropic
from services.gemini_service import query_gemini

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

@app.get("/ai/generate", response_model=AIResponse)
async def generate_ai_response(request: AIRequest):
    """
    Generate AI response using specified provider and model
    """
    try:
        if request.config.provider == Provider.OPENAI:
            output = await query_openai(
                input_text=request.input,
                model_name=request.config.ai_model
            )
        elif request.config.provider == Provider.ANTHROPIC:
            output = await query_anthropic(
                input_text=request.input,
                model_name=request.config.ai_model
            )
        elif request.config.provider == Provider.GEMINI:
            output = await query_gemini(
                input_text=request.input,
                model_name=request.config.ai_model
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported provider")
            
        return AIResponse(output=output)
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 