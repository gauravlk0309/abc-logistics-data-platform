import pandas as pd
from sqlalchemy import create_engine

# ============================================================
# 1. DATABASE CONNECTION
# ============================================================

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

print("=" * 60)
print("INVENTORY MOVEMENTS - SPRINT 2 PREPROCESSING")
print("=" * 60)


# ============================================================
# 2. READ DATA FROM POSTGRESQL STAGING
# ============================================================

df = pd.read_sql(
    "SELECT * FROM staging.inventory_movements",
    engine
)

print("\nData loaded successfully from staging.inventory_movements")


# ============================================================
# 3. BASIC PROFILING
# ============================================================

print("\n" + "=" * 60)
print("INVENTORY MOVEMENTS PROFILING")
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


# ============================================================
# 4. UNIQUE VALUES / COUNTS
# ============================================================

for col in df.columns:
    print("\n" + "-" * 50)
    print(col)
    print("-" * 50)

    print("Unique values:", df[col].nunique(dropna=True))

    if df[col].nunique(dropna=True) <= 20:
        print(df[col].value_counts(dropna=False))


# ============================================================
# 5. NUMERIC COLUMN STATISTICS
# ============================================================

numeric_columns = df.select_dtypes(
    include=["int64", "float64"]
).columns

print("\n" + "=" * 60)
print("NUMERIC STATISTICS")
print("=" * 60)

for col in numeric_columns:
    print("\n", col)
    print(df[col].describe())

    # ============================================================
# 6. INVENTORY MOVEMENTS INVESTIGATION
# ============================================================

print("\n" + "=" * 60)
print("INVENTORY MOVEMENTS INVESTIGATION")
print("=" * 60)


# ------------------------------------------------------------
# 1. DUPLICATE MOVEMENT IDs
# ------------------------------------------------------------

print("\nDuplicate movement_id:")

duplicate_movements = df[
    df["movement_id"].duplicated(keep=False)
].sort_values("movement_id")

print(duplicate_movements.to_string(index=False))

print("\nNumber of duplicate movement_id:")
print(df["movement_id"].duplicated().sum())


# ------------------------------------------------------------
# 2. MISSING WAREHOUSE IDs
# ------------------------------------------------------------

print("\nMissing warehouse_id:")
print(df["warehouse_id"].isna().sum())

print("\nMissing warehouse_id by movement type:")
print(
    df[df["warehouse_id"].isna()]
    ["movement_type"]
    .value_counts(dropna=False)
)


# ------------------------------------------------------------
# 3. WAREHOUSE ID VALUES
# ------------------------------------------------------------

print("\nWarehouse IDs:")
print(
    df["warehouse_id"]
    .dropna()
    .str.strip()
    .str.upper()
    .value_counts()
)


# ------------------------------------------------------------
# 4. MOVEMENT TYPE INVESTIGATION
# ------------------------------------------------------------

print("\nOriginal movement types:")
print(df["movement_type"].value_counts(dropna=False))

print("\nStandardized movement types:")
print(
    df["movement_type"]
    .str.strip()
    .str.upper()
    .value_counts(dropna=False)
)


# ------------------------------------------------------------
# 5. QUANTITY VALIDATION
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
# 6. MOVEMENT DATE INVESTIGATION
# ------------------------------------------------------------

print("\nMovement date samples:")
print(
    df["movement_date"]
    .head(30)
    .to_string(index=False)
)

parsed_dates = pd.to_datetime(
    df["movement_date"],
    errors="coerce",
    format="mixed"
)

print("\nInvalid movement dates:")
print(parsed_dates.isna().sum())

print("\nMovement date range:")
print("Minimum:", parsed_dates.min())
print("Maximum:", parsed_dates.max())


# ------------------------------------------------------------
# 7. MISSING REQUIRED FIELDS
# ------------------------------------------------------------

print("\nMissing movement_id:")
print(df["movement_id"].isna().sum())

print("\nMissing product_id:")
print(df["product_id"].isna().sum())

print("\nMissing movement_type:")
print(df["movement_type"].isna().sum())

print("\nMissing movement_date:")
print(df["movement_date"].isna().sum())

print("\nMissing reference_doc:")
print(df["reference_doc"].isna().sum())

print("\nMissing handled_by:")
print(df["handled_by"].isna().sum())


# ------------------------------------------------------------
# 8. REFERENCE DOCUMENT DUPLICATES
# ------------------------------------------------------------

print("\nDuplicate reference_doc:")
print(
    df["reference_doc"].duplicated().sum()
)


# ------------------------------------------------------------
# 9. HANDLED BY DUPLICATES
# ------------------------------------------------------------

print("\nUnique handled_by:")
print(df["handled_by"].nunique())

# ============================================================
# 7. INVENTORY MOVEMENTS CLEANING
# ============================================================

print("\n" + "=" * 60)
print("INVENTORY MOVEMENTS CLEANING")
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
    "movement_id",
    "warehouse_id",
    "product_id",
    "movement_type",
    "reference_doc",
    "handled_by"
]

for col in text_columns:
    df[col] = df[col].str.strip()


# ------------------------------------------------------------
# 3. STANDARDIZE WAREHOUSE ID
# ------------------------------------------------------------
# Missing warehouse_id remains NULL

df["warehouse_id"] = df["warehouse_id"].str.upper()


# ------------------------------------------------------------
# 4. STANDARDIZE MOVEMENT TYPE
# ------------------------------------------------------------

