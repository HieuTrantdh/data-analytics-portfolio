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

    try:
        resp = requests.get(api_url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print("❌ API error:", e)
        return None

    data = resp.json()

    # Debug 1 lần nếu cần
    # print("DEBUG keys:", data.keys())

    # -------------------------
    # SAFE EXTRACTIONS
    # -------------------------
    seller = data.get("seller") or {}
    seller_name = seller.get("name")

    price = data.get("price")
    original_price = data.get("original_price")

    review_count = data.get("review_count") or 0
    rating_average = data.get("rating_average")

    
    if review_count == 0:
        rating_average = None

   
    quantity = data.get("quantity") or 0
    stock_available = quantity > 0

    return {
        "platform": "tiki",
        "product_id": product_id,
        "name": data.get("name") or "Unknown Product",
        "url": url,

        "price": price or 0,
        "original_price": original_price or price or 0,
        "discount_percent": data.get("discount_rate") or 0,

        "rating_average": rating_average,
        "review_count": review_count,

        "seller_name": seller_name,
        "stock_available": stock_available,

        "scraped_at": datetime.utcnow().isoformat()
    }

