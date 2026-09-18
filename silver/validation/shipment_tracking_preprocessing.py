import pandas as pd
from sqlalchemy import create_engine

# ============================================================
# DATABASE CONNECTION
# ============================================================

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

print("=" * 60)
print("SHIPMENT TRACKING - SPRINT 2 PREPROCESSING")
print("=" * 60)

# ============================================================
# LOAD DATA FROM STAGING
# ============================================================

df = pd.read_sql(
    "SELECT * FROM staging.shipment_tracking",
    engine
)

print("\nData loaded successfully from staging.shipment_tracking")

# ============================================================
# PROFILING
# ============================================================

print("\n" + "=" * 60)
print("SHIPMENT TRACKING PROFILING")
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
# UNIQUE VALUES
# ============================================================

for col in df.columns:

    print("\n" + "-" * 50)
    print(col)
    print("-" * 50)

    print("Unique values:", df[col].nunique(dropna=True))

    if df[col].nunique(dropna=True) <= 20:
        print(df[col].value_counts(dropna=False))

# ============================================================
# NUMERIC STATISTICS
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
# SHIPMENT TRACKING - INVESTIGATION
# ============================================================

print("\n" + "=" * 60)
print("SHIPMENT TRACKING INVESTIGATION")
print("=" * 60)


# ============================================================
# 1. DUPLICATE TRACKING EVENT IDs
# ============================================================

print("\n" + "-" * 60)
print("1. DUPLICATE TRACKING EVENT IDs")
print("-" * 60)

duplicate_ids = df[
    df["tracking_event_id"].duplicated(keep=False)
]

print("Duplicate tracking_event_id count:",
      duplicate_ids["tracking_event_id"].nunique())

if len(duplicate_ids) > 0:
    print(duplicate_ids[
        ["tracking_event_id", "shipment_id", "event_type"]
    ])
else:
    print("No duplicate tracking_event_id found.")


# ============================================================
# 2. EVENT TYPE VALUES
# ============================================================

print("\n" + "-" * 60)
print("2. EVENT TYPE VALUES")
print("-" * 60)

print(df["event_type"].value_counts())


# ============================================================
# 3. EVENT TIMESTAMP INVESTIGATION
# ============================================================

print("\n" + "-" * 60)
print("3. EVENT TIMESTAMP INVESTIGATION")
print("-" * 60)

parsed_timestamp = pd.to_datetime(
    df["event_timestamp"],
    errors="coerce",
    format="mixed"
)

print("Invalid timestamps:",
      parsed_timestamp.isna().sum())

print("Minimum timestamp:",
      parsed_timestamp.min())

print("Maximum timestamp:",
      parsed_timestamp.max())


# ============================================================
# 4. LOCATION MISSING VALUES
# ============================================================

print("\n" + "-" * 60)
print("4. LOCATION INVESTIGATION")
print("-" * 60)

print("Missing location:",
      df["location"].isna().sum())

print("\nExamples of missing location:")

print(
    df[df["location"].isna()][
        ["tracking_event_id",
         "shipment_id",
         "event_type",
         "event_timestamp",
         "scanned_by",
         "remarks"]
    ].head(10)
)


# ============================================================
# 5. SCANNED_BY INVESTIGATION
# ============================================================

print("\n" + "-" * 60)
print("5. SCANNED_BY INVESTIGATION")
print("-" * 60)

print("Missing scanned_by:",
      df["scanned_by"].isna().sum())

print("\nMissing scanned_by by event type:")

print(
    df.groupby("event_type")["scanned_by"]
      .apply(lambda x: x.isna().sum())
      .sort_values(ascending=False)
)


# ============================================================
# 6. REMARKS INVESTIGATION
# ============================================================

print("\n" + "-" * 60)
print("6. REMARKS INVESTIGATION")
print("-" * 60)

print("Missing remarks:",
      df["remarks"].isna().sum())

print("\nRemarks by event type:")

print(
    pd.crosstab(
        df["event_type"],
        df["remarks"],
        dropna=False
    )
)


