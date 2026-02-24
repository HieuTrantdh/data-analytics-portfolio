"""
Data Validation

"""

from datetime import datetime


class DataValidator:
    """Validates product data before saving"""

    @staticmethod
    def validate_product(product_data):
        """
        Validate product data structure and values

        Returns:
            (bool, str): (is_valid, error_message)
        """

        # REQUIRED FIELDS (UPDATED)
        required_fields = [
            'product_id',
            'platform',
            'name',
            'url',
            'price',
            'scraped_at'
        ]

        # Check required fields exist
        for field in required_fields:
            if field not in product_data:
                return False, f"Missing required field: {field}"

            if product_data[field] is None:
                return False, f"Field {field} is None"

        # =============================
        # PRICE VALIDATION
        # =============================
        try:
            price = float(product_data['price'])
            if price <= 0:
                return False, f"Invalid price: {price}"
            if price > 1_000_000_000:  # sanity check
                return False, f"Price too high: {price:,}đ"
        except (ValueError, TypeError):
            return False, f"Price is not a number: {product_data['price']}"

        # =============================
        # ORIGINAL PRICE
        # =============================
        if product_data.get('original_price'):
            try:
                original = float(product_data['original_price'])
                if original < price:
                    return False, (
                        f"Original price ({original}) < current price ({price})"
                    )
            except (ValueError, TypeError):
                return False, f"Original price invalid: {product_data['original_price']}"

        # =============================
        # DISCOUNT
        # =============================
        discount = product_data.get('discount_percent', 0)
        if discount is not None:
            try:
                discount = float(discount)
                if discount < 0 or discount > 100:
                    return False, f"Invalid discount: {discount}%"
            except (ValueError, TypeError):
                return False, f"Discount not a number: {discount}"

        # =============================
        # RATING
        # =============================
        rating = product_data.get('rating_average')
        if rating is not None:
            try:
                rating = float(rating)
                if rating < 0 or rating > 5:
                    return False, f"Rating out of range: {rating}"
            except (ValueError, TypeError):
                return False, f"Rating invalid: {rating}"

        # =============================
        # NAME LENGTH
        # =============================
        if len(product_data['name']) > 500:
            return False, "Product name too long (>500 chars)"

        return True, "Valid"

    # =================================
    # CLEAN DATA
    # =================================
    @staticmethod
    def clean_product_data(product_data):
        """Clean and normalize product data"""

        # Trim whitespace
        for key in ['name', 'url']:
            if key in product_data and isinstance(product_data[key], str):
                product_data[key] = product_data[key].strip()

        # Ensure scraped_at is datetime
        if isinstance(product_data.get('scraped_at'), str):
            product_data['scraped_at'] = datetime.fromisoformat(
                product_data['scraped_at']
            )

        # Default review_count
        if 'review_count' not in product_data:
            product_data['review_count'] = 0

        return product_data


# =============================
# TEST
# =============================
if __name__ == "__main__":
    valid_product = {
        'product_id': '123',
        'platform': 'tiki',
        'name': 'Test Product',
        'url': 'https://tiki.vn/test',
        'price': 100000,
        'original_price': 150000,
        'discount_percent': 33,
        'rating_average': 4.5,
        'scraped_at': datetime.now()
    }

    is_valid, msg = DataValidator.validate_product(valid_product)
    print(f"Valid product: {is_valid} - {msg}")