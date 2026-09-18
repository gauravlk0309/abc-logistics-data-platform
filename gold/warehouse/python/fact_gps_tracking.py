import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234%23@localhost:5432/eldp"
)

print("=" * 70)
print("BUILDING GOLD.FACT_GPS_TRACKING")
print("=" * 70)


# ============================================================
# 1. READ SOURCE AND VEHICLE DIMENSION
# ============================================================

gps = pd.read_sql(
    """
    SELECT *
    FROM silver.gps_tracking
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

print("\nSilver GPS records:", len(gps))
print("Vehicle dimension records:", len(vehicle))


# ============================================================
# 2. CHECK SOURCE GRAIN
# ============================================================

print("\nChecking GPS ping grain...")

print(
    "Duplicate GPS ping IDs:",
    gps["gps_ping_id"].duplicated().sum()
)


# ============================================================
# 3. LOOKUP VEHICLE SURROGATE KEY
# ============================================================

fact = gps.merge(
    vehicle,
    on="vehicle_id",
    how="left"
)

print(
    "Unmatched vehicle records:",
    fact["vehicle_key"].isnull().sum()
)


# ============================================================
# 4. CREATE FACT SURROGATE KEY
# ============================================================

fact.insert(
    0,
    "gps_tracking_key",
    range(1, len(fact) + 1)
)


# ============================================================
# 5. SELECT FACT COLUMNS
# ============================================================

fact_gps_tracking = fact[
    [
        "gps_tracking_key",
        "gps_ping_id",
        "vehicle_key",
        "timestamp",
        "latitude",
        "longitude",
        "speed_kmph",
        "heading_deg",
        "ignition_status",
        "fuel_level_pct"
    ]
]


# ============================================================
# 6. CREATE GOLD SCHEMA
# ============================================================

with engine.begin() as conn:
    conn.execute(
        text("CREATE SCHEMA IF NOT EXISTS gold")
    )


# ============================================================
# 7. LOAD FACT TABLE
# ============================================================

fact_gps_tracking.to_sql(
    "fact_gps_tracking",
    engine,
    schema="gold",
    if_exists="replace",
    index=False
)


# ============================================================
# 8. ADD PRIMARY KEY
# ============================================================

with engine.begin() as conn:
    conn.execute(text("""
        ALTER TABLE gold.fact_gps_tracking
        ADD PRIMARY KEY (gps_tracking_key)
    """))


# ============================================================
# 9. VERIFY FACT TABLE
# ============================================================

check = pd.read_sql(
    """
    SELECT *
    FROM gold.fact_gps_tracking
    ORDER BY gps_tracking_key
    """,
    engine
)

print("\nGold fact table:")
print(check.head())

print("\nTotal fact records:", len(check))

print(
    "Duplicate GPS tracking keys:",
    check["gps_tracking_key"].duplicated().sum()
)

print(
    "Duplicate GPS ping IDs:",
    check["gps_ping_id"].duplicated().sum()
)

print(
    "NULL GPS tracking keys:",
    check["gps_tracking_key"].isnull().sum()
)

print(
    "NULL GPS ping IDs:",
    check["gps_ping_id"].isnull().sum()
)

print(
    "NULL vehicle keys:",
    check["vehicle_key"].isnull().sum()
)


# ============================================================
# 10. CHECK GPS DATA
# ============================================================

print("\nGPS data NULL counts:")

print(
    "NULL timestamp:",
    check["timestamp"].isnull().sum()
)

print(
    "NULL latitude:",
    check["latitude"].isnull().sum()
)

print(
    "NULL longitude:",
    check["longitude"].isnull().sum()
)

print(
    "NULL speed_kmph:",
    check["speed_kmph"].isnull().sum()
)

print(
    "NULL heading_deg:",
    check["heading_deg"].isnull().sum()
)

print(
    "NULL fuel_level_pct:",
    check["fuel_level_pct"].isnull().sum()
)


print("\n" + "=" * 70)
print("FACT_GPS_TRACKING CREATED SUCCESSFULLY")
print("=" * 70)