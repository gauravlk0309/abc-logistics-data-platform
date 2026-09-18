import pandas as pd
from sqlalchemy import create_engine

# ============================================================
# DATABASE CONNECTION
# ============================================================

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

print("=" * 60)
print("IOT SHIPMENT SENSOR DATA - SPRINT 2 PREPROCESSING")
print("=" * 60)

# ============================================================
# LOAD DATA FROM STAGING
# ============================================================

df = pd.read_sql(
    "SELECT * FROM staging.iot_sensor_data",
    engine
)

print("\nData loaded successfully from staging.iot_sensor_data")

# ============================================================
# PROFILING
# ============================================================

print("\n" + "=" * 60)
print("IOT SHIPMENT SENSOR DATA PROFILING")
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
# IOT SHIPMENT SENSOR DATA - INVESTIGATION
# ============================================================

print("\n" + "=" * 60)
print("IOT SHIPMENT SENSOR DATA INVESTIGATION")
print("=" * 60)


# ============================================================
# 1. DUPLICATE SENSOR READING IDs
# ============================================================

print("\n" + "-" * 60)
print("1. DUPLICATE SENSOR READING IDs")
print("-" * 60)

duplicate_ids = df[
    df["sensor_reading_id"].duplicated(keep=False)
]

print(
    "Duplicate sensor_reading_id count:",
    duplicate_ids["sensor_reading_id"].nunique()
)

if len(duplicate_ids) > 0:
    print(duplicate_ids)
else:
    print("No duplicate sensor_reading_id found.")


# ============================================================
# 2. TEMPERATURE INVESTIGATION
# ============================================================

print("\n" + "-" * 60)
print("2. TEMPERATURE INVESTIGATION")
print("-" * 60)

print("Minimum temperature:",
      df["temperature_c"].min())

print("Maximum temperature:",
      df["temperature_c"].max())

print("\nTemperature >= 50°C:")

high_temp = df[
    df["temperature_c"] >= 50
]

print("Count:", len(high_temp))

print(
    high_temp[
        [
            "sensor_reading_id",
            "shipment_id",
            "reading_timestamp",
            "temperature_c",
            "humidity_pct",
            "shock_detected",
            "battery_pct",
            "sensor_id"
        ]
    ]
)


# ============================================================
# 3. EXTREME LOW TEMPERATURE
# ============================================================

print("\n" + "-" * 60)
print("3. LOW TEMPERATURE INVESTIGATION")
print("-" * 60)

low_temp = df[
    df["temperature_c"] < -20
]

print("Temperature < -20°C:", len(low_temp))

if len(low_temp) > 0:
    print(low_temp)


# ============================================================
# 4. HUMIDITY INVESTIGATION
# ============================================================

print("\n" + "-" * 60)
print("4. HUMIDITY INVESTIGATION")
print("-" * 60)

print("Missing humidity:",
      df["humidity_pct"].isna().sum())

print("Minimum humidity:",
      df["humidity_pct"].min())

print("Maximum humidity:",
      df["humidity_pct"].max())

print("\nHumidity outside 0-100%:")

invalid_humidity = df[
    (df["humidity_pct"] < 0) |
    (df["humidity_pct"] > 100)
]

print("Count:", len(invalid_humidity))

if len(invalid_humidity) > 0:
    print(invalid_humidity)


# ============================================================
# 5. BATTERY INVESTIGATION
# ============================================================

print("\n" + "-" * 60)
print("5. BATTERY INVESTIGATION")
print("-" * 60)

print("Minimum battery:",
      df["battery_pct"].min())

print("Maximum battery:",
      df["battery_pct"].max())

invalid_battery = df[
    (df["battery_pct"] < 0) |
    (df["battery_pct"] > 100)
]

print("\nBattery outside 0-100%:")
print("Count:", len(invalid_battery))

if len(invalid_battery) > 0:
    print(invalid_battery)


# ============================================================
# 6. SHOCK DETECTED VALUES
# ============================================================

print("\n" + "-" * 60)
print("6. SHOCK DETECTED INVESTIGATION")
print("-" * 60)

print(df["shock_detected"].value_counts(dropna=False))


# ============================================================
# 7. TIMESTAMP INVESTIGATION
# ============================================================

