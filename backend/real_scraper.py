import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import time
import re
from urllib.parse import quote

class RealEarningsTranscriptScraper:
    def __init__(self, alpha_vantage_key: Optional[str] = None):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.alpha_vantage_key = alpha_vantage_key or os.getenv('ALPHA_VANTAGE_API_KEY')
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
    
    def get_earnings_from_alpha_vantage(self, ticker: str) -> Optional[Dict]:
        """Fetch earnings data from Alpha Vantage API"""
        if not self.alpha_vantage_key:
            print(f"No Alpha Vantage API key found for {ticker}")
            return None
            
        url = f"https://www.alphavantage.co/query"
        params = {
            'function': 'EARNINGS',
            'symbol': ticker,
            'apikey': self.alpha_vantage_key
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'quarterlyEarnings' in data and data['quarterlyEarnings']:
                latest = data['quarterlyEarnings'][0]
                return {
                    'reportedDate': latest.get('reportedDate', ''),
                    'reportedEPS': latest.get('reportedEPS', 'N/A'),
                    'estimatedEPS': latest.get('estimatedEPS', 'N/A'),
                    'surprise': latest.get('surprise', 'N/A'),
                    'surprisePercentage': latest.get('surprisePercentage', 'N/A')
                }
        except Exception as e:
            print(f"Error fetching from Alpha Vantage for {ticker}: {e}")
        
        return None
    
    def scrape_yahoo_finance_transcript(self, ticker: str) -> Optional[str]:
        """Scrape earnings call transcript from Yahoo Finance"""
        # Yahoo Finance doesn't provide full transcripts, but we can get earnings summary
        url = f"https://finance.yahoo.com/quote/{ticker}"
        
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract recent news and analysis
            news_items = []
            news_section = soup.find_all('h3', {'class': 'Mb(5px)'})
            
            for item in news_section[:5]:  # Get top 5 news items
                title = item.get_text(strip=True)
                if 'earnings' in title.lower() or 'quarter' in title.lower():
                    news_items.append(title)
            
            if news_items:
                return f"Recent earnings-related news for {ticker}:\n" + "\n".join(f"- {item}" for item in news_items)
                
        except Exception as e:
            print(f"Error scraping Yahoo Finance for {ticker}: {e}")
        
        return None
    
    def scrape_seeking_alpha_transcript(self, ticker: str) -> Optional[str]:
        """Attempt to get earnings info from Seeking Alpha (limited without subscription)"""
        base_url = f"https://seekingalpha.com/symbol/{ticker}/earnings/transcripts"
        
        try:
            response = requests.get(base_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract available transcript titles and dates
            transcript_links = soup.find_all('a', {'data-test-id': 'post-list-item-title'})
            
            if transcript_links:
                latest_title = transcript_links[0].get_text(strip=True)
                return f"Latest earnings call: {latest_title}\n(Full transcript requires Seeking Alpha subscription)"
            
        except Exception as e:
            print(f"Error accessing Seeking Alpha for {ticker}: {e}")
        
        return None
    
    def get_financial_modeling_prep_transcript(self, ticker: str) -> Optional[str]:
        """Get earnings call transcript from Financial Modeling Prep API (free tier)"""
        # Note: FMP offers limited free requests
        base_url = f"https://financialmodelingprep.com/api/v3/earning_call_transcript/{ticker}"
        params = {'quarter': 1, 'year': 2024}  # Adjust as needed
        
        try:
            response = requests.get(base_url, params=params, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return data[0].get('content', '')[:5000]  # First 5000 chars
        except Exception as e:
            print(f"Error accessing FMP for {ticker}: {e}")
        
        return None
    
    def create_composite_transcript(self, ticker: str) -> Dict:
        """Create a composite transcript from multiple sources"""
        print(f"Gathering real earnings data for {ticker}...")
        
        transcript_parts = []
        
        # Get earnings metrics from Alpha Vantage
        earnings_data = self.get_earnings_from_alpha_vantage(ticker)
        if earnings_data:
            transcript_parts.append(f"Latest Earnings Report:")
            transcript_parts.append(f"Reported Date: {earnings_data['reportedDate']}")
            transcript_parts.append(f"Reported EPS: ${earnings_data['reportedEPS']}")
            transcript_parts.append(f"Estimated EPS: ${earnings_data['estimatedEPS']}")
            transcript_parts.append(f"Surprise: {earnings_data['surprisePercentage']}%")
            transcript_parts.append("")
        
        # Try to get Yahoo Finance summary
        yahoo_summary = self.scrape_yahoo_finance_transcript(ticker)
        if yahoo_summary:
            transcript_parts.append(yahoo_summary)
            transcript_parts.append("")
        
        # Try Seeking Alpha
        sa_info = self.scrape_seeking_alpha_transcript(ticker)
        if sa_info:
            transcript_parts.append(sa_info)
            transcript_parts.append("")
        
        # If we have some real data, use it; otherwise fall back to enhanced mock
        if transcript_parts:
            content = "\n".join(transcript_parts)
        else:
            content = self.generate_realistic_mock_transcript(ticker)
        
        # Determine the most recent quarter
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
            "company": self.companies.get(ticker, ticker),
            "quarter": quarter,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "content": content,
            "source": "composite" if transcript_parts else "mock"
        }
    
    def generate_realistic_mock_transcript(self, ticker: str) -> str:
        """Generate a more realistic mock transcript when real data isn't available"""
        company = self.companies.get(ticker, ticker)
        
        templates = {
            "AAPL": """
Apple Q4 2024 Earnings Call Transcript

Tim Cook - CEO: Thank you for joining us today. I'm pleased to report another strong quarter for Apple. 
Revenue came in at $89.5 billion, up 8% year-over-year, driven by strong iPhone 15 demand and 
continued growth in Services.

Our active device install base has reached an all-time high across all geographic segments 
and product categories. iPhone revenue was $43.8 billion, up 10% year-over-year, with particular 
strength in emerging markets including India, Brazil, and Southeast Asia.

Services set a new all-time revenue record of $22.3 billion, up 16% year-over-year. We now have 
over 1 billion paid subscriptions across our services portfolio.

Luca Maestri - CFO: Gross margin for the quarter was 45.2%, up 80 basis points from last year, 
driven by favorable mix and continued operational efficiency. Operating cash flow was strong at 
$24.6 billion.

Looking ahead to Q1 2025, we expect revenue to grow in the low-to-mid single digits year-over-year, 
with continued strength in Services offsetting typical seasonal patterns in Products.

We remain confident in our long-term prospects, with exciting product launches planned and our 
ongoing investments in AI and machine learning beginning to bear fruit across our ecosystem.
            """,
            
            "MSFT": """
Microsoft Q4 2024 Earnings Call Transcript

Satya Nadella - CEO: We are witnessing the emergence of a new era of AI transformation, and 
Microsoft is leading this wave. Revenue was $65.6 billion, up 15% year-over-year, with cloud 
revenue exceeding $38 billion.

Azure revenue grew 31% year-over-year, with AI services contributing 8 points of growth. Our AI 
customer base has grown to over 60,000, including more than half of the Fortune 500.

Microsoft 365 Copilot is seeing tremendous adoption, with seats growing 100% quarter-over-quarter. 
We're helping organizations worldwide boost productivity with AI.

Amy Hood - CFO: Commercial cloud gross margin improved to 73%, up 2 points year-over-year. 
Operating income increased 18% to $30.6 billion.

For Q1 2025, we expect double-digit revenue growth across our segments. Azure growth is expected 
to remain above 30%, with increasing contribution from AI services. We project AI to be a 
$10 billion annual revenue run rate business by the end of fiscal 2025.

Capital expenditures will increase to support AI infrastructure demand, but we remain disciplined 
in our investments and focused on driving operating leverage.
            """
        }
        
        # Return specific template if available, otherwise generic
        if ticker in templates:
            return templates[ticker]
        
        return f"""
{company} Latest Earnings Call Transcript

CEO Opening Remarks: We delivered solid results this quarter with revenue growth across key segments. 
Our strategic initiatives are gaining traction, and we're seeing positive momentum in our core business.

Financial Highlights:
- Revenue increased year-over-year driven by strong demand
- Operating margins improved through operational efficiency
- Strong cash flow generation supports continued investment in growth

CFO Commentary: We're pleased with our financial performance. Gross margins expanded due to 
favorable product mix and cost management. We're maintaining our disciplined approach to capital 
allocation while investing in high-return opportunities.

Outlook: We expect continued growth momentum in the coming quarters. Our investments in innovation 
and market expansion position us well for long-term value creation. We remain focused on executing 
our strategic priorities and delivering value to shareholders.

Key Risks: Macroeconomic uncertainty, competitive pressures, and supply chain dynamics remain 
areas we're actively monitoring and managing.
        """
    
    def save_transcript(self, ticker: str, data: Dict):
        """Save transcript data to JSON file"""
        os.makedirs("../data/transcripts", exist_ok=True)
        filepath = f"../data/transcripts/{ticker}_latest.json"
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Saved transcript for {ticker} to {filepath} (source: {data.get('source', 'unknown')})")
    
    def scrape_all_companies(self):
        """Scrape transcripts for all configured companies"""
        for ticker in self.companies.keys():
            print(f"\nScraping {ticker}...")
            transcript_data = self.create_composite_transcript(ticker)
            self.save_transcript(ticker, transcript_data)
            time.sleep(2)  # Rate limiting

if __name__ == "__main__":
    # Set your Alpha Vantage API key here or in environment variable
    # Get free key at: https://www.alphavantage.co/support/#api-key
    scraper = RealEarningsTranscriptScraper()
    scraper.scrape_all_companies()