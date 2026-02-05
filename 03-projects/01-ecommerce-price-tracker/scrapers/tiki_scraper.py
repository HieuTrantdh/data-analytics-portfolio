import requests
import time
import random
import re
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}

def extract_product_id(url: str):
    m = re.search(r"-p(\d+)\.html", url)
    return m.group(1) if m else None


def fetch_tiki_product(url: str):
    time.sleep(random.uniform(1.5, 3))

    product_id = extract_product_id(url)
    if not product_id:
        print("❌ Cannot extract product_id")
        return None

    api_url = f"https://tiki.vn/api/v2/products/{product_id}"

    resp = requests.get(api_url, headers=HEADERS, timeout=10)
    if resp.status_code != 200:
        print("❌ API error", resp.status_code)
        return None

    data = resp.json()

    # -------------------------
    # SAFE EXTRACTIONS
    # -------------------------
    seller = data.get("seller")
    seller_name = seller.get("name") if isinstance(seller, dict) else None

    rating_average = data.get("rating_average")
    review_count = data.get("review_count")

    return {
        "platform": "tiki",
        "product_id": product_id,
        "name": data.get("name"),
        "url": url,

        "price": data.get("price"),
        "original_price": data.get("original_price"),
        "discount_percent": data.get("discount_rate"),

        "rating_average": rating_average if review_count and review_count > 0 else None,
        "review_count": review_count or 0,

        "seller_name": seller_name,
        "stock_available": data.get("quantity", 0) > 0,

        "scraped_at": datetime.utcnow().isoformat()
    }
