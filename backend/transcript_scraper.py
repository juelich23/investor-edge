import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from typing import Dict, Optional
import time
import re

class EarningsTranscriptScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def fetch_from_investor_site(self, ticker: str, company_domain: str) -> Optional[Dict]:
        """
        Fetch transcript from company investor relations page
        Example: apple.com/investor/
        """
        try:
            # Common IR page patterns
            ir_patterns = [
                f"https://{company_domain}/investor/",
                f"https://investor.{company_domain}/",
                f"https://ir.{company_domain}/",
                f"https://{company_domain}/investors/",
                f"https://{company_domain}/investor-relations/"
            ]
            
            for url in ir_patterns:
                try:
                    response = self.session.get(url, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Look for earnings call links
                        earnings_links = []
                        for link in soup.find_all('a', href=True):
                            text = link.get_text().lower()
                            if any(term in text for term in ['earnings call', 'earnings transcript', 'quarterly results', 'q1', 'q2', 'q3', 'q4']):
                                earnings_links.append({
                                    'text': link.get_text().strip(),
                                    'href': link['href']
                                })
                        
                        if earnings_links:
                            # Get the most recent transcript
                            latest_link = earnings_links[0]
                            transcript_url = latest_link['href']
                            if not transcript_url.startswith('http'):
                                transcript_url = f"https://{company_domain}{transcript_url}"
                            
                            # Fetch transcript content
                            transcript_response = self.session.get(transcript_url, timeout=10)
                            if transcript_response.status_code == 200:
                                transcript_soup = BeautifulSoup(transcript_response.content, 'html.parser')
                                
                                # Extract transcript text
                                # Remove script and style elements
                                for script in transcript_soup(["script", "style"]):
                                    script.decompose()
                                
                                # Get text content
                                text = transcript_soup.get_text()
                                lines = (line.strip() for line in text.splitlines())
                                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                                text = ' '.join(chunk for chunk in chunks if chunk)
                                
                                return {
                                    'source': 'investor_site',
                                    'url': transcript_url,
                                    'title': latest_link['text'],
                                    'content': text[:50000]  # Limit to 50k chars
                                }
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Error fetching from investor site: {e}")
            
        return None
    
    def fetch_financial_modeling_prep(self, ticker: str) -> Optional[Dict]:
        """
        Fetch transcript from Financial Modeling Prep API (free tier available)
        """
        try:
            # Note: In production, use environment variable for API key
            # Free tier allows limited calls
            api_key = "demo"  # Replace with actual key
            url = f"https://financialmodelingprep.com/api/v3/earning_call_transcript/{ticker}?quarter=1&year=2024&apikey={api_key}"
            
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    transcript = data[0]
                    return {
                        'source': 'financial_modeling_prep',
                        'date': transcript.get('date', ''),
                        'content': transcript.get('content', ''),
                        'quarter': transcript.get('quarter', ''),
                        'year': transcript.get('year', '')
                    }
                    
        except Exception as e:
            print(f"Error fetching from Financial Modeling Prep: {e}")
            
        return None
    
    def fetch_mock_transcript(self, ticker: str) -> Dict:
        """
        Generate a realistic mock transcript using actual financial data
        """
        import yfinance as yf
        
        # Get actual financial data
        stock = yf.Ticker(ticker)
        info = stock.info
        
        company_name = info.get('longName', ticker)
        current_date = datetime.now()
        quarter = f"Q{(current_date.month-1)//3 + 1} {current_date.year}"
        
        # Extract real financial metrics
        revenue = info.get('totalRevenue', 0)
        revenue_millions = revenue / 1000000
        revenue_billions = revenue / 1000000000
        
        revenue_growth = info.get('revenueGrowth', 0.15)
        revenue_growth_pct = int(revenue_growth * 100)
        
        operating_margin = info.get('operatingMargins', 0.15)
        operating_margin_pct = round(operating_margin * 100, 1)
        
        gross_margin = info.get('grossMargins', 0.30)
        gross_margin_pct = round(gross_margin * 100, 1)
        
        profit_margin = info.get('profitMargins', 0.10)
        profit_margin_pct = round(profit_margin * 100, 1)
        
        eps = info.get('trailingEps', 1.0)
        pe_ratio = info.get('trailingPE', 25)
        
        operating_cash_flow = info.get('operatingCashflow', revenue * 0.2)
        free_cash_flow = info.get('freeCashflow', operating_cash_flow * 0.8)
        
        # Format large numbers appropriately
        if revenue_billions >= 1:
            revenue_str = f"${revenue_billions:.1f} billion"
        else:
            revenue_str = f"${revenue_millions:.0f} million"
            
        ocf_millions = operating_cash_flow / 1000000
        fcf_millions = free_cash_flow / 1000000
        
        if ocf_millions >= 1000:
            ocf_str = f"${ocf_millions/1000:.1f} billion"
        else:
            ocf_str = f"${ocf_millions:.0f} million"
            
        if fcf_millions >= 1000:
            fcf_str = f"${fcf_millions/1000:.1f} billion"
        else:
            fcf_str = f"${fcf_millions:.0f} million"
        
        # Calculate next quarter estimates
        next_q_revenue_low = revenue_millions * (1 + revenue_growth * 0.8)
        next_q_revenue_high = revenue_millions * (1 + revenue_growth * 1.2)
        next_q_eps_low = round(eps * (1 + revenue_growth * 0.5) * 0.9, 2)
        next_q_eps_high = round(eps * (1 + revenue_growth * 0.5) * 1.1, 2)
        
        # Generate realistic transcript content
        transcript_content = f"""
{company_name} {quarter} Earnings Call Transcript
Date: {current_date.strftime('%B %d, %Y')}

Operator: Good afternoon, and welcome to the {company_name} {quarter} earnings conference call. I'll now turn the call over to your host.

CEO: Thank you, operator. Good afternoon, everyone, and thank you for joining us today. I'm pleased to report another strong quarter for {company_name}.

Let me start with our financial highlights. We delivered robust revenue growth this quarter, exceeding our guidance and analyst expectations. Our revenue came in at {revenue_str}, representing year-over-year growth of {revenue_growth_pct}%. This growth was driven by strong demand across all our key product lines and geographical regions.

Our operating margins also expanded significantly, reaching {operating_margin_pct}%, up from {operating_margin_pct - 2.5:.1f}% in the same quarter last year. This improvement reflects our continued focus on operational efficiency and the scalability of our business model.

Looking at our key business segments:

First, our core business continues to show impressive momentum. We saw particularly strong adoption among enterprise customers, with several major wins in the Fortune 500. Customer retention remains at industry-leading levels, and our net promoter scores continue to improve.

Second, our new initiatives are gaining traction faster than anticipated. The investments we've made in AI and machine learning are beginning to pay off, with these capabilities now integrated across our product suite. Early customer feedback has been overwhelmingly positive, and we're seeing increased engagement and higher average revenue per user as a result.

Third, our international expansion is proceeding ahead of schedule. We've successfully launched in three new markets this quarter, and the initial response has exceeded our expectations. We're particularly excited about the opportunities in the Asia-Pacific region, where we're seeing rapid adoption.

Now, let me address some of the challenges we're navigating. Like many companies, we're dealing with macroeconomic headwinds, including inflation and supply chain constraints. However, I'm proud of how our team has managed these challenges. We've maintained our product quality and delivery timelines while protecting our margins.

Looking ahead to the next quarter and full year:

For Q{((current_date.month-1)//3 + 2) % 4 + 1}, we expect revenue in the range of ${next_q_revenue_low:.0f} million to ${next_q_revenue_high:.0f} million, representing year-over-year growth of approximately {revenue_growth_pct}%. We anticipate continued margin expansion, with operating margins expected to reach {operating_margin_pct + 0.5:.1f}%.

For the full fiscal year, we're maintaining our positive outlook. We expect continued growth in the {revenue_growth_pct}-{revenue_growth_pct + 5}% range. This reflects our confidence in the underlying strength of our business and the multiple growth drivers we have in place.

Our key strategic priorities for the remainder of the year include:

1. Accelerating our AI and automation initiatives to drive product innovation
2. Expanding our presence in high-growth international markets
3. Deepening relationships with our enterprise customers
4. Continuing to invest in our talent and technology infrastructure

Before I turn it over to our CFO, I want to thank our incredible team for their dedication and hard work. Their commitment to our mission and our customers is what drives our success.

CFO: Thank you. Let me provide more detail on our financial performance and outlook.

Starting with the income statement, total revenue for the quarter was {revenue_str}, up {revenue_growth_pct}% year-over-year and approximately {int(revenue_growth_pct/4)}% sequentially. This exceeded the high end of our guidance range by ${int(revenue_millions * 0.02)} million.

Breaking down revenue by segment:
- Product revenue was ${revenue_millions * 0.6:.0f} million, up {revenue_growth_pct + 5}% year-over-year
- Services revenue was ${revenue_millions * 0.3:.0f} million, up {revenue_growth_pct - 5}% year-over-year
- Subscription revenue showed particular strength at ${revenue_millions * 0.1:.0f} million, up {revenue_growth_pct + 15}% year-over-year

Gross margin for the quarter was {gross_margin_pct}%, compared to {gross_margin_pct - 1.5:.1f}% in the year-ago quarter. The improvement was driven by favorable product mix, pricing actions we took earlier in the year, and continued operational efficiencies.

Operating expenses were ${revenue_millions * (1 - operating_margin):.0f} million, or {100 - operating_margin_pct:.1f}% of revenue, compared to {100 - operating_margin_pct + 2:.1f}% in the prior year. We continue to invest aggressively in R&D while maintaining disciplined spending in other areas.

Operating income was ${revenue_millions * operating_margin:.0f} million, representing an operating margin of {operating_margin_pct}%. This compares to {operating_margin_pct - 2.5:.1f}% in the same quarter last year.

Net income was ${revenue_millions * profit_margin:.0f} million, or ${eps:.2f} per diluted share, compared to ${revenue_millions * profit_margin * 0.8:.0f} million, or ${eps * 0.8:.2f} per diluted share in the year-ago quarter.

Turning to the balance sheet and cash flow:

We ended the quarter with ${revenue_millions * 2:.0f} million in cash and marketable securities. Operating cash flow was {ocf_str}, and free cash flow was {fcf_str}. We returned ${fcf_millions * 0.3:.0f} million to shareholders through our dividend and share repurchase program.

Our balance sheet remains very strong, providing us with significant flexibility to invest in growth opportunities while returning capital to shareholders.

Regarding our outlook:

For Q{((current_date.month-1)//3 + 2) % 4 + 1}, we expect:
- Revenue between ${next_q_revenue_low:.0f} million and ${next_q_revenue_high:.0f} million
- Gross margin of approximately {gross_margin_pct + 0.5:.1f}%
- Operating margin of approximately {operating_margin_pct + 0.5:.1f}%
- EPS between ${next_q_eps_low} and ${next_q_eps_high}

For the full fiscal year, we now expect:
- Revenue growth in the range of {revenue_growth_pct}-{revenue_growth_pct + 5}%
- Gross margin of approximately {gross_margin_pct + 1:.1f}%
- Operating margin of approximately {operating_margin_pct + 1:.1f}%
- Continued strong cash flow generation

These projections reflect our confidence in our business momentum, though we remain mindful of the macroeconomic uncertainties.

With that, let's open the call for questions.

[Q&A Section begins]

Analyst 1: Thank you for taking my question. Can you provide more color on the AI initiatives you mentioned? How are these translating into revenue opportunities?

CEO: Great question. Our AI initiatives are centered around three key areas. First, we're using AI to enhance our core products, making them more intelligent and predictive. This is driving higher engagement and allowing us to command premium pricing. Second, we're developing entirely new AI-powered solutions that address previously unmet customer needs. These are opening up new market opportunities for us. Third, we're using AI internally to improve our operations, from customer service to supply chain optimization. While it's still early, we're already seeing meaningful revenue contribution from our AI-enhanced products, and we expect this to accelerate significantly over the coming quarters.

Analyst 2: Can you discuss your capital allocation priorities and how you're thinking about M&A?

CFO: Our capital allocation framework remains consistent. Our first priority is investing in organic growth opportunities that meet our return thresholds. We're seeing plenty of these opportunities, particularly in R&D and international expansion. Second, we're committed to returning capital to shareholders through our dividend and buyback program. Regarding M&A, we remain active in evaluating opportunities that could accelerate our strategic initiatives or bring us critical capabilities. We have the balance sheet strength to act opportunistically, but we'll remain disciplined in our approach.

[Additional Q&A continues...]

Operator: That concludes our Q&A session. I'll now turn the call back to management for closing remarks.

CEO: Thank you all for joining us today. We're excited about the momentum in our business and the opportunities ahead. We remain focused on executing our strategy, delivering value to our customers, and creating long-term value for our shareholders. We look forward to updating you on our progress next quarter. Thank you.

Operator: This concludes today's conference call. Thank you for participating.
"""
        
        return {
            'source': 'mock',
            'ticker': ticker,
            'company': company_name,
            'quarter': quarter,
            'date': current_date.strftime('%Y-%m-%d'),
            'content': transcript_content,
            'has_qa': True,
            'participants': ['CEO', 'CFO', 'Analysts']
        }
    
    def get_earnings_transcript(self, ticker: str, company_domain: Optional[str] = None) -> Dict:
        """
        Main method to fetch earnings transcript from available sources
        """
        print(f"Fetching earnings transcript for {ticker}...")
        
        # Try different sources in order of preference
        transcript = None
        
        # 1. Try company investor relations site if domain provided
        if company_domain:
            transcript = self.fetch_from_investor_site(ticker, company_domain)
            if transcript:
                print(f"✓ Found transcript on investor site")
                return transcript
        
        # 2. Try Financial Modeling Prep API
        transcript = self.fetch_financial_modeling_prep(ticker)
        if transcript:
            print(f"✓ Found transcript on Financial Modeling Prep")
            return transcript
        
        # 3. Fall back to mock transcript
        print(f"ℹ Using mock transcript for demonstration")
        return self.fetch_mock_transcript(ticker)
    
    def save_transcript(self, ticker: str, transcript_data: Dict):
        """Save transcript to file"""
        os.makedirs("../data/transcripts/full", exist_ok=True)
        filepath = f"../data/transcripts/full/{ticker}_latest_transcript.json"
        
        with open(filepath, 'w') as f:
            json.dump(transcript_data, f, indent=2)
        
        print(f"✓ Saved transcript to {filepath}")

# Company domain mapping for popular stocks
COMPANY_DOMAINS = {
    'AAPL': 'apple.com',
    'MSFT': 'microsoft.com',
    'GOOGL': 'abc.xyz',
    'AMZN': 'amazon.com',
    'META': 'investor.fb.com',
    'NVDA': 'nvidia.com',
    'TSLA': 'tesla.com',
    # Add more as needed
}

if __name__ == "__main__":
    scraper = EarningsTranscriptScraper()
    
    # Test with a few companies
    test_tickers = ['AAPL', 'NVDA', 'SOFI']
    
    for ticker in test_tickers:
        domain = COMPANY_DOMAINS.get(ticker)
        transcript = scraper.get_earnings_transcript(ticker, domain)
        scraper.save_transcript(ticker, transcript)
        
        print(f"\nTranscript preview for {ticker}:")
        print(f"Source: {transcript['source']}")
        print(f"Content length: {len(transcript['content'])} chars")
        print(f"First 500 chars: {transcript['content'][:500]}...")
        print("-" * 50)