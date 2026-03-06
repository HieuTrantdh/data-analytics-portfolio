"""
Simple text-based dashboard
Summary of all data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import get_db_connection
from psycopg2.extras import RealDictCursor
from datetime import datetime


def show_dashboard():
    """Display dashboard summary"""
    
    print("\n" + "="*80)
    print(f" TIKI PRICE TRACKER DASHBOARD")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            
            # Quick stats
            cur.execute("""
                SELECT 
                    COUNT(DISTINCT p.id) as total_products,
                    COUNT(ph.id) as total_price_records,
                    MIN(ph.scraped_at) as first_scrape,
                    MAX(ph.scraped_at) as last_scrape
                FROM products p
                LEFT JOIN price_history ph ON p.id = ph.product_id
            """)
            stats = cur.fetchone()
            
            print(f"\n OVERVIEW")
            print(f"  Products tracked:    {stats['total_products']}")
            print(f"  Price records:       {stats['total_price_records']}")
            print(f"  Tracking since:      {stats['first_scrape']}")
            print(f"  Last updated:        {stats['last_scrape']}")
            
            # Average scrapes per product
            if stats['total_products'] > 0:
                avg_scrapes = stats['total_price_records'] / stats['total_products']
                print(f"  Avg scrapes/product: {avg_scrapes:.1f}")
            
            # Price stats
            cur.execute("""
                SELECT 
                    MIN(price) as min_price,
                    MAX(price) as max_price,
                    SUM(price) as total_value,
                    AVG(price) as avg_price
                FROM latest_prices
                WHERE price > 0
            """)
            prices = cur.fetchone()
            
            if prices['min_price']:
                print(f"\n PRICING")
                print(f"  Cheapest product:    {prices['min_price']:>12,}đ")
                print(f"  Most expensive:      {prices['max_price']:>12,}đ")
                print(f"  Average price:       {prices['avg_price']:>12,.0f}đ")
                print(f"  Total catalog value: {prices['total_value']:>12,}đ")
            
            # Discounts
            cur.execute("""
                SELECT 
                    COUNT(*) as products_on_sale,
                    AVG(discount_percent) as avg_discount,
                    MAX(discount_percent) as max_discount,
                    SUM(original_price - price) as total_savings
                FROM latest_prices
                WHERE discount_percent > 0
            """)
            discounts = cur.fetchone()
            
            if discounts['products_on_sale'] and discounts['products_on_sale'] > 0:
                print(f"\n DISCOUNTS")
                print(f"  Products on sale:    {discounts['products_on_sale']}")
                print(f"  Average discount:    {discounts['avg_discount']:>12.1f}%")
                print(f"  Max discount:        {discounts['max_discount']:>12.1f}%")
                print(f"  Potential savings:   {discounts['total_savings']:>12,}đ")
            else:
                print(f"\n DISCOUNTS")
                print(f"  No active discounts")
            
            # Ratings
            cur.execute("""
                SELECT 
                    COUNT(*) as products_with_ratings,
                    AVG(rating_average) as avg_rating,
                    MAX(rating_average) as max_rating,
                    MIN(rating_average) as min_rating
                FROM latest_prices
                WHERE rating_average > 0
            """)
            ratings = cur.fetchone()
            
            if ratings['products_with_ratings'] and ratings['products_with_ratings'] > 0:
                print(f"\n RATINGS")
                print(f"  Products with ratings: {ratings['products_with_ratings']}")
                print(f"  Average rating:        {ratings['avg_rating']:>12.2f}/5.00")
                print(f"  Highest:               {ratings['max_rating']:>12.2f}/5.00")
                print(f"  Lowest:                {ratings['min_rating']:>12.2f}/5.00")
            
            # Reviews
            cur.execute("""
                SELECT 
                    SUM(review_count) as total_reviews,
                    AVG(review_count) as avg_reviews,
                    MAX(review_count) as max_reviews
                FROM latest_prices
                WHERE review_count > 0
            """)
            reviews = cur.fetchone()
            
            if reviews['total_reviews'] and reviews['total_reviews'] > 0:
                print(f"\n REVIEWS")
                print(f"  Total reviews:       {reviews['total_reviews']:>12,}")
                print(f"  Average per product: {reviews['avg_reviews']:>12,.0f}")
                print(f"  Most reviewed:       {reviews['max_reviews']:>12,}")
            
            # Price changes
            cur.execute("SELECT COUNT(*) as changes FROM price_changes")
            changes = cur.fetchone()
            
            if changes['changes'] and changes['changes'] > 0:
                print(f"\n PRICE CHANGES")
                print(f"  Products with changes: {changes['changes']}")
                
                # Show recent changes
                cur.execute("""
                    SELECT name, previous_price, current_price, percent_change
                    FROM price_changes
                    ORDER BY ABS(percent_change) DESC
                    LIMIT 3
                """)
                
                top_changes = cur.fetchall()
                
                if top_changes:
                    print(f"\n  Top changes:")
                    for c in top_changes:
                        direction = "" if c['percent_change'] < 0 else "📈"
                        print(f"    {direction} {c['name'][:45]}")
                        print(f"       {c['previous_price']:,}đ → {c['current_price']:,}đ ({c['percent_change']:+.1f}%)")
            
            # Top 5 most expensive products
            print(f"\n TOP 5 MOST EXPENSIVE")
            cur.execute("""
                SELECT name, price, discount_percent
                FROM latest_prices
                WHERE price > 0
                ORDER BY price DESC
                LIMIT 5
            """)
            top_expensive = cur.fetchall()
            
            for i, p in enumerate(top_expensive, 1):
                discount_str = f" (-{p['discount_percent']:.0f}%)" if p['discount_percent'] and p['discount_percent'] > 0 else ""
                print(f"  {i}. {p['name'][:50]}")
                print(f"     {p['price']:,}đ{discount_str}")
            
            # Top 5 best deals (highest discount)
            print(f"\n TOP 5 BEST DEALS")
            cur.execute("""
                SELECT name, price, original_price, discount_percent
                FROM latest_prices
                WHERE discount_percent > 0
                ORDER BY discount_percent DESC
                LIMIT 5
            """)
            top_deals = cur.fetchall()
            
            if top_deals:
                for i, p in enumerate(top_deals, 1):
                    savings = p['original_price'] - p['price']
                    print(f"  {i}. {p['name'][:50]}")
                    print(f"     {p['original_price']:,}đ → {p['price']:,}đ (save {savings:,}đ, -{p['discount_percent']:.0f}%)")
            else:
                print(f"  No deals available")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    show_dashboard()