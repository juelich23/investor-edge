from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)
    name = Column(String)
    sector = Column(String)
    
    transcripts = relationship("EarningsTranscript", back_populates="company")
    summaries = relationship("EarningsSummary", back_populates="company")
    historical_earnings = relationship("HistoricalEarnings", back_populates="company")

class EarningsTranscript(Base):
    __tablename__ = "earnings_transcripts"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    quarter = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    content = Column(String)
    
    company = relationship("Company", back_populates="transcripts")
    summary = relationship("EarningsSummary", back_populates="transcript", uselist=False)

class EarningsSummary(Base):
    __tablename__ = "earnings_summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    transcript_id = Column(Integer, ForeignKey("earnings_transcripts.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    summary = Column(String)
    sentiment_score = Column(Float)
    kpis = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    transcript = relationship("EarningsTranscript", back_populates="summary")
    company = relationship("Company", back_populates="summaries")

class HistoricalEarnings(Base):
    __tablename__ = "historical_earnings"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    ticker = Column(String, index=True)
    date = Column(DateTime, index=True)
    quarter = Column(String)
    revenue = Column(Float)
    earnings = Column(Float)
    eps_actual = Column(Float)
    eps_estimate = Column(Float)
    surprise_percent = Column(Float)
    price_on_date = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    company = relationship("Company", back_populates="historical_earnings")

class EarningsTrend(Base):
    __tablename__ = "earnings_trends"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    ticker = Column(String, index=True)
    metric_type = Column(String)  # 'revenue', 'eps', 'sentiment'
    trend_data = Column(JSON)  # Array of {date, value} objects
    analysis = Column(JSON)  # Growth rates, volatility, etc.
    updated_at = Column(DateTime, default=datetime.utcnow)