# ============================================================
# 7. LOCATION + EVENT TYPE
# ============================================================

print("\n" + "-" * 60)
print("7. LOCATION MISSING BY EVENT TYPE")
print("-" * 60)

print(
    df.groupby("event_type")["location"]
      .apply(lambda x: x.isna().sum())
      .sort_values(ascending=False)
)


# ============================================================
# 8. SHIPMENT EVENT COUNTS
# ============================================================

print("\n" + "-" * 60)
print("8. EVENTS PER SHIPMENT")
print("-" * 60)

events_per_shipment = df.groupby(
    "shipment_id"
).size()

print(events_per_shipment.describe())

print("\nShipments with most tracking events:")

print(
    events_per_shipment
    .sort_values(ascending=False)
    .head(10)
)


# ============================================================
# 9. TEXT CLEANING CHECK
# ============================================================

print("\n" + "-" * 60)
print("9. TEXT FORMAT CHECK")
print("-" * 60)

text_columns = [
    "tracking_event_id",
    "shipment_id",
    "event_type",
    "location",
    "scanned_by",
    "remarks"
]

for col in text_columns:

    leading_trailing = (
        df[col].dropna()
        .astype(str)
        .apply(lambda x: x != x.strip())
        .sum()
    )

    print(
        f"{col}: {leading_trailing} "
        "values with leading/trailing spaces"
    )


# ============================================================
# 10. EVENT TIMESTAMP ORDER
# ============================================================

print("\n" + "-" * 60)
print("10. TIMESTAMP ORDER INVESTIGATION")
print("-" * 60)

df["parsed_timestamp"] = parsed_timestamp

out_of_order = 0

for shipment_id, group in df.groupby("shipment_id"):

    timestamps = group["parsed_timestamp"]

    if not timestamps.is_monotonic_increasing:
        out_of_order += 1

print(
    "Shipments with events not in timestamp order:",
    out_of_order
)


# ============================================================
# 11. FINAL INVESTIGATION SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("SHIPMENT TRACKING INVESTIGATION COMPLETED")
print("=" * 60)

# ============================================================
# SHIPMENT TRACKING - CLEANING
# ============================================================

print("\n" + "=" * 60)
print("SHIPMENT TRACKING CLEANING")
print("=" * 60)

# Store original row count
original_rows = len(df)

# ============================================================
# 1. REMOVE DUPLICATE ROWS
# ============================================================

df = df.drop_duplicates().copy()

print("\nDuplicate rows removed:",
      original_rows - len(df))


# ============================================================
# 2. STRIP TEXT COLUMNS
# ============================================================

text_columns = [
    "tracking_event_id",
    "shipment_id",
    "event_type",
    "location",
    "scanned_by",
    "remarks"
]

for col in text_columns:
    df[col] = df[col].str.strip()


# ============================================================
# 3. STANDARDIZE EVENT TYPE
# ============================================================

df["event_type"] = df["event_type"].str.strip()

print("\nEvent types after standardization:")
print(df["event_type"].value_counts())


# ============================================================
# 4. PARSE EVENT TIMESTAMP
# ============================================================

df["event_timestamp"] = pd.to_datetime(
    df["event_timestamp"],
    errors="coerce",
    format="mixed"
)

print("\nInvalid timestamps after parsing:",
      df["event_timestamp"].isna().sum())


# ============================================================
# 5. PRESERVE OPTIONAL MISSING VALUES
# ============================================================

# location:
# Missing values are preserved as NULL.

# scanned_by:
# Missing values are preserved as NULL.

# remarks:
# Missing values are preserved as NULL.


# ============================================================
# 6. FINAL CLEANING SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("SHIPMENT TRACKING CLEANING SUMMARY")
print("=" * 60)

print("\nOriginal rows:", original_rows)
print("Final rows:", len(df))
print("Rows removed:", original_rows - len(df))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDuplicate tracking_event_id:")
print(
    df["tracking_event_id"].duplicated().sum()
)

print("\nData types:")
print(df.dtypes)

print("\nEvent types:")
print(df["event_type"].value_counts())

