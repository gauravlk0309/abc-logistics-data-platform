import pandas as pd
from sqlalchemy import create_engine

# ============================================================
# 1. DATABASE CONNECTION
# ============================================================

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

print("=" * 60)
print("OMS ORDERS - SPRINT 2 PREPROCESSING")
print("=" * 60)


# ============================================================
# 2. READ DATA FROM POSTGRESQL STAGING
# ============================================================

df = pd.read_sql(
    "SELECT * FROM staging.oms_orders",
    engine
)

print("\nData loaded successfully from staging.oms_orders")


# ============================================================
# 3. BASIC PROFILING
# ============================================================

print("\n" + "=" * 60)
print("OMS PROFILING")
print("=" * 60)

print("\nRows:", len(df))
print("Columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDuplicate order_id:")
print(df["order_id"].duplicated().sum())

print("\nOrder status:")
print(df["status"].value_counts(dropna=False))

print("\nPriority:")
print(df["priority"].value_counts(dropna=False))

print("\nDate samples:")
print(df["order_date"].head(20).to_string(index=False))

print("\nQuantity statistics:")
print(df["quantity"].describe())

print("\nUnit price statistics:")
print(df["unit_price"].describe())

print("\nEmail samples:")
print(df["email"].head(10).to_string(index=False))

# ============================================================
# 4. OMS INVESTIGATION
# ============================================================

print("\n" + "=" * 60)
print("OMS INVESTIGATION")
print("=" * 60)


# ------------------------------------------------------------
# 1. INVESTIGATE DUPLICATE ORDER IDs
# ------------------------------------------------------------

print("\nDuplicate order IDs:")

duplicate_orders = df[
    df["order_id"].duplicated(keep=False)
].sort_values("order_id")

print(duplicate_orders.to_string(index=False))


# Check whether duplicate rows are exact duplicates
print("\nExact duplicate rows:")
print(df.duplicated().sum())


# ------------------------------------------------------------
# 2. INVESTIGATE MISSING EMAILS
# ------------------------------------------------------------

print("\nMissing emails:")
print(df["email"].isna().sum())

print("\nMissing email by status:")
print(
    df[df["email"].isna()]
    ["status"]
    .value_counts(dropna=False)
)


# ------------------------------------------------------------
# 3. INVESTIGATE MISSING PRIORITY
# ------------------------------------------------------------

print("\nMissing priority:")
print(df["priority"].isna().sum())

print("\nMissing priority by status:")
print(
    df[df["priority"].isna()]
    ["status"]
    .value_counts(dropna=False)
)


# ------------------------------------------------------------
# 4. INVESTIGATE STATUS VALUES
# ------------------------------------------------------------

print("\nOriginal status values:")
print(df["status"].value_counts(dropna=False))

print("\nStatus values after uppercase:")
print(
    df["status"]
    .str.strip()
    .str.upper()
    .value_counts(dropna=False)
)


# ------------------------------------------------------------
# 5. INVESTIGATE PRIORITY VALUES
# ------------------------------------------------------------

print("\nOriginal priority values:")
print(df["priority"].value_counts(dropna=False))

print("\nPriority values after standardization:")
print(
    df["priority"]
    .dropna()
    .str.strip()
    .str.upper()
    .value_counts()
)


# ------------------------------------------------------------
# 6. INVESTIGATE QUANTITY
# ------------------------------------------------------------

print("\nNegative quantity:")
print((df["quantity"] < 0).sum())

print("\nZero quantity:")
print((df["quantity"] == 0).sum())

print("\nQuantity range:")
print(
    "Minimum:", df["quantity"].min(),
    "| Maximum:", df["quantity"].max()
)


# ------------------------------------------------------------
# 7. INVESTIGATE UNIT PRICE
# ------------------------------------------------------------

print("\nNegative unit price:")
print((df["unit_price"] < 0).sum())

print("\nZero unit price:")
print((df["unit_price"] == 0).sum())

