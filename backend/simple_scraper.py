import yfinance as yf
import json
import os
from datetime import datetime
from typing import Dict
import time

class SimpleEarningsScraper:
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
    
    def get_earnings_summary(self, ticker: str) -> Dict:
        """Get simplified earnings data using yfinance"""
        print(f"Fetching data for {ticker}...")
        
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get company name from info or use ticker
            company_name = info.get('longName', info.get('shortName', ticker))
            
            # Build earnings summary
            content_parts = [
                f"{company_name} Financial Overview",
                f"Data as of: {datetime.now().strftime('%Y-%m-%d')}",
                "",
                "Company Metrics:",
                f"Stock Price: ${info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))}",
                f"Market Cap: ${info.get('marketCap', 0):,.0f}" if info.get('marketCap') else "Market Cap: N/A",
                f"52-Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}",
                f"52-Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}",
                "",
                "Valuation Metrics:",
                f"P/E Ratio (TTM): {info.get('trailingPE', 'N/A')}",
                f"Forward P/E: {info.get('forwardPE', 'N/A')}",
                f"PEG Ratio: {info.get('pegRatio', 'N/A')}",
                f"Price to Book: {info.get('priceToBook', 'N/A')}",
                "",
                "Financial Performance:",
                f"Revenue (TTM): ${info.get('totalRevenue', 0):,.0f}" if info.get('totalRevenue') else "Revenue: N/A",
                f"Revenue Growth (YoY): {info.get('revenueGrowth', 0)*100:.1f}%" if info.get('revenueGrowth') else "Revenue Growth: N/A",
                f"Gross Margins: {info.get('grossMargins', 0)*100:.1f}%" if info.get('grossMargins') else "Gross Margins: N/A",
                f"Operating Margins: {info.get('operatingMargins', 0)*100:.1f}%" if info.get('operatingMargins') else "Operating Margins: N/A",
                f"Profit Margins: {info.get('profitMargins', 0)*100:.1f}%" if info.get('profitMargins') else "Profit Margins: N/A",
                "",
                "Per Share Data:",
                f"EPS (TTM): ${info.get('trailingEps', 'N/A')}",
                f"Book Value: ${info.get('bookValue', 'N/A')}",
                f"Revenue Per Share: ${info.get('revenuePerShare', 'N/A')}",
                "",
                "Analyst Recommendations:",
                f"Recommendation: {info.get('recommendationKey', 'N/A').upper()}",
                f"Target Mean Price: ${info.get('targetMeanPrice', 'N/A')}",
                f"Number of Analysts: {info.get('numberOfAnalystOpinions', 'N/A')}",
                "",
                "Recent Performance:",
                f"Previous Close: ${info.get('previousClose', 'N/A')}",
                f"Day Range: ${info.get('dayLow', 'N/A')} - ${info.get('dayHigh', 'N/A')}",
                f"Volume: {info.get('volume', 0):,}" if info.get('volume') else "Volume: N/A",
                f"Average Volume: {info.get('averageVolume', 0):,}" if info.get('averageVolume') else "Avg Volume: N/A",
            ]
            
            # Get most recent earnings date if available
            if info.get('mostRecentQuarter'):
                recent_date = datetime.fromtimestamp(info['mostRecentQuarter'])
                content_parts.insert(3, f"Most Recent Earnings: {recent_date.strftime('%Y-%m-%d')}")
            
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
                "company": company_name,
                "quarter": quarter,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "content": "\n".join(content_parts),
                "source": "yfinance-simple"
            }
            
        except Exception as e:
            print(f"Error: {e}")
            return self.get_enhanced_mock_data(ticker)
    
    def get_enhanced_mock_data(self, ticker: str) -> Dict:
        """Enhanced mock data when API fails"""
        mock_data = {
            "AAPL": {
                "price": 195.89,
                "marketCap": 3050000000000,
                "pe": 32.5,
                "revenue": 383285000000,
                "revenueGrowth": 0.08,
                "margins": 0.267
            },
            "MSFT": {
                "price": 420.55,
                "marketCap": 3120000000000,
                "pe": 36.8,
                "revenue": 211915000000,
                "revenueGrowth": 0.12,
                "margins": 0.366
            },
            "GOOGL": {
                "price": 175.45,
                "marketCap": 2180000000000,
                "pe": 29.3,
                "revenue": 282836000000,
                "revenueGrowth": 0.10,
                "margins": 0.255
            }
        }
        
        data = mock_data.get(ticker, {
            "price": 100.00,
            "marketCap": 1000000000000,
            "pe": 25.0,
            "revenue": 100000000000,
            "revenueGrowth": 0.05,
            "margins": 0.20
        })
        
        company_name = self.companies.get(ticker, ticker)
        content = f"""
{company_name} Financial Overview (Mock Data)
Data as of: {datetime.now().strftime('%Y-%m-%d')}

Company Metrics:
Stock Price: ${data['price']}
Market Cap: ${data['marketCap']:,.0f}
P/E Ratio: {data['pe']}

Financial Performance:
Revenue (TTM): ${data['revenue']:,.0f}
Revenue Growth: {data['revenueGrowth']*100:.1f}%
Net Margins: {data['margins']*100:.1f}%

Note: This is simulated data for demonstration purposes.
Real-time data requires active internet connection.
        """
        
        return {
            "ticker": ticker,
            "company": company_name,
            "quarter": f"Q3 {datetime.now().year}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "content": content,
            "source": "mock-enhanced"
        }
    
    def save_transcript(self, ticker: str, data: Dict):
        """Save transcript data"""
        os.makedirs("../data/transcripts", exist_ok=True)
        filepath = f"../data/transcripts/{ticker}_latest.json"
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Saved {ticker} (source: {data['source']})")
    
    def scrape_all(self):
        """Process all companies"""
        print("Starting earnings data collection...")
        print("=" * 50)
        
        for ticker in self.companies.keys():
            data = self.get_earnings_summary(ticker)
            self.save_transcript(ticker, data)
            time.sleep(1)  # Rate limiting
        
        print("\n✓ Data collection complete!")

if __name__ == "__main__":
    scraper = SimpleEarningsScraper()
    scraper.scrape_all()