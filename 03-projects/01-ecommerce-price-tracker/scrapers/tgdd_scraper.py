import requests
import time
import random
import re
from datetime import datetime
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}


def extract_slug(url: str):
    return url.rstrip("/").split("/")[-1]


def clean_price(text: str) -> int:
    if not text:
        return 0
    numbers = re.sub(r"[^\d]", "", text)
    return int(numbers) if numbers else 0


def fetch_tgdd_product(url: str):
    time.sleep(random.uniform(1.5, 3))

    product_id = extract_slug(url)

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(" TGDD request error:", e)
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # ===== NAME =====
    name_tag = soup.select_one("h1")
    if not name_tag:
        print(" Cannot find name")
        return None

    name = name_tag.get_text(strip=True)

    # ===== PRICE =====
    price_tag = soup.select_one(".box-price-present")
    if not price_tag:
        price_tag = soup.select_one(".price")

    price_text = price_tag.get_text(strip=True) if price_tag else ""
    price = clean_price(price_text)

    return {
        "platform": "tgdd",
        "product_id": product_id,
        "name": name,
        "url": url,

        "price": price,
        "original_price": price,
        "discount_percent": 0,

        "rating_average": None,
        "review_count": 0,

        "seller_name": None,
        "stock_available": True,

        "scraped_at": datetime.utcnow().isoformat(),
    }