import os
import json
from scrapers.registry import SCRAPER_REGISTRY


def run():
    path = os.path.abspath("data/target-products.json")

    with open(path, encoding="utf-8") as f:
        targets = json.load(f)

    results = []

    print(f" Crawling {len(targets)} products...\n")

    for i, item in enumerate(targets, 1):
        platform = item.get("platform")
        url = item.get("url")

        print(f"[{i}/{len(targets)}] {platform} → {url}")

        scraper = SCRAPER_REGISTRY.get(platform)

        if not scraper:
            print(f"   No scraper for platform: {platform}")
            continue

        product = scraper(url)

        if product:
            results.append(product)
            print(f"   {product['name'][:50]}")
        else:
            print("   Failed")

        print()

    os.makedirs("data", exist_ok=True)

    with open("data/all-products.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f" Done! Saved {len(results)} products")


if __name__ == "__main__":
    run()