import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

print("=" * 60)
print("BUILDING GOLD.DIM_VEHICLE")
print("=" * 60)

# 1. Read standardized vehicle master
df = pd.read_sql(
    "SELECT * FROM silver.vehicle_master",
    engine
)

print("\nSilver vehicle records:", len(df))

# 2. Create surrogate key
df.insert(
    0,
    "vehicle_key",
    range(1, len(df) + 1)
)

# 3. Select dimension columns
dim_vehicle = df[
    [
        "vehicle_key",
        "vehicle_id",
        "vehicle_type",
        "registration_number",
        "fuel_type",
        "capacity_kg",
        "manufacture_year",
        "home_warehouse_id",
        "driver_name",
        "driver_license_no",
        "status"
    ]
]

# 4. Create Gold schema if not already present
with engine.begin() as conn:
    conn.execute(
        text("CREATE SCHEMA IF NOT EXISTS gold")
    )

# 5. Load into Gold
dim_vehicle.to_sql(
    "dim_vehicle",
    engine,
    schema="gold",
    if_exists="replace",
    index=False
)

# 6. Add primary key
with engine.begin() as conn:
    conn.execute(text("""
        ALTER TABLE gold.dim_vehicle
        ADD PRIMARY KEY (vehicle_key)
    """))

# 7. Verify
check = pd.read_sql(
    """
    SELECT *
    FROM gold.dim_vehicle
    ORDER BY vehicle_key
    """,
    engine
)

print("\nGold dimension:")
print(check.head())

print("\nTotal dimension records:",
      len(check))

print(
    "Duplicate vehicle keys:",
    check["vehicle_key"].duplicated().sum()
)

print(
    "Duplicate vehicle IDs:",
    check["vehicle_id"].duplicated().sum()
)

print(
    "NULL vehicle keys:",
    check["vehicle_key"].isnull().sum()
)

print(
    "NULL vehicle IDs:",
    check["vehicle_id"].isnull().sum()
)

print("\n" + "=" * 60)
print("DIM_VEHICLE CREATED SUCCESSFULLY")
print("=" * 60)