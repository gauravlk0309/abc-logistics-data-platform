import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234%23@localhost:5432/eldp"
)

print("=" * 70)
print("BUILDING GOLD.FACT_PURCHASE_ORDER")
print("=" * 70)


# ============================================================
# 1. READ SOURCE AND DIMENSIONS
# ============================================================

po = pd.read_sql(
    """
    SELECT *
    FROM silver.vendor_portal
    """,
    engine
)

supplier = pd.read_sql(
    """
    SELECT supplier_key, supplier_id
    FROM gold.dim_supplier
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

warehouse = pd.read_sql(
    """
    SELECT warehouse_key, warehouse_id
    FROM gold.dim_warehouse
    """,
    engine
)

print("\nSilver Vendor Portal records:", len(po))
print("Supplier dimension records:", len(supplier))
print("Product dimension records:", len(product))
print("Warehouse dimension records:", len(warehouse))


# ============================================================
# 2. CHECK SOURCE GRAIN
# ============================================================

print("\nChecking purchase order grain...")

print(
    "Duplicate PO IDs:",
    po["po_id"].duplicated().sum()
)


# ============================================================
# 3. LOOKUP SUPPLIER KEY
# ============================================================

fact = po.merge(
    supplier,
    on="supplier_id",
    how="left"
)

print(
    "Unmatched supplier records:",
    fact["supplier_key"].isnull().sum()
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
# 5. LOOKUP WAREHOUSE KEY
# ============================================================

fact = fact.merge(
    warehouse,
    left_on="destination_warehouse_id",
    right_on="warehouse_id",
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
    "purchase_order_key",
    range(1, len(fact) + 1)
)


# ============================================================
# 7. SELECT FACT COLUMNS
# ============================================================

fact_purchase_order = fact[
    [
        "purchase_order_key",
        "po_id",
        "supplier_key",
        "product_key",
        "warehouse_key",
        "po_date",
        "quantity_ordered",
        "unit_cost",
        "currency",
        "acknowledged_date",
        "expected_arrival_date",
        "vendor_rating_at_po"
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

fact_purchase_order.to_sql(
    "fact_purchase_order",
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
        ALTER TABLE gold.fact_purchase_order
        ADD PRIMARY KEY (purchase_order_key)
    """))


# ============================================================
# 11. VERIFY FACT TABLE
# ============================================================

check = pd.read_sql(
    """
    SELECT *
    FROM gold.fact_purchase_order
    ORDER BY purchase_order_key
    """,
    engine
)

print("\nGold fact table:")
print(check.head())

print("\nTotal fact records:", len(check))

print(
    "Duplicate purchase order keys:",
    check["purchase_order_key"].duplicated().sum()
)

print(
    "Duplicate PO IDs:",
    check["po_id"].duplicated().sum()
)

print(
    "NULL purchase order keys:",
    check["purchase_order_key"].isnull().sum()
)

print(
    "NULL PO IDs:",
    check["po_id"].isnull().sum()
)

print(
    "NULL supplier keys:",
    check["supplier_key"].isnull().sum()
)

print(
    "NULL product keys:",
    check["product_key"].isnull().sum()
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
    "NULL quantity_ordered:",
    check["quantity_ordered"].isnull().sum()
)

print(
    "NULL unit_cost:",
    check["unit_cost"].isnull().sum()
)

print(
    "NULL vendor_rating_at_po:",
    check["vendor_rating_at_po"].isnull().sum()
)


print("\n" + "=" * 70)
print("FACT_PURCHASE_ORDER CREATED SUCCESSFULLY")
print("=" * 70)