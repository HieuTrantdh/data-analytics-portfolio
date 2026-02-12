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
    SIGNIFICANT_DROP_PERCENT = -5  # Alert if price drops >5%
    MAJOR_DROP_PERCENT = -15       # Major alert if >15%
    
    @staticmethod
    def check_and_alert():
        """
        Check for price changes and send alerts
        """
        print("\n" + "="*70)
        print(" PRICE ALERT CHECK")
        print("="*70)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Get price changes
        changes = DatabaseManager.get_price_changes()
        
        if not changes:
            print(" No price changes detected (need at least 2 scrapes)")
            return []
        
        alerts = []
        
        for product in changes:
            percent = float(product['percent_change'])
            
            # Check if price dropped significantly
            if percent <= PriceAlert.SIGNIFICANT_DROP_PERCENT:
                alert_type = " MAJOR DROP" if percent <= PriceAlert.MAJOR_DROP_PERCENT else "📉 Price Drop"
                
                alert = {
                    'type': alert_type,
                    'product': product['name'],
                    'old_price': product['previous_price'],
                    'new_price': product['current_price'],
                    'savings': abs(product['price_change']),
                    'percent': percent,
                    'platform': product['platform']
                }
                
                alerts.append(alert)
                
                # Display alert
                print(f"{alert_type}")
                print(f"Product: {product['name'][:60]}")
                print(f"Platform: {product['platform'].upper()}")
                print(f"Price: {product['previous_price']:,}đ → {product['current_price']:,}đ")
                print(f" Save: {abs(product['price_change']):,}đ ({percent}%)")
                print(f" Action: Check product on {product['platform']}")
                print("-" * 70)
        
        # Summary
        if alerts:
            print(f"\n Found {len(alerts)} price drop(s)")
        else:
            print("\n No significant price drops detected")
        
        return alerts
    
    @staticmethod
    def send_email_alert(alerts):
        """
        Send email alerts (placeholder for future implementation)
        
        For now, just save to file
        """
        if not alerts:
            return
        
        # Save alerts to file
        with open('data/alerts.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*70}\n")
            f.write(f"Alert Time: {datetime.now()}\n")
            f.write(f"{'='*70}\n\n")
            
            for alert in alerts:
                f.write(f"{alert['type']}\n")
                f.write(f"Product: {alert['product']}\n")
                f.write(f"Price: {alert['old_price']:,}đ → {alert['new_price']:,}đ\n")
                f.write(f"Savings: {alert['savings']:,}đ ({alert['percent']}%)\n")
                f.write(f"\n")
        
        print(f"\n Alerts saved to data/alerts.txt")


if __name__ == "__main__":
    alerts = PriceAlert.check_and_alert()
    
    if alerts:
        PriceAlert.send_email_alert(alerts)