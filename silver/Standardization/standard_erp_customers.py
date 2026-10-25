import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

# Read source customer master
df = pd.read_sql(
    "SELECT * FROM erp_customers",
    engine
)

print("=" * 60)
print("ERP CUSTOMERS - STANDARDIZATION")
print("=" * 60)

print("\nBefore standardization:")
print(df.dtypes)

# --------------------------------------------------
# 1. TEXT STANDARDIZATION
# --------------------------------------------------

text_columns = [
    "customer_id",
    "customer_name",
    "email",
    "phone",
    "city",
    "state",
    "country",
    "region",
    "customer_type"
]

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# Standardize IDs
df["customer_id"] = df["customer_id"].str.upper()

# Standardize email
df["email"] = df["email"].str.lower()

# Standardize location fields
df["city"] = df["city"].str.title()
df["state"] = df["state"].str.title()
df["country"] = df["country"].str.title()
df["region"] = df["region"].str.title()

# Standardize customer type
df["customer_type"] = df["customer_type"].str.title()

# --------------------------------------------------
# 2. DATE STANDARDIZATION
# --------------------------------------------------

df["customer_since"] = pd.to_datetime(
    df["customer_since"],
    errors="coerce"
)

# --------------------------------------------------
# 3. VALIDATION
# --------------------------------------------------

print("\nAfter standardization:")
print(df.dtypes)

print("\nNULL values after conversion:")
print(df.isnull().sum())

print("\nDuplicate customer IDs:")
print(df["customer_id"].duplicated().sum())

print("\nUnique customer types:")
print(df["customer_type"].value_counts())

# --------------------------------------------------
# 4. SAVE TO SILVER
# --------------------------------------------------

df.to_sql(
    "customer_master",
    engine,
    schema="silver",
    if_exists="replace",
    index=False
)

print("\nSuccessfully created silver.customer_master")

# --------------------------------------------------
# 5. FINAL CHECK
# --------------------------------------------------

check = pd.read_sql(
    "SELECT * FROM silver.customer_master",
    engine
)

print("\nSilver customer master:")
print(check.head())

print("\nTotal rows:", len(check))