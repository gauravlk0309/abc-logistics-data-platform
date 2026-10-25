import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

# Read warehouse master
df = pd.read_sql(
    "SELECT * FROM erp_warehouses",
    engine
)

print("=" * 60)
print("ERP WAREHOUSES - STANDARDIZATION")
print("=" * 60)

print("\nBefore standardization:")
print(df.dtypes)

# --------------------------------------------------
# 1. TEXT STANDARDIZATION
# --------------------------------------------------

text_columns = [
    "warehouse_id",
    "warehouse_name",
    "city",
    "state",
    "country",
    "region",
    "manager_name"
]

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# Standardize warehouse ID
df["warehouse_id"] = df["warehouse_id"].str.upper()

# Standardize warehouse name
df["warehouse_name"] = df["warehouse_name"].str.title()

# Standardize location fields
df["city"] = df["city"].str.title()
df["state"] = df["state"].str.title()
df["country"] = df["country"].str.title()
df["region"] = df["region"].str.title()

# --------------------------------------------------
# 2. NUMERIC STANDARDIZATION
# --------------------------------------------------

df["latitude"] = pd.to_numeric(
    df["latitude"],
    errors="coerce"
)

df["longitude"] = pd.to_numeric(
    df["longitude"],
    errors="coerce"
)

df["capacity_sqft"] = pd.to_numeric(
    df["capacity_sqft"],
    errors="coerce"
)

# --------------------------------------------------
# 3. DATE STANDARDIZATION
# --------------------------------------------------

df["operational_since"] = pd.to_datetime(
    df["operational_since"],
    errors="coerce"
)

# --------------------------------------------------
# 4. VALIDATION
# --------------------------------------------------

print("\nAfter standardization:")
print(df.dtypes)

print("\nNULL values after conversion:")
print(df.isnull().sum())

print("\nDuplicate warehouse IDs:")
print(df["warehouse_id"].duplicated().sum())

print("\nLatitude range:")
print(df["latitude"].min(), "-", df["latitude"].max())

print("\nLongitude range:")
print(df["longitude"].min(), "-", df["longitude"].max())

print("\nCapacity range:")
print(df["capacity_sqft"].min(), "-", df["capacity_sqft"].max())

print("\nOperational date range:")
print(
    df["operational_since"].min(),
    "-",
    df["operational_since"].max()
)

print("\nRegions:")
print(df["region"].value_counts())

# --------------------------------------------------
# 5. SAVE TO SILVER
# --------------------------------------------------

df.to_sql(
    "warehouse_master",
    engine,
    schema="silver",
    if_exists="replace",
    index=False
)

print("\nSuccessfully created silver.warehouse_master")

# --------------------------------------------------
# 6. FINAL CHECK
# --------------------------------------------------

check = pd.read_sql(
    "SELECT * FROM silver.warehouse_master",
    engine
)

print("\nSilver warehouse master:")
print(check.head())

print("\nTotal rows:", len(check))