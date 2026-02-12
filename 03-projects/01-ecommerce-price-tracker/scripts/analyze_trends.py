"""
Historical Price Analysis
"""

import os

from database.db_manager import get_db_connection
from psycopg2.extras import RealDictCursor


def get_price_trends():
    """Get price trends for all products"""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    p.name,
                    p.platform,
                    COUNT(ph.id) as scrape_count,
                    MIN(ph.price) as lowest_price,
                    MAX(ph.price) as highest_price,
                    AVG(ph.price) as avg_price,
                    (MAX(ph.price) - MIN(ph.price)) as price_range,
                    MIN(ph.scraped_at) as first_scrape,
                    MAX(ph.scraped_at) as last_scrape
                FROM products p
                JOIN price_history ph ON p.id = ph.product_id
                GROUP BY p.id, p.name, p.platform
                ORDER BY price_range DESC
            """)
            return cur.fetchall()


def get_product_history(product_name):
    """Get detailed price history for a product"""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    ph.price,
                    ph.discount_percent,
                    ph.rating_average,
                    ph.review_count,
                    ph.scraped_at
                FROM price_history ph
                JOIN products p ON ph.product_id = p.id
                WHERE p.name LIKE %s
                ORDER BY ph.scraped_at ASC
            """, (f'%{product_name}%',))
            return cur.fetchall()


def get_best_time_to_buy():
    """Analyze when products are typically cheapest"""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    p.name,
                    MIN(ph.price) as best_price,
                    (
                        SELECT scraped_at 
                        FROM price_history 
                        WHERE product_id = p.id 
                        ORDER BY price ASC, scraped_at ASC 
                        LIMIT 1
                    ) as when_cheapest,
                    (
                        SELECT price 
                        FROM price_history 
                        WHERE product_id = p.id 
                        ORDER BY scraped_at DESC 
                        LIMIT 1
                    ) as current_price
                FROM products p
                JOIN price_history ph ON p.id = ph.product_id
                GROUP BY p.id, p.name
                HAVING COUNT(ph.id) >= 2
            """)

            return cur.fetchall()


def display_trends():
    """Display price trend analysis"""
    print("\n" + "="*80)
    print(" PRICE TREND ANALYSIS")
    print("="*80)
    
    trends = get_price_trends()
    
    for i, product in enumerate(trends, 1):
        print(f"\n{i}. {product['name'][:60]}")
        print(f"   Platform: {product['platform']}")
        print(f"   Scrapes: {product['scrape_count']}")
        print(f"   Price Range: {product['lowest_price']:,}đ - {product['highest_price']:,}đ")
        print(f"   Average: {product['avg_price']:,.0f}đ")
        print(f"   Variation: {product['price_range']:,}đ")
        print(f"   Tracked: {product['first_scrape']} → {product['last_scrape']}")


def display_best_times():
    """Display best time to buy analysis"""
    print("\n" + "="*80)
    print(" BEST TIME TO BUY")
    print("="*80)
    
    products = get_best_time_to_buy()
    
    for i, p in enumerate(products, 1):
        print(f"\n{i}. {p['name'][:60]}")
        print(f"   Best price: {p['best_price']:,}đ (on {p['when_cheapest']})")
        print(f"   Current: {p['current_price']:,}đ")
        
        if p['current_price'] > p['best_price']:
            diff = p['current_price'] - p['best_price']
            percent = (diff / p['best_price']) * 100
            print(f"     Currently {diff:,}đ ({percent:.1f}%) more expensive")
        else:
            print(f"    At best price!")


if __name__ == "__main__":
    display_trends()
    display_best_times()