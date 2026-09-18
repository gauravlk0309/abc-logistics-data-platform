import pandas as pd
from sqlalchemy import create_engine

# ============================================================
# 1. DATABASE CONNECTION
# ============================================================

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234#@localhost:5432/eldp"
)

print("=" * 60)
print("VENDOR & SUPPLIER - SPRINT 2 PREPROCESSING")
print("=" * 60)


# ============================================================
# 2. READ DATA FROM POSTGRESQL STAGING
# ============================================================

df = pd.read_sql(
    "SELECT * FROM staging.vendor_portal",
    engine
)

print("\nData loaded successfully from staging.vendor_supplier")


# ============================================================
# 3. BASIC PROFILING
# ============================================================

print("\n" + "=" * 60)
print("VENDOR & SUPPLIER PROFILING")
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
# 6. VENDOR PORTAL INVESTIGATION
# ============================================================

print("\n" + "=" * 60)
print("VENDOR PORTAL INVESTIGATION")
print("=" * 60)


# ------------------------------------------------------------
# 1. DUPLICATE PO IDs
# ------------------------------------------------------------

print("\nDuplicate po_id:")

duplicate_po = df[
    df["po_id"].duplicated(keep=False)
].sort_values("po_id")

print(duplicate_po.to_string(index=False))

print("\nNumber of duplicate po_id:")
print(df["po_id"].duplicated().sum())


# ------------------------------------------------------------
# 2. MISSING ACKNOWLEDGED DATE
# ------------------------------------------------------------

print("\nMissing acknowledged_date:")
print(df["acknowledged_date"].isna().sum())

print("\nMissing acknowledged_date by currency:")
print(
    df[df["acknowledged_date"].isna()]
    ["currency"]
    .value_counts(dropna=False)
)


# ------------------------------------------------------------
# 3. CURRENCY INVESTIGATION
# ------------------------------------------------------------

print("\nOriginal currency values:")
print(df["currency"].value_counts(dropna=False))

print("\nStandardized currency values:")
print(
    df["currency"]
    .str.strip()
    .str.upper()
    .value_counts(dropna=False)
)


# ------------------------------------------------------------
# 4. QUANTITY VALIDATION
# ------------------------------------------------------------

print("\nNegative quantity_ordered:")
print((df["quantity_ordered"] < 0).sum())

print("\nZero quantity_ordered:")
print((df["quantity_ordered"] == 0).sum())

print("\nQuantity range:")
print(
    "Minimum:", df["quantity_ordered"].min(),
    "| Maximum:", df["quantity_ordered"].max()
)


# ------------------------------------------------------------
# 5. UNIT COST VALIDATION
# ------------------------------------------------------------

print("\nNegative unit_cost:")
print((df["unit_cost"] < 0).sum())

print("\nZero unit_cost:")
print((df["unit_cost"] == 0).sum())

print("\nUnit cost range:")
print(
    "Minimum:", df["unit_cost"].min(),
    "| Maximum:", df["unit_cost"].max()
)


# ------------------------------------------------------------
# 6. VENDOR RATING VALIDATION
# ------------------------------------------------------------

print("\nVendor rating range:")
print(
    "Minimum:", df["vendor_rating_at_po"].min(),
    "| Maximum:", df["vendor_rating_at_po"].max()
)

print("\nRatings outside 1-5:")
print(
    (
        (df["vendor_rating_at_po"] < 1) |
        (df["vendor_rating_at_po"] > 5)
    ).sum()
)


# ------------------------------------------------------------
# 7. DATE INVESTIGATION
# ------------------------------------------------------------

date_columns = [
    "po_date",
    "acknowledged_date",
    "expected_arrival_date"
]

for col in date_columns:

    print("\n" + "-" * 50)
    print(col)
    print("-" * 50)

    print("Sample values:")
    print(
        df[col]
        .dropna()
        .head(20)
        .to_string(index=False)
    )

    parsed = pd.to_datetime(
        df[col],
        errors="coerce",
        format="mixed"
    )

    print("Invalid dates:", parsed.isna().sum())

    print("Minimum:", parsed.min())
    print("Maximum:", parsed.max())


# ------------------------------------------------------------
# 8. DATE BUSINESS RELATIONSHIPS
# ------------------------------------------------------------

po_date = pd.to_datetime(
    df["po_date"],
    errors="coerce",
    format="mixed"
)

