CREATE TABLE inventory_movements (
    movement_id VARCHAR(20),
    warehouse_id VARCHAR(20),
    product_id VARCHAR(20),
    movement_type VARCHAR(30),
    quantity INTEGER,
    movement_date DATE,
    reference_doc VARCHAR(30),
    handled_by VARCHAR(100)
);

SELECT * FROM inventory_movements 