import pandas as pd
from sqlalchemy import create_engine

# ============================================================
# DATABASE CONNECTION
# ============================================================

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

print("=" * 60)
print("CUSTOMER DELIVERY FEEDBACK - SPRINT 2 PREPROCESSING")
print("=" * 60)

# ============================================================
# LOAD DATA FROM STAGING
# ============================================================

df = pd.read_sql(
    "SELECT * FROM staging.customer_feedback",
    engine
)

print("\nData loaded successfully from staging.customer_feedback")

# ============================================================
# PROFILING
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMER DELIVERY FEEDBACK PROFILING")
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
# CUSTOMER DELIVERY FEEDBACK - INVESTIGATION
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMER DELIVERY FEEDBACK INVESTIGATION")
print("=" * 60)


# ============================================================
# 1. DUPLICATE FEEDBACK IDs
# ============================================================

print("\n" + "-" * 60)
print("1. DUPLICATE FEEDBACK IDs")
print("-" * 60)

duplicate_ids = df[
    df["feedback_id"].duplicated(keep=False)
]

print(
    "Duplicate feedback_id count:",
    duplicate_ids["feedback_id"].nunique()
)

if len(duplicate_ids) > 0:
    print(duplicate_ids)
else:
    print("No duplicate feedback_id found.")


# ============================================================
# 2. INVALID RATINGS
# ============================================================

print("\n" + "-" * 60)
print("2. RATING INVESTIGATION")
print("-" * 60)

invalid_rating = df[
    (df["rating"] < 1) |
    (df["rating"] > 5)
]

print("Invalid rating records:",
      len(invalid_rating))

print("\nInvalid rating values:")
print(invalid_rating["rating"].value_counts())

print("\nInvalid rating records:")
print(
    invalid_rating[
        [
            "feedback_id",
            "shipment_id",
            "customer_id",
            "rating",
            "on_time_delivery",
            "comments",
            "feedback_date",
            "channel"
        ]
    ]
)


# ============================================================
# 3. ON-TIME DELIVERY VALUES
# ============================================================

print("\n" + "-" * 60)
print("3. ON-TIME DELIVERY INVESTIGATION")
print("-" * 60)

print(df["on_time_delivery"].value_counts())

print("\nNormalized values:")

print(
    df["on_time_delivery"]
    .str.strip()
    .str.upper()
    .value_counts()
)


# ============================================================
# 4. COMMENTS INVESTIGATION
# ============================================================

print("\n" + "-" * 60)
print("4. COMMENTS INVESTIGATION")
print("-" * 60)

print("Missing comments:",
      df["comments"].isna().sum())

print("\nComments by rating:")

print(
    df.groupby("rating")["comments"]
      .apply(lambda x: x.isna().sum())
)


# ============================================================
# 5. CHANNEL INVESTIGATION
# ============================================================

print("\n" + "-" * 60)
print("5. CHANNEL INVESTIGATION")
print("-" * 60)

print(df["channel"].value_counts())

print("\nNormalized channels:")

print(
    df["channel"]
    .str.strip()
    .str.upper()
    .value_counts()
)


# ============================================================
# 6. FEEDBACK DATE INVESTIGATION
# ============================================================

print("\n" + "-" * 60)
print("6. FEEDBACK DATE INVESTIGATION")
print("-" * 60)

parsed_date = pd.to_datetime(
    df["feedback_date"],
    errors="coerce",
    format="mixed"
)

print("Invalid feedback dates:",
      parsed_date.isna().sum())

print("Minimum feedback date:",
      parsed_date.min())

print("Maximum feedback date:",
      parsed_date.max())


# ============================================================
# 7. TEXT FORMAT CHECK
# ============================================================

print("\n" + "-" * 60)
print("7. TEXT FORMAT CHECK")
print("-" * 60)

