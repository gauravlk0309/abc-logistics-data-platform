**Business Requirement Document**

Enterprise Logistics Data Platform (ELDP)

ABC Logistics Ltd.

| **Field**     | **Value**                                           |
| ------------- | --------------------------------------------------- |
| Document Type | Business Requirement Document                       |
| ---           | ---                                                 |
| Project       | Enterprise Logistics Data Platform (ELDP)           |
| ---           | ---                                                 |
| Sprint        | Sprint 0 — Project Initiation & Architecture        |
| ---           | ---                                                 |
| Version       | 1.0                                                 |
| ---           | ---                                                 |
| Status        | Draft                                               |
| ---           | ---                                                 |
| Repository    | github.com/gauravlk0309/abc-logistics-data-platform |
| ---           | ---                                                 |

# Table of Contents

1. Executive Summary
2. Business Problem Statement
3. Business Stakeholders
4. Logistics Data Sources
5. Project Scope

5.1 In Scope

5.2 Out of Scope

5.3 Assumptions

5.4 Constraints

1. High-Level Architecture

6.1 Architecture Overview

6.2 Architecture Principles

6.3 Technology Stack

1. Enterprise Repository Structure
2. Success Criteria
3. Approval

# 1\. Executive Summary

ABC Logistics Ltd. is a global logistics and supply chain organization operating multiple distribution centers, warehouses, transportation hubs, and delivery fleets across domestic and international markets. The organization currently manages its operations through a collection of independent, disconnected enterprise systems, which limits visibility into shipments, warehouse operations, and fleet performance.

This document defines the business problem, stakeholders, data sources, scope, and high-level architecture for the Enterprise Logistics Data Platform (ELDP) — a unified data platform that will consolidate logistics and supply chain data into a single, trusted PostgreSQL Data Warehouse to support operational and executive decision-making.

# 2\. Business Problem Statement

ABC Logistics generates millions of records every day from systems including the Transportation Management System (TMS), Warehouse Management System (WMS), Fleet Management System, GPS Tracking Devices, Order Management System (OMS), Vendor Portals, Inventory Systems, Customer Service Applications, and IoT-enabled shipment sensors. Because these systems operate independently and in isolation, the organization faces the following business problems:

| **#** | **Problem**                                                                                                                      | **Business Impact**                                                             |
| ----- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| 1     | Fragmented shipment visibility — no single view of a shipment across TMS, GPS, and Shipment Tracking systems                     | Delayed response to shipment delays and exceptions; poor customer communication |
| ---   | ---                                                                                                                              | ---                                                                             |
| 2     | Inefficient route and delivery planning — GPS and fleet data are not integrated with order/shipment data                         | Higher fuel and operating costs; longer delivery times                          |
| ---   | ---                                                                                                                              | ---                                                                             |
| 3     | Inaccurate warehouse and inventory visibility — WMS and Inventory Management data are not reconciled                             | Stockouts, overstocking, and mismatched fulfillment                             |
| ---   | ---                                                                                                                              | ---                                                                             |
| 4     | Poor fleet utilization tracking — Fleet Management and GPS data are siloed                                                       | Underused or overused vehicles; higher maintenance costs                        |
| ---   | ---                                                                                                                              | ---                                                                             |
| 5     | Inconsistent supplier/vendor performance data — Vendor Portal data is disconnected from inbound shipment and inventory records   | Difficulty holding suppliers accountable to SLAs                                |
| ---   | ---                                                                                                                              | ---                                                                             |
| 6     | No unified customer experience view — Customer feedback is not linked to shipment or delivery performance data                   | Missed root-cause analysis of service complaints                                |
| ---   | ---                                                                                                                              | ---                                                                             |
| 7     | Lack of a single source of truth for reporting — Executive Management has no consolidated, trusted dataset for supply chain KPIs | Slow, manual, error-prone reporting; delayed strategic decisions                |
| ---   | ---                                                                                                                              | ---                                                                             |
| 8     | No formal data governance, lineage, or audit trail                                                                               | Compliance risk and difficulty troubleshooting data issues                      |
| ---   | ---                                                                                                                              | ---                                                                             |

**Root Cause:**

Each operational system was designed to serve its own function and was never architected to share data with other systems in a consistent, validated, and traceable way.

**Desired Outcome:**

