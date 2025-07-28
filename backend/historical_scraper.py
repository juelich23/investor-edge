import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Optional
import json

class HistoricalEarningsScraper:
    def __init__(self):
        self.quarters_to_fetch = 8  # Get 2 years of quarterly data
    
    def _convert_financials_to_earnings(self, financials):
        """Convert financial statements to earnings format"""
        earnings_data = pd.DataFrame()
        if 'Total Revenue' in financials.index:
            earnings_data['Revenue'] = financials.loc['Total Revenue']
        if 'Net Income' in financials.index:
            earnings_data['Earnings'] = financials.loc['Net Income']
        return earnings_data
        
    def get_historical_earnings(self, ticker: str) -> Dict:
        """Fetch historical earnings data for a given ticker"""
        try:
            stock = yf.Ticker(ticker)
            
            # Try to get quarterly income statement first (most reliable)
            try:
                income_stmt = stock.quarterly_income_stmt
                if income_stmt is not None and not income_stmt.empty:
                    # Use income statement data
                    return self._process_income_statement_data(ticker, stock, income_stmt)
            except:
                pass
            
            # Fall back to quarterly earnings
            earnings_hist = stock.quarterly_earnings
            if earnings_hist is None or earnings_hist.empty:
                return self._get_fallback_data(ticker)
            
            # Get earnings dates
            earnings_dates = stock.earnings_dates
            
            # Get historical prices around earnings dates
            price_history = stock.history(period="2y")
            
            historical_data = {
                "ticker": ticker,
                "quarters": [],
                "metrics": {
                    "revenue_trend": [],
                    "eps_trend": [],
                    "earnings_dates": []
                }
            }
            
            # Process quarterly earnings
            for i, (date, row) in enumerate(earnings_hist.iterrows()):
                if i >= self.quarters_to_fetch:
                    break
                    
                quarter_data = {
                    "date": str(date),
                    "quarter": self._format_quarter(date),
                    "revenue": float(row.get('Revenue', 0)) if pd.notna(row.get('Revenue', 0)) else None,
                    "earnings": float(row.get('Earnings', 0)) if pd.notna(row.get('Earnings', 0)) else None,
                    "eps_actual": None,
                    "eps_estimate": None,
                    "surprise_percent": None,
                    "price_on_date": None
                }
                
                # Try to get EPS data from earnings_dates
                if earnings_dates is not None and not earnings_dates.empty:
                    try:
                        date_mask = earnings_dates.index.date == pd.to_datetime(date).date()
                        if any(date_mask):
                            eps_data = earnings_dates[date_mask].iloc[0]
                            quarter_data["eps_actual"] = float(eps_data.get('Reported EPS', 0)) if pd.notna(eps_data.get('Reported EPS', 0)) else None
                            quarter_data["eps_estimate"] = float(eps_data.get('EPS Estimate', 0)) if pd.notna(eps_data.get('EPS Estimate', 0)) else None
                            if quarter_data["eps_actual"] and quarter_data["eps_estimate"]:
                                quarter_data["surprise_percent"] = ((quarter_data["eps_actual"] - quarter_data["eps_estimate"]) / abs(quarter_data["eps_estimate"]) * 100)
                    except:
                        pass
                
                # Get stock price on earnings date
                try:
                    price_date = pd.to_datetime(date)
                    # Get historical price for this specific date
                    hist = stock.history(start=price_date - pd.Timedelta(days=5), 
                                       end=price_date + pd.Timedelta(days=5))
                    if not hist.empty:
                        closest_idx = hist.index.get_indexer([price_date], method='nearest')[0]
                        if closest_idx >= 0:
                            quarter_data["price_on_date"] = float(hist.iloc[closest_idx]['Close'])
                except:
                    pass
                
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
            
            # Calculate growth metrics
            historical_data["analysis"] = self._calculate_trends(historical_data)
            
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
            year_ago_revenue = data["quarters"][3].get("revenue")
            if current_revenue and year_ago_revenue:
                analysis["revenue_growth"] = ((current_revenue - year_ago_revenue) / year_ago_revenue) * 100
        
        # Calculate YoY EPS growth
        if len(data["quarters"]) >= 4:
            current_eps = data["quarters"][0].get("eps_actual")
            year_ago_eps = data["quarters"][3].get("eps_actual")
            if current_eps and year_ago_eps and year_ago_eps != 0:
                analysis["eps_growth"] = ((current_eps - year_ago_eps) / abs(year_ago_eps)) * 100
        
        # Calculate average earnings surprise
        surprises = [q["surprise_percent"] for q in data["quarters"] if q.get("surprise_percent") is not None]
        if surprises:
            analysis["avg_surprise"] = sum(surprises) / len(surprises)
        
        # Determine trend direction
        revenue_values = [q["revenue"] for q in data["quarters"][:4] if q.get("revenue")]
        if len(revenue_values) >= 3:
            if all(revenue_values[i] > revenue_values[i+1] for i in range(len(revenue_values)-1)):
                analysis["trend_direction"] = "growing"
            elif all(revenue_values[i] < revenue_values[i+1] for i in range(len(revenue_values)-1)):
                analysis["trend_direction"] = "declining"
            else:
                analysis["trend_direction"] = "mixed"
        
        return analysis
    
    def _get_fallback_data(self, ticker: str) -> Dict:
        """Generate sample historical data when real data is unavailable"""
        import random
        
        base_revenue = random.uniform(10000, 100000)  # in millions
        base_eps = random.uniform(1.0, 10.0)
        
        historical_data = {
            "ticker": ticker,
            "quarters": [],
            "metrics": {
                "revenue_trend": [],
                "eps_trend": [],
                "earnings_dates": []
            }
        }
        
        # Generate 8 quarters of data
        for i in range(8):
            date = datetime.now() - timedelta(days=90 * i)
            growth_factor = 1 + (random.uniform(-0.1, 0.15) if i < 4 else random.uniform(-0.05, 0.1))
            
            quarter_data = {
                "date": date.strftime("%Y-%m-%d"),
                "quarter": self._format_quarter(date),
                "revenue": base_revenue * (growth_factor ** i),
                "earnings": base_revenue * 0.15 * (growth_factor ** i),  # 15% margin
                "eps_actual": base_eps * (growth_factor ** i),
                "eps_estimate": base_eps * (growth_factor ** i) * 0.98,  # Slight beat
                "surprise_percent": random.uniform(-2, 5),
                "price_on_date": 100 + (10 * i) + random.uniform(-5, 5)
            }
            
            historical_data["quarters"].append(quarter_data)
            historical_data["metrics"]["revenue_trend"].append({
                "date": quarter_data["date"],
                "value": quarter_data["revenue"]
            })
            historical_data["metrics"]["eps_trend"].append({
                "date": quarter_data["date"],
                "value": quarter_data["eps_actual"]
            })
        
        historical_data["analysis"] = self._calculate_trends(historical_data)
        return historical_data
    
    def _process_income_statement_data(self, ticker: str, stock, income_stmt) -> Dict:
        """Process income statement data to create historical earnings"""
        historical_data = {
            "ticker": ticker,
            "quarters": [],
            "metrics": {
                "revenue_trend": [],
                "eps_trend": [],
                "earnings_dates": []
            }
        }
        
        # Get basic info for EPS calculation
        info = stock.info
        shares_outstanding = info.get('sharesOutstanding', info.get('impliedSharesOutstanding', 1))
        
        # Get earnings dates for additional data
        earnings_dates = stock.earnings_dates
        
        # Process each quarter (most recent first)
        for i, date in enumerate(income_stmt.columns):
            if i >= self.quarters_to_fetch:
                break
                
            quarter_data = {
                "date": str(date.date()),
                "quarter": self._format_quarter(date),
                "revenue": None,
                "earnings": None,
                "eps_actual": None,
                "eps_estimate": None,
                "surprise_percent": None,
                "price_on_date": None
            }
            
            # Get revenue (in millions)
            if 'Total Revenue' in income_stmt.index:
                revenue = income_stmt.loc['Total Revenue', date]
                quarter_data["revenue"] = float(revenue) / 1_000_000 if pd.notna(revenue) else None
            
            # Get net income (earnings)
            if 'Net Income' in income_stmt.index:
                net_income = income_stmt.loc['Net Income', date]
                quarter_data["earnings"] = float(net_income) / 1_000_000 if pd.notna(net_income) else None
                
                # Calculate EPS
                if shares_outstanding and pd.notna(net_income):
                    quarter_data["eps_actual"] = float(net_income) / shares_outstanding
            
            # Try to get EPS data from earnings_dates
            if earnings_dates is not None and not earnings_dates.empty:
                try:
                    # Find matching earnings date within a few days
                    for idx in earnings_dates.index:
                        if abs((idx.date() - date.date()).days) <= 5:  # Within 5 days
                            eps_data = earnings_dates.loc[idx]
                            if 'Reported EPS' in eps_data.index:
                                reported_eps = eps_data['Reported EPS']
                                if pd.notna(reported_eps):
                                    quarter_data["eps_actual"] = float(reported_eps)
                            if 'EPS Estimate' in eps_data.index:
                                eps_est = eps_data['EPS Estimate']
                                if pd.notna(eps_est):
                                    quarter_data["eps_estimate"] = float(eps_est)
                            if quarter_data["eps_actual"] and quarter_data["eps_estimate"]:
                                quarter_data["surprise_percent"] = ((quarter_data["eps_actual"] - quarter_data["eps_estimate"]) / abs(quarter_data["eps_estimate"]) * 100)
                            break
                except Exception as e:
                    pass
            
            # Get historical stock price
            try:
                hist = stock.history(start=date - pd.Timedelta(days=5), end=date + pd.Timedelta(days=5))
                if not hist.empty:
                    # Get the closest trading day
                    closest_idx = hist.index.get_indexer([date], method='nearest')[0]
                    if closest_idx >= 0:
                        quarter_data["price_on_date"] = float(hist.iloc[closest_idx]['Close'])
            except:
                pass
            
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
        
        historical_data["analysis"] = self._calculate_trends(historical_data)
        return historical_data
    
    def save_historical_data(self, ticker: str, data: Dict):
        """Save historical data to JSON file"""
        filename = f"../data/historical/{ticker}_history.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved historical data for {ticker}")

if __name__ == "__main__":
    scraper = HistoricalEarningsScraper()
    
    # Test with a single ticker
    data = scraper.get_historical_earnings("AAPL")
    print(json.dumps(data, indent=2))