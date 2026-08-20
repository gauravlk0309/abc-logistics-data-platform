# Project Charter: Enterprise Logistics Data Platform (ELDP)
**Organization:** ABC Logistics Ltd.

## 1. Executive Summary & Business Need
ABC Logistics manages operations through independent, disconnected systems (TMS, WMS, Fleet, GPS, OMS, etc.), leading to fragmented shipment visibility, inefficient route planning, inaccurate inventory, and no unified source of truth for reporting. This project will deliver a centralized, governed data platform that ingests, cleans, standardizes, and stores supply chain data into a trusted PostgreSQL Data Warehouse.

## 2. Project Objectives
- Develop a unified PostgreSQL Data Warehouse with a star schema design.
- Implement automated batch ETL pipelines using Pentaho Data Integration.
- Deliver executive and operational reporting via Power BI dashboards.
- Establish data governance, audit logging, and end-to-end data lineage.

## 3. Project Scope
### In Scope
- Batch ingestion of data from 11 heterogeneous source systems.
- Handling of 5 data formats: CSV, Excel, JSON, XML, and SQL.
- Data cleansing, validation, standardization, and deduplication.
- Implementation of a PostgreSQL staging layer and data warehouse layer.
- Development of Power BI dashboards for supply chain KPIs.
- Version control of all artifacts in GitHub.

### Out of Scope
- Real-time or streaming data ingestion.
- Predictive analytics or machine learning models.
- Direct integration with live production source systems (using sample data).
- Automated CI/CD deployment pipelines.
- Mobile application development.
- Data platform security/compliance certification (e.g., SOC 2).

## 4. Assumptions & Constraints
- Source data is available in the specified formats.
- PostgreSQL and Pentaho environments are accessible.
- ETL tooling is limited to Pentaho Data Integration (Community Edition).
- Reporting is restricted to Power BI.

## 5. Key Stakeholders
- Logistics Managers: Real-time shipment status, delay root-cause analysis.
- Warehouse Operations: Accurate stock levels, inventory reconciliation.
- Fleet Management: Vehicle utilization, fuel efficiency, route data.
- Procurement: Supplier performance, PO status.
- Customer Service: Linked shipment and feedback data.
- Executive Management: Consolidated KPIs, strategic oversight.
- Data Engineering & IT Teams: Pipeline development, infrastructure setup.

## 6. Success Criteria & Definition of Done
- All 11 data sources are successfully ingested into PostgreSQL staging tables.
- A validated star schema is fully populated with cleaned data.
- Power BI dashboards deliver the requested KPIs.
- Sprint Definition of Done (DoD) is met: ETL success, data quality checks passed, source-to-target mappings updated, and code committed to Git.
