import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234%23@localhost:5432/eldp"
)

print("=" * 70)
print("BUILDING GOLD.FACT_FLEET_EVENT")
print("=" * 70)


# ============================================================
# 1. READ SOURCE AND DIMENSION
# ============================================================

fleet = pd.read_sql(
    """
    SELECT *
    FROM silver.fleet_management
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

print("\nSilver Fleet records:", len(fleet))
print("Vehicle dimension records:", len(vehicle))


# ============================================================
# 2. CHECK SOURCE GRAIN
# ============================================================

print("\nChecking fleet event grain...")

print(
    "Duplicate fleet_log_ids:",
    fleet["fleet_log_id"].duplicated().sum()
)


# ============================================================
# 3. LOOKUP VEHICLE SURROGATE KEY
# ============================================================

fact = fleet.merge(
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
    "fleet_event_key",
    range(1, len(fact) + 1)
)


# ============================================================
# 5. SELECT FACT COLUMNS
# ============================================================

fact_fleet_event = fact[
    [
        "fleet_event_key",
        "fleet_log_id",
        "vehicle_key",
        "driver_name",
        "event_type",
        "event_date",
        "odometer_km",
        "fuel_liters",
        "maintenance_cost_usd",
        "downtime_hours",
        "notes"
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

fact_fleet_event.to_sql(
    "fact_fleet_event",
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
        ALTER TABLE gold.fact_fleet_event
        ADD PRIMARY KEY (fleet_event_key)
    """))


# ============================================================
# 9. VERIFY FACT TABLE
# ============================================================

check = pd.read_sql(
    """
    SELECT *
    FROM gold.fact_fleet_event
    ORDER BY fleet_event_key
    """,
    engine
)

print("\nGold fact table:")
print(check.head())

print("\nTotal fact records:", len(check))

print(
    "Duplicate fleet event keys:",
    check["fleet_event_key"].duplicated().sum()
)

print(
    "Duplicate fleet log IDs:",
    check["fleet_log_id"].duplicated().sum()
)

print(
    "NULL fleet event keys:",
    check["fleet_event_key"].isnull().sum()
)

print(
    "NULL fleet log IDs:",
    check["fleet_log_id"].isnull().sum()
)

print(
    "NULL vehicle keys:",
    check["vehicle_key"].isnull().sum()
)


# ============================================================
# 10. CHECK MEASURES
# ============================================================

print("\nMeasure NULL counts:")

print(
    "NULL odometer_km:",
    check["odometer_km"].isnull().sum()
)

print(
    "NULL fuel_liters:",
    check["fuel_liters"].isnull().sum()
)

print(
    "NULL maintenance_cost_usd:",
    check["maintenance_cost_usd"].isnull().sum()
)

print(
    "NULL downtime_hours:",
    check["downtime_hours"].isnull().sum()
)


print("\n" + "=" * 70)
print("FACT_FLEET_EVENT CREATED SUCCESSFULLY")
print("=" * 70)