CREATE TABLE vendor_portal (
    po_id VARCHAR(20),
    supplier_id VARCHAR(20),
    product_id VARCHAR(20),
    destination_warehouse_id VARCHAR(20),
    po_date VARCHAR(30),
    quantity_ordered INTEGER,
    unit_cost NUMERIC(12,2),
    currency VARCHAR(10),
    acknowledged_date VARCHAR(30),
    expected_arrival_date VARCHAR(30),
    vendor_rating_at_po NUMERIC(4,2)
);

SELECT * FROM vendor_portal