A centralized, governed logistics data platform that ingests, cleans, standardizes, and stores data from all source systems, enabling accurate, timely, and trusted analytics across logistics operations, warehouse management, fleet performance, and executive reporting.

# 3\. Business Stakeholders

| **Stakeholder Group**                 | **Role in the Project**                                    | **Key Interests / Needs**                                                    |
| ------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Logistics Managers                    | Own shipment and delivery operations                       | Real-time shipment status, on-time delivery rates, delay root-cause analysis |
| ---                                   | ---                                                        | ---                                                                          |
| Warehouse Operations Team             | Manage inventory, stock movement, and warehouse throughput | Accurate stock levels, inventory reconciliation, reorder alerts              |
| ---                                   | ---                                                        | ---                                                                          |
| Fleet Management Team                 | Manage vehicles, drivers, and maintenance                  | Vehicle utilization, fuel efficiency, maintenance scheduling, GPS/route data |
| ---                                   | ---                                                        | ---                                                                          |
| Procurement Team                      | Manage supplier relationships and purchase orders          | Supplier/vendor performance, purchase order status, delivery reliability     |
| ---                                   | ---                                                        | ---                                                                          |
| Customer Service Team                 | Handle customer inquiries and delivery feedback            | Linked shipment + feedback data to resolve complaints and track satisfaction |
| ---                                   | ---                                                        | ---                                                                          |
| Executive Management                  | Strategic decision-making and oversight                    | Consolidated KPIs, executive dashboards, supply chain-wide reporting         |
| ---                                   | ---                                                        | ---                                                                          |
| Data Engineering Team (project team)  | Build and maintain the ELDP platform                       | Clean architecture, reliable pipelines, documented lineage                   |
| ---                                   | ---                                                        | ---                                                                          |
| IT / Infrastructure Team (supporting) | Provision and secure infrastructure                        | Database access, environment provisioning, security compliance               |
| ---                                   | ---                                                        | ---                                                                          |

# 4\. Logistics Data Sources

The ELDP platform will ingest data from the following heterogeneous enterprise systems:

| **#** | **Source System**                      | **Data Domain**                                      | **Format**  |
| ----- | -------------------------------------- | ---------------------------------------------------- | ----------- |
| 1     | Transportation Management System (TMS) | Shipments, carriers, freight cost                    | CSV         |
| ---   | ---                                    | ---                                                  | ---         |
| 2     | Warehouse Management System (WMS)      | Stock levels, bin locations                          | Excel       |
| ---   | ---                                    | ---                                                  | ---         |
| 3     | Fleet Management System                | Vehicle trips, maintenance, fuel                     | JSON        |
| ---   | ---                                    | ---                                                  | ---         |
| 4     | GPS Tracking Devices                   | Vehicle location, speed, ignition status             | CSV         |
| ---   | ---                                    | ---                                                  | ---         |
| 5     | Order Management System (OMS)          | Customer orders, order status                        | XML         |
| ---   | ---                                    | ---                                                  | ---         |
| 6     | Inventory Management System            | Stock movements (inbound/outbound/returns)           | CSV         |
| ---   | ---                                    | ---                                                  | ---         |
| 7     | Vendor & Supplier Portal               | Purchase orders, supplier performance                | Excel       |
| ---   | ---                                    | ---                                                  | ---         |
| 8     | Shipment Tracking System               | Tracking scan events, delivery exceptions            | JSON        |
| ---   | ---                                    | ---                                                  | ---         |
| 9     | Customer Service Application           | Delivery feedback, satisfaction ratings              | CSV         |
| ---   | ---                                    | ---                                                  | ---         |
| 10    | IoT-enabled Shipment Sensors           | Temperature, humidity, shock detection               | JSON        |
| ---   | ---                                    | ---                                                  | ---         |
| 11    | Legacy ERP (Master Data)               | Customers, warehouses, vehicles, suppliers, products | SQL (RDBMS) |
| ---   | ---                                    | ---                                                  | ---         |

Note: All operational sources reference common master entities (customer_id, warehouse_id, vehicle_id, supplier_id, product_id) sourced from the legacy ERP system, ensuring the data can be joined into a unified star schema during Sprint 2.

# 5\. Project Scope

## 5.1 In Scope

