-- Use this file with the sales_analytics.db SQLite database.

-- 1. Monthly revenue and profit
SELECT strftime('%Y-%m', order_date) AS month,
       ROUND(SUM(net_sales),2) AS revenue,
       ROUND(SUM(profit),2) AS profit
FROM fact_sales
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month;

-- 2. Top 10 products by revenue
SELECT p.product_name, p.category,
       ROUND(SUM(f.net_sales),2) AS revenue
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY revenue DESC
LIMIT 10;

-- 3. Revenue by region
SELECT s.region,
       ROUND(SUM(f.net_sales),2) AS revenue,
       ROUND(SUM(f.profit),2) AS profit
FROM fact_sales f
JOIN dim_store s ON f.store_id = s.store_id
GROUP BY s.region
ORDER BY revenue DESC;

-- 4. Category performance
SELECT p.category,
       ROUND(SUM(f.net_sales),2) AS revenue,
       ROUND(SUM(f.profit),2) AS profit,
       ROUND(SUM(f.profit)/NULLIF(SUM(f.net_sales),0)*100,2) AS margin_pct
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;

-- 5. Customer ranking using a window function
WITH customer_sales AS (
    SELECT customer_id, SUM(net_sales) AS revenue
    FROM fact_sales
    GROUP BY customer_id
)
SELECT customer_id,
       ROUND(revenue,2) AS revenue,
       RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM customer_sales
ORDER BY revenue_rank
LIMIT 20;

-- 6. Monthly growth using LAG
WITH monthly AS (
    SELECT strftime('%Y-%m', order_date) AS month,
           SUM(net_sales) AS revenue
    FROM fact_sales
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT month,
       ROUND(revenue,2) AS revenue,
       ROUND((revenue - LAG(revenue) OVER (ORDER BY month))
             / NULLIF(LAG(revenue) OVER (ORDER BY month),0)*100,2) AS mom_growth_pct
FROM monthly
ORDER BY month;

-- 7. Inventory risk
SELECT stock_status,
       COUNT(*) AS sku_count,
       ROUND(SUM(inventory_value),2) AS inventory_value
FROM fact_inventory
GROUP BY stock_status
ORDER BY inventory_value DESC;

-- 8. Customer segment performance
SELECT c.segment,
       COUNT(DISTINCT f.customer_id) AS customers,
       ROUND(SUM(f.net_sales),2) AS revenue
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY c.segment
ORDER BY revenue DESC;
