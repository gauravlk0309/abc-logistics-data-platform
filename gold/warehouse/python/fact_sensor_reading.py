import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234%23@localhost:5432/eldp"
)

print("=" * 70)
print("BUILDING GOLD.FACT_SENSOR_READING")
print("=" * 70)


# ============================================================
# 1. READ SOURCE
# ============================================================

sensor = pd.read_sql(
    """
    SELECT *
    FROM silver.iot_sensor_data
    """,
    engine
)

print("\nSilver IoT Sensor records:", len(sensor))


# ============================================================
# 2. CHECK SOURCE GRAIN
# ============================================================

print("\nChecking sensor reading grain...")

print(
    "Duplicate sensor reading IDs:",
    sensor["sensor_reading_id"].duplicated().sum()
)


# ============================================================
# 3. CREATE FACT SURROGATE KEY
# ============================================================

sensor.insert(
    0,
    "sensor_reading_key",
    range(1, len(sensor) + 1)
)


# ============================================================
# 4. SELECT FACT COLUMNS
# ============================================================

fact_sensor_reading = sensor[
    [
        "sensor_reading_key",
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


# ============================================================
# 5. CREATE GOLD SCHEMA
# ============================================================

with engine.begin() as conn:
    conn.execute(
        text("CREATE SCHEMA IF NOT EXISTS gold")
    )


# ============================================================
# 6. LOAD FACT TABLE
# ============================================================

fact_sensor_reading.to_sql(
    "fact_sensor_reading",
    engine,
    schema="gold",
    if_exists="replace",
    index=False
)


# ============================================================
# 7. ADD PRIMARY KEY
# ============================================================

with engine.begin() as conn:
    conn.execute(text("""
        ALTER TABLE gold.fact_sensor_reading
        ADD PRIMARY KEY (sensor_reading_key)
    """))


# ============================================================
# 8. VERIFY FACT TABLE
# ============================================================

check = pd.read_sql(
    """
    SELECT *
    FROM gold.fact_sensor_reading
    ORDER BY sensor_reading_key
    """,
    engine
)

print("\nGold fact table:")
print(check.head())

print("\nTotal fact records:", len(check))

print(
    "Duplicate sensor reading keys:",
    check["sensor_reading_key"].duplicated().sum()
)

print(
    "Duplicate sensor reading IDs:",
    check["sensor_reading_id"].duplicated().sum()
)

print(
    "NULL sensor reading keys:",
    check["sensor_reading_key"].isnull().sum()
)

print(
    "NULL sensor reading IDs:",
    check["sensor_reading_id"].isnull().sum()
)


# ============================================================
# 9. CHECK SENSOR DATA
# ============================================================

print("\nSensor data NULL counts:")

print(
    "NULL shipment IDs:",
    check["shipment_id"].isnull().sum()
)

print(
    "NULL reading timestamps:",
    check["reading_timestamp"].isnull().sum()
)

print(
    "NULL temperature:",
    check["temperature_c"].isnull().sum()
)

print(
    "NULL humidity:",
    check["humidity_pct"].isnull().sum()
)

print(
    "NULL shock_detected:",
    check["shock_detected"].isnull().sum()
)

print(
    "NULL battery:",
    check["battery_pct"].isnull().sum()
)

print(
    "NULL sensor IDs:",
    check["sensor_id"].isnull().sum()
)


print("\n" + "=" * 70)
print("FACT_SENSOR_READING CREATED SUCCESSFULLY")
print("=" * 70)