print("\nTimestamp range:")
print(df["event_timestamp"].min())
print(df["event_timestamp"].max())

# ============================================================
# SHIPMENT TRACKING BUSINESS VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("SHIPMENT TRACKING BUSINESS VALIDATION")
print("=" * 60)

# ============================================================
# 1. FINAL ROW COUNT
# ============================================================

print("\nFinal row count:")
print(len(df))


# ============================================================
# 2. DUPLICATE ROWS
# ============================================================

print("\nDuplicate rows:")
print(df.duplicated().sum())


# ============================================================
# 3. DUPLICATE TRACKING EVENT ID
# ============================================================

print("\nDuplicate tracking_event_id:")

print(
    df["tracking_event_id"].duplicated().sum()
)


# ============================================================
# 4. REQUIRED FIELD VALIDATION
# ============================================================

required_columns = [
    "tracking_event_id",
    "shipment_id",
    "event_type",
    "event_timestamp"
]

print("\nMissing required fields:")

required_missing = 0

for col in required_columns:

    missing = df[col].isna().sum()

    print(f"{col} : {missing}")

    required_missing += missing


# ============================================================
# 5. EVENT TYPE VALIDATION
# ============================================================

valid_event_types = {
    "In Transit",
    "Arrived at Hub",
    "Picked Up",
    "Delivery Exception",
    "Departed Facility",
    "Delivered",
    "Customs Clearance",
    "Out for Delivery"
}

actual_event_types = set(
    df["event_type"].dropna().unique()
)

unexpected_event_types = (
    actual_event_types - valid_event_types
)

print("\nActual event types:")
print(actual_event_types)

print("\nUnexpected event types:")
print(unexpected_event_types)


# ============================================================
# 6. TIMESTAMP VALIDATION
# ============================================================

print("\nMissing event timestamps:")
print(df["event_timestamp"].isna().sum())

print("\nInvalid event timestamps:")
print(
    pd.to_datetime(
        df["event_timestamp"],
        errors="coerce"
    ).isna().sum()
)


# ============================================================
# 7. EMPTY STRING CHECK
# ============================================================

print("\nEmpty required string fields:")

for col in [
    "tracking_event_id",
    "shipment_id",
    "event_type"
]:

    empty_count = (
        df[col].fillna("").astype(str).str.strip().eq("").sum()
    )

    print(f"{col} : {empty_count}")


# ============================================================
# 8. SHIPMENT ID VALIDATION
# ============================================================

print("\nMissing shipment_id:")
print(df["shipment_id"].isna().sum())

print("\nUnique shipments:")
print(df["shipment_id"].nunique())


# ============================================================
# 9. FINAL VALIDATION RESULT
# ============================================================

validation_passed = (
    len(df) == 2000
    and df.duplicated().sum() == 0
    and df["tracking_event_id"].duplicated().sum() == 0
    and required_missing == 0
    and len(unexpected_event_types) == 0
    and df["event_timestamp"].isna().sum() == 0
)

print("\n" + "=" * 60)

if validation_passed:
    print("SHIPMENT TRACKING BUSINESS VALIDATION PASSED")
else:
    print("SHIPMENT TRACKING BUSINESS VALIDATION FAILED")

print("=" * 60)

# ============================================================
# PREPARE DATA FOR SILVER
# ============================================================

print("\n" + "=" * 60)
print("PREPARING SHIPMENT TRACKING DATA FOR SILVER")
print("=" * 60)

# Remove investigation-only column
if "parsed_timestamp" in df.columns:
    df = df.drop(columns=["parsed_timestamp"])

print("\nColumns to be loaded:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

# ============================================================
# LOAD INTO SILVER
# ============================================================

print("\n" + "=" * 60)
print("LOADING SHIPMENT TRACKING DATA INTO SILVER")
print("=" * 60)

df.to_sql(
    "shipment_tracking",
    engine,
    schema="silver",
    if_exists="append",
    index=False
)

print("\nShipment Tracking data loaded successfully")
print("Target: silver.shipment_tracking")