text_columns = [
    "feedback_id",
    "shipment_id",
    "customer_id",
    "on_time_delivery",
    "comments",
    "channel"
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
# 8. SHIPMENT FEEDBACK COUNTS
# ============================================================

print("\n" + "-" * 60)
print("8. FEEDBACKS PER SHIPMENT")
print("-" * 60)

feedback_per_shipment = df.groupby(
    "shipment_id"
).size()

print(feedback_per_shipment.describe())

print("\nShipments with most feedback records:")

print(
    feedback_per_shipment
    .sort_values(ascending=False)
    .head(10)
)


# ============================================================
# 9. CUSTOMER FEEDBACK COUNTS
# ============================================================

print("\n" + "-" * 60)
print("9. FEEDBACKS PER CUSTOMER")
print("-" * 60)

feedback_per_customer = df.groupby(
    "customer_id"
).size()

print(feedback_per_customer.describe())

print("\nCustomers with most feedback records:")

print(
    feedback_per_customer
    .sort_values(ascending=False)
    .head(10)
)


# ============================================================
# 10. ON-TIME DELIVERY VS RATING
# ============================================================

print("\n" + "-" * 60)
print("10. ON-TIME DELIVERY VS RATING")
print("-" * 60)

print(
    pd.crosstab(
        df["on_time_delivery"],
        df["rating"]
    )
)


# ============================================================
# 11. FINAL INVESTIGATION
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMER DELIVERY FEEDBACK INVESTIGATION COMPLETED")
print("=" * 60)

# ============================================================
# CUSTOMER DELIVERY FEEDBACK - CLEANING
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMER DELIVERY FEEDBACK CLEANING")
print("=" * 60)

original_rows = len(df)


# ============================================================
# 1. REMOVE DUPLICATE ROWS
# ============================================================

df = df.drop_duplicates().copy()

print("\nDuplicate rows removed:",
      original_rows - len(df))


# ============================================================
# 2. REMOVE INVALID RATINGS
# ============================================================

invalid_rating_count = (
    (df["rating"] < 1) |
    (df["rating"] > 5)
).sum()

print("\nInvalid ratings removed:",
      invalid_rating_count)

df = df[
    (df["rating"] >= 1) &
    (df["rating"] <= 5)
].copy()


# ============================================================
# 3. STRIP TEXT COLUMNS
# ============================================================

text_columns = [
    "feedback_id",
    "shipment_id",
    "customer_id",
    "on_time_delivery",
    "comments",
    "channel"
]

for col in text_columns:
    df[col] = df[col].str.strip()


# ============================================================
# 4. STANDARDIZE ON-TIME DELIVERY
# ============================================================

df["on_time_delivery"] = (
    df["on_time_delivery"]
    .str.upper()
)

print("\nOn-time delivery after standardization:")
print(df["on_time_delivery"].value_counts())


# ============================================================
# 5. STANDARDIZE CHANNEL
# ============================================================

df["channel"] = (
    df["channel"]
    .str.upper()
)

print("\nChannel after standardization:")
print(df["channel"].value_counts())


# ============================================================
# 6. PARSE FEEDBACK DATE
# ============================================================

df["feedback_date"] = pd.to_datetime(
    df["feedback_date"],
    errors="coerce",
    format="mixed"
)

print("\nInvalid feedback dates after parsing:",
      df["feedback_date"].isna().sum())


# ============================================================
# 7. PRESERVE MISSING COMMENTS
# ============================================================

# comments are optional.
# Missing comments remain NULL.


# ============================================================
# 8. FINAL CLEANING SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMER DELIVERY FEEDBACK CLEANING SUMMARY")
print("=" * 60)

print("\nOriginal rows:", original_rows)
print("Final rows:", len(df))
print("Rows removed:", original_rows - len(df))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDuplicate feedback_id:")
print(df["feedback_id"].duplicated().sum())

print("\nRating distribution:")
print(df["rating"].value_counts().sort_index())

print("\nOn-time delivery:")
print(df["on_time_delivery"].value_counts())

print("\nChannel:")
print(df["channel"].value_counts())

print("\nFeedback date range:")
print(df["feedback_date"].min())
print(df["feedback_date"].max())

print("\nData types:")
print(df.dtypes)

# ============================================================
# CUSTOMER DELIVERY FEEDBACK BUSINESS VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMER DELIVERY FEEDBACK BUSINESS VALIDATION")
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
# 3. DUPLICATE FEEDBACK ID
# ============================================================

print("\nDuplicate feedback_id:")
print(df["feedback_id"].duplicated().sum())


# ============================================================
# 4. REQUIRED FIELD VALIDATION
# ============================================================

required_columns = [
    "feedback_id",
    "shipment_id",
    "customer_id",
    "rating",
    "on_time_delivery",
    "feedback_date",
    "channel"
]

print("\nMissing required fields:")

required_missing = 0

for col in required_columns:

    missing = df[col].isna().sum()

    print(f"{col} : {missing}")

    required_missing += missing


# ============================================================
# 5. RATING VALIDATION
# ============================================================

print("\nRating minimum:")
print(df["rating"].min())

print("\nRating maximum:")
print(df["rating"].max())

print("\nRatings outside 1-5:")
print(
    ((df["rating"] < 1) |
     (df["rating"] > 5)).sum()
)


# ============================================================
# 6. ON-TIME DELIVERY VALIDATION
# ============================================================

valid_delivery_values = {"YES", "NO"}

actual_delivery_values = set(
    df["on_time_delivery"].dropna().unique()
)

unexpected_delivery_values = (
    actual_delivery_values - valid_delivery_values
)

print("\nActual on_time_delivery values:")
print(actual_delivery_values)

print("\nUnexpected on_time_delivery values:")
print(unexpected_delivery_values)


# ============================================================
# 7. CHANNEL VALIDATION
# ============================================================

valid_channels = {
    "APP",
    "WEBSITE",
    "EMAIL SURVEY",
    "CALL CENTER"
}

actual_channels = set(
    df["channel"].dropna().unique()
)

unexpected_channels = (
    actual_channels - valid_channels
)

print("\nActual channels:")
print(actual_channels)

print("\nUnexpected channels:")
print(unexpected_channels)


# ============================================================
# 8. FEEDBACK DATE VALIDATION
# ============================================================

print("\nMissing feedback dates:")
print(df["feedback_date"].isna().sum())

print("\nInvalid feedback dates:")

parsed_dates = pd.to_datetime(
    df["feedback_date"],
    errors="coerce"
)

print(parsed_dates.isna().sum())


# ============================================================
# 9. EMPTY REQUIRED STRING CHECK
# ============================================================

print("\nEmpty required string fields:")

empty_required = 0

for col in [
    "feedback_id",
    "shipment_id",
    "customer_id",
    "on_time_delivery",
    "channel"
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
# 10. FINAL VALIDATION RESULT
# ============================================================

validation_passed = (
    len(df) == 980
    and df.duplicated().sum() == 0
    and df["feedback_id"].duplicated().sum() == 0
    and required_missing == 0
    and ((df["rating"] < 1) |
         (df["rating"] > 5)).sum() == 0
    and len(unexpected_delivery_values) == 0
    and len(unexpected_channels) == 0
    and parsed_dates.isna().sum() == 0
    and empty_required == 0
)

print("\n" + "=" * 60)

if validation_passed:
    print("CUSTOMER DELIVERY FEEDBACK BUSINESS VALIDATION PASSED")
else:
    print("CUSTOMER DELIVERY FEEDBACK BUSINESS VALIDATION FAILED")

print("=" * 60)

# ============================================================
# PREPARE DATA FOR SILVER
# ============================================================

print("\n" + "=" * 60)
print("PREPARING CUSTOMER FEEDBACK DATA FOR SILVER")
print("=" * 60)

df["feedback_date"] = df["feedback_date"].dt.date

print("\nColumns to be loaded:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

# ============================================================
# LOAD INTO SILVER
# ============================================================

print("\n" + "=" * 60)
print("LOADING CUSTOMER FEEDBACK DATA INTO SILVER")
print("=" * 60)

df.to_sql(
    "customer_feedback",
    engine,
    schema="silver",
    if_exists="append",
    index=False
)

print("\nCustomer Delivery Feedback loaded successfully")
print("Target: silver.customer_feedback")