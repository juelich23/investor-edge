from improved_historical_scraper import ImprovedHistoricalScraper
import time

def process_all_historical():
    companies = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META",
        "TSLA", "NVDA", "JPM", "JNJ", "WMT"
    ]
    
    scraper = ImprovedHistoricalScraper()
    
    for ticker in companies:
        print(f"Processing historical data for {ticker}...")
        try:
            data = scraper.get_historical_earnings(ticker)
            scraper.save_historical_data(ticker, data)
            print(f"✓ Completed {ticker}")
            time.sleep(1)  # Be nice to APIs
        except Exception as e:
            print(f"✗ Error processing {ticker}: {e}")
    
    print("\nHistorical data processing complete!")

if __name__ == "__main__":
    process_all_historical()