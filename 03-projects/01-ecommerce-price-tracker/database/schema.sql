-- ============================================
-- PRICE TRACKER DATABASE SCHEMA (FINAL CLEAN)
-- ============================================

-- ============================================
-- 1. PRODUCTS TABLE
-- ============================================
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,  -- Platform's product ID
    platform VARCHAR(20) NOT NULL,
    name VARCHAR(500) NOT NULL,
    url TEXT NOT NULL,

    -- Tracking metadata
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_scraped TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,

    -- Unique constraint
    CONSTRAINT products_product_platform_key UNIQUE (product_id, platform)
);

-- Indexes
CREATE INDEX idx_products_platform ON products(platform);
CREATE INDEX idx_products_active ON products(is_active);

-- ============================================
-- 2. PRICE HISTORY TABLE (Time-series data)
-- ============================================
CREATE TABLE price_history (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL
        REFERENCES products(id) ON DELETE CASCADE,

    -- Pricing data
    price DECIMAL(12, 2) NOT NULL,
    original_price DECIMAL(12, 2),
    discount_percent DECIMAL(5, 2),

    -- Product metrics at time of scrape
    rating_average DECIMAL(3, 2),
    review_count INTEGER,

    -- Timestamp
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_price_history_product
    ON price_history(product_id);

CREATE INDEX idx_price_history_scraped
    ON price_history(scraped_at DESC);

CREATE INDEX idx_price_history_product_date
    ON price_history(product_id, scraped_at DESC);

-- ============================================
-- VIEWS FOR COMMON QUERIES
-- ============================================

-- Latest price for each product
CREATE VIEW latest_prices AS
SELECT DISTINCT ON (p.id)
    p.id as product_id,
    p.name,
    p.platform,
    ph.price,
    ph.original_price,
    ph.discount_percent,
    ph.rating_average,
    ph.scraped_at
FROM products p
JOIN price_history ph ON p.id = ph.product_id
WHERE p.is_active = TRUE
ORDER BY p.id, ph.scraped_at DESC;

-- Price changes (compared to previous scrape)
CREATE VIEW price_changes AS
WITH current_prices AS (
    SELECT DISTINCT ON (product_id)
        product_id,
        price as current_price,
        scraped_at as current_scrape
    FROM price_history
    ORDER BY product_id, scraped_at DESC
),
previous_prices AS (
    SELECT DISTINCT ON (ph.product_id)
        ph.product_id,
        ph.price as previous_price,
        ph.scraped_at as previous_scrape
    FROM price_history ph
    JOIN current_prices cp ON ph.product_id = cp.product_id
    WHERE ph.scraped_at < cp.current_scrape
    ORDER BY ph.product_id, ph.scraped_at DESC
)
SELECT 
    p.name,
    p.platform,
    cp.current_price,
    pp.previous_price,
    cp.current_price - pp.previous_price AS price_change,
    ROUND(
        ((cp.current_price - pp.previous_price) / pp.previous_price * 100)::numeric,
        2
    ) AS percent_change,
    cp.current_scrape
FROM current_prices cp
JOIN previous_prices pp ON cp.product_id = pp.product_id
JOIN products p ON cp.product_id = p.id
WHERE cp.current_price != pp.previous_price;