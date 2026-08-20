CREATE TABLE tms_shipments (
    shipment_id VARCHAR(20),
    order_ref VARCHAR(20),
    warehouse_id VARCHAR(20),
    customer_id VARCHAR(20),
    vehicle_id VARCHAR(20),
    carrier VARCHAR(100),
    ship_date DATE,
    expected_delivery_date DATE,
    actual_delivery_date DATE,
    distance_km NUMERIC(10,2),
    weight_kg NUMERIC(10,2),
    freight_cost_usd NUMERIC(12,2),
    status VARCHAR(50),
    origin_city VARCHAR(100),
    destination_city VARCHAR(100)
);

Select * from tms_shipments