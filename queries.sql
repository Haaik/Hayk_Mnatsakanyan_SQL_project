
-- 1. Total number of orders

SELECT COUNT(*) AS total_orders
FROM bookstore.orders;


-- 2. Revenue and order count by city
SELECT c.city, COUNT(o.order_id) AS orders_count,
    SUM(o.total_amount) AS total_revenue
FROM bookstore.orders o
JOIN bookstore.customers c
    ON o.customer_id = c.customer_id
GROUP BY c.city
ORDER BY total_revenue DESC;


-- 3. Top 10 customers by number of orders

SELECT customer_id, COUNT(*) AS orders_count
FROM bookstore.orders
GROUP BY customer_id
ORDER BY orders_count DESC
LIMIT 10;


-- 4. Customer ranking using window function

SELECT customer_id, COUNT(*) AS orders_count,
    RANK() OVER (ORDER BY COUNT(*) DESC) AS customer_rank
FROM bookstore.orders
GROUP BY customer_id
LIMIT 10;


-- 5. Monthly revenue trend

SELECT DATE_TRUNC('month', order_date) AS month, SUM(total_amount) AS revenue
FROM bookstore.orders
GROUP BY month
ORDER BY month;


-- 6. Best-selling categories

SELECT cat.name AS category, SUM(oi.quantity) AS total_units_sold
FROM bookstore.order_items oi
JOIN bookstore.products p
    ON oi.product_id = p.product_id
JOIN bookstore.categories cat
    ON p.category_id = cat.category_id
GROUP BY cat.name
ORDER BY total_units_sold DESC;


-- 7. Top 10 best-selling products

SELECT p.name AS product, SUM(oi.quantity) AS total_sold
FROM bookstore.order_items oi
JOIN bookstore.products p
    ON oi.product_id = p.product_id
GROUP BY p.name
ORDER BY total_sold DESC
LIMIT 10;


-- 8. Active products (HAVING clause)

SELECT p.name, SUM(oi.quantity) AS total_sold
FROM bookstore.order_items oi
JOIN bookstore.products p
    ON oi.product_id = p.product_id
GROUP BY p.name
HAVING SUM(oi.quantity) > 20
ORDER BY total_sold DESC;


-- 9. Customers with more than 5 orders (CTE example)

WITH customer_orders AS (
    SELECT customer_id, COUNT(*) AS orders_count
    FROM bookstore.orders
    GROUP BY customer_id
)
SELECT customer_id, orders_count
FROM customer_orders
WHERE orders_count > 5
ORDER BY orders_count DESC;


-- 10. Month-over-month revenue change (LAG window function)

WITH monthly_revenue AS (
    SELECT DATE_TRUNC('month', order_date) AS month,
    SUM(total_amount) AS revenue
    FROM bookstore.orders
    GROUP BY month
)
SELECT month, revenue,
    LAG(revenue) OVER (ORDER BY month) AS previous_month_revenue,
    revenue - LAG(revenue) OVER (ORDER BY month) AS revenue_change
FROM monthly_revenue
ORDER BY month;
