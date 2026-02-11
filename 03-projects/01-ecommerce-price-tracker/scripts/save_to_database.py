"""
Save scraped Tiki products to PostgreSQL
"""

import json
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from scrapers.tiki_scraper import fetch_tiki_product


def save_products_to_db():
    """
    Read target products and save to database
    """
    # Load target products
    with open('data/target-products.json', 'r', encoding='utf-8') as f:
        targets = json.load(f)
    
    tiki_targets = [item for item in targets if item.get('platform') == 'tiki']
    
    print(f"Saving {len(tiki_targets)} products to database...\n")
    
    success_count = 0
    failed_count = 0
    
    for i, target in enumerate(tiki_targets, 1):
        url = target['url']
        print(f"[{i}/{len(tiki_targets)}] {url[:60]}...")

        
        # Scrape product
        product = fetch_tiki_product(url)
        
        if product:
            try:
                # Save to database
                DatabaseManager.save_price_data(product)
                success_count += 1
                
            except Exception as e:
                print(f"Database error: {e}")
                failed_count += 1
        else:
            print(f"Scraping failed")
            failed_count += 1
        
        print()
    
    # Summary
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Saved to database: {success_count}/{len(tiki_targets)}")
    print(f"Failed: {failed_count}")
    
    # Show latest prices
    print("\n" + "="*70)
    print("LATEST PRICES IN DATABASE")
    print("="*70)
    
    latest = DatabaseManager.get_latest_prices()
    for p in latest:
        print(f"{p['name'][:50]}: {p['price']:,}đ (as of {p['scraped_at']})")


if __name__ == "__main__":
    save_products_to_db()