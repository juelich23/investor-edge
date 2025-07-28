import yfinance as yf
import pandas as pd
import requests
import json
from typing import List, Dict
import time
from datetime import datetime

class StockListFetcher:
    def __init__(self):
        self.exchanges = ['NYSE', 'NASDAQ']
        
    def fetch_sp500_stocks(self) -> List[Dict]:
        """Fetch S&P 500 stocks as a starting point"""
        try:
            # Get S&P 500 list from Wikipedia
            url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
            tables = pd.read_html(url)
            sp500_df = tables[0]
            
            stocks = []
            for _, row in sp500_df.iterrows():
                stock = {
                    'ticker': row['Symbol'],
                    'name': row['Security'],
                    'sector': row['GICS Sector'],
                    'sub_industry': row['GICS Sub-Industry'],
                    'exchange': 'NYSE/NASDAQ',  # S&P 500 includes both
                    'market_cap': None,
                    'is_sp500': True
                }
                stocks.append(stock)
            
            print(f"Fetched {len(stocks)} S&P 500 stocks")
            return stocks
        except Exception as e:
            print(f"Error fetching S&P 500 stocks: {e}")
            return []
    
    def fetch_nasdaq_stocks(self) -> List[Dict]:
        """Fetch NASDAQ-listed stocks"""
        try:
            # Using NASDAQ's public data
            nasdaq_url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(nasdaq_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                stocks = []
                
                for row in data.get('data', {}).get('rows', []):
                    # Filter for NYSE and NASDAQ only
                    if row.get('exchange') in ['NYSE', 'NASDAQ']:
                        stock = {
                            'ticker': row.get('symbol', ''),
                            'name': row.get('name', ''),
                            'sector': row.get('sector', ''),
                            'sub_industry': row.get('industry', ''),
                            'exchange': row.get('exchange', ''),
                            'market_cap': row.get('marketCap', 0),
                            'is_sp500': False
                        }
                        stocks.append(stock)
                
                print(f"Fetched {len(stocks)} stocks from NASDAQ API")
                return stocks
            else:
                print(f"Failed to fetch NASDAQ stocks: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error fetching NASDAQ stocks: {e}")
            return []
    
    def fetch_popular_stocks(self) -> List[Dict]:
        """Fetch popular stocks that might be missing from other sources"""
        popular_tickers = [
            # Tech giants
            'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'META', 'NVDA', 'TSLA',
            'NFLX', 'ADBE', 'CRM', 'ORCL', 'INTC', 'AMD', 'QCOM', 'AVGO',
            'TXN', 'CSCO', 'IBM', 'NOW', 'UBER', 'SHOP', 'SQ', 'PYPL',
            'SNAP', 'PINS', 'ROKU', 'ZM', 'DOCU', 'TWLO', 'SPOT', 'NET',
            'PLTR', 'SNOW', 'DDOG', 'CRWD', 'OKTA', 'ZS', 'PANW', 'FTNT',
            
            # Fintech & Digital Finance
            'SOFI', 'HOOD', 'COIN', 'AFRM', 'UPST', 'LC', 'ALLY', 'SYF',
            'DFS', 'NDAQ', 'ICE', 'CME', 'MSCI', 'SPGI', 'MCO',
            
            # Finance
            'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'BLK', 'SCHW', 'AXP',
            'V', 'MA', 'COF', 'USB', 'PNC', 'TFC', 'BK',
            
            # Healthcare & Biotech
            'JNJ', 'PFE', 'UNH', 'CVS', 'ABBV', 'MRK', 'TMO', 'ABT',
            'LLY', 'DHR', 'BMY', 'AMGN', 'GILD', 'MDT', 'ISRG', 'MRNA',
            'BNTX', 'REGN', 'VRTX', 'BIIB', 'HIMS', 'TDOC', 'VEEV', 'DXCM',
            
            # Consumer
            'WMT', 'HD', 'PG', 'KO', 'PEP', 'COST', 'NKE', 'MCD', 'DIS',
            'SBUX', 'TGT', 'LOW', 'CMG', 'YUM', 'MAR', 'BKNG', 'ABNB',
            'DASH', 'LYFT', 'F', 'GM', 'RIVN', 'LCID', 'NIO', 'XPEV',
            
            # Energy
            'XOM', 'CVX', 'COP', 'SLB', 'EOG', 'MPC', 'PSX', 'VLO',
            'OXY', 'DVN', 'FANG', 'PXD', 'HES', 'MRO',
            
            # Other sectors
            'BA', 'CAT', 'GE', 'MMM', 'UPS', 'FDX', 'RTX', 'LMT', 'DE',
            'T', 'VZ', 'TMUS', 'SPG', 'AMT', 'PLD', 'CCI', 'EQIX',
            'DLR', 'WELL', 'ARE', 'VICI', 'O', 'SBAC'
        ]
        
        stocks = []
        for ticker in popular_tickers:
            try:
                stock_info = yf.Ticker(ticker).info
                if stock_info.get('symbol'):
                    stock = {
                        'ticker': ticker,
                        'name': stock_info.get('longName', ticker),
                        'sector': stock_info.get('sector', 'Unknown'),
                        'sub_industry': stock_info.get('industry', 'Unknown'),
                        'exchange': stock_info.get('exchange', 'Unknown'),
                        'market_cap': stock_info.get('marketCap', 0),
                        'is_sp500': False
                    }
                    stocks.append(stock)
                    time.sleep(0.1)  # Rate limiting
            except:
                continue
        
        print(f"Fetched {len(stocks)} popular stocks")
        return stocks
    
    def merge_and_deduplicate(self, *stock_lists) -> List[Dict]:
        """Merge multiple stock lists and remove duplicates"""
        all_stocks = {}
        
        for stock_list in stock_lists:
            for stock in stock_list:
                ticker = stock['ticker']
                if ticker not in all_stocks:
                    all_stocks[ticker] = stock
                else:
                    # Update with better data if available
                    if not all_stocks[ticker]['market_cap'] and stock['market_cap']:
                        all_stocks[ticker]['market_cap'] = stock['market_cap']
                    if stock['is_sp500']:
                        all_stocks[ticker]['is_sp500'] = True
        
        return list(all_stocks.values())
    
    def save_stock_list(self, stocks: List[Dict], filename: str = '../data/nyse_stocks.json'):
        """Save stock list to JSON file"""
        # Sort by market cap (descending) and then by ticker
        stocks_sorted = sorted(stocks, 
                             key=lambda x: (x.get('market_cap') or 0, x['ticker']), 
                             reverse=True)
        
        # Add metadata
        data = {
            'last_updated': datetime.now().isoformat(),
            'total_stocks': len(stocks_sorted),
            'stocks': stocks_sorted
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Saved {len(stocks_sorted)} stocks to {filename}")
        
        # Print summary
        sectors = {}
        for stock in stocks_sorted:
            sector = stock.get('sector', 'Unknown')
            sectors[sector] = sectors.get(sector, 0) + 1
        
        print("\nStock distribution by sector:")
        for sector, count in sorted(sectors.items(), key=lambda x: x[1], reverse=True):
            print(f"  {sector}: {count}")
    
    def fetch_all_stocks(self):
        """Fetch stocks from all sources and save"""
        print("Fetching stock lists...")
        
        # Fetch from different sources
        sp500_stocks = self.fetch_sp500_stocks()
        nasdaq_stocks = self.fetch_nasdaq_stocks()
        popular_stocks = self.fetch_popular_stocks()
        
        # Merge and deduplicate
        all_stocks = self.merge_and_deduplicate(sp500_stocks, nasdaq_stocks, popular_stocks)
        
        # Save to file
        self.save_stock_list(all_stocks)
        
        return all_stocks

if __name__ == "__main__":
    fetcher = StockListFetcher()
    stocks = fetcher.fetch_all_stocks()