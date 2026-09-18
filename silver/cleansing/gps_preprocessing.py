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
# 2. LOAD GPS DATA
# ============================================================

df = pd.read_sql(
    "SELECT * FROM staging.gps_tracking",
    engine
)


# ============================================================
# 3. PROFILING
# ============================================================

print("\n" + "=" * 60)
print("GPS VEHICLE TRACKING PROFILING")
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
print("GPS PROFILING COMPLETE")
print("=" * 60)

# ============================================================
# 4. GPS DATA QUALITY INVESTIGATION
# ============================================================

print("\n" + "=" * 60)
print("GPS DATA QUALITY INVESTIGATION")
print("=" * 60)


# ------------------------------------------------------------
# 1. DUPLICATE GPS PING IDs
# ------------------------------------------------------------

print("\n1. DUPLICATE GPS PING IDs")

duplicate_pings = df[
    df["gps_ping_id"].duplicated(keep=False)
].sort_values("gps_ping_id")

print(duplicate_pings.to_string(index=False))

print(
    "\nDuplicate GPS ping ID count:",
    df["gps_ping_id"].duplicated().sum()
)


# ------------------------------------------------------------
# 2. MISSING SPEED
# ------------------------------------------------------------

print("\n2. MISSING SPEED")

print(
    "Missing speed records:",
    df["speed_kmph"].isna().sum()
)


# ------------------------------------------------------------
# 3. INVALID LATITUDE
# Latitude must be between -90 and +90
# ------------------------------------------------------------

print("\n3. INVALID LATITUDE")

invalid_latitude = df[
    (df["latitude"] < -90) |
    (df["latitude"] > 90)
]

print(
    "Invalid latitude records:",
    len(invalid_latitude)
)

if len(invalid_latitude) > 0:
    print(
        invalid_latitude[
            [
                "gps_ping_id",
                "vehicle_id",
                "latitude",
                "longitude"
            ]
        ].to_string(index=False)
    )


# ------------------------------------------------------------
# 4. INVALID LONGITUDE
# Longitude must be between -180 and +180
# ------------------------------------------------------------

print("\n4. INVALID LONGITUDE")

invalid_longitude = df[
    (df["longitude"] < -180) |
    (df["longitude"] > 180)
]

print(
    "Invalid longitude records:",
    len(invalid_longitude)
)

if len(invalid_longitude) > 0:
    print(
        invalid_longitude[
            [
                "gps_ping_id",
                "vehicle_id",
                "latitude",
                "longitude"
            ]
        ].to_string(index=False)
    )


# ------------------------------------------------------------
# 5. INVALID SPEED
# ------------------------------------------------------------

print("\n5. INVALID SPEED")

negative_speed = df[
    df["speed_kmph"] < 0
]

print(
    "Negative speed records:",
    len(negative_speed)
)

if len(negative_speed) > 0:
    print(
        negative_speed[
            [
                "gps_ping_id",
                "vehicle_id",
                "speed_kmph",
                "ignition_status"
            ]
        ].to_string(index=False)
    )


# ------------------------------------------------------------
# 6. INVALID HEADING
# Heading should be between 0 and 359 degrees
# ------------------------------------------------------------

print("\n6. INVALID HEADING")

invalid_heading = df[
    (df["heading_deg"] < 0) |
    (df["heading_deg"] >= 360)
]

print(
    "Invalid heading records:",
    len(invalid_heading)
)

if len(invalid_heading) > 0:
    print(
        invalid_heading[
            [
                "gps_ping_id",
                "vehicle_id",
                "heading_deg"
            ]
        ].to_string(index=False)
    )


# ------------------------------------------------------------
# 7. INVALID FUEL LEVEL
# Fuel percentage should be between 0 and 100
# ------------------------------------------------------------

print("\n7. INVALID FUEL LEVEL")

invalid_fuel = df[
    (df["fuel_level_pct"] < 0) |
    (df["fuel_level_pct"] > 100)
]

print(
    "Invalid fuel records:",
    len(invalid_fuel)
)

if len(invalid_fuel) > 0:
    print(
        invalid_fuel[
            [
                "gps_ping_id",
                "vehicle_id",
                "fuel_level_pct"
            ]
        ].to_string(index=False)
    )


# ------------------------------------------------------------
# 8. IGNITION STATUS
# ------------------------------------------------------------

print("\n8. IGNITION STATUS")

print(
    df["ignition_status"].value_counts()
)


# ------------------------------------------------------------
# 9. TIMESTAMP CHECK
# ------------------------------------------------------------

print("\n9. TIMESTAMP")

print(
    "Missing timestamps:",
    df["timestamp"].isna().sum()
)

print(
    "Duplicate timestamps:",
    df["timestamp"].duplicated().sum()
)


print("\n" + "=" * 60)
print("GPS DATA QUALITY INVESTIGATION COMPLETE")
print("=" * 60)

# ============================================================
# 5. GPS CLEANING
# ============================================================

print("\n" + "=" * 60)
print("GPS CLEANING")
print("=" * 60)

original_rows = len(df)


# ------------------------------------------------------------
# 1. REMOVE DUPLICATE ROWS
# ------------------------------------------------------------

df = df.drop_duplicates().copy()

print("\nAfter removing duplicate rows:", len(df))


# ------------------------------------------------------------
# 2. REMOVE INVALID LATITUDE
# Latitude must be between -90 and +90
# ------------------------------------------------------------

