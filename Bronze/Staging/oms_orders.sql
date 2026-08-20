CREATE TABLE oms_orders (
    order_id VARCHAR(20),
    customer_id VARCHAR(20),
    product_id VARCHAR(20),
    quantity INTEGER,
    unit_price NUMERIC(12,2),
    order_date DATE,
    status VARCHAR(30),
    email VARCHAR(150),
    priority VARCHAR(30)
);

ALTER TABLE oms_orders
ALTER COLUMN order_date TYPE VARCHAR(20);

SELECT * FROM oms_orders