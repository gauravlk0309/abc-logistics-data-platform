import pandas as pd
from sqlalchemy import create_engine, text

# --------------------------------------------------
# PostgreSQL connection
# --------------------------------------------------

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

print("=" * 60)
print("BUILDING GOLD.DIM_SUPPLIER")
print("=" * 60)

# --------------------------------------------------
# 1. Read standardized Silver master
# --------------------------------------------------

df = pd.read_sql(
    "SELECT * FROM silver.supplier_master",
    engine
)

print("\nSilver supplier records:", len(df))

# --------------------------------------------------
# 2. Create surrogate key
# --------------------------------------------------

df.insert(
    0,
    "supplier_key",
    range(1, len(df) + 1)
)

# --------------------------------------------------
# 3. Select dimension columns
# --------------------------------------------------

dim_supplier = df[
    [
        "supplier_key",
        "supplier_id",
        "supplier_name",
        "contact_person",
        "email",
        "phone",
        "city",
        "country",
        "category",
        "onboarded_date",
        "rating"
    ]
]

# --------------------------------------------------
# 4. Create Gold schema
# --------------------------------------------------

with engine.begin() as conn:
    conn.execute(
        text("CREATE SCHEMA IF NOT EXISTS gold")
    )

# --------------------------------------------------
# 5. Load dimension
# --------------------------------------------------

dim_supplier.to_sql(
    "dim_supplier",
    engine,
    schema="gold",
    if_exists="replace",
    index=False
)

# --------------------------------------------------
# 6. Add Primary Key
# --------------------------------------------------

with engine.begin() as conn:
    conn.execute(text("""
        ALTER TABLE gold.dim_supplier
        ADD PRIMARY KEY (supplier_key)
    """))

# --------------------------------------------------
# 7. Validation
# --------------------------------------------------

check = pd.read_sql(
    """
    SELECT *
    FROM gold.dim_supplier
    ORDER BY supplier_key
    """,
    engine
)

print("\nGold dimension:")
print(check.head())

print("\nTotal dimension records:",
      len(check))

print(
    "Duplicate supplier keys:",
    check["supplier_key"].duplicated().sum()
)

print(
    "Duplicate supplier IDs:",
    check["supplier_id"].duplicated().sum()
)

print(
    "NULL supplier keys:",
    check["supplier_key"].isnull().sum()
)

print(
    "NULL supplier IDs:",
    check["supplier_id"].isnull().sum()
)

print("\n" + "=" * 60)
print("DIM_SUPPLIER CREATED SUCCESSFULLY")
print("=" * 60)