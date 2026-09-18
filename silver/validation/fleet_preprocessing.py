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
# 2. LOAD FLEET DATA
# ============================================================

df = pd.read_sql(
    "SELECT * FROM staging.fleet_management",
    engine
)


# ============================================================
# 3. PROFILING
# ============================================================

print("\n" + "=" * 60)
print("FLEET MANAGEMENT PROFILING")
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
print("FLEET PROFILING COMPLETE")
print("=" * 60)

# ============================================================
# 4. FLEET DATA QUALITY INVESTIGATION
# ============================================================

print("\n" + "=" * 60)
print("FLEET DATA QUALITY INVESTIGATION")
print("=" * 60)


# ------------------------------------------------------------
# 1. DUPLICATE FLEET LOG IDs
# ------------------------------------------------------------

print("\n1. DUPLICATE FLEET LOG IDs")

print(
    "Duplicate fleet_log_id:",
    df["fleet_log_id"].duplicated().sum()
)


# ------------------------------------------------------------
# 2. EVENT TYPES
# ------------------------------------------------------------

print("\n2. EVENT TYPES")

print(df["event_type"].value_counts())


# ------------------------------------------------------------
# 3. MISSING VALUES BY EVENT TYPE
# ------------------------------------------------------------

print("\n3. MISSING VALUES BY EVENT TYPE")

for col in [
    "odometer_km",
    "fuel_liters",
    "maintenance_cost_usd",
    "downtime_hours",
    "notes"
]:
    
    print(f"\n--- {col} ---")
    
    print(
        df.groupby("event_type")[col]
        .apply(lambda x: x.isna().sum())
    )


# ------------------------------------------------------------
# 4. EVENT TYPE VS FUEL
# ------------------------------------------------------------

print("\n4. FUEL LITERS BY EVENT TYPE")

print(
    df.groupby("event_type")["fuel_liters"]
    .agg(["count", "min", "max"])
)


# ------------------------------------------------------------
# 5. EVENT TYPE VS MAINTENANCE COST
# ------------------------------------------------------------

print("\n5. MAINTENANCE COST BY EVENT TYPE")

print(
    df.groupby("event_type")["maintenance_cost_usd"]
    .agg(["count", "min", "max"])
)


# ------------------------------------------------------------
# 6. NEGATIVE NUMERIC VALUES
# ------------------------------------------------------------

print("\n6. NEGATIVE NUMERIC VALUES")

print(
    "Negative odometer:",
    (df["odometer_km"] < 0).sum()
)

print(
    "Negative fuel:",
    (df["fuel_liters"] < 0).sum()
)

print(
    "Negative maintenance cost:",
    (df["maintenance_cost_usd"] < 0).sum()
)

print(
    "Negative downtime:",
    (df["downtime_hours"] < 0).sum()
)


# ------------------------------------------------------------
# 7. ZERO VALUES
# ------------------------------------------------------------

print("\n7. ZERO VALUES")

print(
    "Zero odometer:",
    (df["odometer_km"] == 0).sum()
)

print(
    "Zero fuel:",
    (df["fuel_liters"] == 0).sum()
)

print(
    "Zero maintenance cost:",
    (df["maintenance_cost_usd"] == 0).sum()
)

print(
    "Zero downtime:",
    (df["downtime_hours"] == 0).sum()
)


# ------------------------------------------------------------
# 8. EVENT TYPE VS DOWNTIME
# ------------------------------------------------------------

print("\n8. DOWNTIME BY EVENT TYPE")

print(
    df.groupby("event_type")["downtime_hours"]
    .agg(["count", "min", "max", "mean"])
)


# ------------------------------------------------------------
# 9. DATE CHECK
# ------------------------------------------------------------

print("\n9. EVENT DATE")

converted_date = pd.to_datetime(
    df["event_date"],
    errors="coerce"
)

print(
    "Invalid event dates:",
    converted_date.isna().sum()
)

print(
    "Missing event dates:",
    df["event_date"].isna().sum()
)


# ------------------------------------------------------------
# 10. TEXT VALUES
# ------------------------------------------------------------

print("\n10. EVENT TYPE VALUES")

print(
    sorted(df["event_type"].dropna().unique())
)


# ------------------------------------------------------------
# 11. DRIVER VALUES
# ------------------------------------------------------------

print("\n11. DRIVER INFORMATION")

print(
    "Unique drivers:",
    df["driver_name"].nunique()
)


print("\n" + "=" * 60)
print("FLEET DATA QUALITY INVESTIGATION COMPLETE")
print("=" * 60)

# ============================================================
# 5. FLEET CLEANING
# ============================================================

print("\n" + "=" * 60)
print("FLEET CLEANING")
print("=" * 60)

original_rows = len(df)


# ------------------------------------------------------------
# 1. REMOVE DUPLICATE ROWS
# ------------------------------------------------------------

df = df.drop_duplicates().copy()

print("\nAfter removing duplicate rows:", len(df))


# ------------------------------------------------------------
# 2. REMOVE NEGATIVE FUEL VALUES
# ------------------------------------------------------------

df = df[
    (df["fuel_liters"].isna()) |
    (df["fuel_liters"] >= 0)
].copy()

print(
    "After removing negative fuel records:",
    len(df)
)


# ------------------------------------------------------------
# 3. CONVERT EVENT DATE
# ------------------------------------------------------------

df["event_date"] = pd.to_datetime(
    df["event_date"],
    errors="coerce"
)

print(
    "\nInvalid event dates after conversion:",
    df["event_date"].isna().sum()
)


# ------------------------------------------------------------
# 4. STANDARDIZE TEXT COLUMNS
# ------------------------------------------------------------

