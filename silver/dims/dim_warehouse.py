import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

print("=" * 60)
print("BUILDING GOLD.DIM_WAREHOUSE")
print("=" * 60)

# 1. Read standardized warehouse master
df = pd.read_sql(
    "SELECT * FROM silver.warehouse_master",
    engine
)

print("\nSilver warehouse records:", len(df))

# 2. Create surrogate key
df.insert(
    0,
    "warehouse_key",
    range(1, len(df) + 1)
)

# 3. Select dimension columns
dim_warehouse = df[
    [
        "warehouse_key",
        "warehouse_id",
        "warehouse_name",
        "city",
        "state",
        "country",
        "region",
        "latitude",
        "longitude",
        "capacity_sqft",
        "manager_name",
        "operational_since"
    ]
]

# 4. Create Gold schema
with engine.begin() as conn:
    conn.execute(
        text("CREATE SCHEMA IF NOT EXISTS gold")
    )

# 5. Load into Gold
dim_warehouse.to_sql(
    "dim_warehouse",
    engine,
    schema="gold",
    if_exists="replace",
    index=False
)

# 6. Add primary key
with engine.begin() as conn:
    conn.execute(text("""
        ALTER TABLE gold.dim_warehouse
        ADD PRIMARY KEY (warehouse_key)
    """))

# 7. Verify
check = pd.read_sql(
    """
    SELECT *
    FROM gold.dim_warehouse
    ORDER BY warehouse_key
    """,
    engine
)

print("\nGold dimension:")
print(check.head())

print("\nTotal dimension records:",
      len(check))

print(
    "Duplicate warehouse keys:",
    check["warehouse_key"].duplicated().sum()
)

print(
    "Duplicate warehouse IDs:",
    check["warehouse_id"].duplicated().sum()
)

print(
    "NULL warehouse keys:",
    check["warehouse_key"].isnull().sum()
)

print(
    "NULL warehouse IDs:",
    check["warehouse_id"].isnull().sum()
)

print("\n" + "=" * 60)
print("DIM_WAREHOUSE CREATED SUCCESSFULLY")
print("=" * 60)