ack_date = pd.to_datetime(
    df["acknowledged_date"],
    errors="coerce",
    format="mixed"
)

arrival_date = pd.to_datetime(
    df["expected_arrival_date"],
    errors="coerce",
    format="mixed"
)

print("\nAcknowledged date before PO date:")
print(
    (
        ack_date.notna() &
        (ack_date < po_date)
    ).sum()
)

print("\nExpected arrival before PO date:")
print(
    (arrival_date < po_date).sum()
)

print("\nExpected arrival before acknowledged date:")
print(
    (
        ack_date.notna() &
        (arrival_date < ack_date)
    ).sum()
)


# ------------------------------------------------------------
# 9. REQUIRED FIELD CHECK
# ------------------------------------------------------------

required_columns = [
    "po_id",
    "supplier_id",
    "product_id",
    "destination_warehouse_id",
    "po_date",
    "quantity_ordered",
    "unit_cost",
    "currency",
    "expected_arrival_date",
    "vendor_rating_at_po"
]

print("\n" + "=" * 60)
print("MISSING REQUIRED FIELDS")
print("=" * 60)

for col in required_columns:
    print(col, ":", df[col].isna().sum())

# ============================================================
# 7. VENDOR PORTAL CLEANING
# ============================================================

print("\n" + "=" * 60)
print("VENDOR PORTAL CLEANING")
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
    "po_id",
    "supplier_id",
    "product_id",
    "destination_warehouse_id",
    "currency"
]

for col in text_columns:
    df[col] = df[col].str.strip()


# ------------------------------------------------------------
# 3. STANDARDIZE CURRENCY
# ------------------------------------------------------------

df["currency"] = df["currency"].str.upper()

print("\nStandardized currency values:")
print(df["currency"].value_counts())


# ------------------------------------------------------------
# 4. CONVERT DATE COLUMNS
# ------------------------------------------------------------

date_columns = [
    "po_date",
    "acknowledged_date",
    "expected_arrival_date"
]

for col in date_columns:
    df[col] = pd.to_datetime(
        df[col],
        errors="coerce",
        format="mixed"
    )


# ------------------------------------------------------------
# 5. CLEANING SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("VENDOR PORTAL CLEANING SUMMARY")
print("=" * 60)

print("Original rows:", original_rows)
print("Final rows:", len(df))
print("Rows removed:", original_rows - len(df))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDuplicate po_id:")
print(df["po_id"].duplicated().sum())

print("\nCurrency values:")
print(df["currency"].value_counts())

print("\nNegative quantity:")
print((df["quantity_ordered"] < 0).sum())

print("\nZero quantity:")
print((df["quantity_ordered"] == 0).sum())

print("\nNegative unit cost:")
print((df["unit_cost"] < 0).sum())

print("\nZero unit cost:")
print((df["unit_cost"] == 0).sum())

print("\nRatings outside 1-5:")
print(
    (
        (df["vendor_rating_at_po"] < 1) |
        (df["vendor_rating_at_po"] > 5)
    ).sum()
)

print("\nDate validation:")
for col in date_columns:
    print(col, "invalid:", df[col].isna().sum())

print("\nData types:")
print(df.dtypes)

# ============================================================
# 8. VENDOR PORTAL BUSINESS VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("VENDOR PORTAL BUSINESS VALIDATION")
print("=" * 60)


# ------------------------------------------------------------
# 1. BASIC VALIDATION
# ------------------------------------------------------------

print("\nFinal row count:")
print(len(df))

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDuplicate po_id:")
print(df["po_id"].duplicated().sum())


# ------------------------------------------------------------
# 2. REQUIRED FIELD VALIDATION
# ------------------------------------------------------------

required_columns = [
    "po_id",
    "supplier_id",
    "product_id",
    "destination_warehouse_id",
    "po_date",
    "quantity_ordered",
    "unit_cost",
    "currency",
    "expected_arrival_date",
    "vendor_rating_at_po"
]

print("\nMissing required fields:")

for col in required_columns:
    print(col, ":", df[col].isna().sum())


# ------------------------------------------------------------
# 3. QUANTITY VALIDATION
# ------------------------------------------------------------

print("\nNegative quantity_ordered:")
print((df["quantity_ordered"] < 0).sum())

print("\nZero quantity_ordered:")
print((df["quantity_ordered"] == 0).sum())


# ------------------------------------------------------------
# 4. UNIT COST VALIDATION
# ------------------------------------------------------------