- Ingestion of data from all 11 source systems listed in Section 4, across CSV, Excel, JSON, XML, and SQL formats
- Data cleansing, validation, standardization, and deduplication of operational, shipment, and inventory data
- Design and implementation of a star schema (fact and dimension tables) in an enterprise PostgreSQL Data Warehouse
- Metadata management, audit logging, and end-to-end data lineage documentation
- Source-to-target mapping and business glossary
- ETL pipeline development using Pentaho Data Integration (Spoon), orchestrated via Pentaho Jobs
- Executive and operational reporting via Power BI dashboards covering: shipment and delivery performance, warehouse inventory movement, fleet utilization and vehicle performance, supplier and carrier performance, executive supply chain summary
- Version control of all ETL artifacts, SQL scripts, and documentation via Git and GitHub
- Enterprise-standard technical documentation (BRD, architecture, data dictionary, lineage, project report)

## 5.2 Out of Scope

- Real-time / streaming data ingestion (batch ingestion only for this phase)
- Predictive analytics or machine learning models (e.g., demand forecasting, route optimization algorithms)
- Direct integration with live production source systems (synthetic/sample data used for this capstone)
- Mobile application development
- Automated CI/CD deployment pipelines (manual Git-based workflow only)
- Data platform security/compliance certification (e.g., SOC 2, ISO 27001) — governance is limited to lineage, metadata, and audit logging

## 5.3 Assumptions

- Source data is made available in the formats defined in Section 4 (CSV, Excel, JSON, XML, SQL)
- PostgreSQL and Pentaho environments are available and accessible to the project team
- Data volumes for this phase are representative samples (batch loads), not full production-scale volumes

## 5.4 Constraints

- ETL tooling limited to Pentaho Data Integration (Community Edition)
- Reporting limited to Power BI
- All code and documentation must be version-controlled in the designated GitHub repository

# 6\. High-Level Architecture

## 6.1 Architecture Overview

The ELDP follows a standard layered data platform architecture: Source → Ingestion → Staging → Data Warehouse → Reporting, with governance (metadata, lineage, audit logs) and version control running across every layer.

| **Layer**      | **Color**             | **Contents**                                                                                                                                                                                                                                                          |
| -------------- | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source Systems | Gray                  | TMS, WMS, Fleet, GPS, OMS, Inventory, Vendor Portal, Shipment Tracking, Customer Service, IoT Sensors, Legacy ERP (SQL) — CSV, Excel, JSON, XML, SQL                                                                                                                  |
| ---            | ---                   | ---                                                                                                                                                                                                                                                                   |
| Ingestion      | Blue                  | Pentaho Data Integration transformations (.ktr) per source, with error handling and load-timestamp/source-file tagging, orchestrated via a Pentaho Job (.kjb)                                                                                                         |
| ---            | ---                   | ---                                                                                                                                                                                                                                                                   |
| Staging        | Teal                  | PostgreSQL staging schema — raw, minimally-typed tables mirroring each source as-is (stg_shipments, stg_inventory, stg_fleet, stg_orders, etc.)                                                                                                                       |
| ---            | ---                   | ---                                                                                                                                                                                                                                                                   |
| Data Warehouse | Purple / Pink / Coral | PostgreSQL warehouse schema — star schema with dimension tables (dim_customer, dim_warehouse, dim_product, etc.) and fact tables (fact_shipments, fact_inventory_movement, fact_fleet_activity, fact_feedback), populated after Python/Pandas profiling and cleansing |
| ---            | ---                   | ---                                                                                                                                                                                                                                                                   |
| Reporting      | Coral                 | Power BI dashboards — shipment & delivery performance, warehouse inventory movement, fleet utilization, supplier & carrier performance, executive KPIs                                                                                                                |
| ---            | ---                   | ---                                                                                                                                                                                                                                                                   |

Governance — metadata repository, end-to-end data lineage, and audit logs — runs across every layer, and all ETL artifacts, SQL scripts, and documentation are version-controlled in Git/GitHub throughout.

## 6.2 Architecture Principles

