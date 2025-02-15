from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Example(Base):
    __tablename__ = 'examples'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow) 