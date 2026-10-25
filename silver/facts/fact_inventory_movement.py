import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234%23@localhost:5432/eldp"
)

print("=" * 70)
print("BUILDING GOLD.FACT_INVENTORY_MOVEMENT")
print("=" * 70)


# ============================================================
# 1. READ SOURCE AND DIMENSIONS
# ============================================================

movements = pd.read_sql(
    """
    SELECT *
    FROM silver.inventory_movements
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

product = pd.read_sql(
    """
    SELECT product_key, product_id
    FROM gold.dim_product
    """,
    engine
)

print("\nSilver Inventory Movement records:", len(movements))
print("Warehouse dimension records:", len(warehouse))
print("Product dimension records:", len(product))


# ============================================================
# 2. CHECK SOURCE GRAIN
# ============================================================

print("\nChecking inventory movement grain...")

print(
    "Duplicate movement IDs:",
    movements["movement_id"].duplicated().sum()
)


# ============================================================
# 3. LOOKUP WAREHOUSE SURROGATE KEY
# ============================================================

fact = movements.merge(
    warehouse,
    on="warehouse_id",
    how="left"
)

print(
    "Unmatched warehouse records:",
    fact["warehouse_key"].isnull().sum()
)


# ============================================================
# 4. LOOKUP PRODUCT SURROGATE KEY
# ============================================================

fact = fact.merge(
    product,
    on="product_id",
    how="left"
)

print(
    "Unmatched product records:",
    fact["product_key"].isnull().sum()
)


# ============================================================
# 5. CREATE FACT SURROGATE KEY
# ============================================================

fact.insert(
    0,
    "movement_key",
    range(1, len(fact) + 1)
)


# ============================================================
# 6. SELECT FACT COLUMNS
# ============================================================

fact_inventory_movement = fact[
    [
        "movement_key",
        "movement_id",
        "warehouse_key",
        "product_key",
        "movement_type",
        "quantity",
        "movement_date",
        "reference_doc",
        "handled_by"
    ]
]


# ============================================================
# 7. CREATE GOLD SCHEMA
# ============================================================

with engine.begin() as conn:
    conn.execute(
        text("CREATE SCHEMA IF NOT EXISTS gold")
    )


# ============================================================
# 8. LOAD FACT TABLE
# ============================================================

fact_inventory_movement.to_sql(
    "fact_inventory_movement",
    engine,
    schema="gold",
    if_exists="replace",
    index=False
)


# ============================================================
# 9. ADD PRIMARY KEY
# ============================================================

with engine.begin() as conn:
    conn.execute(text("""
        ALTER TABLE gold.fact_inventory_movement
        ADD PRIMARY KEY (movement_key)
    """))


# ============================================================
# 10. VERIFY FACT TABLE
# ============================================================

check = pd.read_sql(
    """
    SELECT *
    FROM gold.fact_inventory_movement
    ORDER BY movement_key
    """,
    engine
)

print("\nGold fact table:")
print(check.head())

print("\nTotal fact records:", len(check))

print(
    "Duplicate movement keys:",
    check["movement_key"].duplicated().sum()
)

print(
    "Duplicate movement IDs:",
    check["movement_id"].duplicated().sum()
)

print(
    "NULL movement keys:",
    check["movement_key"].isnull().sum()
)

print(
    "NULL movement IDs:",
    check["movement_id"].isnull().sum()
)

print(
    "NULL warehouse keys:",
    check["warehouse_key"].isnull().sum()
)

print(
    "NULL product keys:",
    check["product_key"].isnull().sum()
)


# ============================================================
# 11. CHECK MEASURES
# ============================================================

print("\nMeasure NULL counts:")

print(
    "NULL quantity:",
    check["quantity"].isnull().sum()
)


print("\n" + "=" * 70)
print("FACT_INVENTORY_MOVEMENT CREATED SUCCESSFULLY")
print("=" * 70)