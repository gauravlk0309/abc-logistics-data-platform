import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

# Read staging table
df = pd.read_sql(
    "SELECT * FROM staging.wms_inventory",
    engine
)

print("=" * 60)
print("WMS INVENTORY PROFILING")
print("=" * 60)

# 1. Dataset size
print("\n1. DATASET SIZE")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# 2. Column names
print("\n2. COLUMN NAMES")
print(df.columns.tolist())

# 3. First 5 rows
print("\n3. FIRST 5 ROWS")
print(df.head())

# 4. Data types
print("\n4. DATA TYPES")
print(df.dtypes)

# 5. Missing values
print("\n5. MISSING VALUES")
print(df.isnull().sum())

# 6. Duplicate rows
print("\n6. DUPLICATE ROWS")
print("Duplicate rows:", df.duplicated().sum())

# 7. Duplicate stock record IDs
print("\n7. DUPLICATE STOCK RECORD IDs")
print("Duplicate stock_record_id:",
      df["stock_record_id"].duplicated().sum())

# 8. Statistical summary
print("\n8. STATISTICAL SUMMARY")
print(df.describe())

# 9. Negative values
print("\n9. NEGATIVE VALUES")

print(
    "Negative quantity_on_hand:",
    (df["quantity_on_hand"] < 0).sum()
)

print(
    "Negative reorder_level:",
    (df["reorder_level"] < 0).sum()
)

print(
    "Negative damaged_units:",
    (df["damaged_units"] < 0).sum()
)

# 10. Unique values
print("\n10. UNIQUE VALUES")

print("Warehouses:", df["warehouse_id"].nunique())
print("Products:", df["product_id"].nunique())
print("Units of measure:", df["unit_of_measure"].unique())


print("\nNEGATIVE QUANTITY RECORDS")
print(
    df[df["quantity_on_hand"] < 0][
        [
            "stock_record_id",
            "warehouse_id",
            "product_id",
            "quantity_on_hand",
            "reorder_level"
        ]
    ]
)


print("\n" + "=" * 60)
print("RECORDS REQUIRING CLEANING")
print("=" * 60)

print("\n1. Missing bin_location records:")
print(
    df[df["bin_location"].isna()][
        [
            "stock_record_id",
            "warehouse_id",
            "product_id",
            "bin_location",
            "quantity_on_hand"
        ]
    ].head(20)
)

print("\nTotal missing bin_location:",
      df["bin_location"].isna().sum())

print("\n2. Negative quantity records:")
print(
    df[df["quantity_on_hand"] < 0][
        [
            "stock_record_id",
            "warehouse_id",
            "product_id",
            "quantity_on_hand",
            "reorder_level"
        ]
    ]
)

print("\nTotal negative quantities:",
      (df["quantity_on_hand"] < 0).sum())

print("\n" + "=" * 60)
print("PROFILING COMPLETE")
print("=" * 60)

# ============================================================
# WMS CLEANING
# ============================================================

print("\n" + "=" * 60)
print("WMS CLEANING")
print("=" * 60)

# Keep original row count
original_rows = len(df)

# ------------------------------------------------------------
# 1. Remove completely duplicate rows
# ------------------------------------------------------------

df = df.drop_duplicates()

print("\nAfter removing duplicate rows:", len(df))


# ------------------------------------------------------------
# 2. Remove records with negative inventory quantity
# ------------------------------------------------------------

df = df[df["quantity_on_hand"] >= 0].copy()

print("After removing negative quantities:", len(df))


# ------------------------------------------------------------
# 3. Handle missing bin locations
# ------------------------------------------------------------

df["bin_location"] = df["bin_location"].fillna("UNKNOWN")

print(
    "Missing bin_location after cleaning:",
    df["bin_location"].isna().sum()
)


# ------------------------------------------------------------
# 4. Standardize Unit of Measure
# ------------------------------------------------------------

df["unit_of_measure"] = (
    df["unit_of_measure"]
    .str.strip()
    .str.upper()
    .replace({
        "EACH": "EA"
    })
)

print(
    "Standardized UOM values:",
    df["unit_of_measure"].unique()
)


# ------------------------------------------------------------
# 5. Convert date from string to datetime
# ------------------------------------------------------------

df["last_stock_count_date"] = pd.to_datetime(
    df["last_stock_count_date"],
    errors="coerce"
)

print(
    "Invalid dates after conversion:",
    df["last_stock_count_date"].isna().sum()
)


# ------------------------------------------------------------
# 6. Strip unnecessary spaces from text columns
# ------------------------------------------------------------

text_columns = [
    "stock_record_id",
    "warehouse_id",
    "product_id",
    "bin_location"
]

for col in text_columns:
    df[col] = df[col].str.strip()


# ------------------------------------------------------------
# Cleaning summary
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("CLEANING SUMMARY")
print("=" * 60)

print("Original rows:", original_rows)
print("Final rows:", len(df))
print("Rows removed:", original_rows - len(df))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

print(
    "\nNegative quantity_on_hand:",
    (df["quantity_on_hand"] < 0).sum()
)

print(
    "\nUOM values:",
    df["unit_of_measure"].unique()
)

print("\nData types:")
print(df.dtypes)

# ============================================================
# 6. VALIDATION — AFTER CLEANING
# ============================================================

print("\n" + "=" * 60)
print("WMS DATA VALIDATION")
print("=" * 60)

# 1. Row count
print("\n1. ROW COUNT")
print("Cleaned rows:", len(df))

# 2. Missing values
print("\n2. MISSING VALUES")
print(df.isnull().sum())

# 3. Duplicate rows
print("\n3. DUPLICATE ROWS")
print("Duplicate rows:", df.duplicated().sum())

# 4. Duplicate stock_record_id
print("\n4. DUPLICATE STOCK RECORD IDs")
print(
    "Duplicate IDs:",
    df["stock_record_id"].duplicated().sum()
)

# 5. Negative inventory
print("\n5. NEGATIVE INVENTORY")
print(
    "Negative quantity_on_hand:",
    (df["quantity_on_hand"] < 0).sum()
)

# 6. Negative reorder level
print("\n6. NEGATIVE REORDER LEVEL")
print(
    "Negative reorder_level:",
    (df["reorder_level"] < 0).sum()
)

# 7. Negative damaged units
print("\n7. NEGATIVE DAMAGED UNITS")
print(
    "Negative damaged_units:",
    (df["damaged_units"] < 0).sum()
)

# 8. Date validation
print("\n8. INVALID DATES")
print(
    "Invalid dates:",
    df["last_stock_count_date"].isna().sum()
)

# 9. UOM validation
print("\n9. STANDARDIZED UOM")
print(
    df["unit_of_measure"].unique()
)

# 10. Final data types
print("\n10. DATA TYPES")
print(df.dtypes)

print("\n" + "=" * 60)
print("VALIDATION COMPLETE")
print("=" * 60)

# ============================================================
# 7. LOAD CLEANED DATA INTO SILVER
# ============================================================

print("\n" + "=" * 60)
print("LOADING DATA INTO SILVER")
print("=" * 60)

df.to_sql(
    "wms_inventory",
    engine,
    schema="silver",
    if_exists="append",
    index=False
)

print("\nData successfully loaded into silver.wms_inventory")
print("Rows loaded:", len(df))