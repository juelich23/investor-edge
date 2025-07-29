"""
Initialize historical data cache with pre-populated data
"""
import os
import json
from datetime import datetime

INITIAL_HISTORICAL_DATA = {
    "NVDA": {
        "ticker": "NVDA",
        "quarters": [
            {
                "date": "2024-08-28",
                "quarter": "Q2 2024",
                "revenue": 30040000000,
                "earnings": 16599000000,
                "eps_actual": 0.68,
                "eps_estimate": 0.64,
                "surprise_percent": 6.25,
                "price_on_date": 125.61,
                "revenue_growth": 122.4,
                "earnings_growth": 168.1
            },
            {
                "date": "2024-05-22",
                "quarter": "Q1 2024", 
                "revenue": 26044000000,
                "earnings": 14881000000,
                "eps_actual": 0.60,
                "eps_estimate": 0.52,
                "surprise_percent": 15.38,
                "price_on_date": 104.75,
                "revenue_growth": 262.1,
                "earnings_growth": 628.0
            },
            {
                "date": "2024-02-21",
                "quarter": "Q4 2023",
                "revenue": 22103000000,
                "earnings": 12285000000,
                "eps_actual": 0.49,
                "eps_estimate": 0.41,
                "surprise_percent": 19.51,
                "price_on_date": 78.17,
                "revenue_growth": 265.3,
                "earnings_growth": 769.1
            },
            {
                "date": "2023-11-21",
                "quarter": "Q3 2023",
                "revenue": 18120000000,
                "earnings": 9243000000,
                "eps_actual": 0.37,
                "eps_estimate": 0.33,
                "surprise_percent": 12.12,
                "price_on_date": 49.46,
                "revenue_growth": 205.5,
                "earnings_growth": 1259.3
            }
        ],
        "metrics": {
            "revenue_trend": [
                {"date": "2024-08-28", "value": 30040000000},
                {"date": "2024-05-22", "value": 26044000000},
                {"date": "2024-02-21", "value": 22103000000},
                {"date": "2023-11-21", "value": 18120000000}
            ],
            "eps_trend": [
                {"date": "2024-08-28", "value": 0.68},
                {"date": "2024-05-22", "value": 0.60},
                {"date": "2024-02-21", "value": 0.49},
                {"date": "2023-11-21", "value": 0.37}
            ],
            "earnings_dates": ["2024-08-28", "2024-05-22", "2024-02-21", "2023-11-21"]
        },
        "analysis": {
            "avg_revenue_growth": 212.6,
            "avg_earnings_surprise": 13.31,
            "consistency_score": 95,
            "trend_direction": "growing"
        }
    },
    "AAPL": {
        "ticker": "AAPL",
        "quarters": [
            {
                "date": "2024-08-01",
                "quarter": "Q3 2024",
                "revenue": 85777000000,
                "earnings": 21448000000,
                "eps_actual": 1.40,
                "eps_estimate": 1.35,
                "surprise_percent": 3.70,
                "price_on_date": 218.36,
                "revenue_growth": 4.9,
                "earnings_growth": 7.9
            },
            {
                "date": "2024-05-02",
                "quarter": "Q2 2024",
                "revenue": 90753000000,
                "earnings": 23636000000,
                "eps_actual": 1.53,
                "eps_estimate": 1.50,
                "surprise_percent": 2.00,
                "price_on_date": 173.03,
                "revenue_growth": -4.3,
                "earnings_growth": -2.2
            },
            {
                "date": "2024-02-01",
                "quarter": "Q1 2024",
                "revenue": 119575000000,
                "earnings": 33916000000,
                "eps_actual": 2.18,
                "eps_estimate": 2.10,
                "surprise_percent": 3.81,
                "price_on_date": 186.86,
                "revenue_growth": 2.1,
                "earnings_growth": 13.1
            },
            {
                "date": "2023-11-02",
                "quarter": "Q4 2023",
                "revenue": 89498000000,
                "earnings": 22956000000,
                "eps_actual": 1.46,
                "eps_estimate": 1.39,
                "surprise_percent": 5.04,
                "price_on_date": 176.65,
                "revenue_growth": -0.7,
                "earnings_growth": 10.8
            }
        ],
        "metrics": {
            "revenue_trend": [
                {"date": "2024-08-01", "value": 85777000000},
                {"date": "2024-05-02", "value": 90753000000},
                {"date": "2024-02-01", "value": 119575000000},
                {"date": "2023-11-02", "value": 89498000000}
            ],
            "eps_trend": [
                {"date": "2024-08-01", "value": 1.40},
                {"date": "2024-05-02", "value": 1.53},
                {"date": "2024-02-01", "value": 2.18},
                {"date": "2023-11-02", "value": 1.46}
            ],
            "earnings_dates": ["2024-08-01", "2024-05-02", "2024-02-01", "2023-11-02"]
        },
        "analysis": {
            "avg_revenue_growth": 0.4,
            "avg_earnings_surprise": 3.64,
            "consistency_score": 85,
            "trend_direction": "stable"
        }
    }
}

def init_historical_cache():
    """Initialize historical data cache"""
    cache_dir = "../data/cache"
    historical_dir = "../data/historical"
    
    os.makedirs(cache_dir, exist_ok=True)
    os.makedirs(historical_dir, exist_ok=True)
    
    initialized = 0
    for ticker, data in INITIAL_HISTORICAL_DATA.items():
        # Save to cache directory
        cache_file = os.path.join(cache_dir, f"{ticker}_historical.json")
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Also save to historical directory
        historical_file = os.path.join(historical_dir, f"{ticker}_history.json")
        with open(historical_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        initialized += 1
        print(f"  ✓ Cached historical data for {ticker}")
    
    print(f"Historical cache initialization complete. Initialized {initialized} stocks.")

if __name__ == "__main__":
    init_historical_cache()