df["movement_type"] = df["movement_type"].str.upper()

print("\nStandardized movement types:")
print(df["movement_type"].value_counts())


# ------------------------------------------------------------
# 5. CONVERT MOVEMENT DATE
# ------------------------------------------------------------

df["movement_date"] = pd.to_datetime(
    df["movement_date"],
    errors="coerce",
    format="mixed"
)

print("\nInvalid movement dates after conversion:")
print(df["movement_date"].isna().sum())


# ------------------------------------------------------------
# 6. CLEANING SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("INVENTORY MOVEMENTS CLEANING SUMMARY")
print("=" * 60)

print("Original rows:", original_rows)
print("Final rows:", len(df))
print("Rows removed:", original_rows - len(df))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDuplicate movement_id:")
print(df["movement_id"].duplicated().sum())

print("\nMovement types:")
print(df["movement_type"].value_counts())

print("\nWarehouse IDs:")
print(
    df["warehouse_id"]
    .value_counts(dropna=False)
)

print("\nNegative quantity:")
print((df["quantity"] < 0).sum())

print("\nZero quantity:")
print((df["quantity"] == 0).sum())

print("\nMovement date range:")
print("Minimum:", df["movement_date"].min())
print("Maximum:", df["movement_date"].max())

print("\nData types:")
print(df.dtypes)

# ============================================================
# 8. INVENTORY MOVEMENTS BUSINESS VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("INVENTORY MOVEMENTS BUSINESS VALIDATION")
print("=" * 60)


# ------------------------------------------------------------
# 1. BASIC VALIDATION
# ------------------------------------------------------------

print("\nFinal row count:")
print(len(df))

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDuplicate movement_id:")
print(df["movement_id"].duplicated().sum())


# ------------------------------------------------------------
# 2. REQUIRED FIELD VALIDATION
# ------------------------------------------------------------

print("\nMissing movement_id:")
print(df["movement_id"].isna().sum())

print("\nMissing product_id:")
print(df["product_id"].isna().sum())

print("\nMissing movement_type:")
print(df["movement_type"].isna().sum())

print("\nMissing movement_date:")
print(df["movement_date"].isna().sum())

print("\nMissing reference_doc:")
print(df["reference_doc"].isna().sum())

print("\nMissing handled_by:")
print(df["handled_by"].isna().sum())


# ------------------------------------------------------------
# 3. WAREHOUSE ID
# ------------------------------------------------------------

print("\nMissing warehouse_id:")
print(df["warehouse_id"].isna().sum())


# ------------------------------------------------------------
# 4. QUANTITY VALIDATION
# ------------------------------------------------------------

print("\nNegative quantity:")
print((df["quantity"] < 0).sum())

print("\nZero quantity:")
print((df["quantity"] == 0).sum())


# ------------------------------------------------------------
# 5. MOVEMENT TYPE VALIDATION
# ------------------------------------------------------------

expected_movement_types = {
    "INBOUND",
    "OUTBOUND",
    "RETURN",
    "ADJUSTMENT"
}

actual_movement_types = set(
    df["movement_type"].dropna().unique()
)

print("\nActual movement types:")
print(actual_movement_types)

print("\nUnexpected movement types:")
print(actual_movement_types - expected_movement_types)


# ------------------------------------------------------------
# 6. DATE VALIDATION
# ------------------------------------------------------------

print("\nInvalid movement dates:")
print(df["movement_date"].isna().sum())

print("\nMovement date range:")
print("Minimum:", df["movement_date"].min())
print("Maximum:", df["movement_date"].max())


# ------------------------------------------------------------
# 7. REFERENCE DOCUMENT
# ------------------------------------------------------------

print("\nDuplicate reference_doc:")
print(df["reference_doc"].duplicated().sum())


# ------------------------------------------------------------
# 8. FINAL VALIDATION RESULT
# ------------------------------------------------------------

validation_passed = (
    len(df) == 1400
    and df.duplicated().sum() == 0
    and df["movement_id"].duplicated().sum() == 0
    and df["movement_id"].isna().sum() == 0
    and df["product_id"].isna().sum() == 0
    and df["movement_type"].isna().sum() == 0
    and df["movement_date"].isna().sum() == 0
    and df["reference_doc"].isna().sum() == 0
    and df["handled_by"].isna().sum() == 0
    and (df["quantity"] < 0).sum() == 0
    and (df["quantity"] == 0).sum() == 0
    and len(actual_movement_types - expected_movement_types) == 0
)


print("\n" + "=" * 60)

if validation_passed:
    print("INVENTORY MOVEMENTS BUSINESS VALIDATION PASSED")
else:
    print("INVENTORY MOVEMENTS BUSINESS VALIDATION FAILED")

print("=" * 60)

# ============================================================
# 9. PREPARE DATA FOR SILVER
# ============================================================

print("\n" + "=" * 60)
print("PREPARING INVENTORY MOVEMENTS FOR SILVER")
print("=" * 60)

df["movement_date"] = df["movement_date"].dt.date

print("\nData types before loading:")
print(df.dtypes)

# ============================================================
# 10. LOAD INTO SILVER
# ============================================================

print("\n" + "=" * 60)
print("LOADING INVENTORY MOVEMENTS INTO SILVER")
print("=" * 60)

df.to_sql(
    "inventory_movements",
    engine,
    schema="silver",
    if_exists="append",
    index=False
)

print(
    "\nInventory Movements data loaded successfully "
    "into silver.inventory_movements"
)