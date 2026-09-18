import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234%23@localhost:5432/eldp"
)

print("=" * 70)
print("BUILDING GOLD.FACT_ORDER")
print("=" * 70)


# ============================================================
# 1. READ SOURCE AND DIMENSIONS
# ============================================================

orders = pd.read_sql(
    """
    SELECT *
    FROM silver.oms_orders
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

product = pd.read_sql(
    """
    SELECT product_key, product_id
    FROM gold.dim_product
    """,
    engine
)

print("\nSilver OMS records:", len(orders))
print("Customer dimension records:", len(customer))
print("Product dimension records:", len(product))


# ============================================================
# 2. CHECK SOURCE GRAIN
# ============================================================

print("\nChecking order grain...")

print(
    "Duplicate order IDs:",
    orders["order_id"].duplicated().sum()
)


# ============================================================
# 3. LOOKUP CUSTOMER SURROGATE KEY
# ============================================================

fact = orders.merge(
    customer,
    on="customer_id",
    how="left"
)

print(
    "Unmatched customer records:",
    fact["customer_key"].isnull().sum()
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
    "order_key",
    range(1, len(fact) + 1)
)


# ============================================================
# 6. SELECT FACT COLUMNS
# ============================================================

fact_order = fact[
    [
        "order_key",
        "order_id",
        "customer_key",
        "product_key",
        "quantity",
        "unit_price",
        "order_date",
        "status",
        "priority",
        "email"
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

fact_order.to_sql(
    "fact_order",
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
        ALTER TABLE gold.fact_order
        ADD PRIMARY KEY (order_key)
    """))


# ============================================================
# 10. VERIFY FACT TABLE
# ============================================================

check = pd.read_sql(
    """
    SELECT *
    FROM gold.fact_order
    ORDER BY order_key
    """,
    engine
)

print("\nGold fact table:")
print(check.head())

print("\nTotal fact records:", len(check))

print(
    "Duplicate order keys:",
    check["order_key"].duplicated().sum()
)

print(
    "Duplicate order IDs:",
    check["order_id"].duplicated().sum()
)

print(
    "NULL order keys:",
    check["order_key"].isnull().sum()
)

print(
    "NULL order IDs:",
    check["order_id"].isnull().sum()
)

print(
    "NULL customer keys:",
    check["customer_key"].isnull().sum()
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

print(
    "NULL unit_price:",
    check["unit_price"].isnull().sum()
)


print("\n" + "=" * 70)
print("FACT_ORDER CREATED SUCCESSFULLY")
print("=" * 70)