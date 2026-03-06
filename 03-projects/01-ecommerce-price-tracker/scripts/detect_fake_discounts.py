"""
Detect fake discounts using advertised vs historical pricing signals.

Output groups:
- RED: likely fake discount
- YELLOW: suspicious discount
- GREEN: likely real discount
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import get_db_connection
from psycopg2.extras import RealDictCursor


def fetch_discount_signals():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    p.name,
                    p.platform,
                    latest.price AS current_price,
                    latest.original_price,
                    latest.discount_percent AS advertised_discount,
                    stats.min_price,
                    stats.max_price,
                    stats.avg_price,
                    stats.snapshots
                FROM products p
                JOIN latest_prices latest ON latest.product_id = p.id
                JOIN (
                    SELECT
                        product_id,
                        MIN(price) AS min_price,
                        MAX(price) AS max_price,
                        AVG(price) AS avg_price,
                        COUNT(*) AS snapshots
                    FROM price_history
                    GROUP BY product_id
                ) stats ON stats.product_id = p.id
                WHERE p.is_active = TRUE
                ORDER BY latest.discount_percent DESC NULLS LAST, p.name
                """
            )
            return cur.fetchall()


def classify_discount(item):
    current_price = float(item["current_price"] or 0)
    original_price = float(item["original_price"] or 0)
    advertised_discount = float(item["advertised_discount"] or 0)
    historical_avg = float(item["avg_price"] or 0)
    historical_max = float(item["max_price"] or 0)

    if current_price <= 0:
        return "RED", "invalid current price"

    # No advertised discount -> treat as healthy baseline
    if advertised_discount <= 0:
        return "GREEN", "no active advertised discount"

    real_discount_vs_avg = 0.0
    if historical_avg > 0:
        real_discount_vs_avg = ((historical_avg - current_price) / historical_avg) * 100

    gap = advertised_discount - real_discount_vs_avg
    inflated_original = historical_max > 0 and original_price > historical_max * 1.20

    if inflated_original or gap >= 20:
        return "RED", "discount gap too large vs history"
    if gap >= 10:
        return "YELLOW", "discount gap moderate vs history"
    return "GREEN", "discount is consistent with historical prices"


def main():
    rows = fetch_discount_signals()

    if not rows:
        print("No products found for discount analysis")
        return

    groups = {"RED": [], "YELLOW": [], "GREEN": []}

    for row in rows:
        status, reason = classify_discount(row)
        row["status"] = status
        row["reason"] = reason
        groups[status].append(row)

    print("\n" + "=" * 90)
    print("FAKE DISCOUNT DETECTOR")
    print("=" * 90)

    print(
        f"Summary -> RED: {len(groups['RED'])} | "
        f"YELLOW: {len(groups['YELLOW'])} | GREEN: {len(groups['GREEN'])}"
    )

    for level in ["RED", "YELLOW", "GREEN"]:
        print("\n" + "-" * 90)
        print(f"{level} ({len(groups[level])})")
        print("-" * 90)

        if not groups[level]:
            print("No products in this group")
            continue

        for item in groups[level][:10]:
            current_price = float(item["current_price"] or 0)
            original_price = float(item["original_price"] or 0)
            min_price = float(item["min_price"] or 0)
            max_price = float(item["max_price"] or 0)
            avg_price = float(item["avg_price"] or 0)
            advertised_discount = float(item["advertised_discount"] or 0)

            print(f" {item['name'][:65]}")
            print(
                f"  Current: {current_price:,.0f}đ | "
                f"Original: {original_price:,.0f}đ | "
                f"Ad: {advertised_discount:.1f}%"
            )
            print(
                f"  History: min {min_price:,.0f}đ / avg {avg_price:,.0f}đ / max {max_price:,.0f}đ"
            )
            print(f"  Reason: {item['reason']}")


if __name__ == "__main__":
    main()
