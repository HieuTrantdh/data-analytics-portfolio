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

---

### **RANK vs DENSE_RANK**
-- RANK: 1,2,2,4 (skip 3)
-- DENSE_RANK: 1,2,2,3 (no skip)
```sql
SELECT 
    student_name,
    score,
    RANK() OVER (ORDER BY score DESC) as rank,
    DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank
FROM students;
