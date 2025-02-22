from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/examples/", response_model=ExampleSchema)
def create_example(example: ExampleCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating new example: {example.name}")
    try:
        db_example = Example(name=example.name)
        db.add(db_example)
        db.commit()
        db.refresh(db_example)
        return db_example
    except Exception as e:
        logger.error(f"Error creating example: {str(e)}", exc_info=True)
        raise

@app.get("/examples/", response_model=List[ExampleSchema])
def read_examples(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Fetching examples - skip: {skip}, limit: {limit}")
    try:
        examples = db.query(Example).offset(skip).limit(limit).all()
        return examples
    except Exception as e:
        logger.error(f"Error fetching examples: {str(e)}", exc_info=True)
        raise

@app.get("/examples/{example_id}", response_model=ExampleSchema)
def read_example(example_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching example with id: {example_id}")
    try:
        example = db.query(Example).filter(Example.id == example_id).first()
        if example is None:
            logger.warning(f"Example not found: {example_id}")
            raise HTTPException(status_code=404, detail="Example not found")
        return example
    except Exception as e:
        logger.error(f"Error fetching example: {str(e)}", exc_info=True)
        raise

@app.get("/generate")
async def generate(
    input: str,
    provider: str,
    ai_model: str
):
    logger.info(f"Received request - Provider: {provider}, Model: {ai_model}")
    logger.info(f"Input text: {input[:100]}...")  # Log first 100 chars of input
    
    supported_providers = ["openai", "anthropic", "gemini", "deepseek"]
    if provider not in supported_providers:
        error_msg = f"Invalid provider. Supported providers are: {', '.join(supported_providers)}"
        logger.error(error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
        
    try:
        if provider == "openai":
            logger.info("Calling OpenAI API")
            response = await query_openai(input, ai_model)
        elif provider == "anthropic":
            logger.info("Calling Anthropic API")
            response = await query_anthropic(input, ai_model)
        elif provider == "gemini":
            logger.info("Calling Gemini API")
            response = await query_gemini(input, ai_model)
        elif provider == "deepseek":
            logger.info("Calling Ollama API")
            response = await query_ollama(input, ai_model)
            
        logger.info("Successfully generated response")
        return {"output": response}
    
    except Exception as e:
        error_msg = f"Error processing request: {str(e)}"
        logger.error(error_msg, exc_info=True)  # Include stack trace
        raise HTTPException(status_code=500, detail=error_msg) 