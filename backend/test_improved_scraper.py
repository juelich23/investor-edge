from improved_historical_scraper import ImprovedHistoricalScraper
import json

scraper = ImprovedHistoricalScraper()
print("Fetching NVDA historical data...")
data = scraper.get_historical_earnings('NVDA')
scraper.save_historical_data('NVDA', data)

print(f"\nFound {len(data['quarters'])} quarters of data")
print("\nFirst 3 quarters:")
for i in range(min(3, len(data['quarters']))):
    q = data['quarters'][i]
    print(f"\nQ{i+1}: {q['quarter']}")
    print(f"  Revenue: ${q['revenue']}M" if q['revenue'] else "  Revenue: N/A")
    print(f"  EPS Act: ${q['eps_actual']:.2f}" if q['eps_actual'] else "  EPS Act: N/A")
    print(f"  EPS Est: ${q['eps_estimate']:.2f}" if q['eps_estimate'] else "  EPS Est: N/A")
    print(f"  Surprise: {q['surprise_percent']:.1f}%" if q['surprise_percent'] else "  Surprise: N/A")
    print(f"  Price: ${q['price_on_date']:.2f}" if q['price_on_date'] else "  Price: N/A")