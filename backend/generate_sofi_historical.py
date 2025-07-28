from improved_historical_scraper import ImprovedHistoricalScraper

scraper = ImprovedHistoricalScraper()
print('Fetching historical data for SOFI...')
data = scraper.get_historical_earnings('SOFI')
scraper.save_historical_data('SOFI', data)
print('Done!')

# Show summary
print(f"\nFound {len(data['quarters'])} quarters of data")
if data['quarters']:
    for i, q in enumerate(data['quarters'][:3]):
        print(f"\nQuarter {i+1}: {q['quarter']}")
        print(f"  EPS Actual: ${q['eps_actual']:.2f}" if q['eps_actual'] else "  EPS Actual: N/A")
        print(f"  EPS Estimate: ${q['eps_estimate']:.2f}" if q['eps_estimate'] else "  EPS Estimate: N/A") 
        print(f"  Surprise: {q['surprise_percent']:.1f}%" if q['surprise_percent'] else "  Surprise: N/A")
        print(f"  Stock Price: ${q['price_on_date']:.2f}" if q['price_on_date'] else "  Stock Price: N/A")