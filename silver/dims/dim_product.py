import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

print("=" * 60)
print("BUILDING GOLD.DIM_PRODUCT")
print("=" * 60)

# 1. Read ERP product master
df = pd.read_sql(
    "SELECT * FROM erp_products",
    engine
)

print("\nERP product records:", len(df))

# 2. Clean / standardize numeric columns
df["unit_weight_kg"] = pd.to_numeric(
    df["unit_weight_kg"],
    errors="coerce"
)

df["unit_price"] = pd.to_numeric(
    df["unit_price"],
    errors="coerce"
)

# Standardize text fields
df["product_id"] = df["product_id"].astype(str).str.strip().str.upper()
df["product_name"] = df["product_name"].astype(str).str.strip()
df["category"] = df["category"].astype(str).str.strip().str.title()
df["supplier_id"] = df["supplier_id"].astype(str).str.strip().str.upper()

# 3. Create surrogate key
df.insert(
    0,
    "product_key",
    range(1, len(df) + 1)
)

# 4. Select dimension columns
dim_product = df[
    [
        "product_key",
        "product_id",
        "product_name",
        "category",
        "unit_weight_kg",
        "unit_price",
        "supplier_id"
    ]
]

# 5. Create Gold schema
with engine.begin() as conn:
    conn.execute(
        text("CREATE SCHEMA IF NOT EXISTS gold")
    )

# 6. Load into Gold
dim_product.to_sql(
    "dim_product",
    engine,
    schema="gold",
    if_exists="replace",
    index=False
)

# 7. Add primary key
with engine.begin() as conn:
    conn.execute(text("""
        ALTER TABLE gold.dim_product
        ADD PRIMARY KEY (product_key)
    """))

# 8. Verify
check = pd.read_sql(
    """
    SELECT *
    FROM gold.dim_product
    ORDER BY product_key
    """,
    engine
)

print("\nGold dimension:")
print(check.head())

print("\nTotal dimension records:",
      len(check))

print(
    "Duplicate product keys:",
    check["product_key"].duplicated().sum()
)

print(
    "Duplicate product IDs:",
    check["product_id"].duplicated().sum()
)

print(
    "NULL product keys:",
    check["product_key"].isnull().sum()
)

print(
    "NULL product IDs:",
    check["product_id"].isnull().sum()
)

print(
    "NULL unit weight:",
    check["unit_weight_kg"].isnull().sum()
)

print(
    "NULL unit price:",
    check["unit_price"].isnull().sum()
)

print("\n" + "=" * 60)
print("DIM_PRODUCT CREATED SUCCESSFULLY")
print("=" * 60)