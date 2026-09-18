import pandas as pd
from sqlalchemy import create_engine

# ============================================================
# 1. DATABASE CONNECTION
# ============================================================

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

print("PostgreSQL connection successful!")


# ============================================================
# 2. LOAD TMS DATA
# ============================================================

df = pd.read_sql(
    "SELECT * FROM staging.tms_shipments",
    engine
)


# ============================================================
# 3. PROFILING
# ============================================================

print("\n" + "=" * 60)
print("TMS SHIPMENTS PROFILING")
print("=" * 60)

print("\n1. DATASET SIZE")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\n2. COLUMN NAMES")
print(df.columns.tolist())

print("\n3. FIRST 5 ROWS")
print(df.head().to_string())

print("\n4. DATA TYPES")
print(df.dtypes)

print("\n5. MISSING VALUES")
print(df.isnull().sum())

print("\n6. DUPLICATE ROWS")
print("Duplicate rows:", df.duplicated().sum())

print("\n7. STATISTICAL SUMMARY")
print(df.describe(include="all").transpose())

print("\n8. UNIQUE VALUES")

for col in df.columns:
    print(f"\n{col}:")
    print("Unique count:", df[col].nunique())

print("\n" + "=" * 60)
print("TMS PROFILING COMPLETE")
print("=" * 60)

# ============================================================
# 4. TMS DATA QUALITY INVESTIGATION
# ============================================================

print("\n" + "=" * 60)
print("TMS DATA QUALITY INVESTIGATION")
print("=" * 60)


# ------------------------------------------------------------
# 1. DUPLICATE SHIPMENT IDs
# ------------------------------------------------------------

print("\n1. DUPLICATE SHIPMENT IDs")

duplicate_shipments = df[
    df["shipment_id"].duplicated(keep=False)
].sort_values("shipment_id")

print(duplicate_shipments.to_string(index=False))

print(
    "\nDuplicate shipment ID count:",
    df["shipment_id"].duplicated().sum()
)


# ------------------------------------------------------------
# 2. STATUS VS MISSING ACTUAL DELIVERY DATE
# ------------------------------------------------------------

print("\n2. STATUS VS MISSING ACTUAL DELIVERY DATE")

print(
    pd.crosstab(
        df["status"],
        df["actual_delivery_date"].isna()
    )
)


# ------------------------------------------------------------
# 3. NEGATIVE DISTANCE
# ------------------------------------------------------------

print("\n3. NEGATIVE DISTANCE")

negative_distance = df[df["distance_km"] < 0]

print(
    negative_distance[
        [
            "shipment_id",
            "origin_city",
            "destination_city",
            "distance_km",
            "weight_kg",
            "freight_cost_usd"
        ]
    ].to_string(index=False)
)

print(
    "\nTotal negative distance records:",
    len(negative_distance)
)


# ------------------------------------------------------------
# 4. OTHER NEGATIVE NUMERIC VALUES
# ------------------------------------------------------------

print("\n4. NEGATIVE NUMERIC VALUES")

print(
    "Negative distance:",
    (df["distance_km"] < 0).sum()
)

print(
    "Negative weight:",
    (df["weight_kg"] < 0).sum()
)

print(
    "Negative freight cost:",
    (df["freight_cost_usd"] < 0).sum()
)


# ------------------------------------------------------------
# 5. DATE CONVERSION CHECK
# ------------------------------------------------------------

print("\n5. DATE CONVERSION CHECK")

date_columns = [
    "ship_date",
    "expected_delivery_date",
    "actual_delivery_date"
]

for col in date_columns:

    converted = pd.to_datetime(
        df[col],
        errors="coerce"
    )

    print(
        col,
        "invalid dates:",
        converted.isna().sum()
    )


# ------------------------------------------------------------
# 6. STATUS VALUES
# ------------------------------------------------------------

print("\n6. STATUS VALUES")

print(df["status"].value_counts())


# ------------------------------------------------------------
# 7. CARRIER VALUES
# ------------------------------------------------------------

print("\n7. CARRIER VALUES")

print(df["carrier"].value_counts())


# ------------------------------------------------------------
# 8. WAREHOUSE ID VALUES
# ------------------------------------------------------------

print("\n8. WAREHOUSE IDs")

print(
    sorted(df["warehouse_id"].unique())
)


print("\n" + "=" * 60)
print("DATA QUALITY INVESTIGATION COMPLETE")
print("=" * 60)

# ============================================================
# 5. TMS CLEANING
# ============================================================

print("\n" + "=" * 60)
print("TMS CLEANING")
print("=" * 60)

original_rows = len(df)


# ------------------------------------------------------------
# 1. REMOVE DUPLICATE ROWS
# ------------------------------------------------------------

df = df.drop_duplicates().copy()

print("\nAfter removing duplicate rows:", len(df))


# ------------------------------------------------------------
# 2. REMOVE NEGATIVE DISTANCE
# ------------------------------------------------------------

df = df[df["distance_km"] >= 0].copy()

print(
    "After removing negative distance records:",
    len(df)
)


# ------------------------------------------------------------
# 3. STANDARDIZE WAREHOUSE IDs
# ------------------------------------------------------------