print("\nUnit price range:")
print(
    "Minimum:", df["unit_price"].min(),
    "| Maximum:", df["unit_price"].max()
)


# ------------------------------------------------------------
# 8. INVESTIGATE ORDER DATE FORMATS
# ------------------------------------------------------------

print("\nUnique order date values:")
print(df["order_date"].head(50).to_string(index=False))


# Try parsing dates
parsed_dates = pd.to_datetime(
    df["order_date"],
    errors="coerce",
    format="mixed"
)

print("\nInvalid dates after mixed-format parsing:")
print(parsed_dates.isna().sum())


# ------------------------------------------------------------
# 9. DATE RANGE
# ------------------------------------------------------------

print("\nOrder date range:")

print("Minimum date:", parsed_dates.min())
print("Maximum date:", parsed_dates.max())


# ------------------------------------------------------------
# 10. CHECK IDs FOR MISSING VALUES
# ------------------------------------------------------------

print("\nMissing order IDs:")
print(df["order_id"].isna().sum())

print("\nMissing customer IDs:")
print(df["customer_id"].isna().sum())

print("\nMissing product IDs:")
print(df["product_id"].isna().sum())

# ============================================================
# 5. OMS CLEANING
# ============================================================

print("\n" + "=" * 60)
print("OMS CLEANING")
print("=" * 60)

original_rows = len(df)


# ------------------------------------------------------------
# 1. REMOVE EXACT DUPLICATE ROWS
# ------------------------------------------------------------

df = df.drop_duplicates().copy()

print("\nAfter removing duplicate rows:", len(df))


# ------------------------------------------------------------
# 2. STANDARDIZE TEXT COLUMNS
# ------------------------------------------------------------

text_columns = [
    "order_id",
    "customer_id",
    "product_id",
    "status",
    "email",
    "priority"
]

for col in text_columns:
    df[col] = df[col].str.strip()


# ------------------------------------------------------------
# 3. STANDARDIZE STATUS
# ------------------------------------------------------------

df["status"] = df["status"].str.upper()

print("\nStandardized status values:")
print(df["status"].value_counts())


# ------------------------------------------------------------
# 4. STANDARDIZE PRIORITY
# ------------------------------------------------------------

df["priority"] = df["priority"].str.upper()

print("\nStandardized priority values:")
print(df["priority"].value_counts(dropna=False))


# ------------------------------------------------------------
# 5. CONVERT ORDER DATE
# ------------------------------------------------------------

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce",
    format="mixed"
)

print("\nInvalid order dates after conversion:")
print(df["order_date"].isna().sum())


# ------------------------------------------------------------
# 6. NUMERIC VALIDATION
# ------------------------------------------------------------

print("\nNegative quantity:")
print((df["quantity"] < 0).sum())

print("\nZero quantity:")
print((df["quantity"] == 0).sum())

print("\nNegative unit price:")
print((df["unit_price"] < 0).sum())

print("\nZero unit price:")
print((df["unit_price"] == 0).sum())


# ------------------------------------------------------------
# 7. CLEANING SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("OMS CLEANING SUMMARY")
print("=" * 60)

print("Original rows:", original_rows)
print("Final rows:", len(df))
print("Rows removed:", original_rows - len(df))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDuplicate order_id:")
print(df["order_id"].duplicated().sum())

print("\nStatus values:")
print(df["status"].value_counts())

print("\nPriority values:")
print(df["priority"].value_counts(dropna=False))

print("\nOrder date range:")
print("Minimum:", df["order_date"].min())
print("Maximum:", df["order_date"].max())

print("\nData types:")
print(df.dtypes)

# ============================================================
# 6. OMS BUSINESS VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("OMS BUSINESS VALIDATION")
print("=" * 60)


# ------------------------------------------------------------
# 1. BASIC VALIDATION
# ------------------------------------------------------------

print("\nFinal row count:")
print(len(df))

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDuplicate order_id:")
print(df["order_id"].duplicated().sum())


# ------------------------------------------------------------
# 2. REQUIRED ID VALIDATION
# ------------------------------------------------------------