print("\nNegative unit_cost:")
print((df["unit_cost"] < 0).sum())

print("\nZero unit_cost:")
print((df["unit_cost"] == 0).sum())


# ------------------------------------------------------------
# 5. CURRENCY VALIDATION
# ------------------------------------------------------------

expected_currencies = {
    "USD",
    "EUR",
    "INR"
}

actual_currencies = set(
    df["currency"].dropna().unique()
)

print("\nActual currencies:")
print(actual_currencies)

print("\nUnexpected currencies:")
print(actual_currencies - expected_currencies)


# ------------------------------------------------------------
# 6. VENDOR RATING VALIDATION
# ------------------------------------------------------------

print("\nVendor rating minimum:")
print(df["vendor_rating_at_po"].min())

print("\nVendor rating maximum:")
print(df["vendor_rating_at_po"].max())

print("\nRatings outside 1-5:")
print(
    (
        (df["vendor_rating_at_po"] < 1) |
        (df["vendor_rating_at_po"] > 5)
    ).sum()
)


# ------------------------------------------------------------
# 7. DATE VALIDATION
# ------------------------------------------------------------

print("\nMissing PO dates:")
print(df["po_date"].isna().sum())

print("\nMissing acknowledged dates:")
print(df["acknowledged_date"].isna().sum())

print("\nMissing expected arrival dates:")
print(df["expected_arrival_date"].isna().sum())


# ------------------------------------------------------------
# 8. DATE BUSINESS RULES
# ------------------------------------------------------------

print("\nAcknowledged date before PO date:")

invalid_ack = (
    df["acknowledged_date"].notna() &
    (df["acknowledged_date"] < df["po_date"])
)

print(invalid_ack.sum())


print("\nExpected arrival before PO date:")

invalid_arrival = (
    df["expected_arrival_date"] < df["po_date"]
)

print(invalid_arrival.sum())


print("\nExpected arrival before acknowledged date:")

invalid_sequence = (
    df["acknowledged_date"].notna() &
    (df["expected_arrival_date"] < df["acknowledged_date"])
)

print(invalid_sequence.sum())


# ------------------------------------------------------------
# 9. FINAL VALIDATION RESULT
# ------------------------------------------------------------

validation_passed = (
    len(df) == 1100
    and df.duplicated().sum() == 0
    and df["po_id"].duplicated().sum() == 0

    # Required fields
    and all(
        df[col].isna().sum() == 0
        for col in required_columns
    )

    # Quantity
    and (df["quantity_ordered"] < 0).sum() == 0
    and (df["quantity_ordered"] == 0).sum() == 0

    # Unit cost
    and (df["unit_cost"] < 0).sum() == 0
    and (df["unit_cost"] == 0).sum() == 0

    # Currency
    and len(actual_currencies - expected_currencies) == 0

    # Rating
    and (
        (
            (df["vendor_rating_at_po"] < 1) |
            (df["vendor_rating_at_po"] > 5)
        ).sum() == 0
    )

    # Required dates
    and df["po_date"].isna().sum() == 0
    and df["expected_arrival_date"].isna().sum() == 0

    # Date relationships
    and invalid_ack.sum() == 0
    and invalid_arrival.sum() == 0
    and invalid_sequence.sum() == 0
)


print("\n" + "=" * 60)

if validation_passed:
    print("VENDOR PORTAL BUSINESS VALIDATION PASSED")
else:
    print("VENDOR PORTAL BUSINESS VALIDATION FAILED")

print("=" * 60)

# ============================================================
# 9. PREPARE DATA FOR SILVER
# ============================================================

print("\n" + "=" * 60)
print("PREPARING VENDOR PORTAL DATA FOR SILVER")
print("=" * 60)

date_columns = [
    "po_date",
    "acknowledged_date",
    "expected_arrival_date"
]

for col in date_columns:
    df[col] = df[col].dt.date

print("\nData types before loading:")
print(df.dtypes)

# ============================================================
# 10. LOAD INTO SILVER
# ============================================================

print("\n" + "=" * 60)
print("LOADING VENDOR PORTAL DATA INTO SILVER")
print("=" * 60)

df.to_sql(
    "vendor_portal",
    engine,
    schema="silver",
    if_exists="append",
    index=False
)

print(
    "\nVendor Portal data loaded successfully "
    "into silver.vendor_portal"
)