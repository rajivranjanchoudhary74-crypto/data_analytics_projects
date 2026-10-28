import sqlite3
import pandas as pd

# -------------------------------------------------------------
# 1. CREATE SQL DATABASE & LOAD DATASET
# -------------------------------------------------------------
print("Setting up SQL database from sales_data.csv...")

# Connect to local SQLite database (creates sales.db file automatically)
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# Load CSV and write to SQL table named 'sales'
df = pd.read_csv("sales_data.csv")
df.to_sql("sales", conn, if_exists="replace", index=False)

# Create a second table for JOIN demonstration (Regional Managers)
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS regional_managers (
    region TEXT PRIMARY KEY,
    manager_name TEXT,
    support_email TEXT
)
"""
)

# Insert sample relational data
cursor.executemany(
    """
INSERT OR REPLACE INTO regional_managers VALUES (?, ?, ?)
""",
    [
        ("North", "Sarah Connor", "north_sales@company.com"),
        ("South", "James Miller", "south_sales@company.com"),
        ("East", "Elena Rostova", "east_sales@company.com"),
        ("West", "Marcus Vance", "west_sales@company.com"),
    ],
)
conn.commit()


# Helper function to print SQL results neatly
def run_query(title, query):
    print("\n" + "=" * 70)
    print(f"📌 {title.upper()}")
    print("=" * 70)
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))
    return result


# -------------------------------------------------------------
# 2. RUNNING PROJECT QUERIES (WEEK 2 TOPICS)
# -------------------------------------------------------------

# Query 1: Basic SELECT and WHERE
q1 = """
SELECT order_id, customer_name, category, total_price, region
FROM sales
WHERE total_price > 20000 AND region = 'East'
ORDER BY total_price DESC;
"""
run_query("1. High-Value Orders in East Region (SELECT, WHERE, ORDER BY)", q1)

# Query 2: Project Requirement - Top Customers by Total Spend
q2 = """
SELECT 
    customer_name,
    COUNT(order_id) AS total_orders_placed,
    SUM(quantity) AS total_items_bought,
    ROUND(SUM(total_price), 2) AS total_spend
FROM sales
GROUP BY customer_name
ORDER BY total_spend DESC
LIMIT 10;
"""
run_query("2. Top 10 Customers by Spend (Aggregations & GROUP BY)", q2)

# Query 3: Project Requirement - Average Order Value (AOV)
q3 = """
SELECT 
    COUNT(order_id) AS total_orders,
    ROUND(SUM(total_price), 2) AS total_revenue,
    ROUND(AVG(total_price), 2) AS overall_avg_order_value
FROM sales;
"""
run_query("3. Overall Average Order Value (AOV)", q3)

# Query 4: Category-Wise Breakdown & AOV
q4 = """
SELECT 
    category,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(total_price), 2) AS category_revenue,
    ROUND(AVG(total_price), 2) AS category_avg_order_value
FROM sales
GROUP BY category
ORDER BY category_revenue DESC;
"""
run_query("4. Category Performance & Average Order Value", q4)

# Query 5: CASE Statement - Customer Value Segmentation
q5 = """
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
ORDER BY total_spent DESC
LIMIT 15;
"""
run_query("5. Customer Segmentation Using CASE Statements", q5)

# Query 6: Subquery - Orders Greater Than Overall Average
q6 = """
SELECT 
    order_id,
    customer_name,
    product_name,
    total_price
FROM sales
WHERE total_price > (SELECT AVG(total_price) FROM sales)
ORDER BY total_price DESC
LIMIT 10;
"""
run_query(
    "6. Subquery: Orders Significantly Higher than Average Order Value", q6
)

# Query 7: Relational JOIN - Sales Table with Regional Managers Table
q7 = """
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
"""
run_query(
    "7. INNER JOIN: Sales Table Joined With Regional Managers Table", q7
)

# Close connection
conn.close()
print("\n✅ All SQL queries executed successfully!")