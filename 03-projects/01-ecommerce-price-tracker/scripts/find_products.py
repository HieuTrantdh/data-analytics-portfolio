import os
import json
from scrapers.tiki_scraper import fetch_tiki_product


def find_products():
    path = os.path.abspath("data/target-products.json")
    print("DEBUG loading from:", path)

    with open(path, encoding="utf-8") as f:
        targets = json.load(f)

    tiki_targets = [i for i in targets if i.get("platform") == "tiki"]

    results = []

    print(f"🔎 Crawling {len(tiki_targets)} Tiki products...\n")

    for i, item in enumerate(tiki_targets, 1):
        url = item["url"]
        print(f"[{i}/{len(tiki_targets)}] {url}")

        product = fetch_tiki_product(url)

        if product:
            results.append(product)
            print(f"  ✅ {product['name'][:50]} - {product['price']:,}đ")
        else:
            print("  ❌ Failed")

        print()

    with open("data/tiki-products.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ Done! Saved {len(results)} products")


if __name__ == "__main__":
    find_products()
