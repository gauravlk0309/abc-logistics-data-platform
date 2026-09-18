import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234%23@localhost:5432/eldp"
)

print("=" * 70)
print("BUILDING GOLD.FACT_INVENTORY_SNAPSHOT")
print("=" * 70)


# ============================================================
# 1. READ SOURCE AND DIMENSIONS
# ============================================================

inventory = pd.read_sql(
    """
    SELECT *
    FROM silver.wms_inventory
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

print("\nSilver WMS records:", len(inventory))
print("Warehouse dimension records:", len(warehouse))
print("Product dimension records:", len(product))


# ============================================================
# 2. CHECK SOURCE GRAIN
# ============================================================

print("\nChecking inventory snapshot grain...")

print(
    "Duplicate stock record IDs:",
    inventory["stock_record_id"].duplicated().sum()
)


# ============================================================
# 3. LOOKUP WAREHOUSE KEY
# ============================================================

fact = inventory.merge(
    warehouse,
    on="warehouse_id",
    how="left"
)

print(
    "Unmatched warehouse records:",
    fact["warehouse_key"].isnull().sum()
)


# ============================================================
# 4. LOOKUP PRODUCT KEY
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
    "inventory_snapshot_key",
    range(1, len(fact) + 1)
)


# ============================================================
# 6. SELECT FACT COLUMNS
# ============================================================

fact_inventory_snapshot = fact[
    [
        "inventory_snapshot_key",
        "stock_record_id",
        "warehouse_key",
        "product_key",
        "bin_location",
        "quantity_on_hand",
        "unit_of_measure",
        "reorder_level",
        "last_stock_count_date",
        "aisle",
        "damaged_units"
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

fact_inventory_snapshot.to_sql(
    "fact_inventory_snapshot",
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
        ALTER TABLE gold.fact_inventory_snapshot
        ADD PRIMARY KEY (inventory_snapshot_key)
    """))


# ============================================================
# 10. VERIFY FACT TABLE
# ============================================================

check = pd.read_sql(
    """
    SELECT *
    FROM gold.fact_inventory_snapshot
    ORDER BY inventory_snapshot_key
    """,
    engine
)

print("\nGold fact table:")
print(check.head())

print("\nTotal fact records:", len(check))

print(
    "Duplicate inventory snapshot keys:",
    check["inventory_snapshot_key"].duplicated().sum()
)

print(
    "Duplicate stock record IDs:",
    check["stock_record_id"].duplicated().sum()
)

print(
    "NULL inventory snapshot keys:",
    check["inventory_snapshot_key"].isnull().sum()
)

print(
    "NULL stock record IDs:",
    check["stock_record_id"].isnull().sum()
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
# 11. CHECK INVENTORY MEASURES
# ============================================================

print("\nInventory measure NULL counts:")

print(
    "NULL quantity_on_hand:",
    check["quantity_on_hand"].isnull().sum()
)

print(
    "NULL reorder_level:",
    check["reorder_level"].isnull().sum()
)

print(
    "NULL damaged_units:",
    check["damaged_units"].isnull().sum()
)


print("\n" + "=" * 70)
print("FACT_INVENTORY_SNAPSHOT CREATED SUCCESSFULLY")
print("=" * 70)