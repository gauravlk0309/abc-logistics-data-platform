import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:acm1234%23@localhost:5432/eldp"
)

print("=" * 70)
print("BUILDING GOLD.FACT_CUSTOMER_FEEDBACK")
print("=" * 70)


# ============================================================
# 1. READ SOURCE AND CUSTOMER DIMENSION
# ============================================================

feedback = pd.read_sql(
    """
    SELECT *
    FROM silver.customer_feedback
    """,
    engine
)

customer = pd.read_sql(
    """
    SELECT customer_key, customer_id
    FROM gold.dim_customer
    """,
    engine
)

print("\nSilver Customer Feedback records:", len(feedback))
print("Customer dimension records:", len(customer))


# ============================================================
# 2. CHECK SOURCE GRAIN
# ============================================================

print("\nChecking feedback grain...")

print(
    "Duplicate feedback IDs:",
    feedback["feedback_id"].duplicated().sum()
)


# ============================================================
# 3. LOOKUP CUSTOMER SURROGATE KEY
# ============================================================

fact = feedback.merge(
    customer,
    on="customer_id",
    how="left"
)

print(
    "Unmatched customer records:",
    fact["customer_key"].isnull().sum()
)


# ============================================================
# 4. CREATE FACT SURROGATE KEY
# ============================================================

fact.insert(
    0,
    "feedback_key",
    range(1, len(fact) + 1)
)


# ============================================================
# 5. SELECT FACT COLUMNS
# ============================================================

fact_customer_feedback = fact[
    [
        "feedback_key",
        "feedback_id",
        "customer_key",
        "shipment_id",
        "rating",
        "on_time_delivery",
        "comments",
        "feedback_date",
        "channel"
    ]
]


# ============================================================
# 6. CREATE GOLD SCHEMA
# ============================================================

with engine.begin() as conn:
    conn.execute(
        text("CREATE SCHEMA IF NOT EXISTS gold")
    )


# ============================================================
# 7. LOAD FACT TABLE
# ============================================================

fact_customer_feedback.to_sql(
    "fact_customer_feedback",
    engine,
    schema="gold",
    if_exists="replace",
    index=False
)


# ============================================================
# 8. ADD PRIMARY KEY
# ============================================================

with engine.begin() as conn:
    conn.execute(text("""
        ALTER TABLE gold.fact_customer_feedback
        ADD PRIMARY KEY (feedback_key)
    """))


# ============================================================
# 9. VERIFY FACT TABLE
# ============================================================

check = pd.read_sql(
    """
    SELECT *
    FROM gold.fact_customer_feedback
    ORDER BY feedback_key
    """,
    engine
)

print("\nGold fact table:")
print(check.head())

print("\nTotal fact records:", len(check))

print(
    "Duplicate feedback keys:",
    check["feedback_key"].duplicated().sum()
)

print(
    "Duplicate feedback IDs:",
    check["feedback_id"].duplicated().sum()
)

print(
    "NULL feedback keys:",
    check["feedback_key"].isnull().sum()
)

print(
    "NULL feedback IDs:",
    check["feedback_id"].isnull().sum()
)

print(
    "NULL customer keys:",
    check["customer_key"].isnull().sum()
)


# ============================================================
# 10. CHECK FEEDBACK DATA
# ============================================================

print("\nFeedback data NULL counts:")

print(
    "NULL shipment IDs:",
    check["shipment_id"].isnull().sum()
)

print(
    "NULL ratings:",
    check["rating"].isnull().sum()
)

print(
    "NULL on_time_delivery:",
    check["on_time_delivery"].isnull().sum()
)

print(
    "NULL comments:",
    check["comments"].isnull().sum()
)

print(
    "NULL feedback dates:",
    check["feedback_date"].isnull().sum()
)

print(
    "NULL channels:",
    check["channel"].isnull().sum()
)


print("\n" + "=" * 70)
print("FACT_CUSTOMER_FEEDBACK CREATED SUCCESSFULLY")
print("=" * 70)