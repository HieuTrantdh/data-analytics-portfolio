# Day 08 – Scraper Robustness & Data Quality
Date: 03/02/2026  
Phase: Week 2 – Project 1 (E-commerce Price Tracker)

---

## Focus
Improve reliability of the Tiki scraper and ensure extracted data is safe for downstream storage and analysis.

---

## Work Done

### 1. Improved Tiki Scraper Robustness
Refactored JSON parsing logic to handle missing or inconsistent fields returned by Tiki API.

Key changes:
- Replaced direct dictionary access with `.get()` to avoid runtime errors
- Added type checks for nested objects (e.g. `seller`)
- Ensured scraper does not fail when optional fields are missing

Result:
- Scraper can run continuously without breaking on edge cases
- More stable data ingestion for daily automation

---

### 2. Standardized Extracted Data Fields
Reviewed and aligned output schema to support database storage and analysis.

Standardized fields include:
- product_id
- name
- price
- original_price
- discount_percent
- rating_average
- review_count
- seller_name
- url
- platform

Rationale:
- Stable schema simplifies PostgreSQL table design
- Reduces defensive checks in analysis code

---

### 3. Basic Data Verification
Added an initial data verification step to detect:
- Missing critical fields (e.g. price, product_id)
- Invalid values (price = 0, rating without reviews)

This serves as a foundation for future data quality checks in the ETL pipeline.

---

### 4. Version Control & Documentation
- Committed changes with clear, descriptive commit message
- Updated main README to reflect Week 2 progress
- Continued organizing daily learning logs consistently

---

## Key Takeaways
- Real-world scraped data is noisy and inconsistent
- Reliability is more important than scraping speed
- Data quality should be handled as early as possible in the pipeline
- Clean ingestion simplifies analysis and modeling later

---

## Next Steps
- Design PostgreSQL schema for price history tracking
- Define mandatory vs optional fields
- Integrate scraper output with database insertion logic
- Prepare for automated daily scraping
