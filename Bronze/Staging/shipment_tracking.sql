CREATE TABLE shipment_tracking(
    tracking_event_id VARCHAR(30),
    shipment_id VARCHAR(20),
    event_type VARCHAR(50),
    event_timestamp DATE,
    location VARCHAR(150),
    scanned_by VARCHAR(100),
    remarks TEXT
);

ALTER TABLE shipment_tracking
ALTER COLUMN event_timestamp TYPE VARCHAR(30)

SELECT * FROM shipment_tracking