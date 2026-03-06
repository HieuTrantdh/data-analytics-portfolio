"""
Best time to buy analysis.

Output groups:
- BUY NOW
- GOOD DEAL
- WAIT
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import get_db_connection
from psycopg2.extras import RealDictCursor


def fetch_price_position_data():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    p.name,
                    p.platform,
                    latest.price AS current_price,
                    stats.lowest_price,
                    stats.avg_price,
                    stats.highest_price,
                    stats.snapshots
                FROM products p
                JOIN latest_prices latest ON latest.product_id = p.id
                JOIN (
                    SELECT
                        product_id,
                        MIN(price) AS lowest_price,
                        MAX(price) AS highest_price,
                        AVG(price) AS avg_price,
                        COUNT(*) AS snapshots
                    FROM price_history
                    GROUP BY product_id
                ) stats ON stats.product_id = p.id
                WHERE p.is_active = TRUE
                ORDER BY p.name
                """
            )
            return cur.fetchall()


def classify_buy_timing(item):
    current_price = float(item["current_price"] or 0)
    lowest_price = float(item["lowest_price"] or 0)

    if current_price <= 0 or lowest_price <= 0:
        return "WAIT", 0.0

    premium_percent = ((current_price - lowest_price) / lowest_price) * 100

    if premium_percent <= 3:
        return "BUY NOW", premium_percent
    if premium_percent <= 10:
        return "GOOD DEAL", premium_percent
    return "WAIT", premium_percent


def main():
    rows = fetch_price_position_data()

    if not rows:
        print("No product data available")
        return

    groups = {"BUY NOW": [], "GOOD DEAL": [], "WAIT": []}

    for row in rows:
        group, premium_percent = classify_buy_timing(row)
        row["group"] = group
        row["premium_percent"] = premium_percent
        groups[group].append(row)

    print("\n" + "=" * 90)
    print("BEST TIME TO BUY")
    print("=" * 90)
    print(
        f"Summary -> BUY NOW: {len(groups['BUY NOW'])} | "
        f"GOOD DEAL: {len(groups['GOOD DEAL'])} | WAIT: {len(groups['WAIT'])}"
    )

    for group in ["BUY NOW", "GOOD DEAL", "WAIT"]:
        print("\n" + "-" * 90)
        print(f"{group} ({len(groups[group])})")
        print("-" * 90)

        if not groups[group]:
            print("No products in this group")
            continue

        sorted_items = sorted(groups[group], key=lambda item: item["premium_percent"])

        for item in sorted_items[:10]:
            current_price = float(item["current_price"] or 0)
            lowest_price = float(item["lowest_price"] or 0)
            diff = current_price - lowest_price
            sign = "+" if item["premium_percent"] >= 0 else ""

            print(f"• {item['name'][:65]} ({item['platform']})")
            print(
                f"  Current vs Lowest: {current_price:,.0f}đ vs {lowest_price:,.0f}đ"
            )
            print(
                f"  Difference: {diff:,.0f}đ ({sign}{item['premium_percent']:.2f}%) | "
                f"Snapshots: {item['snapshots']}"
            )


if __name__ == "__main__":
    main()
