import pandas as pd
from sqlalchemy import create_engine, text

# --------------------------------------------------
# PostgreSQL connection
# --------------------------------------------------

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

print("=" * 60)
print("BUILDING GOLD.DIM_CUSTOMER")
print("=" * 60)

# --------------------------------------------------
# 1. Read standardized Silver master
# --------------------------------------------------

df = pd.read_sql(
    "SELECT * FROM silver.customer_master",
    engine
)

print("\nSilver customer records:", len(df))

# --------------------------------------------------
# 2. Create surrogate key
# --------------------------------------------------

df.insert(
    0,
    "customer_key",
    range(1, len(df) + 1)
)

# --------------------------------------------------
# 3. Select dimension columns
# --------------------------------------------------

dim_customer = df[
    [
        "customer_key",
        "customer_id",
        "customer_name",
        "email",
        "phone",
        "city",
        "state",
        "country",
        "region",
        "customer_since",
        "customer_type"
    ]
]

# --------------------------------------------------
# 4. Create Gold schema
# --------------------------------------------------

with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS gold"))

# --------------------------------------------------
# 5. Load dimension
# --------------------------------------------------

dim_customer.to_sql(
    "dim_customer",
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
        ALTER TABLE gold.dim_customer
        ADD PRIMARY KEY (customer_key)
    """))

# --------------------------------------------------
# 7. Validation
# --------------------------------------------------

check = pd.read_sql(
    "SELECT * FROM gold.dim_customer ORDER BY customer_key",
    engine
)

print("\nGold dimension:")
print(check.head())

print("\nTotal dimension records:", len(check))

print(
    "Duplicate customer keys:",
    check["customer_key"].duplicated().sum()
)

print(
    "Duplicate customer IDs:",
    check["customer_id"].duplicated().sum()
)

print(
    "NULL customer keys:",
    check["customer_key"].isnull().sum()
)

print("\n" + "=" * 60)
print("DIM_CUSTOMER CREATED SUCCESSFULLY")
print("=" * 60)