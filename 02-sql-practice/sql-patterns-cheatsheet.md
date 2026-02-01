# SQL Patterns Cheatsheet - From 50 LeetCode Problems

## 1. Window Functions

### ROW_NUMBER - Assign unique sequential number
```sql
-- Use case: Get top N per group
SELECT *
FROM (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY sales DESC) as rn
    FROM products
) ranked
WHERE rn <= 5;


**### RANK vs DENSE_RANK**
-- RANK: 1,2,2,4 (skip 3)
-- DENSE_RANK: 1,2,2,3 (no skip)
SELECT 
    student_name,
    score,
    RANK() OVER (ORDER BY score DESC) as rank,
    DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank
FROM students;


### LAG/LEAD - Previous/Next row
-- Calculate MoM growth
SELECT 
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) as prev_month,
    revenue - LAG(revenue) OVER (ORDER BY month) as growth
FROM monthly_sales;


## 2. CTEs (Common Table Expressions)
### Basic CTE
WITH high_value_customers AS (
    SELECT customer_id, SUM(amount) as total
    FROM orders
    GROUP BY customer_id
    HAVING SUM(amount) > 1000
)
SELECT * FROM high_value_customers;

### Multiple CTEs
WITH 
    monthly_revenue AS (...),
    monthly_costs AS (...)
SELECT 
    r.month,
    r.revenue,
    c.costs,
    r.revenue - c.costs as profit
FROM monthly_revenue r
JOIN monthly_costs c ON r.month = c.month;

## 3. JOINs Patterns
### Find unmatched records
-- Customers who never ordered
SELECT c.*
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.customer_id IS NULL;

### Self JOIN
-- Employees earning more than their manager
SELECT e1.name as employee
FROM employees e1
JOIN employees e2 ON e1.manager_id = e2.id
WHERE e1.salary > e2.salary;


## 4. Date Functions
-- Extract parts
EXTRACT(YEAR FROM date_column)
EXTRACT(MONTH FROM date_column)
DATE_TRUNC('month', date_column)

-- Date arithmetic
date_column + INTERVAL '7 days'
DATEDIFF(end_date, start_date)

## 5. Analytical Patterns
### RFM Segmentation
WITH rfm AS (
    SELECT 
        customer_id,
        DATEDIFF(CURRENT_DATE, MAX(order_date)) as recency,
        COUNT(DISTINCT order_id) as frequency,
        SUM(amount) as monetary
    FROM orders
    GROUP BY customer_id
)
SELECT 
    customer_id,
    NTILE(5) OVER (ORDER BY recency DESC) as r_score,
    NTILE(5) OVER (ORDER BY frequency) as f_score,
    NTILE(5) OVER (ORDER BY monetary) as m_score
FROM rfm;

### Cohort Analysis
WITH first_purchase AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) as cohort_month
    FROM orders
    GROUP BY customer_id
)
SELECT 
    f.cohort_month,
    DATE_TRUNC('month', o.order_date) as order_month,
    COUNT(DISTINCT o.customer_id) as customers
FROM orders o
JOIN first_purchase f ON o.customer_id = f.customer_id
GROUP BY f.cohort_month, DATE_TRUNC('month', o.order_date);

