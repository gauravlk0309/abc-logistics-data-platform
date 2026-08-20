CREATE TABLE fleet_management(
    fleet_log_id VARCHAR(20),
    vehicle_id VARCHAR(20),
    driver_name VARCHAR(100),
    event_type VARCHAR(30),
    event_date DATE,
    odometer_km INTEGER,
    fuel_liters NUMERIC(10,2),
    maintenance_cost_usd NUMERIC(12,2),
    downtime_hours NUMERIC(8,2),
    notes TEXT
);

ALTER TABLE fleet_management
ALTER COLUMN event_date TYPE VARCHAR(30);

SELECT * FROM fleet_management