#!/usr/bin/env python3
"""
Pre-fetch real data from yfinance to populate cache
This should be run periodically (e.g., via cron) to ensure data availability
"""
import json
import os
import time
from datetime import datetime
from simple_scraper import SimpleEarningsScraper
from improved_historical_scraper import ImprovedHistoricalScraper
from transcript_scraper import TranscriptScraper
from cache_manager import cache_manager
from rate_limiter import yfinance_limiter

def prefetch_stock_data():
    """Pre-fetch data for popular stocks"""
    
    # Load stock list
    with open("../data/nyse_stocks.json", "r") as f:
        stock_data = json.load(f)
    
    # Priority stocks to always have fresh data
    priority_stocks = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", 
        "JPM", "JNJ", "WMT", "SOFI", "HIMS", "AMD", "PLTR", "V",
        "MA", "PG", "HD", "DIS", "ADBE", "CRM", "NFLX", "PFE"
    ]
    
    simple_scraper = SimpleEarningsScraper()
    historical_scraper = ImprovedHistoricalScraper()
    transcript_scraper = TranscriptScraper()
    
    success_count = 0
    error_count = 0
    
    for ticker in priority_stocks:
        print(f"\nPre-fetching data for {ticker}...")
        
        try:
            # Apply rate limiting
            yfinance_limiter.wait_if_needed()
            
            # Fetch earnings summary
            summary = simple_scraper.get_earnings_summary(ticker)
            print(f"  ✓ Earnings summary fetched")
            
            # Small delay between different data types
            time.sleep(1)
            
            # Fetch historical data
            historical = historical_scraper.get_historical_earnings(ticker)
            print(f"  ✓ Historical data fetched")
            
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            error_count += 1
            continue
        
        # Delay between stocks
        time.sleep(2)
    
    print(f"\n=== Pre-fetch Complete ===")
    print(f"Success: {success_count}")
    print(f"Errors: {error_count}")
    print(f"Cache populated at: {datetime.now()}")
    
    # Save prefetch status
    status = {
        "last_run": datetime.now().isoformat(),
        "success_count": success_count,
        "error_count": error_count,
        "stocks_processed": priority_stocks[:success_count]
    }
    
    with open("../data/cache/prefetch_status.json", "w") as f:
        json.dump(status, f, indent=2)

if __name__ == "__main__":
    prefetch_stock_data()