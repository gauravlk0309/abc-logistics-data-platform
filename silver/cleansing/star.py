import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

tables = [
    "customer_feedback",
    "fleet_management",
    "gps_tracking",
    "inventory_movements",
    "iot_sensor_data",
    "oms_orders",
    "shipment_tracking",
    "tms_shipments",
    "vendor_portal",
    "wms_inventory"
]

print("=" * 70)
print("SILVER TABLE STRUCTURE")
print("=" * 70)

for table in tables:

    df = pd.read_sql(
        f"SELECT * FROM silver.{table} LIMIT 1",
        engine
    )

    print(f"\n{'=' * 70}")
    print(f"TABLE: silver.{table}")
    print(f"{'=' * 70}")

    for column in df.columns:
        print(f"{column:35} {df[column].dtype}")


# --------------------------------------------------
# ERP PRODUCTS
# --------------------------------------------------

print(f"\n{'=' * 70}")
print("TABLE: erp_products")
print(f"{'=' * 70}")

df = pd.read_sql(
    "SELECT * FROM erp_products LIMIT 1",
    engine
)

for column in df.columns:
    print(f"{column:35} {df[column].dtype}")