import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Optional
import json
from rate_limiter import yfinance_limiter
from cache_manager import cache_manager

class ImprovedHistoricalScraper:
    def __init__(self):
        self.quarters_to_fetch = 8  # Get 2 years of quarterly data
        
    def get_historical_earnings(self, ticker: str) -> Dict:
        """Fetch historical earnings data combining multiple sources"""
        # Check cache first
        cached_data = cache_manager.get_cached_data(ticker, "historical", cache_hours=24)
        if cached_data:
            print(f"Using cached historical data for {ticker}")
            return cached_data
        
        # Apply rate limiting
        yfinance_limiter.wait_if_needed()
        
        try:
            stock = yf.Ticker(ticker)
            
            # Get earnings dates first (has EPS estimates and surprises)
            earnings_dates = stock.earnings_dates
            if earnings_dates is None or earnings_dates.empty:
                print(f"No earnings dates found for {ticker}")
                return self._get_fallback_data(ticker)
            
            # Filter for past earnings only
            try:
                # Handle timezone comparison safely
                today = pd.Timestamp.now(tz='America/New_York')
                past_earnings = earnings_dates[earnings_dates.index < today]
            except:
                # Fallback: just take all but the first few entries which are usually future
                past_earnings = earnings_dates.iloc[1:] if len(earnings_dates) > 1 else earnings_dates
            
            if past_earnings.empty:
                print(f"No past earnings found for {ticker}")
                return self._get_fallback_data(ticker)
            
            # Get income statement for revenue data
            income_stmt = stock.quarterly_income_stmt
            
            # Get historical prices
            info = stock.info
            
            historical_data = {
                "ticker": ticker,
                "quarters": [],
                "metrics": {
                    "revenue_trend": [],
                    "eps_trend": [],
                    "earnings_dates": []
                }
            }
            
            # Process earnings dates
            for i, (date, row) in enumerate(past_earnings.iterrows()):
                if i >= self.quarters_to_fetch:
                    break
                
                # Skip if not an earnings event
                if pd.notna(row.get('Event Type')) and row['Event Type'] != 'Earnings':
                    continue
                    
                quarter_data = {
                    "date": str(date.date()),
                    "quarter": self._format_quarter(date),
                    "revenue": None,
                    "earnings": None,
                    "eps_actual": float(row['Reported EPS']) if pd.notna(row.get('Reported EPS')) else None,
                    "eps_estimate": float(row['EPS Estimate']) if pd.notna(row.get('EPS Estimate')) else None,
                    "surprise_percent": float(row['Surprise(%)']) if pd.notna(row.get('Surprise(%)')) else None,
                    "price_on_date": None
                }
                
                # Try to get revenue from income statement
                if income_stmt is not None and not income_stmt.empty:
                    # Find the closest quarter in income statement
                    for col in income_stmt.columns:
                        try:
                            # Handle timezone comparison
                            col_date = col.tz_localize(None) if hasattr(col, 'tz') and col.tz else col
                            date_compare = date.tz_localize(None) if hasattr(date, 'tz') and date.tz else date
                            if abs((col_date - date_compare).days) <= 45:  # Within 45 days
                                if 'Total Revenue' in income_stmt.index:
                                    revenue = income_stmt.loc['Total Revenue', col]
                                    if pd.notna(revenue):
                                        quarter_data["revenue"] = float(revenue) / 1_000_000
                                if 'Net Income' in income_stmt.index:
                                    earnings = income_stmt.loc['Net Income', col]
                                    if pd.notna(earnings):
                                        quarter_data["earnings"] = float(earnings) / 1_000_000
                                break
                        except:
                            continue
                
                # Get stock price on earnings date
                try:
                    # Get price around earnings date
                    start_date = date - pd.Timedelta(days=5)
                    end_date = date + pd.Timedelta(days=5)
                    hist = stock.history(start=start_date, end=end_date)
                    
                    if not hist.empty:
                        # Try exact date first
                        if date.date() in hist.index.date:
                            quarter_data["price_on_date"] = float(hist[hist.index.date == date.date()].iloc[0]['Close'])
                        else:
                            # Get closest trading day
                            closest_idx = hist.index.get_indexer([date], method='nearest')[0]
                            if closest_idx >= 0:
                                quarter_data["price_on_date"] = float(hist.iloc[closest_idx]['Close'])
                except Exception as e:
                    print(f"Error getting price for {date}: {e}")
                
                historical_data["quarters"].append(quarter_data)
                
                # Add to trend data
                if quarter_data["revenue"]:
                    historical_data["metrics"]["revenue_trend"].append({
                        "date": quarter_data["date"],
                        "value": quarter_data["revenue"]
                    })
                
                if quarter_data["eps_actual"]:
                    historical_data["metrics"]["eps_trend"].append({
                        "date": quarter_data["date"],
                        "value": quarter_data["eps_actual"]
                    })
                
                historical_data["metrics"]["earnings_dates"].append(quarter_data["date"])
            
            # Calculate trends
            historical_data["analysis"] = self._calculate_trends(historical_data)
            
            # Save to cache before returning
            cache_manager.save_to_cache(ticker, "historical", historical_data)
            
            return historical_data
            
        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {e}")
            return self._get_fallback_data(ticker)
    
    def _format_quarter(self, date) -> str:
        """Format date into quarter string (e.g., Q1 2024)"""
        if isinstance(date, str):
            date = pd.to_datetime(date)
        quarter = (date.month - 1) // 3 + 1
        return f"Q{quarter} {date.year}"
    
    def _calculate_trends(self, data: Dict) -> Dict:
        """Calculate trend analysis metrics"""
        analysis = {
            "revenue_growth": None,
            "eps_growth": None,
            "avg_surprise": None,
            "volatility": None,
            "trend_direction": "neutral"
        }
        
        # Calculate YoY revenue growth
        if len(data["quarters"]) >= 4:
            current_revenue = data["quarters"][0].get("revenue")
            year_ago_revenue = None
            
            # Find revenue from ~4 quarters ago
            for i in range(3, min(6, len(data["quarters"]))):
                if data["quarters"][i].get("revenue"):
                    year_ago_revenue = data["quarters"][i]["revenue"]
                    break
                    
            if current_revenue and year_ago_revenue and year_ago_revenue != 0:
                analysis["revenue_growth"] = ((current_revenue - year_ago_revenue) / year_ago_revenue) * 100
        
        # Calculate YoY EPS growth
        if len(data["quarters"]) >= 4:
            current_eps = data["quarters"][0].get("eps_actual")
            year_ago_eps = None
            
            # Find EPS from ~4 quarters ago
            for i in range(3, min(6, len(data["quarters"]))):
                if data["quarters"][i].get("eps_actual"):
                    year_ago_eps = data["quarters"][i]["eps_actual"]
                    break
                    
            if current_eps and year_ago_eps and year_ago_eps != 0:
                analysis["eps_growth"] = ((current_eps - year_ago_eps) / abs(year_ago_eps)) * 100
        
        # Calculate average earnings surprise
        surprises = [q["surprise_percent"] for q in data["quarters"] if q.get("surprise_percent") is not None]
        if surprises:
            analysis["avg_surprise"] = sum(surprises) / len(surprises)
        
        # Determine trend direction based on recent quarters
        revenue_values = [q["revenue"] for q in data["quarters"][:4] if q.get("revenue")]
        if len(revenue_values) >= 3:
            # Check if generally increasing or decreasing
            recent_avg = sum(revenue_values[:2]) / 2
            older_avg = sum(revenue_values[2:]) / len(revenue_values[2:])
            
            if recent_avg > older_avg * 1.05:  # 5% growth threshold
                analysis["trend_direction"] = "growing"
            elif recent_avg < older_avg * 0.95:  # 5% decline threshold
                analysis["trend_direction"] = "declining"
            else:
                analysis["trend_direction"] = "stable"
        
        return analysis
    
    def _get_fallback_data(self, ticker: str) -> Dict:
        """Generate sample historical data when real data is unavailable"""
        from fallback_data import fallback_provider
        return fallback_provider.get_historical_data(ticker)
    
    def save_historical_data(self, ticker: str, data: Dict):
        """Save historical data to JSON file"""
        filename = f"../data/historical/{ticker}_history.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved historical data for {ticker}")

if __name__ == "__main__":
    scraper = ImprovedHistoricalScraper()
    
    # Test with NVDA
    print("Testing improved scraper with NVDA...")
    data = scraper.get_historical_earnings("NVDA")
    
    print(f"\nFound {len(data['quarters'])} quarters of data")
    if data['quarters']:
        print("\nMost recent quarter:")
        print(json.dumps(data['quarters'][0], indent=2))
        
        print("\nAnalysis:")
        print(json.dumps(data['analysis'], indent=2))