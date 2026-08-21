# Data Dictionary

## Enterprise Logistics Data Platform (ELDP) — ABC Logistics Ltd.

| | |
|---|---|
| **Document Type** | Data Dictionary |
| **Project** | Enterprise Logistics Data Platform (ELDP) |
| **Sprint** | Sprint 1 — Data Discovery & Ingestion |
| **Version** | 1.0 |
| **Repository** | [abc-logistics-data-platform](https://github.com/gauravlk0309/abc-logistics-data-platform) |
| **Layer** | Bronze (staging) — reflects source data structure as ingested |

---

## How to read this document

Each source system below is documented with:
- **Field** — column name as it appears in the source file
- **Data Type** — recommended staging data type in PostgreSQL
- **Description** — business meaning of the field
- **Sample Value** — a representative value
- **Nullable** — whether the field can be blank/missing
- **Key** — PK (Primary Key), FK (Foreign Key, with reference), or blank
- **Known Data Quality Notes** — issues to expect during Sprint 2 profiling

Staging table names use the prefix `stg_`. All staging tables additionally carry two audit columns not listed per-table below:

| Field | Data Type | Description |
|---|---|---|
| `load_timestamp` | TIMESTAMP | Date/time the record was loaded into staging by Pentaho |
| `source_file` | TEXT | Name of the source file/system the record was ingested from |

---

## 1. Master / Reference Data

### 1.1 Customers — `master_customers.csv` → `stg_customers`

| Field | Data Type | Description | Sample Value | Nullable | Key |
|---|---|---|---|---|---|
| customer_id | VARCHAR(10) | Unique customer identifier | CUST00271 | No | PK |
| customer_name | TEXT | Customer or company name | Hernandez LLC | No | |
| email | TEXT | Customer contact email | jeremy54@hernandez.info | No | |
| phone | TEXT | Customer contact phone number | 555-014-2231 | No | |
| city | TEXT | Customer city | Chicago | No | |
| state | TEXT | Customer state/province | IL | No | |
| country | TEXT | Customer country | USA | No | |
| region | TEXT | Business region grouping | North | No | |
| customer_since | DATE | Date customer relationship began | 2022-03-15 | No | |
| customer_type | TEXT | Customer segment | Retail, Wholesale, Enterprise, E-commerce | No | |

### 1.2 Warehouses — `master_warehouses.csv` → `stg_warehouses`

| Field | Data Type | Description | Sample Value | Nullable | Key |
|---|---|---|---|---|---|
| warehouse_id | VARCHAR(10) | Unique warehouse identifier | WH005 | No | PK |
| warehouse_name | TEXT | Warehouse/distribution center name | Rotterdam Distribution Center 5 | No | |
| city | TEXT | Warehouse city | Rotterdam | No | |
| state | TEXT | Warehouse state/province | ZH | No | |
| country | TEXT | Warehouse country | Netherlands | No | |
| region | TEXT | Business region grouping | Central | No | |
| latitude | DECIMAL(9,6) | Warehouse latitude | 51.924420 | No | |
| longitude | DECIMAL(9,6) | Warehouse longitude | 4.477730 | No | |
| capacity_sqft | INTEGER | Total warehouse floor capacity | 275000 | No | |
| manager_name | TEXT | Warehouse manager name | Sarah Collins | No | |
| operational_since | DATE | Date warehouse became operational | 2018-06-01 | No | |

### 1.3 Vehicles — `master_vehicles.csv` → `stg_vehicles`

| Field | Data Type | Description | Sample Value | Nullable | Key |
|---|---|---|---|---|---|
| vehicle_id | VARCHAR(10) | Unique vehicle identifier | VEH0021 | No | PK |
| vehicle_type | TEXT | Type/class of vehicle | Truck-Large, Van, Trailer, Refrigerated Truck | No | |
| registration_number | TEXT | Vehicle registration/license plate | AB-1234-CD | No | |
| fuel_type | TEXT | Fuel type | Diesel, Petrol, Electric, CNG | No | |
| capacity_kg | INTEGER | Maximum load capacity in kg | 10000 | No | |
| manufacture_year | INTEGER | Year vehicle was manufactured | 2020 | No | |
| home_warehouse_id | VARCHAR(10) | Warehouse the vehicle is based at | WH012 | No | FK → stg_warehouses.warehouse_id |
| driver_name | TEXT | Assigned driver name | Michael Torres | No | |
| driver_license_no | TEXT | Driver's license number | DL-88213045 | No | |
| status | TEXT | Current vehicle status | Active, In Maintenance, Idle | No | |

### 1.4 Suppliers — `master_suppliers.csv` → `stg_suppliers`

| Field | Data Type | Description | Sample Value | Nullable | Key |
|---|---|---|---|---|---|
| supplier_id | VARCHAR(10) | Unique supplier identifier | SUP0014 | No | PK |
| supplier_name | TEXT | Supplier company name | Global Textiles Inc. | No | |
| contact_person | TEXT | Supplier point of contact | Angela Martinez | No | |
| email | TEXT | Supplier contact email | contact@globaltextiles.com | No | |
| phone | TEXT | Supplier contact phone | 555-902-1187 | No | |
| city | TEXT | Supplier city | Mumbai | No | |
| country | TEXT | Supplier country | India | No | |
| category | TEXT | Supplier product category | Raw Material, Packaging, Electronics, Textiles, FMCG, Automotive Parts | No | |
| onboarded_date | DATE | Date supplier relationship began | 2019-11-20 | No | |
| rating | DECIMAL(2,1) | Supplier performance rating (1.0–5.0) | 4.2 | No | |

### 1.5 Products — `master_products.csv` → `stg_products`

| Field | Data Type | Description | Sample Value | Nullable | Key |
|---|---|---|---|---|---|
| product_id | VARCHAR(10) | Unique product identifier | PRD00028 | No | PK |
| product_name | TEXT | Product name/description | Synergistic Bandwidth Array | No | |
| category | TEXT | Product category | Electronics, Apparel, Grocery, Furniture, Automotive, Pharma, Toys, Industrial | No | |
| unit_weight_kg | DECIMAL(6,2) | Weight per unit | 12.45 | No | |
| unit_price | DECIMAL(8,2) | Price per unit (USD) | 1446.25 | No | |
| supplier_id | VARCHAR(10) | Supplier of this product | SUP0014 | No | FK → stg_suppliers.supplier_id |

---

## 2. Operational Source Systems

### 2.1 Transportation Management System (TMS) — `tms_shipments.csv` → `stg_shipments`

| Field | Data Type | Description | Sample Value | Nullable | Key |
|---|---|---|---|---|---|
| shipment_id | VARCHAR(10) | Unique shipment identifier | SHP001411 | No | PK |
| order_ref | VARCHAR(10) | Related order reference | ORD000415 | No | FK → stg_orders.order_id |
| warehouse_id | VARCHAR(10) | Originating warehouse | WH012 | No | FK → stg_warehouses.warehouse_id |
| customer_id | VARCHAR(10) | Receiving customer | CUST00361 | No | FK → stg_customers.customer_id |
| vehicle_id | VARCHAR(10) | Vehicle used for delivery | VEH0021 | No | FK → stg_vehicles.vehicle_id |
| carrier | TEXT | Carrier/shipping company | FedEx, DHL, In-house Fleet | No | |
| ship_date | DATE | Date shipment left the warehouse | 2026-02-24 | No | |
| expected_delivery_date | DATE | Planned delivery date | 2026-02-28 | No | |
| actual_delivery_date | DATE | Actual delivery date | 2026-02-28 | **Yes** — blank if still in transit (~10%) | |
| distance_km | DECIMAL(8,1) | Distance traveled in km | 1965.2 | No | Data quality: ~2% negative values |
| weight_kg | DECIMAL(8,1) | Total shipment weight | 2449.2 | No | |
| freight_cost_usd | DECIMAL(10,2) | Freight cost in USD | 757.56 | No | |
| status | TEXT | Shipment status | In Transit, Delivered, Delayed, Cancelled | No | |
| origin_city | TEXT | City of origin | Hamburg | No | |
| destination_city | TEXT | Delivery destination city | Jamesborough | No | |

**Known data quality notes:** ~1.5% duplicate shipment_id rows; warehouse_id occasionally lowercase (e.g. `wh007`); ~2% negative distance_km values.

### 2.2 Warehouse Management System (WMS) — `wms_inventory.xlsx` → `stg_inventory`

| Field | Data Type | Description | Sample Value | Nullable | Key |
|---|---|---|---|---|---|
| stock_record_id | VARCHAR(10) | Unique stock record identifier | WMS000452 | No | PK |
| warehouse_id | VARCHAR(10) | Warehouse holding the stock | WH005 | No | FK → stg_warehouses.warehouse_id |
| product_id | VARCHAR(10) | Product being stocked | PRD00076 | No | FK → stg_products.product_id |
| bin_location | TEXT | Physical bin/shelf location | C-14-3 | **Yes** — ~6% missing | |
| quantity_on_hand | INTEGER | Current stock quantity | 2450 | No | Data quality: some negative values (entry errors) |
| unit_of_measure | TEXT | Unit of measure | EA, ea, Each, BOX, PCS, KG | No | Inconsistent casing/format |
| reorder_level | INTEGER | Minimum stock threshold before reorder | 150 | No | |
| last_stock_count_date | DATE | Date of last physical stock count | 2026-06-10 | No | |
| aisle | INTEGER | Warehouse aisle number | 14 | No | |
| damaged_units | INTEGER | Units marked as damaged | 2 | No | |

### 2.3 Fleet Management System — `fleet_management.json` → `stg_fleet`

| Field | Data Type | Description | Sample Value | Nullable | Key |
|---|---|---|---|---|---|
| fleet_log_id | VARCHAR(10) | Unique fleet log entry identifier | FLT000512 | No | PK |
| vehicle_id | VARCHAR(10) | Vehicle associated with the log entry | VEH0053 | No | FK → stg_vehicles.vehicle_id |
| driver_name | TEXT | Driver on record | Michael Torres | No | |
| event_type | TEXT | Type of fleet event | Trip, Maintenance, Refuel, Inspection, Breakdown | No | |
| event_date | DATE | Date of the event | 2026-05-02 | No | |
| odometer_km | INTEGER | Odometer reading at event time | 154200 | **Yes** — ~5% missing | |
| fuel_liters | DECIMAL(6,1) | Fuel volume (Trip/Refuel events only) | 85.4 | Yes — null for non-fuel events | Data quality: ~3% negative values |
| maintenance_cost_usd | DECIMAL(8,2) | Maintenance cost (Maintenance events only) | 620.00 | Yes — null unless event_type = Maintenance | |
| downtime_hours | DECIMAL(5,1) | Vehicle downtime (Maintenance/Breakdown) | 6.5 | No — 0 if not applicable | |
| notes | TEXT | Free-text notes | "Brake pads replaced" | Yes — often blank | |

### 2.4 GPS Vehicle Tracking — `gps_tracking.csv` → `stg_gps`

| Field | Data Type | Description | Sample Value | Nullable | Key |
|---|---|---|---|---|---|
| gps_ping_id | VARCHAR(10) | Unique GPS ping identifier | GPS0004521 | No | PK |
| vehicle_id | VARCHAR(10) | Vehicle transmitting the ping | VEH0059 | No | FK → stg_vehicles.vehicle_id |
| timestamp | TIMESTAMP | Date/time of the GPS ping | 2026-06-12 14:32:05 | No | |
| latitude | DECIMAL(9,6) | GPS latitude | 41.878114 | No | Data quality: ~3% out-of-range (>90°) |
| longitude | DECIMAL(9,6) | GPS longitude | -87.629798 | No | |
| speed_kmph | DECIMAL(5,1) | Vehicle speed at time of ping | 62.3 | **Yes** — ~2% missing | |
| heading_deg | INTEGER | Direction of travel (0–359°) | 187 | No | |
| ignition_status | TEXT | Ignition on/off | ON, OFF | No | |
| fuel_level_pct | DECIMAL(4,1) | Fuel level percentage | 74.5 | No | |

**Known data quality notes:** ~1.5% duplicate ping records; highest-volume dataset (2,500+ records), useful for illustrating deduplication logic in Sprint 2.

### 2.5 Order Management System (OMS) — `oms_orders.xml` → `stg_orders`

| Field | Data Type | Description | Sample Value | Nullable | Key |
|---|---|---|---|---|---|
| order_id | VARCHAR(10) | Unique order identifier | ORD000415 | No | PK |
| customer_id | VARCHAR(10) | Customer placing the order | CUST00271 | No | FK → stg_customers.customer_id |
| product_id | VARCHAR(10) | Product ordered | PRD00028 | No | FK → stg_products.product_id |
| quantity | INTEGER | Quantity ordered | 7 | No | |
| unit_price | DECIMAL(8,2) | Unit price at time of order | 1446.25 | No | |
| order_date | TEXT (raw) | Date order was placed | 08/16/2026 (mixed formats) | No | Data quality: 4 different date formats used |
| status | TEXT | Order status | Placed, placed, SHIPPED, Delivered | No | Inconsistent casing |
| email | TEXT | Customer email at time of order | jeremy54@hernandez.info | **Yes** — ~8% missing | |
| priority | TEXT | Order priority | Standard, Express | **Yes** | |

**Known data quality notes:** ~1.5% duplicate order_id rows; order_date appears in 4 different formats (`%Y-%m-%d`, `%d/%m/%Y`, `%m-%d-%Y`, `%Y/%m/%d`) — must be standardized during Sprint 2 transformation.

### 2.6 Inventory Management System — `inventory_movements.csv` → `stg_inventory_movements`

| Field | Data Type | Description | Sample Value | Nullable | Key |
|---|---|---|---|---|---|
| movement_id | VARCHAR(10) | Unique movement transaction identifier | INV000842 | No | PK |
| warehouse_id | VARCHAR(10) | Warehouse where movement occurred | WH006 | **Yes** — ~4% missing | FK → stg_warehouses.warehouse_id |
| product_id | VARCHAR(10) | Product moved | PRD00076 | No | FK → stg_products.product_id |
| movement_type | TEXT | Type of stock movement | INBOUND, inbound, Outbound, RETURN, ADJUSTMENT | No | Inconsistent casing |
| quantity | INTEGER | Quantity moved | 320 | No | |
| movement_date | DATE | Date of movement | 2026-04-18 | No | |
| reference_doc | TEXT | Reference document number | REF48213 | No | |
| handled_by | TEXT | Staff member who processed the movement | Priya Nair | No | |

### 2.7 Vendor & Supplier Portal — `vendor_portal.xlsx` → `stg_vendor_po`

| Field | Data Type | Description | Sample Value | Nullable | Key |
|---|---|---|---|---|---|
| po_id | VARCHAR(10) | Unique purchase order identifier | PO000512 | No | PK |
| supplier_id | VARCHAR(10) | Supplier fulfilling the order | SUP0014 | No | FK → stg_suppliers.supplier_id |
| product_id | VARCHAR(10) | Product ordered | PRD00076 | No | FK → stg_products.product_id |
| destination_warehouse_id | VARCHAR(10) | Delivery destination warehouse | WH006 | No | FK → stg_warehouses.warehouse_id |
| po_date | DATE | Date purchase order was raised | 2026-03-01 | No | |
| quantity_ordered | INTEGER | Quantity ordered from supplier | 5000 | No | |
| unit_cost | DECIMAL(8,2) | Cost per unit | 42.50 | No | |
| currency | TEXT | Currency code | USD, usd, INR, EUR | No | Inconsistent casing |
| acknowledged_date | DATE | Date supplier acknowledged the PO | 2026-03-02 | **Yes** — ~12% missing | |
| expected_arrival_date | DATE | Expected delivery date from supplier | 2026-04-15 | No | |
| vendor_rating_at_po | DECIMAL(2,1) | Supplier rating at time of PO | 4.2 | No | |

### 2.8 Shipment Tracking System — `shipment_tracking.json` → `stg_tracking_events`

| Field | Data Type | Description | Sample Value | Nullable | Key |
|---|---|---|---|---|---|
| tracking_event_id | VARCHAR(10) | Unique tracking event identifier | TRK0004521 | No | PK |
| shipment_id | VARCHAR(10) | Related shipment | SHP001411 | No | FK → stg_shipments.shipment_id |
| event_type | TEXT | Type of tracking scan event | Picked Up, Departed Facility, Arrived at Hub, Delivered, Delivery Exception | No | |
| event_timestamp | TIMESTAMP | Date/time of the scan | 2026-05-11T09:14:22 | No | |
| location | TEXT | Location of the scan event | Denver | **Yes** — ~5% missing | |
| scanned_by | TEXT | Staff member who scanned the event | Carlos | **Yes** — ~30% missing | |
| remarks | TEXT | Free-text remarks | "Delayed due to weather" | Yes — often blank | |

### 2.9 Customer Delivery Feedback — `customer_feedback.csv` → `stg_feedback`

| Field | Data Type | Description | Sample Value | Nullable | Key |
|---|---|---|---|---|---|
| feedback_id | VARCHAR(10) | Unique feedback record identifier | FBK000512 | No | PK |
| shipment_id | VARCHAR(10) | Related shipment | SHP001411 | No | FK → stg_shipments.shipment_id |
| customer_id | VARCHAR(10) | Customer providing feedback | CUST00361 | No | FK → stg_customers.customer_id |
| rating | INTEGER | Customer satisfaction rating (expected 1–5) | 4 | No | Data quality: ~2% invalid values (0, 6, -1) |
| on_time_delivery | TEXT | Whether delivery was on time | Yes, No, yes, NO | No | Inconsistent casing |
| comments | TEXT | Free-text feedback comments | "Driver was late by several hours." | Yes — often blank | |
| feedback_date | DATE | Date feedback was submitted | 2026-05-15 | No | |
| channel | TEXT | Feedback submission channel | App, Email Survey, Call Center, Website | No | |

### 2.10 IoT-Enabled Shipment Sensors — `iot_sensor_data.json` → `stg_iot`

| Field | Data Type | Description | Sample Value | Nullable | Key |
|---|---|---|---|---|---|
| sensor_reading_id | VARCHAR(10) | Unique sensor reading identifier | IOT0004521 | No | PK |
| shipment_id | VARCHAR(10) | Related shipment | SHP001411 | No | FK → stg_shipments.shipment_id |
| reading_timestamp | TIMESTAMP | Date/time of the sensor reading | 2026-05-12T03:44:10 | No | |
| temperature_c | DECIMAL(5,1) | Ambient temperature (Celsius) | 18.2 | No | Data quality: ~1.5% extreme outliers (80–150°C, sensor fault) |
| humidity_pct | DECIMAL(4,1) | Ambient humidity percentage | 55.3 | **Yes** — ~3% missing | |
| shock_detected | BOOLEAN | Whether a physical shock/impact was detected | TRUE, FALSE | No | |
| battery_pct | DECIMAL(4,1) | Sensor battery level percentage | 68.0 | No | |
| sensor_id | VARCHAR(10) | Physical sensor device identifier | SNR0142 | No | |

### 2.11 Legacy ERP (SQL Source) — `erp_master_source.sql` → `stg_customers`, `stg_warehouses`, `stg_vehicles`, `stg_suppliers`, `stg_products`

This source provides the same master entities described in Section 1, delivered via SQL `CREATE TABLE` + `INSERT` statements rather than flat files, simulating extraction from a legacy operational ERP database using Pentaho's **Table Input** step. Field definitions are identical to Section 1.

---

## 3. Cross-System Key Relationships

| Key | Origin Table | Referenced By |
|---|---|---|
| `customer_id` | stg_customers | stg_orders, stg_shipments, stg_feedback |
| `warehouse_id` | stg_warehouses | stg_vehicles, stg_shipments, stg_inventory, stg_inventory_movements, stg_vendor_po |
| `vehicle_id` | stg_vehicles | stg_shipments, stg_fleet, stg_gps |
| `supplier_id` | stg_suppliers | stg_products, stg_vendor_po |
| `product_id` | stg_products | stg_orders, stg_inventory, stg_inventory_movements, stg_vendor_po |
| `shipment_id` | stg_shipments | stg_tracking_events, stg_feedback, stg_iot |
| `order_id` / `order_ref` | stg_orders | stg_shipments |

These relationships are what enable the star schema fact/dimension joins built in Sprint 2 (see `docs/data-lineage.md` for the full source-to-target mapping).

---

## 4. Summary — Record Volumes by Source

| Source System | File | Records |
|---|---|---|
| Master: Customers | master_customers.csv | 600 |
| Master: Warehouses | master_warehouses.csv | 15 |
| Master: Vehicles | master_vehicles.csv | 60 |
| Master: Suppliers | master_suppliers.csv | 45 |
| Master: Products | master_products.csv | 150 |
| TMS | tms_shipments.csv | 1,515 |
| WMS | wms_inventory.xlsx | 1,300 |
| Fleet Management | fleet_management.json | 1,000 |
| GPS Tracking | gps_tracking.csv | 2,538 |
| OMS | oms_orders.xml | 1,218 |
| Inventory Movements | inventory_movements.csv | 1,400 |
| Vendor Portal | vendor_portal.xlsx | 1,100 |
| Shipment Tracking | shipment_tracking.json | 2,000 |
| Customer Feedback | customer_feedback.csv | 1,000 |
| IoT Sensors | iot_sensor_data.json | 2,200 |
| Legacy ERP (SQL) | erp_master_source.sql | 870 rows |
