import pandas as pd
from sqlalchemy import create_engine

# ============================================================
# DATABASE CONNECTION
# ============================================================

engine = create_engine(
    "postgresql+psycopg2://postgres:acm124#@localhost:5432/eldp"
)

print("=" * 60)
print("ERP CUSTOMERS - SPRINT 2 PREPROCESSING")
print("=" * 60)

# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_sql(
    "SELECT * FROM staging.erp_customers",
    engine
)

print("\nData loaded successfully from staging.erp_customers")

# ============================================================
# PROFILING
# ============================================================

print("\n" + "=" * 60)
print("ERP CUSTOMERS PROFILING")
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