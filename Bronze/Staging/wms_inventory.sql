CREATE TABLE wms_inventory (
    stock_record_id VARCHAR(30),
    warehouse_id VARCHAR(20),
    product_id VARCHAR(20),
    bin_location VARCHAR(30),
    quantity_on_hand INTEGER,
    unit_of_measure VARCHAR(20),
    reorder_level INTEGER,
    last_stock_count_date VARCHAR(30),
    aisle INTEGER,
    damaged_units INTEGER
);

SELECT * FROM wms_inventory