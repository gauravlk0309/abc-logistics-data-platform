# Sprint 1 Backlog: Data Ingestion & Staging Setup

**Sprint Goal:** Set up the PostgreSQL staging layer and build 11 specific Pentaho Data Integration pipelines to ingest heterogeneous data sources  with proper audit logging.

| Task ID | Task Description | Status |
| :--- | :--- | :--- |
| **ELDP-101** | Create staging schema and execute `create_staging_tables.sql` for all 11 source tables. | Done |
| **ELDP-102** | Develop ETL pipeline (`tms_shipments.ktr`) for `tms_shipments.csv` . | Done |
| **ELDP-103** | Develop ETL pipeline (`wms_inventory.ktr`) for `wms_inventory.xlsx`. | Done |
| **ELDP-104** | Develop ETL pipeline (`fleet_management.ktr`) for `fleet_management.json`. | Done |
| **ELDP-105** | Develop ETL pipeline (`gps_tracking.ktr`) for `gps_tracking.csv`. | Done |
| **ELDP-106** | Develop ETL pipeline (`oms_orders.ktr`) for `oms_orders.xml`. | Done |
| **ELDP-107** | Develop ETL pipeline (`inventory_movements.ktr`) for `inventory_movements.csv`. | Done |
| **ELDP-108** | Develop ETL pipeline (`vendor_portal.ktr`) for `vendor_portal.xlsx`. | Done |
| **ELDP-109** | Develop ETL pipeline (`shipment_tracking.ktr`) for `shipment_tracking.json`. | Done |
| **ELDP-110** | Develop ETL pipeline (`customer_feedback.ktr`) for `customer_feedback.csv`. | Done |
| **ELDP-111** | Develop ETL pipeline (`iot_sensors_data.ktr`) for `iot_sensor_data.json`. | Done |
| **ELDP-112** | Implement audit logging: ensure all transformations map `source_file` and `load_timestamp` fields to staging. | Done |
| **ELDP-113** | Commit all `.sql`, `.ktr`, and `.kjb` files to GitHub with meaningful commit messages. | Done |