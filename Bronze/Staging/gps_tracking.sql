CREATE TABLE gps_tracking (
    gps_ping_id VARCHAR(20),
    vehicle_id VARCHAR(20),
    timestamp TIMESTAMP,
    latitude NUMERIC(10,6),
    longitude NUMERIC(10,6),
    speed_kmph NUMERIC(8,2),
    heading_deg NUMERIC(6,2),
    ignition_status VARCHAR(20),
    fuel_level_pct NUMERIC(5,2)
);

SELECT * FROM gps_tracking