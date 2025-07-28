import yfinance as yf
import requests
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional

class YFinanceEarningsScraper:
    def __init__(self):
        self.companies = {
            "AAPL": "Apple Inc.",
            "MSFT": "Microsoft Corporation",
            "GOOGL": "Alphabet Inc.",
            "AMZN": "Amazon.com Inc.",
            "META": "Meta Platforms Inc.",
            "TSLA": "Tesla Inc.",
            "NVDA": "NVIDIA Corporation",
            "JPM": "JPMorgan Chase & Co.",
            "JNJ": "Johnson & Johnson",
            "WMT": "Walmart Inc."
        }
    
    def get_earnings_data(self, ticker: str) -> Dict:
        """Get comprehensive earnings data using yfinance"""
        print(f"Fetching real earnings data for {ticker}...")
        
        try:
            stock = yf.Ticker(ticker)
            
            # Get basic info
            info = stock.info
            
            # Get earnings data from income statement
            quarterly_income = stock.quarterly_income_stmt
            annual_income = stock.income_stmt
            
            # Get recent financials
            financials = stock.quarterly_financials
            
            # Get recent news
            news = stock.news[:5]  # Get latest 5 news items
            
            # Build transcript content from real data
            content_parts = [
                f"{self.companies[ticker]} Earnings Overview",
                f"Last Updated: {datetime.now().strftime('%Y-%m-%d')}",
                "",
                "Company Information:",
                f"- Market Cap: ${info.get('marketCap', 'N/A'):,.0f}" if info.get('marketCap') else "- Market Cap: N/A",
                f"- Current Price: ${info.get('currentPrice', 'N/A')}",
                f"- 52 Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}",
                f"- 52 Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}",
                f"- PE Ratio: {info.get('trailingPE', 'N/A')}",
                "",
                "Recent Earnings Performance:"
            ]
            
            # Add quarterly earnings data from income statement
            if quarterly_income is not None and not quarterly_income.empty:
                latest_quarter = quarterly_income.iloc[:, 0]  # Most recent quarter
                revenue = latest_quarter.get('Total Revenue', 0)
                net_income = latest_quarter.get('Net Income', 0)
                content_parts.extend([
                    f"- Total Revenue: ${revenue:,.0f}" if revenue else "- Total Revenue: N/A",
                    f"- Net Income: ${net_income:,.0f}" if net_income else "- Net Income: N/A",
                ])
            
            # Add recent performance metrics
            if info.get('trailingEps'):
                content_parts.extend([
                    "",
                    "Earnings Per Share:",
                    f"- Trailing EPS: ${info.get('trailingEps', 'N/A')}",
                    f"- Forward EPS: ${info.get('forwardEps', 'N/A')}"
                ])
            
            # Add key financial metrics
            if not financials.empty:
                latest_financials = financials.iloc[:, 0]  # Most recent quarter
                content_parts.extend([
                    "",
                    "Key Financial Metrics:",
                    f"- Total Revenue: ${latest_financials.get('Total Revenue', 0):,.0f}" if 'Total Revenue' in latest_financials else "",
                    f"- Gross Profit: ${latest_financials.get('Gross Profit', 0):,.0f}" if 'Gross Profit' in latest_financials else "",
                    f"- Operating Income: ${latest_financials.get('Operating Income', 0):,.0f}" if 'Operating Income' in latest_financials else "",
                    f"- Net Income: ${latest_financials.get('Net Income', 0):,.0f}" if 'Net Income' in latest_financials else "",
                ])
            
            # Add analyst recommendations
            recommendations = stock.recommendations
            if recommendations is not None and not recommendations.empty:
                recent_recs = recommendations.tail(5)
                content_parts.extend([
                    "",
                    "Recent Analyst Actions:",
                ])
                for _, rec in recent_recs.iterrows():
                    content_parts.append(f"- {rec['Firm']}: {rec['To Grade']} ({rec['Action']})")
            
            # Add recent news
            if news:
                content_parts.extend([
                    "",
                    "Recent News:",
                ])
                for article in news:
                    content_parts.append(f"- {article.get('title', 'N/A')}")
            
            # Determine quarter
            current_date = datetime.now()
            if current_date.month <= 3:
                quarter = f"Q4 {current_date.year - 1}"
            elif current_date.month <= 6:
                quarter = f"Q1 {current_date.year}"
            elif current_date.month <= 9:
                quarter = f"Q2 {current_date.year}"
            else:
                quarter = f"Q3 {current_date.year}"
            
            return {
                "ticker": ticker,
                "company": self.companies[ticker],
                "quarter": quarter,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "content": "\n".join(filter(None, content_parts)),
                "source": "yfinance",
                "metrics": {
                    "marketCap": info.get('marketCap'),
                    "currentPrice": info.get('currentPrice'),
                    "peRatio": info.get('trailingPE'),
                    "revenue": latest_quarter.get('Total Revenue', 0) if quarterly_income is not None and not quarterly_income.empty else None
                }
            }
            
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return self.get_fallback_data(ticker)
    
    def get_fallback_data(self, ticker: str) -> Dict:
        """Fallback data when yfinance fails"""
        return {
            "ticker": ticker,
            "company": self.companies[ticker],
            "quarter": f"Q4 {datetime.now().year}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "content": f"Unable to fetch real-time data for {ticker}. Please check your internet connection or try again later.",
            "source": "fallback"
        }
    
    def save_transcript(self, ticker: str, data: Dict):
        """Save transcript data to JSON file"""
        os.makedirs("../data/transcripts", exist_ok=True)
        filepath = f"../data/transcripts/{ticker}_latest.json"
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Saved {ticker} earnings data (source: {data['source']})")
    
    def scrape_all_companies(self):
        """Scrape earnings data for all companies"""
        for ticker in self.companies.keys():
            print(f"\nProcessing {ticker}...")
            data = self.get_earnings_data(ticker)
            self.save_transcript(ticker, data)

if __name__ == "__main__":
    scraper = YFinanceEarningsScraper()
    scraper.scrape_all_companies()