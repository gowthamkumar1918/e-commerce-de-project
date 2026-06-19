SELECT 
    o.order_id,
    o.customer_id,
    c.name,
    c.city,
    c.state,
    p.product_name,
    p.category,
    o.quantity,
    p.price,
    o.quantity * p.price AS total_amount,
    o.order_date,
    o.status,
    EXTRACT(YEAR FROM o.order_date::date)  AS order_year,
    EXTRACT(MONTH FROM o.order_date::date) AS order_month
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p  ON o.product_id  = p.product_id
