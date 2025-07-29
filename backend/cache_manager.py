import json
import os
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class CacheManager:
    def __init__(self, cache_dir: str = "../data/cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
    def get_cache_path(self, ticker: str, data_type: str) -> str:
        return os.path.join(self.cache_dir, f"{ticker}_{data_type}.json")
    
    def is_cache_valid(self, filepath: str, hours: int = 1) -> bool:
        """Check if cache file exists and is recent enough"""
        if not os.path.exists(filepath):
            return False
        
        file_time = os.path.getmtime(filepath)
        current_time = time.time()
        age_hours = (current_time - file_time) / 3600
        
        return age_hours < hours
    
    def get_cached_data(self, ticker: str, data_type: str, cache_hours: int = 1) -> Optional[Dict[str, Any]]:
        """Get data from cache if valid"""
        cache_path = self.get_cache_path(ticker, data_type)
        
        if self.is_cache_valid(cache_path, cache_hours):
            try:
                with open(cache_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return None
    
    def save_to_cache(self, ticker: str, data_type: str, data: Dict[str, Any]):
        """Save data to cache"""
        cache_path = self.get_cache_path(ticker, data_type)
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving cache for {ticker}: {e}")

# Global cache manager instance
cache_manager = CacheManager()