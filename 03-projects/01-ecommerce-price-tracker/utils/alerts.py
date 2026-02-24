"""
Price Alert System
Notifies when prices drop significantly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from datetime import datetime


class PriceAlert:
    """Handles price drop alerts"""

    # Alert thresholds
    SIGNIFICANT_DROP_PERCENT = -5
    MAJOR_DROP_PERCENT = -15

    @staticmethod
    def check_and_alert():
        """
        Check for price changes and send alerts
        """

        print("\n" + "=" * 70)
        print("PRICE ALERT CHECK")
        print("=" * 70)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Get price changes
        changes = DatabaseManager.get_price_changes()

        if not changes:
            print("No price changes detected (need at least 2 scrapes)")
            return []

        alerts = []

        for product in changes:
            percent_raw = product.get("percent_change")

            if percent_raw is None:
                continue

            try:
                percent = float(percent_raw)
            except (TypeError, ValueError):
                continue

            name = product.get("name", "Unknown")
            platform = product.get("platform", "unknown")
            old_price = product.get("previous_price", 0)
            new_price = product.get("current_price", 0)
            change = product.get("price_change", 0)

            # skip nếu không đổi giá
            if old_price == new_price:
                continue

            # check thực sự là giảm
            is_drop = new_price < old_price

            if is_drop and percent <= PriceAlert.SIGNIFICANT_DROP_PERCENT:

                alert_type = (
                    " MAJOR DROP"
                    if percent <= PriceAlert.MAJOR_DROP_PERCENT
                    else "--> Price Drop"
                )

                alert = {
                    "type": alert_type,
                    "product": name,
                    "old_price": old_price,
                    "new_price": new_price,
                    "savings": abs(change),
                    "percent": percent,
                    "platform": platform,
                }

                alerts.append(alert)

                # Pretty output
                print(alert_type)
                print(f"Product: {product['name'][:60]}")
                print(f"Platform: {product['platform'].upper()}")
                print(
                    f"Price: {product['previous_price']:,}đ → {product['current_price']:,}đ"
                )
                print(
                    f"Save: {abs(product['price_change']):,}đ ({percent:.2f}%)"
                )
                print("-" * 70)

        # Summary
        if alerts:
            print(f"\nFound {len(alerts)} price drop(s)")
        else:
            print("\nNo significant price drops detected")

        return alerts

    @staticmethod
    def send_email_alert(alerts):
        """
        Save alerts to file (email later)
        """

        if not alerts:
            return

        os.makedirs("data", exist_ok=True)

        with open("data/alerts.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{'='*70}\n")
            f.write(f"Alert Time: {datetime.now()}\n")
            f.write(f"{'='*70}\n\n")

            for alert in alerts:
                f.write(f"{alert['type']}\n")
                f.write(f"Product: {alert['product']}\n")
                f.write(
                    f"Price: {alert['old_price']:,}đ → {alert['new_price']:,}đ\n"
                )
                f.write(
                    f"Savings: {alert['savings']:,}đ ({alert['percent']:.2f}%)\n\n"
                )

        print("\nAlerts saved to data/alerts.txt")


if __name__ == "__main__":
    alerts = PriceAlert.check_and_alert()
    
    if alerts:
        PriceAlert.send_email_alert(alerts)