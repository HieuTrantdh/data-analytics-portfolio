"""
Database Manager
"""

import os
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from utils.validators import DataValidator


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
    """Context manager for database connections"""
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

    # =============================
    # TEST CONNECTION
    # =============================
    @staticmethod
    def test_connection():
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT version();")
                    version = cur.fetchone()[0]
                    print(" Connected to PostgreSQL")
                    print(f"Version: {version[:50]}...")
                    return True
        except Exception as e:
            print(f" Connection failed: {e}")
            return False

    # =============================
    # GET OR CREATE PRODUCT 
    # =============================
    @staticmethod
    def get_or_create_product(product_data):

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO products (
                        product_id,
                        platform,
                        name,
                        url,
                        last_scraped
                    )
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                    ON CONFLICT (product_id, platform)
                    DO UPDATE SET
                        name = EXCLUDED.name,
                        url = EXCLUDED.url,
                        last_scraped = CURRENT_TIMESTAMP
                    RETURNING id
                """, (
                    product_data['product_id'],
                    product_data['platform'],
                    product_data['name'],
                    product_data['url'],
                ))

                return cur.fetchone()[0]

    # =============================
    # SAVE PRICE DATA
    # =============================
    @staticmethod
    def save_price_data(product_data):
        """Save product price snapshot"""

        #  Validate
        is_valid, error_msg = DataValidator.validate_product(product_data)
        if not is_valid:
            print(f"⚠ Validation failed: {error_msg}")
            return None

        #  Clean
        product_data = DataValidator.clean_product_data(product_data)

        #  Get/Create product
        product_id = DatabaseManager.get_or_create_product(product_data)

        #  Insert price history (MATCH NEW SCHEMA)
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
                        scraped_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    product_id,
                    product_data['price'],
                    product_data.get('original_price'),
                    product_data.get('discount_percent'),
                    product_data.get('rating_average'),
                    product_data.get('review_count', 0),
                    product_data['scraped_at']
                ))

                history_id = cur.fetchone()[0]
                print(f"   Saved price: {product_data['price']:,}đ")
                return history_id

    # =============================
    # READ HELPERS
    # =============================
    @staticmethod
    def get_latest_prices():
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM latest_prices")
                return cur.fetchall()

    @staticmethod
    def get_price_changes():
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM price_changes")
                return cur.fetchall()

    @staticmethod
    def get_price_history(product_name, limit=30):
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


# =============================
# TEST
# =============================
if __name__ == "__main__":
    print(" Testing Database Connection...\n")

    if DatabaseManager.test_connection():
        print("\n Database is ready!")
    else:
        print("\n Please check your database configuration")