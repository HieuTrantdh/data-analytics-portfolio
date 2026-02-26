"""
Data Quality Report
Check completeness and accuracy of scraped data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import get_db_connection
from psycopg2.extras import RealDictCursor


def generate_quality_report():
    """Generate comprehensive data quality report"""
    
    print("\n" + "="*80)
    print("📊 DATA QUALITY REPORT")
    print("="*80)
    
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            
            # 1. Overall stats
            print("\n1. OVERALL STATISTICS")
            print("-" * 80)
            
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
            print(f"Total products:      {stats['total_products']}")
            print(f"Total price records: {stats['total_price_records']}")
            print(f"First scrape:        {stats['first_scrape']}")
            print(f"Last scrape:         {stats['last_scrape']}")
            
            # Average records per product
            if stats['total_products'] > 0:
                avg_records = stats['total_price_records'] / stats['total_products']
                print(f"Avg records/product: {avg_records:.1f}")
            
            # 2. Data completeness
            print("\n2. DATA COMPLETENESS")
            print("-" * 80)
            
            cur.execute("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN price > 0 THEN 1 END) as with_price,
                    COUNT(CASE WHEN original_price IS NOT NULL THEN 1 END) as with_original_price,
                    COUNT(CASE WHEN rating_average > 0 THEN 1 END) as with_rating,
                    COUNT(CASE WHEN review_count > 0 THEN 1 END) as with_reviews,
                    COUNT(CASE WHEN discount_percent > 0 THEN 1 END) as with_discount
                FROM latest_prices
            """)
            
            completeness = cur.fetchone()
            total = completeness['total']
            
            if total > 0:
                print(f"Price:             {completeness['with_price']}/{total} ({completeness['with_price']/total*100:.1f}%)")
                print(f"Original price:    {completeness['with_original_price']}/{total} ({completeness['with_original_price']/total*100:.1f}%)")
                print(f"Rating:            {completeness['with_rating']}/{total} ({completeness['with_rating']/total*100:.1f}%)")
                print(f"Reviews:           {completeness['with_reviews']}/{total} ({completeness['with_reviews']/total*100:.1f}%)")
                print(f"Active discounts:  {completeness['with_discount']}/{total} ({completeness['with_discount']/total*100:.1f}%)")
            else:
                print("⚠️  No data in latest_prices view")
            
            # 3. Price ranges
            print("\n3. PRICE DISTRIBUTION")
            print("-" * 80)
            
            cur.execute("""
                SELECT 
                    MIN(price) as min_price,
                    MAX(price) as max_price,
                    AVG(price) as avg_price,
                    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) as median_price
                FROM latest_prices
                WHERE price > 0
            """)
            
            prices = cur.fetchone()
            
            if prices['min_price']:
                print(f"Min price:     {prices['min_price']:>12,}đ")
                print(f"Max price:     {prices['max_price']:>12,}đ")
                print(f"Average:       {prices['avg_price']:>12,.0f}đ")
                print(f"Median:        {prices['median_price']:>12,.0f}đ")
            else:
                print("⚠️  No valid prices found")
            
            # 4. Discount analysis
            print("\n4. DISCOUNT ANALYSIS")
            print("-" * 80)
            
            cur.execute("""
                SELECT 
                    COUNT(*) as products_with_discount,
                    AVG(discount_percent) as avg_discount,
                    MAX(discount_percent) as max_discount,
                    MIN(discount_percent) as min_discount
                FROM latest_prices
                WHERE discount_percent > 0
            """)
            
            discounts = cur.fetchone()
            
            if discounts['products_with_discount'] and discounts['products_with_discount'] > 0:
                print(f"Products on sale:    {discounts['products_with_discount']}/{total}")
                print(f"Average discount:    {discounts['avg_discount']:.1f}%")
                print(f"Max discount:        {discounts['max_discount']:.1f}%")
                print(f"Min discount:        {discounts['min_discount']:.1f}%")
            else:
                print("ℹ️  No products currently on discount")
            
            # 5. Products with highest discounts
            print("\n5. TOP 5 DISCOUNTS")
            print("-" * 80)
            
            cur.execute("""
                SELECT 
                    name,
                    price,
                    original_price,
                    discount_percent
                FROM latest_prices
                WHERE discount_percent > 0
                ORDER BY discount_percent DESC
                LIMIT 5
            """)
            
            top_discounts = cur.fetchall()
            
            if top_discounts:
                for i, p in enumerate(top_discounts, 1):
                    print(f"{i}. {p['name'][:55]}")
                    print(f"   {p['original_price']:,}đ → {p['price']:,}đ (-{p['discount_percent']:.1f}%)")
            else:
                print("ℹ️  No discounts found")
            
            # 6. Rating distribution
            print("\n6. RATING DISTRIBUTION")
            print("-" * 80)
            
            cur.execute("""
                SELECT 
                    COUNT(*) as total_with_ratings,
                    AVG(rating_average) as avg_rating,
                    MIN(rating_average) as min_rating,
                    MAX(rating_average) as max_rating
                FROM latest_prices
                WHERE rating_average > 0
            """)
            
            ratings = cur.fetchone()
            
            if ratings['total_with_ratings'] and ratings['total_with_ratings'] > 0:
                print(f"Products with ratings: {ratings['total_with_ratings']}/{total}")
                print(f"Average rating:        {ratings['avg_rating']:.2f}/5.00")
                print(f"Lowest rating:         {ratings['min_rating']:.2f}/5.00")
                print(f"Highest rating:        {ratings['max_rating']:.2f}/5.00")
            else:
                print("ℹ️  No ratings data available")
            
            # 7. Review volume
            print("\n7. REVIEW VOLUME")
            print("-" * 80)
            
            cur.execute("""
                SELECT 
                    COUNT(*) as products_with_reviews,
                    SUM(review_count) as total_reviews,
                    AVG(review_count) as avg_reviews,
                    MAX(review_count) as max_reviews
                FROM latest_prices
                WHERE review_count > 0
            """)
            
            reviews = cur.fetchone()
            
            if reviews['products_with_reviews'] and reviews['products_with_reviews'] > 0:
                print(f"Products with reviews: {reviews['products_with_reviews']}/{total}")
                print(f"Total reviews:         {reviews['total_reviews']:,}")
                print(f"Average per product:   {reviews['avg_reviews']:,.0f}")
                print(f"Most reviewed:         {reviews['max_reviews']:,} reviews")
            else:
                print("ℹ️  No review data available")
            
            # 8. Data quality issues
            print("\n8. POTENTIAL ISSUES")
            print("-" * 80)
            
            issues = []
            
            # Check for missing prices
            cur.execute("SELECT COUNT(*) as count FROM latest_prices WHERE price = 0 OR price IS NULL")
            missing_prices = cur.fetchone()['count']
            if missing_prices > 0:
                issues.append(f"❌ {missing_prices} products with missing/zero price")
            
            # Check for suspicious discounts (>50%)
            cur.execute("SELECT COUNT(*) as count FROM latest_prices WHERE discount_percent > 50")
            high_discounts = cur.fetchone()['count']
            if high_discounts > 0:
                issues.append(f"⚠️  {high_discounts} products with >50% discount (verify if legitimate)")
            
            # Check for suspiciously high discounts (>70%)
            cur.execute("SELECT COUNT(*) as count FROM latest_prices WHERE discount_percent > 70")
            very_high_discounts = cur.fetchone()['count']
            if very_high_discounts > 0:
                issues.append(f"🚨 {very_high_discounts} products with >70% discount (likely fake)")
            
            # Check for products with no ratings
            cur.execute("SELECT COUNT(*) as count FROM latest_prices WHERE rating_average = 0 OR rating_average IS NULL")
            no_ratings = cur.fetchone()['count']
            if no_ratings > 0:
                issues.append(f"ℹ️  {no_ratings} products with no ratings (might be new products)")
            
            # Check for invalid rating values
            cur.execute("SELECT COUNT(*) as count FROM latest_prices WHERE rating_average > 5")
            invalid_ratings = cur.fetchone()['count']
            if invalid_ratings > 0:
                issues.append(f"❌ {invalid_ratings} products with invalid rating (>5)")
            
            # Check for negative prices
            cur.execute("SELECT COUNT(*) as count FROM latest_prices WHERE price < 0")
            negative_prices = cur.fetchone()['count']
            if negative_prices > 0:
                issues.append(f"❌ {negative_prices} products with negative price (data error)")
            
            if issues:
                for issue in issues:
                    print(issue)
            else:
                print("✅ No major issues detected")
            
            # 9. Scraping frequency check
            print("\n9. SCRAPING FREQUENCY")
            print("-" * 80)
            
            cur.execute("""
                SELECT 
                    p.name,
                    MAX(ph.scraped_at) as last_scraped,
                    COUNT(ph.id) as scrape_count
                FROM products p
                LEFT JOIN price_history ph ON p.id = ph.product_id
                GROUP BY p.id, p.name
                HAVING MAX(ph.scraped_at) < NOW() - INTERVAL '48 hours'
                   OR MAX(ph.scraped_at) IS NULL
                ORDER BY last_scraped NULLS FIRST
            """)
            
            stale_products = cur.fetchall()
            
            if stale_products:
                print(f"⚠️  {len(stale_products)} products not scraped in 48+ hours:")
                for p in stale_products[:5]:  # Show first 5
                    if p['last_scraped']:
                        print(f"   • {p['name'][:50]} (last: {p['last_scraped']})")
                    else:
                        print(f"   • {p['name'][:50]} (never scraped)")
            else:
                print("✅ All products scraped within 48 hours")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    generate_quality_report()