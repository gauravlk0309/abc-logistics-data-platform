CREATE TABLE iot_sensor_data (
    sensor_reading_id VARCHAR(30),
    shipment_id VARCHAR(20),
    reading_timestamp VARCHAR(30),
    temperature_c NUMERIC(8,2),
    humidity_pct NUMERIC(8,2),
    shock_detected BOOLEAN,
    battery_pct NUMERIC(6,2),
    sensor_id VARCHAR(20)
);

SELECT * FROM iot_sensor_data