text_columns = [
    "fleet_log_id",
    "vehicle_id",
    "driver_name",
    "event_type",
    "notes"
]

for col in text_columns:
    df[col] = df[col].str.strip()


# ------------------------------------------------------------
# 5. CLEANING SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FLEET CLEANING SUMMARY")
print("=" * 60)

print("Original rows:", original_rows)
print("Final rows:", len(df))
print("Rows removed:", original_rows - len(df))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print(
    "\nDuplicate fleet_log_id:",
    df["fleet_log_id"].duplicated().sum()
)

print(
    "\nNegative odometer:",
    (df["odometer_km"] < 0).sum()
)

print(
    "\nNegative fuel:",
    (df["fuel_liters"] < 0).sum()
)

print(
    "\nNegative maintenance cost:",
    (df["maintenance_cost_usd"] < 0).sum()
)

print(
    "\nNegative downtime:",
    (df["downtime_hours"] < 0).sum()
)

print("\nEvent types:")
print(df["event_type"].value_counts())

print("\nData types:")
print(df.dtypes)

# ============================================================
# 6. FLEET BUSINESS VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("FLEET BUSINESS VALIDATION")
print("=" * 60)

# ------------------------------------------------------------
# 1. BASIC VALIDATION
# ------------------------------------------------------------

print("\nFinal row count:")
print(len(df))

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDuplicate fleet_log_id:")
print(df["fleet_log_id"].duplicated().sum())


# ------------------------------------------------------------
# 2. NUMERIC RANGE VALIDATION
# ------------------------------------------------------------

print("\nNegative odometer:")
print((df["odometer_km"] < 0).sum())

print("\nNegative fuel:")
print((df["fuel_liters"] < 0).sum())

print("\nNegative maintenance cost:")
print((df["maintenance_cost_usd"] < 0).sum())

print("\nNegative downtime:")
print((df["downtime_hours"] < 0).sum())


# ------------------------------------------------------------
# 3. EVENT DATE VALIDATION
# ------------------------------------------------------------

print("\nMissing event dates:")
print(df["event_date"].isna().sum())


# ------------------------------------------------------------
# 4. EVENT TYPE VALIDATION
# ------------------------------------------------------------

expected_event_types = {
    "Trip",
    "Maintenance",
    "Breakdown",
    "Refuel",
    "Inspection"
}

actual_event_types = set(df["event_type"].dropna().unique())

print("\nActual event types:")
print(actual_event_types)

print("\nUnexpected event types:")
print(actual_event_types - expected_event_types)


# ------------------------------------------------------------
# 5. FUEL BUSINESS RULE
# ------------------------------------------------------------
# Fuel should be present for:
#   Refuel
#   Trip
#
# Fuel should be NULL for:
#   Maintenance
#   Breakdown
#   Inspection

fuel_expected_events = ["Refuel", "Trip"]
fuel_not_expected_events = ["Maintenance", "Breakdown", "Inspection"]

print("\nFuel missing where it is expected:")

fuel_missing_invalid = df[
    df["event_type"].isin(fuel_expected_events) &
    df["fuel_liters"].isna()
]

print(len(fuel_missing_invalid))

print("\nFuel present where it is not expected:")

fuel_present_invalid = df[
    df["event_type"].isin(fuel_not_expected_events) &
    df["fuel_liters"].notna()
]

print(len(fuel_present_invalid))


# ------------------------------------------------------------
# 6. MAINTENANCE COST BUSINESS RULE
# ------------------------------------------------------------
# Maintenance cost should be present only for:
#   Maintenance
#
# It should be NULL for:
#   Trip
#   Breakdown
#   Refuel
#   Inspection

print("\nMaintenance cost missing for Maintenance:")

maintenance_missing_invalid = df[
    (df["event_type"] == "Maintenance") &
    df["maintenance_cost_usd"].isna()
]

print(len(maintenance_missing_invalid))

print("\nMaintenance cost present for non-Maintenance events:")

maintenance_present_invalid = df[
    (df["event_type"] != "Maintenance") &
    df["maintenance_cost_usd"].notna()
]

print(len(maintenance_present_invalid))


# ------------------------------------------------------------
# 7. DOWNTIME BUSINESS RULE
# ------------------------------------------------------------

print("\nDowntime statistics:")
print(df.groupby("event_type")["downtime_hours"].agg(
    ["min", "max", "mean"]
))


# ------------------------------------------------------------
# 8. FINAL VALIDATION RESULT
# ------------------------------------------------------------

validation_passed = (
    len(df) == 982
    and df.duplicated().sum() == 0
    and df["fleet_log_id"].duplicated().sum() == 0
    and (df["odometer_km"] < 0).sum() == 0
    and (df["fuel_liters"] < 0).sum() == 0
    and (df["maintenance_cost_usd"] < 0).sum() == 0
    and (df["downtime_hours"] < 0).sum() == 0
    and df["event_date"].isna().sum() == 0
    and len(actual_event_types - expected_event_types) == 0
    and len(fuel_missing_invalid) == 0
    and len(fuel_present_invalid) == 0
    and len(maintenance_missing_invalid) == 0
    and len(maintenance_present_invalid) == 0
)

print("\n" + "=" * 60)

if validation_passed:
    print("FLEET BUSINESS VALIDATION PASSED")
else:
    print("FLEET BUSINESS VALIDATION FAILED")

print("=" * 60)

# Convert odometer to nullable integer
df["odometer_km"] = df["odometer_km"].astype("Int64")

print("\n" + "=" * 60)
print("LOADING FLEET DATA INTO SILVER")
print("=" * 60)

df.to_sql(
    "fleet_management",
    engine,
    schema="silver",
    if_exists="append",
    index=False
)

print("Fleet data loaded successfully into silver.fleet_management")