print("\nMissing order_id:")
print(df["order_id"].isna().sum())

print("\nMissing customer_id:")
print(df["customer_id"].isna().sum())

print("\nMissing product_id:")
print(df["product_id"].isna().sum())


# ------------------------------------------------------------
# 3. QUANTITY VALIDATION
# ------------------------------------------------------------

print("\nNegative quantity:")
print((df["quantity"] < 0).sum())

print("\nZero quantity:")
print((df["quantity"] == 0).sum())


# ------------------------------------------------------------
# 4. UNIT PRICE VALIDATION
# ------------------------------------------------------------

print("\nNegative unit price:")
print((df["unit_price"] < 0).sum())

print("\nZero unit price:")
print((df["unit_price"] == 0).sum())


# ------------------------------------------------------------
# 5. DATE VALIDATION
# ------------------------------------------------------------

print("\nMissing order dates:")
print(df["order_date"].isna().sum())


# ------------------------------------------------------------
# 6. STATUS VALIDATION
# ------------------------------------------------------------

expected_statuses = {
    "DELIVERED",
    "SHIPPED",
    "PLACED",
    "CANCELLED",
    "PROCESSING",
    "CONFIRMED"
}

actual_statuses = set(df["status"].dropna().unique())

print("\nActual statuses:")
print(actual_statuses)

print("\nUnexpected statuses:")
print(actual_statuses - expected_statuses)


# ------------------------------------------------------------
# 7. PRIORITY VALIDATION
# ------------------------------------------------------------

expected_priorities = {
    "STANDARD",
    "EXPRESS"
}

actual_priorities = set(
    df["priority"].dropna().unique()
)

print("\nActual priorities:")
print(actual_priorities)

print("\nUnexpected priorities:")
print(actual_priorities - expected_priorities)


# ------------------------------------------------------------
# 8. MISSING EMAIL / PRIORITY
# ------------------------------------------------------------

print("\nMissing emails:")
print(df["email"].isna().sum())

print("\nMissing priorities:")
print(df["priority"].isna().sum())


# ------------------------------------------------------------
# 9. DATE RANGE
# ------------------------------------------------------------

print("\nOrder date range:")
print("Minimum:", df["order_date"].min())
print("Maximum:", df["order_date"].max())


# ------------------------------------------------------------
# 10. FINAL VALIDATION RESULT
# ------------------------------------------------------------

validation_passed = (
    len(df) == 1200
    and df.duplicated().sum() == 0
    and df["order_id"].duplicated().sum() == 0
    and df["order_id"].isna().sum() == 0
    and df["customer_id"].isna().sum() == 0
    and df["product_id"].isna().sum() == 0
    and (df["quantity"] < 0).sum() == 0
    and (df["quantity"] == 0).sum() == 0
    and (df["unit_price"] < 0).sum() == 0
    and (df["unit_price"] == 0).sum() == 0
    and df["order_date"].isna().sum() == 0
    and len(actual_statuses - expected_statuses) == 0
    and len(actual_priorities - expected_priorities) == 0
)


print("\n" + "=" * 60)

if validation_passed:
    print("OMS BUSINESS VALIDATION PASSED")
else:
    print("OMS BUSINESS VALIDATION FAILED")

print("=" * 60)

# ============================================================
# 7. PREPARE DATA FOR SILVER
# ============================================================

print("\n" + "=" * 60)
print("PREPARING OMS DATA FOR SILVER")
print("=" * 60)

# Convert pandas datetime to Python date
df["order_date"] = df["order_date"].dt.date

print("\nData types before loading:")
print(df.dtypes)

# ============================================================
# 8. LOAD INTO SILVER
# ============================================================

print("\n" + "=" * 60)
print("LOADING OMS DATA INTO SILVER")
print("=" * 60)

df.to_sql(
    "oms_orders",
    engine,
    schema="silver",
    if_exists="append",
    index=False
)

print("\nOMS data loaded successfully into silver.oms_orders")