| **Principle**                | **Description**                                                                                                                           |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Layered separation           | Raw (staging) and curated (warehouse) data are kept physically separate to preserve traceability and allow reprocessing                   |
| ---                          | ---                                                                                                                                       |
| Format-agnostic ingestion    | Pentaho transformations normalize CSV, Excel, JSON, XML, and SQL sources into a consistent staging structure                              |
| ---                          | ---                                                                                                                                       |
| Single source of truth       | The PostgreSQL Data Warehouse (star schema) is the only dataset used for reporting — no dashboard queries staging or source data directly |
| ---                          | ---                                                                                                                                       |
| Traceability by design       | Every staging table carries source_file and load_timestamp fields; every warehouse table is documented in the source-to-target mapping    |
| ---                          | ---                                                                                                                                       |
| Version-controlled artifacts | All ETL transformations, SQL scripts, and documentation are stored and versioned in GitHub                                                |
| ---                          | ---                                                                                                                                       |

## 6.3 Technology Stack

| **Layer**                  | **Technology**                   |
| -------------------------- | -------------------------------- |
| ETL / Orchestration        | Pentaho Data Integration (Spoon) |
| ---                        | ---                              |
| Database / Data Warehouse  | PostgreSQL                       |
| ---                        | ---                              |
| Data Profiling & Cleansing | Python (Pandas)                  |
| ---                        | ---                              |
| Reporting & Dashboards     | Power BI                         |
| ---                        | ---                              |
| Version Control            | Git & GitHub                     |
| ---                        | ---                              |
| Documentation              | Markdown / MS Word               |
| ---                        | ---                              |
| Project Management         | Agile Scrum                      |
| ---                        | ---                              |

# 7\. Enterprise Repository Structure

**Repository:**

github.com/gauravlk0309/abc-logistics-data-platform

abc-logistics-data-platform/

- README.md
- .gitignore
- docs/
  - BRD.md / BRD.docx
  - solution-architecture.md
  - project-charter.md
  - business-glossary.md
  - data-profiling-report.md
  - data-quality-report.md
  - project-report.md
  - product-backlog.md and sprint backlogs (Consolidated from the former project-management directory)
- config/
- datasets/
  - bronze/
    - ingestion/
      - **Masters**: master_customers.csv, master_warehouses.csv, master_vehicles.csv, master_suppliers.csv, master_products.csv
      - **Source Systems**: tms_shipments.csv, wms_inventory.xlsx, fleet_management.json, gps_tracking.csv, oms_orders.xml, inventory_movements.csv, vendor_portal.xlsx, shipment_tracking.json, customer_feedback.csv, iot_sensor_data.json, erp_master_source.sql
    - staging/
  - silver/
    - cleansing/
    - validation/
    - transformations/
  - gold/
    - warehouse/
    - datamarts/
    - analytics/
- pentaho/
  - transformations/ (Contains .ktr files, one per source)
  - jobs/
    - master_ingestion_job.kjb
- python/
  - data_profiling.ipynb
  - data_quality_checks.ipynb
- sql/
  - staging/create_staging_tables.sql
  - warehouse/create_dimension_tables.sql
  - warehouse/create_fact_tables.sql
  - reporting/logistics_reporting_queries.sql
- metadata/
  - data-dictionary.md
  - lineage/
    - data-lineage.md
- dashboards/
  - logistics_executive_dashboard.pbix
- deployment/
- tests/

# 8\. Success Criteria

The ELDP project will be considered successful when:

- All 10+ heterogeneous data sources are ingested into PostgreSQL staging tables with logging and error handling in place
- A validated star schema data warehouse is populated with cleaned, deduplicated, and standardized data
- End-to-end data lineage from source to warehouse is documented
- Power BI dashboards deliver the KPIs required by each stakeholder group identified in Section 3
- All ETL pipelines, SQL scripts, and documentation are version-controlled in the abc-logistics-data-platform GitHub repository
- Enterprise-standard documentation (BRD, architecture, data dictionary, lineage, project report) is complete and approved

# 9\. Approval

| **Role**              | **Name** | **Date** | **Signature** |
| --------------------- | -------- | -------- | ------------- |
| Project Sponsor       |          |          |               |
| ---                   | ---      | ---      | ---           |
| Logistics Manager     |          |          |               |
| ---                   | ---      | ---      | ---           |
| Data Engineering Lead |          |          |               |
| ---                   | ---      | ---      | ---           |
| Executive Sponsor     |          |          |               |
| ---                   | ---      | ---      | ---           |