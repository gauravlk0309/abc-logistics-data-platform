import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234%23@localhost:5432/eldp"
)

print("=" * 70)
print("BUILDING GOLD.FACT_SHIPMENT")
print("=" * 70)


# ============================================================
# 1. READ SOURCE AND DIMENSIONS
# ============================================================

tms = pd.read_sql(
    """
    SELECT *
    FROM silver.tms_shipments
    """,
    engine
)

customer = pd.read_sql(
    """
    SELECT customer_key, customer_id
    FROM gold.dim_customer
    """,
    engine
)

vehicle = pd.read_sql(
    """
    SELECT vehicle_key, vehicle_id
    FROM gold.dim_vehicle
    """,
    engine
)

warehouse = pd.read_sql(
    """
    SELECT warehouse_key, warehouse_id
    FROM gold.dim_warehouse
    """,
    engine
)

print("\nSilver TMS records:", len(tms))
print("Customer dimension records:", len(customer))
print("Vehicle dimension records:", len(vehicle))
print("Warehouse dimension records:", len(warehouse))


# ============================================================
# 2. CHECK SOURCE GRAIN
# ============================================================

print("\nChecking shipment grain...")

print(
    "Duplicate shipment IDs:",
    tms["shipment_id"].duplicated().sum()
)


# ============================================================
# 3. LOOKUP CUSTOMER SURROGATE KEY
# ============================================================

fact = tms.merge(
    customer,
    on="customer_id",
    how="left"
)

print(
    "Unmatched customer records:",
    fact["customer_key"].isnull().sum()
)


# ============================================================
# 4. LOOKUP VEHICLE SURROGATE KEY
# ============================================================

fact = fact.merge(
    vehicle,
    on="vehicle_id",
    how="left"
)

print(
    "Unmatched vehicle records:",
    fact["vehicle_key"].isnull().sum()
)


# ============================================================
# 5. LOOKUP WAREHOUSE SURROGATE KEY
# ============================================================

fact = fact.merge(
    warehouse,
    on="warehouse_id",
    how="left"
)

print(
    "Unmatched warehouse records:",
    fact["warehouse_key"].isnull().sum()
)


# ============================================================
# 6. CREATE FACT SURROGATE KEY
# ============================================================

fact.insert(
    0,
    "shipment_key",
    range(1, len(fact) + 1)
)


# ============================================================
# 7. SELECT FACT COLUMNS
# ============================================================

fact_shipment = fact[
    [
        "shipment_key",
        "shipment_id",
        "order_ref",
        "customer_key",
        "vehicle_key",
        "warehouse_key",
        "carrier",
        "ship_date",
        "expected_delivery_date",
        "actual_delivery_date",
        "distance_km",
        "weight_kg",
        "freight_cost_usd",
        "status",
        "origin_city",
        "destination_city"
    ]
]


# ============================================================
# 8. CREATE GOLD SCHEMA
# ============================================================

with engine.begin() as conn:
    conn.execute(
        text("CREATE SCHEMA IF NOT EXISTS gold")
    )


# ============================================================
# 9. LOAD FACT TABLE
# ============================================================

fact_shipment.to_sql(
    "fact_shipment",
    engine,
    schema="gold",
    if_exists="replace",
    index=False
)


# ============================================================
# 10. ADD PRIMARY KEY
# ============================================================

with engine.begin() as conn:
    conn.execute(text("""
        ALTER TABLE gold.fact_shipment
        ADD PRIMARY KEY (shipment_key)
    """))


# ============================================================
# 11. VERIFY FACT TABLE
# ============================================================

check = pd.read_sql(
    """
    SELECT *
    FROM gold.fact_shipment
    ORDER BY shipment_key
    """,
    engine
)

print("\nGold fact table:")
print(check.head())

print("\nTotal fact records:", len(check))

print(
    "Duplicate shipment keys:",
    check["shipment_key"].duplicated().sum()
)

print(
    "Duplicate shipment IDs:",
    check["shipment_id"].duplicated().sum()
)

print(
    "NULL shipment keys:",
    check["shipment_key"].isnull().sum()
)

print(
    "NULL shipment IDs:",
    check["shipment_id"].isnull().sum()
)

print(
    "NULL customer keys:",
    check["customer_key"].isnull().sum()
)

print(
    "NULL vehicle keys:",
    check["vehicle_key"].isnull().sum()
)

print(
    "NULL warehouse keys:",
    check["warehouse_key"].isnull().sum()
)


# ============================================================
# 12. CHECK MEASURES
# ============================================================

print("\nMeasure NULL counts:")

print(
    "NULL distance_km:",
    check["distance_km"].isnull().sum()
)

print(
    "NULL weight_kg:",
    check["weight_kg"].isnull().sum()
)

print(
    "NULL freight_cost_usd:",
    check["freight_cost_usd"].isnull().sum()
)


print("\n" + "=" * 70)
print("FACT_SHIPMENT CREATED SUCCESSFULLY")
print("=" * 70)