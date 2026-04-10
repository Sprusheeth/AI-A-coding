"""
Task 3 – Environmental Sensor Data Preparation
================================================
Clean and preprocess environmental sensor data using AI-assisted scripts.

Steps:
  1. Handle missing values in temperature, humidity, and air_quality_index.
  2. Scale numerical features using standard scaling.
  3. Encode categorical fields such as sensor_status.
  4. Split the dataset into training and testing subsets.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

# ── 1. Create sample sensor dataset ─────────────────────────────────────────
np.random.seed(42)
n = 20

raw_data = {
    "sensor_id":         np.random.choice(["S01", "S02", "S03", "S04"], n),
    "timestamp":         pd.date_range("2024-06-01", periods=n, freq="h"),
    "temperature":       np.where(
        np.random.rand(n) < 0.15, np.nan,
        np.round(np.random.uniform(20, 45, n), 1)
    ),
    "humidity":          np.where(
        np.random.rand(n) < 0.10, np.nan,
        np.round(np.random.uniform(30, 90, n), 1)
    ),
    "air_quality_index": np.where(
        np.random.rand(n) < 0.20, np.nan,
        np.random.randint(50, 300, n).astype(float)
    ),
    "sensor_status":     np.random.choice(
        ["Active", "Inactive", "Maintenance", "Active", "Active"], n
    ),
}

data = pd.DataFrame(raw_data)

# Save raw CSV
data.to_csv("sensor_data.csv", index=False)

print("=" * 60)
print("ORIGINAL DATASET")
print("=" * 60)
print(data)
print(f"\nShape : {data.shape}")
print(f"Nulls :\n{data.isnull().sum()}")

# ── 2. Handle missing values ────────────────────────────────────────────────
# Fill numerical columns with their respective column means
for col in ["temperature", "humidity", "air_quality_index"]:
    mean_val = data[col].mean()
    data[col] = data[col].fillna(mean_val)
    print(f">> Filled missing '{col}' with mean = {mean_val:.2f}")

print(f"\nNulls after filling:\n{data.isnull().sum()}")

# ── 3. Scale numerical features using StandardScaler ────────────────────────
numerical_cols = ["temperature", "humidity", "air_quality_index"]
scaler = StandardScaler()
data[["temp_scaled", "humidity_scaled", "aqi_scaled"]] = scaler.fit_transform(
    data[numerical_cols]
)
print("\n>> Applied StandardScaler to numerical features.")
print(f"   Means  : {dict(zip(numerical_cols, np.round(scaler.mean_, 2)))}")
print(f"   Scales : {dict(zip(numerical_cols, np.round(scaler.scale_, 2)))}")

# ── 4. Encode categorical field (sensor_status) ─────────────────────────────
le = LabelEncoder()
data["status_encoded"] = le.fit_transform(data["sensor_status"])
print(f"\n>> Encoded 'sensor_status'.")
print(f"   Mapping: {dict(zip(le.classes_, le.transform(le.classes_)))}")

# ── 5. Split into training and testing subsets ───────────────────────────────
# Use scaled numerical features + encoded status as features
feature_cols = ["temp_scaled", "humidity_scaled", "aqi_scaled", "status_encoded"]
target_col   = "air_quality_index"   # Using original AQI as the target

X = data[feature_cols]
y = data[target_col]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\n>> Train-test split (80/20):")
print(f"   X_train : {X_train.shape}  |  y_train : {y_train.shape}")
print(f"   X_test  : {X_test.shape}   |  y_test  : {y_test.shape}")

# ── 6. Display preprocessed dataset ─────────────────────────────────────────
print("\n" + "=" * 60)
print("PREPROCESSED DATASET")
print("=" * 60)
print(data.to_string())

# Save cleaned CSV
data.to_csv("sensor_data_cleaned.csv", index=False)
print("\n>> Saved preprocessed dataset to 'sensor_data_cleaned.csv'.")
