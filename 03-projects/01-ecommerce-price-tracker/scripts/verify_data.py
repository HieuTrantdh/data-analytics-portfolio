"""
Data verification script
Schema V2 - Tiki product detail
"""

import json
import sys

REQUIRED_FIELDS = [
    "platform",
    "product_id",
    "name",
    "url",
    "price",
    "original_price",
    "discount_percent",
    "scraped_at"
]

def verify_tiki_data(json_file="data/tiki-products.json"):
    with open(json_file, encoding="utf-8") as f:
        products = json.load(f)

    print("\n" + "=" * 70)
    print("TIKI DATA QUALITY REPORT (SCHEMA V2)")
    print("=" * 70)

    valid = 0

    for i, p in enumerate(products, 1):
        print(f"{i}. {p.get('name', 'NO NAME')[:60]}")

        missing = [f for f in REQUIRED_FIELDS if p.get(f) is None]

        logic = []

        if not isinstance(p.get("price"), int) or p["price"] <= 0:
            logic.append("price invalid")

        if not isinstance(p.get("original_price"), int):
            logic.append("original_price invalid")

        if p.get("original_price", 0) < p.get("price", 0):
            logic.append("original_price < price")

        if not isinstance(p.get("discount_percent"), (int, float)):
            logic.append("discount_percent invalid")

        rating = p.get("rating_average")
        review_count = p.get("review_count", 0)

        if rating is not None:
            if not (0 <= rating <= 5):
                logic.append("rating out of range")
        else:
            if review_count > 0:
                logic.append("rating missing but review_count > 0")

        if missing or logic:
            print("   ⚠️ Issues:")
            if missing:
                print("     Missing:", missing)
            if logic:
                print("     Logic:", logic)
        else:
            valid += 1
            print("   ✅ Valid")

        print()

    print("=" * 70)
    print(f"Valid: {valid}/{len(products)} ({valid/len(products)*100:.1f}%)")


if __name__ == "__main__":
    verify_tiki_data(sys.argv[1] if len(sys.argv) > 1 else "data/tiki-products.json")
