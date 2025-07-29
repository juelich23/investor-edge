"""
Alternative data fetching using yfinance with better error handling
"""
import yfinance as yf
import time
from typing import Dict, Optional
from datetime import datetime
import requests
from cache_manager import cache_manager

class AlternativeDataFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_stock_data(self, ticker: str) -> Optional[Dict]:
        """Try multiple methods to get stock data"""
        
        # Method 1: Check cache first (extend cache time for production)
        cached_data = cache_manager.get_cached_data(ticker, "stock_info", cache_hours=168)  # 7 days cache
        if cached_data:
            print(f"Using cached data for {ticker} (7-day cache)")
            return cached_data
        
        # Method 2: Try yfinance with custom session
        try:
            print(f"Attempting to fetch {ticker} with custom session...")
            stock = yf.Ticker(ticker, session=self.session)
            
            # Get basic quote data (less likely to be rate limited)
            history = stock.history(period="1d")
            if not history.empty:
                current_price = history['Close'].iloc[-1]
                
                # Try to get more info with delay
                time.sleep(2)  # Longer delay
                
                info = {}
                try:
                    info = stock.info
                except:
                    print(f"Could not fetch full info for {ticker}, using basic data")
                
                data = {
                    "ticker": ticker,
                    "price": current_price,
                    "company": info.get('longName', ticker),
                    "marketCap": info.get('marketCap', 0),
                    "pe": info.get('trailingPE', 0),
                    "volume": int(history['Volume'].iloc[-1]),
                    "previousClose": info.get('previousClose', current_price),
                    "dayLow": history['Low'].iloc[-1],
                    "dayHigh": history['High'].iloc[-1],
                    "fiftyTwoWeekLow": info.get('fiftyTwoWeekLow', 0),
                    "fiftyTwoWeekHigh": info.get('fiftyTwoWeekHigh', 0),
                    "timestamp": datetime.now().isoformat()
                }
                
                # Cache for 7 days
                cache_manager.save_to_cache(ticker, "stock_info", data)
                return data
                
        except Exception as e:
            print(f"Alternative method failed for {ticker}: {e}")
            
        return None

# Global instance
alt_fetcher = AlternativeDataFetcher()