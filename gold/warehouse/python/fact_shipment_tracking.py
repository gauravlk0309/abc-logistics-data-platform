import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234%23@localhost:5432/eldp"
)

print("=" * 70)
print("BUILDING GOLD.FACT_SHIPMENT_TRACKING")
print("=" * 70)


# ============================================================
# 1. READ SOURCE
# ============================================================

tracking = pd.read_sql(
    """
    SELECT *
    FROM silver.shipment_tracking
    """,
    engine
)

print("\nSilver Shipment Tracking records:", len(tracking))


# ============================================================
# 2. CHECK SOURCE GRAIN
# ============================================================

print("\nChecking shipment tracking event grain...")

print(
    "Duplicate tracking event IDs:",
    tracking["tracking_event_id"].duplicated().sum()
)


# ============================================================
# 3. CREATE FACT SURROGATE KEY
# ============================================================

tracking.insert(
    0,
    "tracking_event_key",
    range(1, len(tracking) + 1)
)


# ============================================================
# 4. SELECT FACT COLUMNS
# ============================================================

fact_shipment_tracking = tracking[
    [
        "tracking_event_key",
        "tracking_event_id",
        "shipment_id",
        "event_type",
        "event_timestamp",
        "location",
        "scanned_by",
        "remarks"
    ]
]


# ============================================================
# 5. CREATE GOLD SCHEMA
# ============================================================

with engine.begin() as conn:
    conn.execute(
        text("CREATE SCHEMA IF NOT EXISTS gold")
    )


# ============================================================
# 6. LOAD FACT TABLE
# ============================================================

fact_shipment_tracking.to_sql(
    "fact_shipment_tracking",
    engine,
    schema="gold",
    if_exists="replace",
    index=False
)


# ============================================================
# 7. ADD PRIMARY KEY
# ============================================================

with engine.begin() as conn:
    conn.execute(text("""
        ALTER TABLE gold.fact_shipment_tracking
        ADD PRIMARY KEY (tracking_event_key)
    """))


# ============================================================
# 8. VERIFY FACT TABLE
# ============================================================

check = pd.read_sql(
    """
    SELECT *
    FROM gold.fact_shipment_tracking
    ORDER BY tracking_event_key
    """,
    engine
)

print("\nGold fact table:")
print(check.head())

print("\nTotal fact records:", len(check))

print(
    "Duplicate tracking event keys:",
    check["tracking_event_key"].duplicated().sum()
)

print(
    "Duplicate tracking event IDs:",
    check["tracking_event_id"].duplicated().sum()
)

print(
    "NULL tracking event keys:",
    check["tracking_event_key"].isnull().sum()
)

print(
    "NULL tracking event IDs:",
    check["tracking_event_id"].isnull().sum()
)

print(
    "NULL shipment IDs:",
    check["shipment_id"].isnull().sum()
)


# ============================================================
# 9. CHECK OPTIONAL ATTRIBUTES
# ============================================================

print("\nOptional attribute NULL counts:")

print(
    "NULL location:",
    check["location"].isnull().sum()
)

print(
    "NULL scanned_by:",
    check["scanned_by"].isnull().sum()
)

print(
    "NULL remarks:",
    check["remarks"].isnull().sum()
)


print("\n" + "=" * 70)
print("FACT_SHIPMENT_TRACKING CREATED SUCCESSFULLY")
print("=" * 70)