df["warehouse_id"] = (
    df["warehouse_id"]
    .str.strip()
    .str.upper()
)

print(
    "\nUnique warehouse IDs after standardization:",
    df["warehouse_id"].nunique()
)


# ------------------------------------------------------------
# 4. CONVERT DATE COLUMNS
# ------------------------------------------------------------

date_columns = [
    "ship_date",
    "expected_delivery_date",
    "actual_delivery_date"
]

for col in date_columns:

    df[col] = pd.to_datetime(
        df[col],
        errors="coerce"
    )


# ------------------------------------------------------------
# 5. REMOVE EXTRA WHITESPACE FROM TEXT COLUMNS
# ------------------------------------------------------------

text_columns = [
    "shipment_id",
    "order_ref",
    "warehouse_id",
    "customer_id",
    "vehicle_id",
    "carrier",
    "status",
    "origin_city",
    "destination_city"
]

for col in text_columns:

    df[col] = df[col].str.strip()


# ------------------------------------------------------------
# 6. CLEANING SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("TMS CLEANING SUMMARY")
print("=" * 60)

print("Original rows:", original_rows)
print("Final rows:", len(df))
print("Rows removed:", original_rows - len(df))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDuplicate shipment IDs:")
print(df["shipment_id"].duplicated().sum())

print("\nNegative distance:")
print((df["distance_km"] < 0).sum())

print("\nWarehouse IDs:")
print(sorted(df["warehouse_id"].unique()))

print("\nData types:")
print(df.dtypes)

# ============================================================
# 6. TMS BUSINESS RULE VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("TMS BUSINESS RULE VALIDATION")
print("=" * 60)


# ------------------------------------------------------------
# 1. EXPECTED DELIVERY BEFORE SHIP DATE
# ------------------------------------------------------------

invalid_expected_dates = df[
    df["expected_delivery_date"] < df["ship_date"]
]

print("\n1. EXPECTED DELIVERY BEFORE SHIP DATE")

print(
    "Invalid records:",
    len(invalid_expected_dates)
)

if len(invalid_expected_dates) > 0:
    print(
        invalid_expected_dates[
            [
                "shipment_id",
                "ship_date",
                "expected_delivery_date"
            ]
        ].to_string(index=False)
    )


# ------------------------------------------------------------
# 2. ACTUAL DELIVERY BEFORE SHIP DATE
# ------------------------------------------------------------

invalid_actual_dates = df[
    df["actual_delivery_date"].notna()
    &
    (
        df["actual_delivery_date"]
        < df["ship_date"]
    )
]

print("\n2. ACTUAL DELIVERY BEFORE SHIP DATE")

print(
    "Invalid records:",
    len(invalid_actual_dates)
)

if len(invalid_actual_dates) > 0:
    print(
        invalid_actual_dates[
            [
                "shipment_id",
                "ship_date",
                "actual_delivery_date"
            ]
        ].to_string(index=False)
    )


# ------------------------------------------------------------
# 3. ACTUAL DELIVERY BEFORE EXPECTED DELIVERY
# ------------------------------------------------------------

early_deliveries = df[
    df["actual_delivery_date"].notna()
    &
    (
        df["actual_delivery_date"]
        < df["expected_delivery_date"]
    )
]

print("\n3. ACTUAL DELIVERY BEFORE EXPECTED DELIVERY")

print(
    "Records delivered early:",
    len(early_deliveries)
)


# ------------------------------------------------------------
# 4. STATUS VS ACTUAL DELIVERY DATE
# ------------------------------------------------------------

print("\n4. STATUS VS ACTUAL DELIVERY DATE")

status_date_check = pd.crosstab(
    df["status"],
    df["actual_delivery_date"].isna()
)

print(status_date_check)


# ------------------------------------------------------------
# 5. FINAL NUMERIC VALIDATION
# ------------------------------------------------------------

print("\n5. NUMERIC VALIDATION")

print(
    "Negative distance:",
    (df["distance_km"] < 0).sum()
)

print(
    "Negative weight:",
    (df["weight_kg"] < 0).sum()
)

print(
    "Negative freight cost:",
    (df["freight_cost_usd"] < 0).sum()
)


# ------------------------------------------------------------
# 6. FINAL DUPLICATE VALIDATION
# ------------------------------------------------------------

print("\n6. DUPLICATE VALIDATION")

print(
    "Duplicate rows:",
    df.duplicated().sum()
)

print(
    "Duplicate shipment IDs:",
    df["shipment_id"].duplicated().sum()
)


# ------------------------------------------------------------
# 7. MISSING VALUE VALIDATION
# ------------------------------------------------------------

print("\n7. MISSING VALUE VALIDATION")

print(df.isnull().sum())


print("\n" + "=" * 60)
print("TMS BUSINESS VALIDATION COMPLETE")
print("=" * 60)

# ============================================================
# 7. LOAD CLEANED TMS DATA INTO SILVER
# ============================================================

print("\n" + "=" * 60)
print("LOADING TMS DATA INTO SILVER")
print("=" * 60)

df.to_sql(
    "tms_shipments",
    engine,
    schema="silver",
    if_exists="append",
    index=False
)

print("\nTMS data successfully loaded into silver.tms_shipments")
print("Rows loaded:", len(df))