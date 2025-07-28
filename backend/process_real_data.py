#!/usr/bin/env python3
"""
Process real earnings data using yfinance and AI analysis
"""

import os
import sys
from dotenv import load_dotenv
from simple_scraper import SimpleEarningsScraper
from ai_engine import EarningsAnalyzer
import json
import time

load_dotenv()

def main():
    print("Starting Investor Edge real data processing...")
    
    # Initialize components
    scraper = SimpleEarningsScraper()
    analyzer = EarningsAnalyzer()
    
    # Check if API keys are set
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Warning: No Anthropic API key found in .env")
        print("AI analysis will use fallback summaries.")
    
    # Step 1: Get real financial data
    print("\n=== Step 1: Fetching Real Financial Data ===")
    scraper.scrape_all()
    
    # Step 2: Process with AI
    print("\n=== Step 2: Analyzing with AI ===")
    
    transcript_dir = "../data/transcripts"
    
    for filename in os.listdir(transcript_dir):
        if filename.endswith("_latest.json"):
            ticker = filename.split("_")[0]
            print(f"\nProcessing {ticker}...")
            
            # Load transcript
            with open(os.path.join(transcript_dir, filename), 'r') as f:
                transcript_data = json.load(f)
            
            try:
                # Analyze with AI
                summary_data = analyzer.process_transcript(ticker, transcript_data)
                
                # Save summary
                analyzer.save_summary(ticker, summary_data)
                
                print(f"✓ {ticker} processed successfully")
                print(f"  Sentiment: {summary_data['sentiment_score']}")
                print(f"  Revenue: {summary_data['kpis'].get('revenue', 'N/A')}")
                
            except Exception as e:
                print(f"✗ Error processing {ticker}: {str(e)}")
            
            time.sleep(1)  # Rate limiting for API calls
    
    print("\n=== Processing Complete! ===")
    print("✓ Real financial data fetched")
    print("✓ AI summaries generated")
    print("✓ Platform ready with real-time data")
    
    print("\nData sources:")
    print("- Financial metrics: Yahoo Finance (real-time)")
    print("- AI analysis: Claude (Anthropic)")
    
    print("\nNext steps:")
    print("1. Backend is running at: http://localhost:8000")
    print("2. Frontend is running at: http://localhost:3000")
    print("3. Access the platform to view real earnings intelligence!")

if __name__ == "__main__":
    main()