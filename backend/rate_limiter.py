import time
from typing import Dict
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests: int = 5, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window  # seconds
        self.requests: Dict[str, list] = {}
    
    def can_make_request(self, key: str = "global") -> bool:
        """Check if we can make a request"""
        current_time = time.time()
        
        if key not in self.requests:
            self.requests[key] = []
        
        # Remove old requests outside the time window
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if current_time - req_time < self.time_window
        ]
        
        # Check if we can make a new request
        return len(self.requests[key]) < self.max_requests
    
    def add_request(self, key: str = "global"):
        """Record a new request"""
        if key not in self.requests:
            self.requests[key] = []
        self.requests[key].append(time.time())
    
    def wait_if_needed(self, key: str = "global"):
        """Wait if rate limit is exceeded"""
        while not self.can_make_request(key):
            time.sleep(1)
        self.add_request(key)

# Global rate limiter for yfinance
yfinance_limiter = RateLimiter(max_requests=2, time_window=5)