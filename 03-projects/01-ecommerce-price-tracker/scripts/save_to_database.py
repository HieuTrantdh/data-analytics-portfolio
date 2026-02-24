"""
Save scraped products (Tiki) to PostgreSQL
"""

import json

from database.db_manager import DatabaseManager
from scrapers.tiki_scraper import fetch_tiki_product



# ==============================
# SCRAPER ROUTER
# ==============================
SCRAPER_MAP = {
    "tiki": fetch_tiki_product,
    
}


def save_products_to_db():
    """
    Read target products and save to database
    """

    # Load target products
    with open("data/target-products.json", "r", encoding="utf-8") as f:
        targets = json.load(f)

    print(f"Total targets: {len(targets)}\n")

    success_count = 0
    failed_count = 0

    for i, target in enumerate(targets, 1):
        platform = target.get("platform")
        url = target.get("url")

        print(f"[{i}/{len(targets)}] ({platform}) {url[:60]}...")

        # ==============================
        # CHOOSE SCRAPER
        # ==============================
        scraper = SCRAPER_MAP.get(platform)

        if not scraper:
            print(f" Unsupported platform: {platform}")
            failed_count += 1
            print()
            continue

        # ==============================
        # SCRAPE
        # ==============================
        product = scraper(url)

        if product:
            try:
                DatabaseManager.save_price_data(product)
                success_count += 1
            except Exception as e:
                print(f" Database error: {e}")
                failed_count += 1
        else:
            print(" Scraping failed")
            failed_count += 1

        print()

    # ==============================
    # SUMMARY
    # ==============================
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Saved to database: {success_count}/{len(targets)}")
    print(f"Failed: {failed_count}")

    # ==============================
    # SHOW LATEST
    # ==============================
    print("\n" + "=" * 70)
    print("LATEST PRICES IN DATABASE")
    print("=" * 70)

    latest = DatabaseManager.get_latest_prices()
    for p in latest:
        print(f"{p['name'][:50]}: {int(p['price']):,}đ (as of {p['scraped_at']})")


if __name__ == "__main__":
    save_products_to_db()