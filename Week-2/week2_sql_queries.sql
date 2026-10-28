-- ========================================================
-- WEEK 2: SQL FOR DATA ANALYSIS ASSIGNMENT
-- Dataset: Retail Sales Dataset (200 Records)
-- ========================================================

-- 1. Filter High-Value Orders in the East Region
SELECT order_id, customer_name, category, total_price, region
FROM sales
WHERE total_price > 20000 AND region = 'East'
ORDER BY total_price DESC;

-- 2. Top Customers by Total Spend (Aggregations & GROUP BY)
SELECT 
    customer_name,
    COUNT(order_id) AS total_orders_placed,
    SUM(quantity) AS total_items_bought,
    ROUND(SUM(total_price), 2) AS total_spend
FROM sales
GROUP BY customer_name
ORDER BY total_spend DESC
LIMIT 10;

-- 3. Overall Average Order Value (AOV)
SELECT 
    COUNT(order_id) AS total_orders,
    ROUND(SUM(total_price), 2) AS total_revenue,
    ROUND(AVG(total_price), 2) AS overall_avg_order_value
FROM sales;

-- 4. Category-Wise Revenue and Average Order Value
SELECT 
    category,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(total_price), 2) AS category_revenue,
    ROUND(AVG(total_price), 2) AS category_avg_order_value
FROM sales
GROUP BY category
ORDER BY category_revenue DESC;

-- 5. Customer Segmentation Using CASE Statements
SELECT 
    customer_name,
    SUM(total_price) AS total_spent,
    CASE 
        WHEN SUM(total_price) >= 30000 THEN 'Platinum Tier'
        WHEN SUM(total_price) BETWEEN 15000 AND 29999 THEN 'Gold Tier'
        ELSE 'Silver Tier'
    END AS customer_segment
FROM sales
GROUP BY customer_name
ORDER BY total_spent DESC;

-- 6. Subquery: Orders Greater Than Overall Average
SELECT 
    order_id,
    customer_name,
    product_name,
    total_price
FROM sales
WHERE total_price > (SELECT AVG(total_price) FROM sales)
ORDER BY total_price DESC;

-- 7. INNER JOIN: Combine Sales with Regional Manager Dimension
SELECT 
    s.region,
    m.manager_name,
    COUNT(s.order_id) AS total_orders,
    ROUND(SUM(s.total_price), 2) AS regional_revenue
FROM sales s
INNER JOIN regional_managers m 
    ON s.region = m.region
GROUP BY s.region, m.manager_name
ORDER BY regional_revenue DESC;
