from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import os
from datetime import datetime
from historical_scraper import HistoricalEarningsScraper

app = FastAPI(title="Investor Edge API")

from config import settings

# Create necessary directories on startup
os.makedirs("../data/cache", exist_ok=True)
os.makedirs("../data/summaries", exist_ok=True)
os.makedirs("../data/transcripts", exist_ok=True)
os.makedirs("../data/historical", exist_ok=True)
os.makedirs("../data/analyses", exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin for origin in settings.allowed_origins if origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscriptResponse(BaseModel):
    ticker: str
    quarter: str
    content: str
    date: str

class SummaryResponse(BaseModel):
    ticker: str
    quarter: str
    summary: str
    sentiment_score: float
    kpis: Dict[str, str]
    date: Optional[str] = None
    financial_data: Optional[Dict[str, str]] = None
    guidance: Optional[Dict[str, Any]] = None
    transcript_analysis: Optional[Dict[str, Any]] = None

class HistoricalAnalysis(BaseModel):
    revenue_growth: Optional[float] = None
    eps_growth: Optional[float] = None
    avg_surprise: Optional[float] = None
    volatility: Optional[float] = None
    trend_direction: str = "neutral"

class TrendPoint(BaseModel):
    date: str
    value: float

class HistoricalMetrics(BaseModel):
    revenue_trend: List[TrendPoint]
    eps_trend: List[TrendPoint]
    earnings_dates: List[str]

class HistoricalEarningsResponse(BaseModel):
    ticker: str
    quarters: List[Dict]
    metrics: HistoricalMetrics
    analysis: HistoricalAnalysis

@app.get("/")
def read_root():
    return {"message": "Investor Edge API is running"}

@app.get("/api/transcripts/{ticker}")
async def get_transcript(ticker: str):
    ticker = ticker.upper()
    transcript_path = f"../data/transcripts/{ticker}_latest.json"
    
    if not os.path.exists(transcript_path):
        # Try to scrape if it doesn't exist
        from simple_scraper import SimpleEarningsScraper
        
        try:
            scraper = SimpleEarningsScraper()
            transcript_data = scraper.get_earnings_summary(ticker)
            
            # Save transcript
            os.makedirs("../data/transcripts", exist_ok=True)
            with open(transcript_path, 'w') as f:
                json.dump(transcript_data, f, indent=2)
                
            return TranscriptResponse(**transcript_data)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Unable to fetch transcript for {ticker}: {str(e)}")
    
    with open(transcript_path, 'r') as f:
        data = json.load(f)
    
    return TranscriptResponse(**data)

@app.get("/api/summaries/{ticker}")
async def get_summary(ticker: str):
    ticker = ticker.upper()
    summary_path = f"../data/summaries/{ticker}_latest.json"
    transcript_path = f"../data/transcripts/{ticker}_latest.json"
    
    # If summary doesn't exist, try to create it
    if not os.path.exists(summary_path):
        # Import scraper and AI engine
        from simple_scraper import SimpleEarningsScraper
        from ai_engine import AIEngine
        
        try:
            # Scrape latest earnings data
            scraper = SimpleEarningsScraper()
            transcript_data = scraper.get_earnings_summary(ticker)
            
            # Save transcript
            os.makedirs("../data/transcripts", exist_ok=True)
            with open(transcript_path, 'w') as f:
                json.dump(transcript_data, f, indent=2)
            
            # Generate AI summary
            ai_engine = AIEngine()
            summary = ai_engine.summarize_transcript(transcript_data['content'])
            
            # Prepare summary data
            summary_data = {
                "ticker": ticker,
                "quarter": transcript_data.get('quarter', 'Latest'),
                "summary": summary['summary'],
                "sentiment_score": summary['sentiment_score'],
                "kpis": summary['kpis'],
                "guidance": summary.get('guidance', {}),
                "date": transcript_data.get('date', datetime.now().strftime("%Y-%m-%d"))
            }
            
            # Save summary
            os.makedirs("../data/summaries", exist_ok=True)
            with open(summary_path, 'w') as f:
                json.dump(summary_data, f, indent=2)
                
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Unable to fetch data for {ticker}: {str(e)}")
    
    else:
        with open(summary_path, 'r') as f:
            summary_data = json.load(f)
    
    # Try to load financial data from transcript
    financial_data = None
    if os.path.exists(transcript_path):
        with open(transcript_path, 'r') as f:
            transcript_data = json.load(f)
            # Extract financial metrics from transcript content
            content = transcript_data.get('content', '')
            financial_data = extract_financial_metrics(content)
    
    response_data = summary_data.copy()
    response_data['financial_data'] = financial_data
    # Ensure guidance is included
    if 'guidance' not in response_data:
        response_data['guidance'] = {}
    
    # Check if we have transcript analysis
    analysis_path = f"../data/analyses/{ticker}_latest_analysis.json"
    if os.path.exists(analysis_path):
        with open(analysis_path, 'r') as f:
            transcript_analysis = json.load(f)
            response_data['transcript_analysis'] = transcript_analysis.get('analysis', {})
    
    return SummaryResponse(**response_data)

def extract_financial_metrics(content: str) -> Dict:
    """Extract financial metrics from transcript content"""
    metrics = {}
    lines = content.split('\n')
    
    for line in lines:
        if 'Stock Price:' in line:
            metrics['currentPrice'] = line.split('$')[-1].strip()
        elif 'Market Cap:' in line:
            metrics['marketCap'] = line.split('$')[-1].strip()
        elif '52-Week High:' in line:
            metrics['yearHigh'] = line.split('$')[-1].strip()
        elif '52-Week Low:' in line:
            metrics['yearLow'] = line.split('$')[-1].strip()
        elif 'P/E Ratio (TTM):' in line:
            metrics['peRatio'] = line.split(':')[-1].strip()
        elif 'Revenue Growth (YoY):' in line:
            metrics['revenueGrowth'] = line.split(':')[-1].strip()
        elif 'Profit Margins:' in line and 'margins' not in line.lower():
            metrics['profitMargins'] = line.split(':')[-1].strip()
        elif 'EPS (TTM):' in line:
            metrics['epsTrailing'] = line.split('$')[-1].strip()
        elif 'Recommendation:' in line:
            metrics['recommendation'] = line.split(':')[-1].strip()
        elif 'Target Mean Price:' in line:
            metrics['targetPrice'] = line.split('$')[-1].strip()
    
    return metrics

@app.get("/api/companies")
async def get_companies(limit: int = 10, search: Optional[str] = None):
    # Load stock data
    stock_file = "../data/nyse_stocks.json"
    
    if os.path.exists(stock_file):
        with open(stock_file, 'r') as f:
            stock_data = json.load(f)
            all_stocks = stock_data.get('stocks', [])
    else:
        # Fallback to original list
        all_stocks = [
            {"ticker": "AAPL", "name": "Apple Inc.", "sector": "Technology", "market_cap": 3000000000000},
            {"ticker": "MSFT", "name": "Microsoft Corporation", "sector": "Technology", "market_cap": 2800000000000},
            {"ticker": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology", "market_cap": 1800000000000},
            {"ticker": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Discretionary", "market_cap": 1700000000000},
            {"ticker": "META", "name": "Meta Platforms Inc.", "sector": "Technology", "market_cap": 1200000000000},
            {"ticker": "TSLA", "name": "Tesla Inc.", "sector": "Consumer Discretionary", "market_cap": 800000000000},
            {"ticker": "NVDA", "name": "NVIDIA Corporation", "sector": "Technology", "market_cap": 1100000000000},
            {"ticker": "JPM", "name": "JPMorgan Chase & Co.", "sector": "Financials", "market_cap": 500000000000},
            {"ticker": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare", "market_cap": 450000000000},
            {"ticker": "WMT", "name": "Walmart Inc.", "sector": "Consumer Staples", "market_cap": 400000000000}
        ]
    
    # Filter by search term if provided
    if search:
        search_lower = search.lower()
        filtered_stocks = [
            stock for stock in all_stocks
            if search_lower in stock['ticker'].lower() or 
               search_lower in stock['name'].lower() or
               (stock.get('sector') and search_lower in stock['sector'].lower())
        ]
    else:
        filtered_stocks = all_stocks
    
    # Limit results
    limited_stocks = filtered_stocks[:limit]
    
    return {
        "companies": limited_stocks,
        "total": len(filtered_stocks),
        "has_more": len(filtered_stocks) > limit
    }

@app.get("/api/transcript/{ticker}")
async def get_earnings_transcript(ticker: str):
    """Fetch and analyze full earnings call transcript"""
    ticker = ticker.upper()
    
    # Check if we have a cached analysis
    analysis_path = f"../data/analyses/{ticker}_latest_analysis.json"
    if os.path.exists(analysis_path):
        with open(analysis_path, 'r') as f:
            return json.load(f)
    
    # Otherwise, fetch and analyze
    from transcript_scraper import EarningsTranscriptScraper, COMPANY_DOMAINS
    from enhanced_ai_engine import TranscriptProcessor
    
    try:
        # Fetch transcript
        scraper = EarningsTranscriptScraper()
        domain = COMPANY_DOMAINS.get(ticker)
        transcript_data = scraper.get_earnings_transcript(ticker, domain)
        
        # Get financial data
        from simple_scraper import SimpleEarningsScraper
        financial_scraper = SimpleEarningsScraper()
        financial_info = financial_scraper.get_earnings_summary(ticker)
        
        # Process with AI
        processor = TranscriptProcessor()
        analysis = processor.process_full_transcript(
            ticker, 
            transcript_data,
            extract_financial_metrics(financial_info.get('content', ''))
        )
        
        return analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing transcript: {str(e)}")

@app.get("/api/historical/{ticker}")
async def get_historical_earnings(ticker: str):
    ticker = ticker.upper()
    historical_path = f"../data/historical/{ticker}_history.json"
    
    # Check if cached data exists
    if os.path.exists(historical_path):
        with open(historical_path, 'r') as f:
            data = json.load(f)
        return HistoricalEarningsResponse(**data)
    
    # Otherwise, fetch fresh data
    from improved_historical_scraper import ImprovedHistoricalScraper
    
    try:
        scraper = ImprovedHistoricalScraper()
        data = scraper.get_historical_earnings(ticker)
        
        # Save for caching
        scraper.save_historical_data(ticker, data)
        
        return HistoricalEarningsResponse(**data)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Unable to fetch historical data for {ticker}: {str(e)}")