df = df[
    (df["latitude"] >= -90) &
    (df["latitude"] <= 90)
].copy()

print(
    "After removing invalid latitude:",
    len(df)
)


# ------------------------------------------------------------
# 3. KEEP MISSING SPEED AS NULL
# ------------------------------------------------------------

print(
    "\nMissing speed values retained:",
    df["speed_kmph"].isna().sum()
)


# ------------------------------------------------------------
# 4. STANDARDIZE TEXT COLUMNS
# ------------------------------------------------------------

text_columns = [
    "gps_ping_id",
    "vehicle_id",
    "ignition_status"
]

for col in text_columns:
    df[col] = df[col].str.strip()


# ------------------------------------------------------------
# 5. CLEANING SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("GPS CLEANING SUMMARY")
print("=" * 60)

print("Original rows:", original_rows)
print("Final rows:", len(df))
print("Rows removed:", original_rows - len(df))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDuplicate GPS ping IDs:")
print(df["gps_ping_id"].duplicated().sum())

print("\nInvalid latitude:")
print(
    (
        (df["latitude"] < -90) |
        (df["latitude"] > 90)
    ).sum()
)

print("\nInvalid longitude:")
print(
    (
        (df["longitude"] < -180) |
        (df["longitude"] > 180)
    ).sum()
)

print("\nNegative speed:")
print(
    (df["speed_kmph"] < 0).sum()
)

print("\nInvalid heading:")
print(
    (
        (df["heading_deg"] < 0) |
        (df["heading_deg"] >= 360)
    ).sum()
)

print("\nInvalid fuel:")
print(
    (
        (df["fuel_level_pct"] < 0) |
        (df["fuel_level_pct"] > 100)
    ).sum()
)

print("\nData types:")
print(df.dtypes)

# ============================================================
# 6. GPS DATA VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("GPS DATA VALIDATION")
print("=" * 60)


# ------------------------------------------------------------
# 1. ROW COUNT
# ------------------------------------------------------------

print("\n1. ROW COUNT")
print("Cleaned rows:", len(df))


# ------------------------------------------------------------
# 2. MISSING VALUES
# ------------------------------------------------------------

print("\n2. MISSING VALUES")
print(df.isnull().sum())


# ------------------------------------------------------------
# 3. DUPLICATE ROWS
# ------------------------------------------------------------

print("\n3. DUPLICATE ROWS")
print("Duplicate rows:", df.duplicated().sum())


# ------------------------------------------------------------
# 4. DUPLICATE GPS PING IDs
# ------------------------------------------------------------

print("\n4. DUPLICATE GPS PING IDs")
print(
    "Duplicate GPS ping IDs:",
    df["gps_ping_id"].duplicated().sum()
)


# ------------------------------------------------------------
# 5. LATITUDE VALIDATION
# ------------------------------------------------------------

print("\n5. LATITUDE VALIDATION")

print(
    "Invalid latitude:",
    (
        (df["latitude"] < -90) |
        (df["latitude"] > 90)
    ).sum()
)


# ------------------------------------------------------------
# 6. LONGITUDE VALIDATION
# ------------------------------------------------------------

print("\n6. LONGITUDE VALIDATION")

print(
    "Invalid longitude:",
    (
        (df["longitude"] < -180) |
        (df["longitude"] > 180)
    ).sum()
)


# ------------------------------------------------------------
# 7. SPEED VALIDATION
# ------------------------------------------------------------

print("\n7. SPEED VALIDATION")

print(
    "Negative speed:",
    (df["speed_kmph"] < 0).sum()
)

print(
    "Missing speed:",
    df["speed_kmph"].isna().sum()
)


# ------------------------------------------------------------
# 8. HEADING VALIDATION
# ------------------------------------------------------------

print("\n8. HEADING VALIDATION")

print(
    "Invalid heading:",
    (
        (df["heading_deg"] < 0) |
        (df["heading_deg"] >= 360)
    ).sum()
)


# ------------------------------------------------------------
# 9. FUEL VALIDATION
# ------------------------------------------------------------

print("\n9. FUEL VALIDATION")

print(
    "Invalid fuel percentage:",
    (
        (df["fuel_level_pct"] < 0) |
        (df["fuel_level_pct"] > 100)
    ).sum()
)


# ------------------------------------------------------------
# 10. TIMESTAMP VALIDATION
# ------------------------------------------------------------

print("\n10. TIMESTAMP VALIDATION")

print(
    "Missing timestamps:",
    df["timestamp"].isna().sum()
)


# ------------------------------------------------------------
# 11. IGNITION STATUS
# ------------------------------------------------------------

print("\n11. IGNITION STATUS")

print(df["ignition_status"].value_counts())


# ------------------------------------------------------------
# 12. FINAL DATA TYPES
# ------------------------------------------------------------

print("\n12. DATA TYPES")

print(df.dtypes)


print("\n" + "=" * 60)
print("GPS VALIDATION COMPLETE")
print("=" * 60)

# ============================================================
# 7. LOAD CLEANED GPS DATA INTO SILVER
# ============================================================

print("\n" + "=" * 60)
print("LOADING GPS DATA INTO SILVER")
print("=" * 60)

df.to_sql(
    "gps_tracking",
    engine,
    schema="silver",
    if_exists="append",
    index=False
)

print("\nGPS data successfully loaded into silver.gps_tracking")
print("Rows loaded:", len(df))