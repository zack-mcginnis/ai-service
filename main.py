from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db
from models import Base, Example
from schemas import ExampleCreate, Example as ExampleSchema

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