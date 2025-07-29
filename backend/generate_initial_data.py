#!/usr/bin/env python3
"""
Generate initial data for all stocks to avoid API calls in production
"""
import json
import os
import time
from datetime import datetime
from simple_scraper import SimpleEarningsScraper
from historical_scraper import HistoricalEarningsScraper
from transcript_scraper import TranscriptScraper
from ai_engine import AIEngine
from enhanced_ai_engine import EnhancedAIEngine

def generate_mock_financial_data(ticker: str) -> dict:
    """Generate realistic mock financial data when API fails"""
    base_prices = {
        "AAPL": 195.89, "MSFT": 440.37, "GOOGL": 163.94, "AMZN": 219.65,
        "META": 595.94, "TSLA": 248.23, "NVDA": 132.65, "JPM": 245.84,
        "JNJ": 145.21, "WMT": 97.20, "SOFI": 15.42, "HIMS": 24.85,
        "AMD": 138.25, "PLTR": 73.12
    }
    
    base_price = base_prices.get(ticker, 100)
    
    return {
        "ticker": ticker,
        "company": ticker,
        "quarter": "Q3 2024",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "content": f"""
{ticker} Financial Overview
Data as of: {datetime.now().strftime('%Y-%m-%d')}

Company Metrics:
Stock Price: ${base_price:.2f}
Market Cap: ${(base_price * 1000000000):.0f}
52-Week High: ${base_price * 1.3:.2f}
52-Week Low: ${base_price * 0.7:.2f}

Valuation Metrics:
P/E Ratio (TTM): {20 + (ord(ticker[0]) % 20):.1f}
Forward P/E: {18 + (ord(ticker[1]) % 15):.1f}
PEG Ratio: {1.2 + (ord(ticker[0]) % 10) / 10:.2f}
Price to Book: {3.5 + (ord(ticker[1]) % 5):.1f}

Financial Performance:
Revenue (TTM): ${(base_price * 100000000):.0f}
Revenue Growth (YoY): {10 + (ord(ticker[0]) % 20):.1f}%
Gross Margin: {30 + (ord(ticker[1]) % 40):.1f}%
Operating Margin: {15 + (ord(ticker[0]) % 25):.1f}%
Net Margin: {10 + (ord(ticker[1]) % 20):.1f}%

Trading Information:
Beta: {0.8 + (ord(ticker[0]) % 10) / 10:.2f}
Dividend Yield: {(ord(ticker[1]) % 4):.2f}%
Previous Close: ${base_price * 0.98:.2f}
Day Range: ${base_price * 0.97:.2f} - ${base_price * 1.02:.2f}
Volume: {1000000 + (ord(ticker[0]) * 100000):,}
Average Volume: {1500000 + (ord(ticker[1]) * 100000):,}
        """.strip(),
        "source": "mock-data"
    }

def main():
    # Create directories
    os.makedirs("../data/initial", exist_ok=True)
    
    # Load stock list
    with open("../data/nyse_stocks.json", "r") as f:
        stock_data = json.load(f)
    
    # Get top 50 stocks
    top_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", 
                  "JPM", "JNJ", "WMT", "SOFI", "HIMS", "AMD", "PLTR", "V",
                  "MA", "PG", "HD", "DIS", "ADBE", "CRM", "NFLX", "PFE",
                  "TMO", "ABT", "CVX", "ABBV", "NKE", "MRK", "UNH", "XOM",
                  "T", "VZ", "INTC", "CSCO", "ORCL", "IBM", "QCOM", "TXN",
                  "HON", "UPS", "PM", "RTX", "CAT", "BA", "MMM", "GS", 
                  "BLK", "AMGN", "GILD"]
    
    all_data = {}
    
    for i, ticker in enumerate(top_stocks):
        print(f"Generating data for {ticker} ({i+1}/{len(top_stocks)})...")
        
        try:
            # Generate mock data
            financial_data = generate_mock_financial_data(ticker)
            
            # Generate mock historical data
            historical_data = {
                "ticker": ticker,
                "quarters": []
            }
            
            for q in range(4):
                quarter_data = {
                    "quarter": f"Q{q+1} 2024",
                    "date": f"2024-{(q+1)*3:02d}-15",
                    "revenue": (100 + q * 10) * 1000000,
                    "revenue_growth": 10 + q * 2,
                    "eps_actual": 1.5 + q * 0.1,
                    "eps_estimate": 1.4 + q * 0.1,
                    "earnings_surprise": ((0.1 + q * 0.01) / (1.4 + q * 0.1)) * 100,
                    "stock_price": float(financial_data["content"].split("Stock Price: $")[1].split("\n")[0]) * (0.9 + q * 0.05)
                }
                historical_data["quarters"].append(quarter_data)
            
            # Generate mock transcript
            transcript_data = {
                "ticker": ticker,
                "content": f"Earnings call transcript for {ticker}. Management discussed strong performance and positive outlook.",
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            
            # Store all data
            all_data[ticker] = {
                "financial": financial_data,
                "historical": historical_data,
                "transcript": transcript_data,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating data for {ticker}: {e}")
            continue
        
        # Small delay to avoid any potential issues
        time.sleep(0.1)
    
    # Save all data
    with open("../data/initial/stock_data.json", "w") as f:
        json.dump(all_data, f, indent=2)
    
    print(f"\nGenerated initial data for {len(all_data)} stocks")
    print("Saved to ../data/initial/stock_data.json")

if __name__ == "__main__":
    main()