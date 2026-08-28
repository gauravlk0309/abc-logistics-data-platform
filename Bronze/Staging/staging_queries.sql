CREATE SCHEMA IF NOT EXISTS staging;

ALTER TABLE public.tms_shipments
SET SCHEMA staging;

ALTER TABLE public.wms_inventory
SET SCHEMA staging;

ALTER TABLE public.fleet_management
SET SCHEMA staging;

ALTER TABLE public.gps_tracking
SET SCHEMA staging;

ALTER TABLE public.oms_orders
SET SCHEMA staging;

ALTER TABLE public.inventory_movements
SET SCHEMA staging;

ALTER TABLE public.vendor_portal
SET SCHEMA staging;

ALTER TABLE public.shipment_tracking
SET SCHEMA staging;

ALTER TABLE public.customer_feedback
SET SCHEMA staging;

ALTER TABLE public.iot_sensor_data
SET SCHEMA staging;