print("\n" + "-" * 60)
print("7. TIMESTAMP INVESTIGATION")
print("-" * 60)

parsed_timestamp = pd.to_datetime(
    df["reading_timestamp"],
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
# 8. SENSOR READING COUNTS
# ============================================================

print("\n" + "-" * 60)
print("8. READINGS PER SENSOR")
print("-" * 60)

readings_per_sensor = df.groupby(
    "sensor_id"
).size()

print(readings_per_sensor.describe())

print("\nSensors with most readings:")

print(
    readings_per_sensor
    .sort_values(ascending=False)
    .head(10)
)


# ============================================================
# 9. READINGS PER SHIPMENT
# ============================================================

print("\n" + "-" * 60)
print("9. READINGS PER SHIPMENT")
print("-" * 60)

readings_per_shipment = df.groupby(
    "shipment_id"
).size()

print(readings_per_shipment.describe())

print("\nShipments with most sensor readings:")

print(
    readings_per_shipment
    .sort_values(ascending=False)
    .head(10)
)


# ============================================================
# 10. TEXT FORMAT CHECK
# ============================================================

print("\n" + "-" * 60)
print("10. TEXT FORMAT CHECK")
print("-" * 60)

text_columns = [
    "sensor_reading_id",
    "shipment_id",
    "sensor_id"
]

for col in text_columns:

    leading_trailing = (
        df[col]
        .dropna()
        .astype(str)
        .apply(lambda x: x != x.strip())
        .sum()
    )

    print(
        f"{col}: {leading_trailing} "
        "values with leading/trailing spaces"
    )


# ============================================================
# 11. FINAL INVESTIGATION
# ============================================================

print("\n" + "=" * 60)
print("IOT SHIPMENT SENSOR DATA INVESTIGATION COMPLETED")
print("=" * 60)

# ============================================================
# IOT SHIPMENT SENSOR DATA - CLEANING
# ============================================================

print("\n" + "=" * 60)
print("IOT SHIPMENT SENSOR DATA CLEANING")
print("=" * 60)

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
    "sensor_reading_id",
    "shipment_id",
    "sensor_id"
]

for col in text_columns:
    df[col] = df[col].str.strip()


# ============================================================
# 3. PARSE READING TIMESTAMP
# ============================================================

df["reading_timestamp"] = pd.to_datetime(
    df["reading_timestamp"],
    errors="coerce",
    format="mixed"
)

print("\nInvalid timestamps after parsing:",
      df["reading_timestamp"].isna().sum())


# ============================================================
# 4. VALIDATE SHOCK DETECTED
# ============================================================

df["shock_detected"] = df["shock_detected"].astype(bool)

print("\nShock detected values:")
print(df["shock_detected"].value_counts())


# ============================================================
# 5. PRESERVE MISSING HUMIDITY
# ============================================================

# Missing humidity values are preserved as NULL.
# We do not fill them because there is no reliable
# information to reconstruct the actual sensor reading.


# ============================================================
# 6. IDENTIFY EXTREME TEMPERATURES
# ============================================================

high_temperature_count = (
    df["temperature_c"] >= 50
).sum()

print("\nTemperature readings >= 50°C:")
print(high_temperature_count)

print(
    "\nThese readings are retained because no documented "
    "business threshold was provided for this dataset."
)


# ============================================================
# 7. FINAL CLEANING SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("IOT SHIPMENT SENSOR DATA CLEANING SUMMARY")
print("=" * 60)

print("\nOriginal rows:", original_rows)
print("Final rows:", len(df))
print("Rows removed:", original_rows - len(df))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDuplicate sensor_reading_id:")
print(df["sensor_reading_id"].duplicated().sum())

print("\nTemperature range:")
print(df["temperature_c"].min())
print(df["temperature_c"].max())

print("\nHumidity range:")
print(df["humidity_pct"].min())
print(df["humidity_pct"].max())

print("\nBattery range:")
print(df["battery_pct"].min())
print(df["battery_pct"].max())

print("\nShock detected:")
print(df["shock_detected"].value_counts())

print("\nTimestamp range:")
print(df["reading_timestamp"].min())
print(df["reading_timestamp"].max())

print("\nData types:")
print(df.dtypes)

