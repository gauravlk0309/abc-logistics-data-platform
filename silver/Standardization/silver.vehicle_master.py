import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

# Read source master
df = pd.read_sql(
    "SELECT * FROM erp_vehicles",
    engine
)

print("Before standardization:")
print(df.dtypes)

# ---------------------------------------------
# TEXT STANDARDIZATION
# ---------------------------------------------

text_columns = [
    "vehicle_id",
    "vehicle_type",
    "registration_number",
    "fuel_type",
    "home_warehouse_id",
    "driver_name",
    "driver_license_no",
    "status"
]

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# Standardize selected categorical fields
df["vehicle_type"] = df["vehicle_type"].str.title()
df["fuel_type"] = df["fuel_type"].str.title()
df["status"] = df["status"].str.title()

# Standardize IDs
df["vehicle_id"] = df["vehicle_id"].str.upper()
df["registration_number"] = df["registration_number"].str.upper()
df["home_warehouse_id"] = df["home_warehouse_id"].str.upper()
df["driver_license_no"] = df["driver_license_no"].str.upper()

# ---------------------------------------------
# NUMERIC STANDARDIZATION
# ---------------------------------------------

df["capacity_kg"] = pd.to_numeric(
    df["capacity_kg"],
    errors="coerce"
)

df["manufacture_year"] = pd.to_numeric(
    df["manufacture_year"],
    errors="coerce"
).astype("Int64")

# ---------------------------------------------
# VALIDATION AFTER STANDARDIZATION
# ---------------------------------------------

print("\nAfter standardization:")
print(df.dtypes)

print("\nNULL values after conversion:")
print(df.isnull().sum())

print("\nDuplicate vehicle IDs:")
print(df["vehicle_id"].duplicated().sum())

# ---------------------------------------------
# SAVE TO SILVER
# ---------------------------------------------

df.to_sql(
    "vehicle_master",
    engine,
    schema="silver",
    if_exists="replace",
    index=False
)

print("\nSuccessfully created silver.vehicle_master")

# ---------------------------------------------
# FINAL CHECK
# ---------------------------------------------

check = pd.read_sql(
    "SELECT * FROM silver.vehicle_master",
    engine
)

print("\nSilver vehicle master:")
print(check.head())

print("\nTotal rows:", len(check))