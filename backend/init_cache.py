"""
Initialize cache with pre-defined data on startup
This runs when the app starts if no cache exists
"""
import os
import json
from datetime import datetime

INITIAL_CACHE_DATA = {
    "AAPL": {
        "ticker": "AAPL",
        "company": "Apple Inc.",
        "quarter": "Q4 2024",
        "date": "2024-07-29",
        "content": """Apple Inc. Financial Overview
Data as of: 2024-07-29

Company Metrics:
Stock Price: $195.89
Market Cap: $3,040,000,000,000
52-Week High: $237.23
52-Week Low: $164.08

Valuation Metrics:
P/E Ratio (TTM): 33.5
Forward P/E: 30.2
PEG Ratio: 3.2
Price to Book: 49.8

Financial Performance:
Revenue (TTM): $385,603,000,000
Revenue Growth (YoY): 0.4%
Gross Margin: 45.2%
Operating Margin: 30.8%
Net Margin: 25.3%

Trading Information:
Beta: 1.29
Dividend Yield: 0.43%
Previous Close: $194.50
Day Range: $193.15 - $196.38
Volume: 52,164,506
Average Volume: 56,789,129""",
        "source": "init-cache"
    },
    "MSFT": {
        "ticker": "MSFT",
        "company": "Microsoft Corporation",
        "quarter": "Q4 2024",
        "date": "2024-07-29",
        "content": """Microsoft Corporation Financial Overview
Data as of: 2024-07-29

Company Metrics:
Stock Price: $440.37
Market Cap: $3,270,000,000,000
52-Week High: $468.35
52-Week Low: $309.42

Valuation Metrics:
P/E Ratio (TTM): 37.8
Forward P/E: 32.5
PEG Ratio: 2.4
Price to Book: 15.9

Financial Performance:
Revenue (TTM): $245,122,000,000
Revenue Growth (YoY): 15.7%
Gross Margin: 69.8%
Operating Margin: 44.6%
Net Margin: 36.4%

Trading Information:
Beta: 0.90
Dividend Yield: 0.66%
Previous Close: $437.11
Day Range: $435.25 - $442.88
Volume: 21,456,789
Average Volume: 23,124,000""",
        "source": "init-cache"
    },
    "NVDA": {
        "ticker": "NVDA",
        "company": "NVIDIA Corporation",
        "quarter": "Q4 2024",
        "date": "2024-07-29",
        "content": """NVIDIA Corporation Financial Overview
Data as of: 2024-07-29

Company Metrics:
Stock Price: $132.65
Market Cap: $3,270,000,000,000
52-Week High: $140.76
52-Week Low: $39.23

Valuation Metrics:
P/E Ratio (TTM): 65.4
Forward P/E: 42.1
PEG Ratio: 0.9
Price to Book: 56.2

Financial Performance:
Revenue (TTM): $60,922,000,000
Revenue Growth (YoY): 262.1%
Gross Margin: 75.0%
Operating Margin: 54.1%
Net Margin: 48.9%

Trading Information:
Beta: 1.68
Dividend Yield: 0.02%
Previous Close: $130.78
Day Range: $129.45 - $134.22
Volume: 298,456,789
Average Volume: 312,789,000""",
        "source": "init-cache"
    }
}

def init_cache():
    """Initialize cache with pre-defined data"""
    cache_dir = "../data/cache"
    
    # Create cache directory
    os.makedirs(cache_dir, exist_ok=True)
    
    # Check if cache already exists
    existing_files = [f for f in os.listdir(cache_dir) if f.endswith('.json')]
    if len(existing_files) > 0:
        print(f"Cache already contains {len(existing_files)} files. Skipping initialization.")
        return
    
    print("Initializing cache with pre-defined data...")
    
    # Create cache files
    initialized = 0
    for ticker, data in INITIAL_CACHE_DATA.items():
        cache_file = os.path.join(cache_dir, f"{ticker}_earnings_summary.json")
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)
        initialized += 1
        print(f"  ✓ Cached {ticker}")
    
    # Create status file
    status = {
        "last_run": datetime.now().isoformat(),
        "success_count": initialized,
        "error_count": 0,
        "stocks_processed": list(INITIAL_CACHE_DATA.keys()),
        "cache_validity_hours": 168,
        "source": "init-cache"
    }
    
    with open(os.path.join(cache_dir, "prefetch_status.json"), 'w') as f:
        json.dump(status, f, indent=2)
    
    print(f"Cache initialization complete. Initialized {initialized} stocks.")

if __name__ == "__main__":
    init_cache()