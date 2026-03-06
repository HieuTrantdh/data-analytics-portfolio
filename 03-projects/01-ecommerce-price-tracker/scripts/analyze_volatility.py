"""
Price volatility analysis based on historical price movement.

Output groups:
- HIGH
- MEDIUM
- STABLE
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import get_db_connection
from psycopg2.extras import RealDictCursor


def fetch_volatility_data():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    p.name,
                    p.platform,
                    COUNT(ph.id) AS snapshots,
                    MIN(ph.price) AS min_price,
                    MAX(ph.price) AS max_price,
                    AVG(ph.price) AS avg_price,
                    STDDEV_POP(ph.price) AS std_dev
                FROM products p
                JOIN price_history ph ON ph.product_id = p.id
                WHERE p.is_active = TRUE
                GROUP BY p.id, p.name, p.platform
                HAVING COUNT(ph.id) >= 2
                ORDER BY p.name
                """
            )
            return cur.fetchall()


def classify_volatility(item):
    min_price = float(item["min_price"] or 0)
    max_price = float(item["max_price"] or 0)
    avg_price = float(item["avg_price"] or 0)
    std_dev = float(item["std_dev"] or 0)

    if avg_price <= 0:
        return "STABLE", 0.0, 0.0

    cv_percent = (std_dev / avg_price) * 100
    range_percent = ((max_price - min_price) / avg_price) * 100

    if cv_percent >= 12 or range_percent >= 25:
        return "HIGH", cv_percent, range_percent
    if cv_percent >= 6 or range_percent >= 10:
        return "MEDIUM", cv_percent, range_percent
    return "STABLE", cv_percent, range_percent


def main():
    rows = fetch_volatility_data()

    if not rows:
        print("No enough historical data. Need at least 2 snapshots per product.")
        return

    groups = {"HIGH": [], "MEDIUM": [], "STABLE": []}

    for row in rows:
        level, cv_percent, range_percent = classify_volatility(row)
        row["volatility_level"] = level
        row["cv_percent"] = cv_percent
        row["range_percent"] = range_percent
        groups[level].append(row)

    print("\n" + "=" * 90)
    print("PRICE VOLATILITY ANALYSIS")
    print("=" * 90)
    print(
        f"Summary -> HIGH: {len(groups['HIGH'])} | "
        f"MEDIUM: {len(groups['MEDIUM'])} | STABLE: {len(groups['STABLE'])}"
    )

    for level in ["HIGH", "MEDIUM", "STABLE"]:
        print("\n" + "-" * 90)
        print(f"{level} ({len(groups[level])})")
        print("-" * 90)

        if not groups[level]:
            print("No products in this group")
            continue

        sorted_items = sorted(
            groups[level],
            key=lambda item: item["cv_percent"],
            reverse=True,
        )

        for item in sorted_items[:10]:
            print(f"• {item['name'][:65]} ({item['platform']})")
            print(
                f"  Snapshots: {item['snapshots']} | "
                f"Price range: {float(item['min_price']):,.0f}đ - {float(item['max_price']):,.0f}đ"
            )
            print(
                f"  CV: {item['cv_percent']:.2f}% | "
                f"Range/Avg: {item['range_percent']:.2f}%"
            )


if __name__ == "__main__":
    main()