# ============================================================
# IOT SHIPMENT SENSOR DATA BUSINESS VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("IOT SHIPMENT SENSOR DATA BUSINESS VALIDATION")
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
# 3. DUPLICATE SENSOR READING ID
# ============================================================

print("\nDuplicate sensor_reading_id:")
print(
    df["sensor_reading_id"].duplicated().sum()
)


# ============================================================
# 4. REQUIRED FIELD VALIDATION
# ============================================================

required_columns = [
    "sensor_reading_id",
    "shipment_id",
    "reading_timestamp",
    "temperature_c",
    "shock_detected",
    "battery_pct",
    "sensor_id"
]

print("\nMissing required fields:")

required_missing = 0

for col in required_columns:

    missing = df[col].isna().sum()

    print(f"{col} : {missing}")

    required_missing += missing


# ============================================================
# 5. HUMIDITY VALIDATION
# ============================================================

print("\nHumidity outside 0-100%:")

invalid_humidity = (
    (df["humidity_pct"] < 0) |
    (df["humidity_pct"] > 100)
).sum()

print(invalid_humidity)

print("\nMissing humidity:")
print(df["humidity_pct"].isna().sum())


# ============================================================
# 6. BATTERY VALIDATION
# ============================================================

print("\nBattery below 0%:")
print((df["battery_pct"] < 0).sum())

print("\nBattery above 100%:")
print((df["battery_pct"] > 100).sum())


# ============================================================
# 7. SHOCK DETECTED VALIDATION
# ============================================================

print("\nShock detected values:")
print(df["shock_detected"].value_counts())

invalid_shock = (
    ~df["shock_detected"].isin([True, False])
).sum()

print("\nInvalid shock_detected values:")
print(invalid_shock)


# ============================================================
# 8. TIMESTAMP VALIDATION
# ============================================================

print("\nMissing reading timestamps:")
print(df["reading_timestamp"].isna().sum())

parsed_timestamp = pd.to_datetime(
    df["reading_timestamp"],
    errors="coerce"
)

print("\nInvalid reading timestamps:")
print(parsed_timestamp.isna().sum())


# ============================================================
# 9. TEMPERATURE INFORMATION
# ============================================================

print("\nTemperature minimum:")
print(df["temperature_c"].min())

print("\nTemperature maximum:")
print(df["temperature_c"].max())

print("\nTemperature >= 50°C:")
print(
    (df["temperature_c"] >= 50).sum()
)

print(
    "\nNote: Extreme temperatures are retained because "
    "no documented business threshold was provided."
)


# ============================================================
# 10. EMPTY REQUIRED STRING CHECK
# ============================================================

print("\nEmpty required string fields:")

empty_required = 0

for col in [
    "sensor_reading_id",
    "shipment_id",
    "sensor_id"
]:

    empty_count = (
        df[col]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    print(f"{col} : {empty_count}")

    empty_required += empty_count


# ============================================================
# 11. FINAL VALIDATION RESULT
# ============================================================

validation_passed = (
    len(df) == 2200
    and df.duplicated().sum() == 0
    and df["sensor_reading_id"].duplicated().sum() == 0
    and required_missing == 0
    and invalid_humidity == 0
    and (df["battery_pct"] < 0).sum() == 0
    and (df["battery_pct"] > 100).sum() == 0
    and invalid_shock == 0
    and parsed_timestamp.isna().sum() == 0
    and empty_required == 0
)

print("\n" + "=" * 60)

if validation_passed:
    print("IOT SHIPMENT SENSOR DATA BUSINESS VALIDATION PASSED")
else:
    print("IOT SHIPMENT SENSOR DATA BUSINESS VALIDATION FAILED")

print("=" * 60)

# ============================================================
# PREPARE DATA FOR SILVER
# ============================================================

print("\n" + "=" * 60)
print("PREPARING IOT SENSOR DATA FOR SILVER")
print("=" * 60)

print("\nColumns to be loaded:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

# ============================================================
# LOAD INTO SILVER
# ============================================================

print("\n" + "=" * 60)
print("LOADING IOT SENSOR DATA INTO SILVER")
print("=" * 60)

df.to_sql(
    "iot_sensor_data",
    engine,
    schema="silver",
    if_exists="append",
    index=False
)

print("\nIoT Shipment Sensor Data loaded successfully")
print("Target: silver.iot_sensor_data")