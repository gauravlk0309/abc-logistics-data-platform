import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

# Read supplier master
df = pd.read_sql(
    "SELECT * FROM erp_suppliers",
    engine
)

print("=" * 60)
print("ERP SUPPLIERS - STANDARDIZATION")
print("=" * 60)

print("\nBefore standardization:")
print(df.dtypes)

# --------------------------------------------------
# 1. TEXT STANDARDIZATION
# --------------------------------------------------

text_columns = [
    "supplier_id",
    "supplier_name",
    "contact_person",
    "email",
    "phone",
    "city",
    "country",
    "category"
]

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# Standardize supplier ID
df["supplier_id"] = df["supplier_id"].str.upper()

# Standardize email
df["email"] = df["email"].str.lower()

# Standardize location
df["city"] = df["city"].str.title()
df["country"] = df["country"].str.title()

# Standardize category
df["category"] = df["category"].str.title()

# --------------------------------------------------
# 2. DATE STANDARDIZATION
# --------------------------------------------------

df["onboarded_date"] = pd.to_datetime(
    df["onboarded_date"],
    errors="coerce"
)

# --------------------------------------------------
# 3. NUMERIC STANDARDIZATION
# --------------------------------------------------

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

# --------------------------------------------------
# 4. VALIDATION
# --------------------------------------------------

print("\nAfter standardization:")
print(df.dtypes)

print("\nNULL values after conversion:")
print(df.isnull().sum())

print("\nDuplicate supplier IDs:")
print(df["supplier_id"].duplicated().sum())

print("\nRating range:")
print(df["rating"].min(), "-", df["rating"].max())

print("\nSupplier categories:")
print(df["category"].value_counts())

print("\nCountries:")
print(df["country"].value_counts())

# --------------------------------------------------
# 5. SAVE TO SILVER
# --------------------------------------------------

df.to_sql(
    "supplier_master",
    engine,
    schema="silver",
    if_exists="replace",
    index=False
)

print("\nSuccessfully created silver.supplier_master")

# --------------------------------------------------
# 6. FINAL CHECK
# --------------------------------------------------

check = pd.read_sql(
    "SELECT * FROM silver.supplier_master",
    engine
)

print("\nSilver supplier master:")
print(check.head())

print("\nTotal rows:", len(check))