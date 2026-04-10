"""
Task 2 – Financial Transaction Data Preprocessing
===================================================
Preprocess financial transaction data using AI-generated Python code.

Steps:
  1. Convert transaction date columns to datetime format.
  2. Create derived features such as transaction month and year.
  3. Normalize the transaction amount column.
  4. Identify and handle extreme transaction values.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# ── 1. Create sample transaction dataset ─────────────────────────────────────
np.random.seed(42)
n = 15

raw_data = {
    "transaction_id": range(1001, 1001 + n),
    "customer_id":    np.random.choice([201, 202, 203, 204, 205], n),
    "transaction_date": [
        "2024-01-15", "2024/02/20", "15-03-2024", "2024-04-10",
        "2024-05-22", "06/15/2024", "2024-07-08", "2024-08-19",
        "2024-09-30", "2024-10-05", "2024-11-11", "2024-12-25",
        "2025-01-01", "2025-02-14", "2025-03-17",
    ],
    "amount": [
        250.0, 1200.0, 75.0, 500.0, 50000.0,   # 50000 is an outlier
        340.0, 890.0, 120.0, 99999.0, 430.0,     # 99999 is an outlier
        670.0, 310.0, 1500.0, 210.0, 780.0,
    ],
    "category": [
        "Food", "Electronics", "Food", "Clothing", "Electronics",
        "Utilities", "Food", "Clothing", "Electronics", "Utilities",
        "Food", "Clothing", "Electronics", "Food", "Utilities",
    ],
}

transactions = pd.DataFrame(raw_data)

# Save raw CSV
transactions.to_csv("transactions.csv", index=False)

print("=" * 65)
print("ORIGINAL DATASET")
print("=" * 65)
print(transactions)
print(f"\n{transactions.info()}")

# ── 2. Convert dates to datetime ────────────────────────────────────────────
transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"], dayfirst=False, format="mixed"
)
print("\n>> Converted 'transaction_date' to datetime.")

# ── 3. Create derived time features ─────────────────────────────────────────
transactions["transaction_year"]    = transactions["transaction_date"].dt.year
transactions["transaction_month"]   = transactions["transaction_date"].dt.month
transactions["transaction_day"]     = transactions["transaction_date"].dt.day
transactions["transaction_weekday"] = transactions["transaction_date"].dt.day_name()

print(">> Created derived features: year, month, day, weekday.")

# ── 4. Identify and handle extreme values (outliers) ────────────────────────
Q1 = transactions["amount"].quantile(0.25)
Q3 = transactions["amount"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = transactions[
    (transactions["amount"] < lower_bound) |
    (transactions["amount"] > upper_bound)
]
print(f"\n>> Outlier bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
print(f">> Outliers detected ({len(outliers)}):")
print(outliers[["transaction_id", "amount"]])

# Cap (winsorize) outliers to the bounds
transactions["amount"] = transactions["amount"].clip(lower=lower_bound,
                                                      upper=upper_bound)
print(">> Capped extreme values to IQR bounds.")

# ── 5. Normalize transaction amount ─────────────────────────────────────────
scaler = MinMaxScaler()
transactions["amount_normalized"] = scaler.fit_transform(
    transactions[["amount"]]
)
print(">> Normalized 'amount' using MinMaxScaler.")

# ── 6. Display transformed dataset ──────────────────────────────────────────
print("\n" + "=" * 65)
print("TRANSFORMED DATASET")
print("=" * 65)
print(transactions.to_string())

# Save cleaned CSV
transactions.to_csv("transactions_cleaned.csv", index=False)
print("\n>> Saved transformed dataset to 'transactions_cleaned.csv'.")
