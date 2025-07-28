from sqlalchemy import create_engine, Column, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = "sqlite:///./investor_edge.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class EarningsTranscript(Base):
    __tablename__ = "earnings_transcripts"
    
    id = Column(String, primary_key=True)  # Format: TICKER_QUARTER_YEAR
    ticker = Column(String, index=True)
    company_name = Column(String)
    quarter = Column(String)
    date = Column(DateTime)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class EarningsSummary(Base):
    __tablename__ = "earnings_summaries"
    
    id = Column(String, primary_key=True)  # Format: TICKER_QUARTER_YEAR
    ticker = Column(String, index=True)
    quarter = Column(String)
    date = Column(DateTime)
    summary = Column(Text)
    sentiment_score = Column(Float)
    kpis = Column(JSON)
    processed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")