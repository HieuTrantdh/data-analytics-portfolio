"""
Visualize price history over time.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import get_db_connection
from psycopg2.extras import RealDictCursor

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter


def format_vnd(value, _position):
    return f"{value:,.0f}"


def plot_price_history(product_name=None, limit=10):
    """
    Plot price history for products.

    Args:
        product_name: Specific product to plot (or None for top volatile).
        limit: Number of products to plot if product_name is None.
    """

    os.makedirs("data", exist_ok=True)

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if product_name:
                cur.execute(
                    """
                    SELECT
                        p.name,
                        ph.scraped_at,
                        ph.price,
                        ph.original_price
                    FROM price_history ph
                    JOIN products p ON ph.product_id = p.id
                    WHERE p.name ILIKE %s
                    ORDER BY ph.scraped_at ASC
                    """,
                    (f"%{product_name}%",),
                )

                history = cur.fetchall()

                if not history:
                    print(f" No history found for: {product_name}")
                    return

                fig, ax = plt.subplots(figsize=(12, 6))

                dates = [row["scraped_at"] for row in history]
                prices = [float(row["price"] or 0) for row in history]
                original_prices = [
                    float(row["original_price"] or row["price"] or 0)
                    for row in history
                ]

                ax.plot(
                    dates,
                    prices,
                    marker="o",
                    label="Current Price",
                    linewidth=2,
                )
                ax.plot(
                    dates,
                    original_prices,
                    marker="s",
                    label="Original Price",
                    linestyle="--",
                    alpha=0.7,
                )

                ax.set_xlabel("Date")
                ax.set_ylabel("Price (VND)")
                ax.set_title(f"Price History: {history[0]['name'][:60]}")
                ax.legend()
                ax.grid(True, alpha=0.3)
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
                plt.xticks(rotation=45)
                ax.yaxis.set_major_formatter(FuncFormatter(format_vnd))

                plt.tight_layout()

                safe_name = product_name[:30].replace(" ", "_").replace("/", "_")
                filename = f"data/price_history_{safe_name}.png"
                plt.savefig(filename, dpi=300, bbox_inches="tight")
                plt.close(fig)
                print(f" Saved: {filename}")
                return

            cur.execute(
                """
                SELECT
                    p.id,
                    p.name,
                    ((MAX(ph.price) - MIN(ph.price)) / NULLIF(MAX(ph.price), 0)) * 100 AS volatility
                FROM products p
                JOIN price_history ph ON p.id = ph.product_id
                GROUP BY p.id, p.name
                HAVING COUNT(ph.id) >= 2
                ORDER BY volatility DESC NULLS LAST
                LIMIT %s
                """,
                (limit,),
            )

            top_products = cur.fetchall()

            if not top_products:
                print(" Not enough data for plotting")
                return

            n_subplots = min(len(top_products), 4)
            fig, axes = plt.subplots(n_subplots, 1, figsize=(12, 3 * n_subplots))

            if n_subplots == 1:
                axes = [axes]

            for index, product in enumerate(top_products[:n_subplots]):
                cur.execute(
                    """
                    SELECT scraped_at, price
                    FROM price_history
                    WHERE product_id = %s
                    ORDER BY scraped_at ASC
                    """,
                    (product["id"],),
                )

                history = cur.fetchall()
                dates = [row["scraped_at"] for row in history]
                prices = [float(row["price"] or 0) for row in history]

                axes[index].plot(dates, prices, marker="o", linewidth=2)
                axes[index].set_title(
                    f"{product['name'][:50]} (Volatility: {float(product['volatility'] or 0):.1f}%)",
                    fontsize=10,
                )
                axes[index].set_ylabel("Price (VND)")
                axes[index].grid(True, alpha=0.3)
                axes[index].yaxis.set_major_formatter(FuncFormatter(format_vnd))
                axes[index].xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
                plt.setp(axes[index].xaxis.get_majorticklabels(), rotation=45, ha="right")

            plt.tight_layout()
            filename = "data/price_history_top_volatile.png"
            plt.savefig(filename, dpi=300, bbox_inches="tight")
            plt.close(fig)
            print(f" Saved: {filename}")


if __name__ == "__main__":
    print(" Generating price history charts...\n")

    plot_price_history(limit=4)

    choice = input("\nPlot specific product? (enter name or press Enter to skip): ").strip()
    if choice:
        plot_price_history(product_name=choice)

    print("\n Visualizations complete!")
