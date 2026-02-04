import requests
import time
import random
import re

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

    return {
        "platform": "tiki",
        "name": data.get("name"),
        "price": data.get("price", 0),
        "original_price": data.get("original_price"),
        "discount_rate": data.get("discount_rate"),
        "rating": data.get("rating_average"),
        "url": url,
    }
