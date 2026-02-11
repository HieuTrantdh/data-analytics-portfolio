"""
Database Manager
Handles PostgreSQL connections and operations
"""

import os
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'price_tracker'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD', '')
}


@contextmanager
def get_db_connection():
    """
    Context manager for database connections
    Automatically handles connection closing
    """
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


class DatabaseManager:
    """Manages database operations for price tracker"""
    
    @staticmethod
    def test_connection():
        """Test database connection"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT version();")
                    version = cur.fetchone()[0]
                    print(f"✅ Connected to PostgreSQL")
                    print(f"Version: {version[:50]}...")
                    return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    @staticmethod
    def get_or_create_seller(seller_name, platform):
        """
        Get seller_id, create if doesn't exist
        
        Returns:
            int: seller_id
        """
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Try to get existing seller
                cur.execute("""
                    SELECT seller_id FROM sellers 
                    WHERE seller_name = %s AND platform = %s
                """, (seller_name, platform))
                
                result = cur.fetchone()
                
                if result:
                    return result[0]
                
                # Create new seller
                cur.execute("""
                    INSERT INTO sellers (seller_name, platform)
                    VALUES (%s, %s)
                    RETURNING seller_id
                """, (seller_name, platform))
                
                seller_id = cur.fetchone()[0]
                print(f"  📝 Created new seller: {seller_name}")
                return seller_id
    
    @staticmethod
    def get_or_create_product(product_data):
        """
        Get product ID, create if doesn't exist
        
        Args:
            product_data: dict with product info
            
        Returns:
            int: product database ID
        """
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                seller_name = product_data.get('seller_name') or 'Unknow Seller'

                seller_id = DatabaseManager.get_or_create_seller(
                    seller_name,
                    product_data['platform']
                )
                
                # Try to get existing product
                cur.execute("""
                    SELECT id FROM products
                    WHERE product_id = %s AND platform = %s
                """, (product_data['product_id'], product_data['platform']))
                
                result = cur.fetchone()
                
                if result:
                    # Update last_scraped
                    cur.execute("""
                        UPDATE products
                        SET last_scraped = CURRENT_TIMESTAMP
                        WHERE id = %s
                    """, (result[0],))
                    return result[0]
                
                # Create new product
                cur.execute("""
                    INSERT INTO products (
                        product_id, platform, name, url, seller_id
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    product_data['product_id'],
                    product_data['platform'],
                    product_data['name'],
                    product_data['url'],
                    seller_id
                ))
                
                product_id = cur.fetchone()[0]
                print(f"  📦 Created new product: {product_data['name'][:50]}")
                return product_id
    
    @staticmethod
    def save_price_data(product_data):
        """
        Save product price data to database
        
        Args:
            product_data: dict from Tiki scraper
            
        Returns:
            int: price_history ID
        """
        # Get product ID (create if new)
        product_id = DatabaseManager.get_or_create_product(product_data)
        
        # Insert price history
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO price_history (
                        product_id,
                        price,
                        original_price,
                        discount_percent,
                        rating_average,
                        review_count,
                        quantity_sold,
                        stock_available,
                        scraped_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    product_id,
                    product_data['price'],
                    product_data['original_price'],
                    product_data['discount_percent'],
                    product_data['rating_average'],
                    product_data['review_count'],
                    product_data.get('quantity_sold', 0),
                    product_data['stock_available'],
                    product_data['scraped_at']
                ))
                
                history_id = cur.fetchone()[0]
                print(f"  ✅ Saved price: {product_data['price']:,}đ")
                return history_id
    
    @staticmethod
    def get_latest_prices():
        """Get latest price for all products"""
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM latest_prices")
                return cur.fetchall()
    
    @staticmethod
    def get_price_changes():
        """Get products with price changes"""
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM price_changes")
                return cur.fetchall()
    
    @staticmethod
    def get_price_history(product_name, limit=30):
        """Get price history for a product"""
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        ph.price,
                        ph.discount_percent,
                        ph.scraped_at
                    FROM price_history ph
                    JOIN products p ON ph.product_id = p.id
                    WHERE p.name LIKE %s
                    ORDER BY ph.scraped_at DESC
                    LIMIT %s
                """, (f'%{product_name}%', limit))
                return cur.fetchall()


# Test function
if __name__ == "__main__":
    print("🧪 Testing Database Connection...\n")
    
    if DatabaseManager.test_connection():
        print("\n✅ Database is ready!")
    else:
        print("\n❌ Please check your database configuration")