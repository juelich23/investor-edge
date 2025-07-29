#!/usr/bin/env python3
"""
Populate cache with real data - run this locally or during off-peak hours
"""
import json
import time
from datetime import datetime
from alternative_data import alt_fetcher
from simple_scraper import SimpleEarningsScraper
import sys

def populate_cache_carefully():
    """Carefully populate cache with real data"""
    
    # Priority stocks
    priority_stocks = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", 
        "JPM", "JNJ", "WMT", "SOFI", "HIMS", "AMD", "PLTR"
    ]
    
    scraper = SimpleEarningsScraper()
    success = 0
    failed = 0
    
    print(f"Starting cache population at {datetime.now()}")
    print(f"Processing {len(priority_stocks)} priority stocks...")
    
    for i, ticker in enumerate(priority_stocks):
        print(f"\n[{i+1}/{len(priority_stocks)}] Processing {ticker}...")
        
        try:
            # Use alternative fetcher with longer delays
            data = alt_fetcher.get_stock_data(ticker)
            if data:
                print(f"  ✓ Basic data cached for {ticker}")
                success += 1
            else:
                print(f"  ✗ Failed to fetch data for {ticker}")
                failed += 1
            
            # Wait between requests
            print("  Waiting 15 seconds before next request...")
            time.sleep(15)
            
        except Exception as e:
            print(f"  ✗ Error for {ticker}: {e}")
            failed += 1
            time.sleep(30)  # Longer wait on error
    
    print(f"\n=== Cache Population Complete ===")
    print(f"Success: {success}")
    print(f"Failed: {failed}")
    print(f"Completed at: {datetime.now()}")

if __name__ == "__main__":
    if "--confirm" not in sys.argv:
        print("This script will make API requests to populate the cache.")
        print("Run with --confirm to proceed.")
        print("Best to run during off-peak hours (late night/early morning)")
        sys.exit(1)
    
    populate_cache_carefully()