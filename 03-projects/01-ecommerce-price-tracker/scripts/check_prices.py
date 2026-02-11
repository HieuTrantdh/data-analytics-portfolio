"""
Check latest prices and price changes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager


def show_latest_prices():
    """Display latest prices for all products"""
    print("\n" + "="*70)
    print("LATEST PRICES")
    print("="*70)
    
    prices = DatabaseManager.get_latest_prices()
    
    for i, p in enumerate(prices, 1):
        print(f"\n{i}. {p['name'][:60]}")
        print(f"   Platform: {p['platform']}")
        print(f"   Price: {p['price']:,}đ")
        
        if p['original_price'] and p['original_price'] > p['price']:
            print(f"   Original: {p['original_price']:,}đ (-{p['discount_percent']}%)")
        
        print(f"   Rating: {p['rating_average']}/5")
        print(f"   Last updated: {p['scraped_at']}")


def show_price_changes():
    """Display products with price changes"""
    print("\n" + "="*70)
    print("PRICE CHANGES")
    print("="*70)
    
    changes = DatabaseManager.get_price_changes()
    
    if not changes:
        print("\n No price changes yet (need at least 2 scrapes)")
        return
    
    for i, p in enumerate(changes, 1):
        print(f"\n{i}. {p['name'][:60]}")
        
        if p['percent_change'] < 0:
            print(f"    Price DROP: {p['previous_price']:,}đ → {p['current_price']:,}đ")
            print(f"    Save: {abs(p['price_change']):,}đ ({p['percent_change']}%)")
        else:
            print(f"    Price UP: {p['previous_price']:,}đ → {p['current_price']:,}đ")
            print(f"   Increase: {p['price_change']:,}đ (+{p['percent_change']}%)")


if __name__ == "__main__":
    show_latest_prices()
    show_price_changes()