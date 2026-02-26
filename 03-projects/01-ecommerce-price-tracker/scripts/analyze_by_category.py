"""
Analyze products by category
Find pricing patterns and insights
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import get_db_connection
from psycopg2.extras import RealDictCursor
import json


def analyze_categories():
    """
    Analyze products by category
    Requires category info in target-products.json
    """
    
    # Load product categories from target-products.json
    try:
        with open('data/target-products.json', 'r', encoding='utf-8') as f:
            products_config = json.load(f)
    except FileNotFoundError:
        print("❌ Error: data/target-products.json not found")
        return
    
    # Map product names to categories (fuzzy matching)
    category_map = {}
    for p in products_config:
        # Use product name or URL as key
        key = p.get('name', '').lower()
        category_map[key] = p.get('category', 'unknown')
    
    print("\n" + "="*80)
    print("📊 CATEGORY ANALYSIS")
    print("="*80)
    
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Get all products with latest prices
            cur.execute("""
                SELECT 
                    p.name,
                    ph.price,
                    ph.original_price,
                    ph.discount_percent,
                    ph.rating_average,
                    ph.review_count
                FROM products p
                JOIN (
                    SELECT DISTINCT ON (product_id)
                        product_id,
                        price,
                        original_price,
                        discount_percent,
                        rating_average,
                        review_count
                    FROM price_history
                    ORDER BY product_id, scraped_at DESC
                ) ph ON p.id = ph.product_id
                WHERE p.is_active = TRUE
            """)
            
            products_data = cur.fetchall()
    
    if not products_data:
        print("❌ No product data found")
        return
    
    # Group by category
    categories = {}
    for p in products_data:
        # Find category from map (fuzzy match)
        category = 'unknown'
        product_name_lower = p['name'].lower()
        
        for key, cat in category_map.items():
            if key in product_name_lower or product_name_lower in key:
                category = cat
                break
        
        if category not in categories:
            categories[category] = []
        
        categories[category].append(p)
    
    # Analyze each category
    for category, items in sorted(categories.items()):
        print(f"\n{'='*80}")
        print(f"📦 {category.upper().replace('_', ' ')}")
        print('='*80)
        
        if not items:
            print("No products in this category")
            continue
        
        # Calculate stats
        prices = [p['price'] for p in items if p['price']]
        discounts = [p['discount_percent'] for p in items if p['discount_percent'] and p['discount_percent'] > 0]
        ratings = [p['rating_average'] for p in items if p['rating_average'] and p['rating_average'] > 0]
        reviews = [p['review_count'] for p in items if p['review_count'] and p['review_count'] > 0]
        
        print(f"Products: {len(items)}")
        
        # Price stats
        if prices:
            print(f"\n💰 PRICE RANGE:")
            print(f"  Min:     {min(prices):>12,}đ")
            print(f"  Max:     {max(prices):>12,}đ")
            print(f"  Average: {sum(prices)/len(prices):>12,.0f}đ")
            print(f"  Median:  {sorted(prices)[len(prices)//2]:>12,}đ")
        
        # Discount stats
        if discounts:
            print(f"\n🔥 DISCOUNTS:")
            print(f"  Products on sale:  {len(discounts)}/{len(items)} ({len(discounts)/len(items)*100:.0f}%)")
            print(f"  Average discount:  {sum(discounts)/len(discounts):>12.1f}%")
            print(f"  Max discount:      {max(discounts):>12.1f}%")
            
            # Potential savings
            savings = sum(
                (p['original_price'] - p['price']) 
                for p in items 
                if p['original_price'] and p['price'] and p['original_price'] > p['price']
            )
            if savings > 0:
                print(f"  Total savings:     {savings:>12,}đ")
        else:
            print(f"\n🔥 DISCOUNTS:")
            print(f"  No active discounts in this category")
        
        # Rating stats
        if ratings:
            print(f"\n⭐ RATINGS:")
            print(f"  Products with ratings: {len(ratings)}/{len(items)} ({len(ratings)/len(items)*100:.0f}%)")
            print(f"  Average rating:        {sum(ratings)/len(ratings):>12.2f}/5.00")
            print(f"  Highest:               {max(ratings):>12.2f}/5.00")
            print(f"  Lowest:                {min(ratings):>12.2f}/5.00")
        
        # Review stats
        if reviews:
            print(f"\n💬 REVIEWS:")
            print(f"  Total reviews:     {sum(reviews):>12,}")
            print(f"  Average per product: {sum(reviews)/len(reviews):>10,.0f}")
            print(f"  Most reviewed:     {max(reviews):>12,}")
        
        # List products
        print(f"\n📋 PRODUCTS:")
        # Sort by price descending
        sorted_items = sorted(items, key=lambda x: x['price'] if x['price'] else 0, reverse=True)
        
        for i, p in enumerate(sorted_items, 1):
            print(f"\n  {i}. {p['name'][:60]}")
            
            # Price
            price_str = f"     💰 {p['price']:,}đ"
            if p['discount_percent'] and p['discount_percent'] > 0:
                price_str += f" (was {p['original_price']:,}đ, -{p['discount_percent']:.0f}%)"
            print(price_str)
            
            # Rating & reviews
            info_parts = []
            if p['rating_average'] and p['rating_average'] > 0:
                info_parts.append(f"⭐ {p['rating_average']:.1f}/5")
            if p['review_count'] and p['review_count'] > 0:
                info_parts.append(f"💬 {p['review_count']:,} reviews")
            
            if info_parts:
                print(f"     {' | '.join(info_parts)}")
    
    # Summary across all categories
    print(f"\n{'='*80}")
    print("📊 SUMMARY ACROSS ALL CATEGORIES")
    print('='*80)
    
    print(f"\nTotal categories: {len(categories)}")
    print(f"Total products:   {len(products_data)}")
    
    # Category with most products
    largest_cat = max(categories.items(), key=lambda x: len(x[1]))
    print(f"Largest category: {largest_cat[0]} ({len(largest_cat[1])} products)")
    
    # Category with highest avg price
    cat_avg_prices = {
        cat: sum(p['price'] for p in items if p['price']) / len([p for p in items if p['price']])
        for cat, items in categories.items()
        if any(p['price'] for p in items)
    }
    
    if cat_avg_prices:
        most_expensive_cat = max(cat_avg_prices.items(), key=lambda x: x[1])
        print(f"Most expensive category: {most_expensive_cat[0]} (avg {most_expensive_cat[1]:,.0f}đ)")
    
    # Category with most discounts
    cat_discount_rates = {
        cat: len([p for p in items if p['discount_percent'] and p['discount_percent'] > 0]) / len(items)
        for cat, items in categories.items()
    }
    
    if cat_discount_rates:
        most_discounted_cat = max(cat_discount_rates.items(), key=lambda x: x[1])
        print(f"Most discounted category: {most_discounted_cat[0]} ({most_discounted_cat[1]*100:.0f}% of products on sale)")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    analyze_categories()