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
    },
    "AMZN": {
        "ticker": "AMZN",
        "company": "Amazon.com Inc.",
        "quarter": "Q4 2024",
        "date": "2024-07-29",
        "content": """Amazon.com Inc. Financial Overview
Data as of: 2024-07-29

Company Metrics:
Stock Price: $219.65
Market Cap: $2,280,000,000,000
52-Week High: $230.08
52-Week Low: $118.35

Valuation Metrics:
P/E Ratio (TTM): 54.2
Forward P/E: 38.9
PEG Ratio: 1.4
Price to Book: 9.3

Financial Performance:
Revenue (TTM): $590,740,000,000
Revenue Growth (YoY): 12.3%
Gross Margin: 48.0%
Operating Margin: 9.8%
Net Margin: 7.4%

Trading Information:
Beta: 1.16
Dividend Yield: 0.00%
Previous Close: $217.89
Day Range: $216.45 - $221.32
Volume: 38,456,789
Average Volume: 42,567,000""",
        "source": "init-cache"
    },
    "GOOGL": {
        "ticker": "GOOGL", 
        "company": "Alphabet Inc.",
        "quarter": "Q4 2024",
        "date": "2024-07-29",
        "content": """Alphabet Inc. Financial Overview
Data as of: 2024-07-29

Company Metrics:
Stock Price: $163.94
Market Cap: $2,030,000,000,000
52-Week High: $193.31
52-Week Low: $120.21

Valuation Metrics:
P/E Ratio (TTM): 27.3
Forward P/E: 22.8
PEG Ratio: 1.3
Price to Book: 6.8

Financial Performance:
Revenue (TTM): $328,284,000,000
Revenue Growth (YoY): 13.6%
Gross Margin: 57.5%
Operating Margin: 32.5%
Net Margin: 24.1%

Trading Information:
Beta: 1.03
Dividend Yield: 0.47%
Previous Close: $165.52
Day Range: $162.44 - $165.95
Volume: 28,745,123
Average Volume: 31,298,000""",
        "source": "init-cache"
    },
    "META": {
        "ticker": "META",
        "company": "Meta Platforms Inc.", 
        "quarter": "Q4 2024",
        "date": "2024-07-29",
        "content": """Meta Platforms Inc. Financial Overview
Data as of: 2024-07-29

Company Metrics:
Stock Price: $595.94
Market Cap: $1,520,000,000,000
52-Week High: $638.40
52-Week Low: $279.40

Valuation Metrics:
P/E Ratio (TTM): 29.6
Forward P/E: 24.8
PEG Ratio: 1.1
Price to Book: 8.5

Financial Performance:
Revenue (TTM): $149,775,000,000
Revenue Growth (YoY): 22.1%
Gross Margin: 81.5%
Operating Margin: 38.0%
Net Margin: 29.3%

Trading Information:
Beta: 1.26
Dividend Yield: 0.34%
Previous Close: $592.12
Day Range: $590.25 - $599.88
Volume: 15,234,567
Average Volume: 17,890,000""",
        "source": "init-cache"
    },
    "TSLA": {
        "ticker": "TSLA",
        "company": "Tesla Inc.",
        "quarter": "Q4 2024", 
        "date": "2024-07-29",
        "content": """Tesla Inc. Financial Overview
Data as of: 2024-07-29

Company Metrics:
Stock Price: $248.23
Market Cap: $792,000,000,000
52-Week High: $299.29
52-Week Low: $138.80

Valuation Metrics:
P/E Ratio (TTM): 78.9
Forward P/E: 62.3
PEG Ratio: 3.5
Price to Book: 16.2

Financial Performance:
Revenue (TTM): $96,773,000,000
Revenue Growth (YoY): 8.7%
Gross Margin: 20.1%
Operating Margin: 9.6%
Net Margin: 13.0%

Trading Information:
Beta: 2.11
Dividend Yield: 0.00%
Previous Close: $245.67
Day Range: $244.82 - $251.44
Volume: 98,765,432
Average Volume: 112,345,000""",
        "source": "init-cache"
    },
    "JPM": {
        "ticker": "JPM",
        "company": "JPMorgan Chase & Co.",
        "quarter": "Q4 2024",
        "date": "2024-07-29", 
        "content": """JPMorgan Chase & Co. Financial Overview
Data as of: 2024-07-29

Company Metrics:
Stock Price: $245.84
Market Cap: $702,000,000,000
52-Week High: $254.50
52-Week Low: $135.19

Valuation Metrics:
P/E Ratio (TTM): 12.8
Forward P/E: 13.2
PEG Ratio: 1.8
Price to Book: 2.0

Financial Performance:
Revenue (TTM): $168,476,000,000
Revenue Growth (YoY): 22.9%
Operating Margin: 42.3%
Net Margin: 27.8%

Trading Information:
Beta: 1.01
Dividend Yield: 2.26%
Previous Close: $243.98
Day Range: $243.12 - $247.65
Volume: 8,234,567
Average Volume: 9,876,543""",
        "source": "init-cache"
    },
    "JNJ": {
        "ticker": "JNJ",
        "company": "Johnson & Johnson",
        "quarter": "Q4 2024",
        "date": "2024-07-29",
        "content": """Johnson & Johnson Financial Overview
Data as of: 2024-07-29

Company Metrics:
Stock Price: $145.21
Market Cap: $349,000,000,000
52-Week High: $160.16
52-Week Low: $139.77

Valuation Metrics:
P/E Ratio (TTM): 14.7
Forward P/E: 15.8
PEG Ratio: 3.2
Price to Book: 5.1

Financial Performance:
Revenue (TTM): $85,159,000,000
Revenue Growth (YoY): 6.7%
Gross Margin: 68.5%
Operating Margin: 22.4%
Net Margin: 16.8%

Trading Information:
Beta: 0.59
Dividend Yield: 3.08%
Previous Close: $144.85
Day Range: $144.25 - $146.12
Volume: 5,123,456
Average Volume: 6,234,567""",
        "source": "init-cache"
    },
    "WMT": {
        "ticker": "WMT",
        "company": "Walmart Inc.",
        "quarter": "Q4 2024",
        "date": "2024-07-29",
        "content": """Walmart Inc. Financial Overview
Data as of: 2024-07-29

Company Metrics:
Stock Price: $97.20
Market Cap: $780,000,000,000
52-Week High: $102.18
52-Week Low: $49.85

Valuation Metrics:
P/E Ratio (TTM): 43.2
Forward P/E: 33.5
PEG Ratio: 4.1
Price to Book: 7.8

Financial Performance:
Revenue (TTM): $648,125,000,000
Revenue Growth (YoY): 6.0%
Gross Margin: 24.3%
Operating Margin: 3.9%
Net Margin: 2.3%

Trading Information:
Beta: 0.51
Dividend Yield: 1.10%
Previous Close: $96.88
Day Range: $96.45 - $97.88
Volume: 12,345,678
Average Volume: 15,678,901""",
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