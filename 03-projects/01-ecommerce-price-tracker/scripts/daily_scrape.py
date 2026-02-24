"""
Daily Automated Scraper
- Scrapes all target products
- Saves to database
- Checks for price alerts
- Logs results
"""

import json
import os
from datetime import datetime

from database.db_manager import DatabaseManager
from scrapers.tiki_scraper import fetch_tiki_product
from utils.alerts import PriceAlert


# ==============================
# SCRAPER ROUTER
# ==============================
SCRAPER_MAP = {
    "tiki": fetch_tiki_product,
}


def log_scrape(message, level="INFO"):
    """Simple logging"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {level}: {message}\n"

    print(log_line.strip())

    with open("logs/scrape.log", "a", encoding="utf-8") as f:
        f.write(log_line)


def daily_scrape():
    """
    Main daily scraping function
    """

    print("\n" + "=" * 80)
    print(" AUTOMATED DAILY SCRAPE")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    log_scrape("=" * 50)
    log_scrape("Daily scrape started")

    # ==============================
    # LOAD TARGETS
    # ==============================
    try:
        with open("data/target-products.json", "r", encoding="utf-8") as f:
            targets = json.load(f)
    except FileNotFoundError:
        log_scrape("target-products.json not found", "ERROR")
        return

    log_scrape(f"Found {len(targets)} total products to scrape")

    stats = {
        "total": len(targets),
        "success": 0,
        "failed": 0,
        "errors": [],
    }

    # ==============================
    # SCRAPE LOOP
    # ==============================
    for i, target in enumerate(targets, 1):
        platform = target.get("platform")
        url = target.get("url")

        print(f"\n[{i}/{stats['total']}] ({platform}) Scraping...")
        log_scrape(f"Scraping [{i}/{stats['total']}] ({platform})")

        scraper = SCRAPER_MAP.get(platform)

        if not scraper:
            msg = f"Unsupported platform: {platform}"
            stats["failed"] += 1
            stats["errors"].append(msg)
            log_scrape(msg, "ERROR")
            continue

        try:
            product = scraper(url)

            if product:
                name = product["name"][:50]

                print(f"   → {name}")
                log_scrape(f"   Product: {name}")

                DatabaseManager.save_price_data(product)

                stats["success"] += 1
                log_scrape(f"   Success: {int(product['price']):,}đ")
            else:
                stats["failed"] += 1
                stats["errors"].append(f"{url}: Scraper returned None")
                log_scrape("   Failed: Scraper returned None", "ERROR")

        except Exception as e:
            stats["failed"] += 1
            error_msg = f"{url}: {str(e)}"
            stats["errors"].append(error_msg)
            log_scrape(f"   Error: {str(e)}", "ERROR")

    # ==============================
    # SUMMARY
    # ==============================
    print("\n" + "=" * 80)
    print("SCRAPING SUMMARY")
    print("=" * 80)
    print(f" Success: {stats['success']}/{stats['total']}")
    print(f" Failed: {stats['failed']}/{stats['total']}")

    log_scrape("=" * 50)
    log_scrape(
        f"Scraping complete: {stats['success']}/{stats['total']} success"
    )

    if stats["errors"]:
        print("\nErrors:")
        for error in stats["errors"]:
            print(f"  - {error}")
            log_scrape(f"Error detail: {error}", "ERROR")

    # ==============================
    # PRICE ALERTS
    # ==============================
    print("\n" + "=" * 80)
    log_scrape("Checking for price alerts...")

    alerts = PriceAlert.check_and_alert()

    if alerts:
        PriceAlert.send_email_alert(alerts)
        log_scrape(f"Found {len(alerts)} price alerts")
    else:
        log_scrape("No price alerts")

    print("=" * 80)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_scrape("Daily scrape finished")
    log_scrape("=" * 50 + "\n")


if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    daily_scrape()