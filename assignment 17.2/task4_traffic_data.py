"""
Task 4 – Real-Time Application: Smart City Traffic Data Cleaning
=================================================================
A smart city system collects traffic data from multiple sensors,
resulting in noisy and inconsistent records.

Steps:
  1. Standardize road and location names.
  2. Fill missing traffic density values using appropriate statistical methods.
  3. Remove duplicate sensor readings.
  4. Normalize speed and vehicle count metrics.
  5. Generate a brief summary comparing dataset quality before and after cleaning.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# ── 1. Create sample traffic dataset ────────────────────────────────────────
np.random.seed(42)
n = 20

roads_raw = [
    "Main Street", "main street", "MAIN STREET", "Main St.",
    "  Broadway ", "broadway", "BROADWAY", "Broadway Ave",
    "MG Road", "mg road", "M.G. Road", "MG Road",
    "Park Lane", "park lane", "PARK LANE", "Park Ln.",
    "Main Street", "Broadway", "MG Road", "Park Lane",
]

locations_raw = [
    "Zone-A", "zone a", "ZONE A", "Zone A",
    "Zone-B", "zone-b", "ZONE B", "Zone B",
    "Zone-A", "Zone A", "zone a", "ZONE-A",
    "Zone-B", "zone b", "ZONE-B", "Zone B",
    "Zone-A", "Zone-B", "Zone-A", "Zone-B",
]

raw_data = {
    "sensor_id":       [f"TS{str(i).zfill(3)}" for i in range(1, n + 1)],
    "timestamp":       pd.date_range("2024-09-01 06:00", periods=n, freq="30min"),
    "road_name":       roads_raw,
    "location":        locations_raw,
    "traffic_density": np.where(
        np.random.rand(n) < 0.20, np.nan,
        np.random.randint(20, 100, n).astype(float)
    ),
    "avg_speed_kmh":   np.round(np.random.uniform(10, 80, n), 1),
    "vehicle_count":   np.random.randint(50, 500, n),
}

traffic = pd.DataFrame(raw_data)
# Inject a duplicate row
traffic = pd.concat([traffic, traffic.iloc[[2]]], ignore_index=True)

# Save raw CSV
traffic.to_csv("traffic_data.csv", index=False)

print("=" * 70)
print("ORIGINAL DATASET")
print("=" * 70)
print(traffic.to_string())

# ── Capture "before" quality metrics ────────────────────────────────────────
before_shape      = traffic.shape
before_nulls      = traffic.isnull().sum().sum()
before_duplicates = traffic.duplicated().sum()
before_describe   = traffic.describe()

# ── 2. Remove duplicate sensor readings ─────────────────────────────────────
traffic = traffic.drop_duplicates().reset_index(drop=True)
print(f"\n>> Removed duplicates. Shape: {before_shape} → {traffic.shape}")

# ── 3. Standardize road and location names ──────────────────────────────────
road_map = {
    "main street": "Main Street",
    "main st.":    "Main Street",
    "broadway":    "Broadway",
    "broadway ave":"Broadway",
    "mg road":     "MG Road",
    "m.g. road":   "MG Road",
    "park lane":   "Park Lane",
    "park ln.":    "Park Lane",
}

location_map = {
    "zone-a": "Zone A",
    "zone a": "Zone A",
    "zone-b": "Zone B",
    "zone b": "Zone B",
}

traffic["road_name"] = (
    traffic["road_name"].str.strip().str.lower().map(road_map)
)
traffic["location"] = (
    traffic["location"].str.strip().str.lower().map(location_map)
)
print(">> Standardized road and location names.")

# ── 4. Fill missing traffic density using group median ──────────────────────
# Use median density per road to fill gaps (more robust than mean)
traffic["traffic_density"] = traffic.groupby("road_name")[
    "traffic_density"
].transform(lambda x: x.fillna(x.median()))

# Fallback: overall median for any remaining NaNs
traffic["traffic_density"] = traffic["traffic_density"].fillna(traffic["traffic_density"].median())
print(">> Filled missing traffic_density with group median.")

# ── 5. Normalize speed and vehicle count ────────────────────────────────────
scaler = MinMaxScaler()
traffic[["speed_normalized", "vehicle_count_normalized"]] = scaler.fit_transform(
    traffic[["avg_speed_kmh", "vehicle_count"]]
)
print(">> Normalized 'avg_speed_kmh' and 'vehicle_count' using MinMaxScaler.")

# ── 6. Data-quality improvement summary ─────────────────────────────────────
after_shape      = traffic.shape
after_nulls      = traffic.isnull().sum().sum()
after_duplicates = traffic.duplicated().sum()

print("\n" + "=" * 70)
print("DATA-QUALITY IMPROVEMENT SUMMARY")
print("=" * 70)
summary = pd.DataFrame({
    "Metric":  ["Rows", "Columns", "Total Nulls", "Duplicate Rows"],
    "Before":  [before_shape[0], before_shape[1], before_nulls, before_duplicates],
    "After":   [after_shape[0], after_shape[1], after_nulls, after_duplicates],
})
summary["Change"] = summary["After"].astype(int) - summary["Before"].astype(int)
print(summary.to_string(index=False))

print(f"\n>> Road names unique values  : {traffic['road_name'].nunique()} "
      f"(standardized)")
print(f">> Location unique values    : {traffic['location'].nunique()} "
      f"(standardized)")
print(f">> Normalized columns added  : speed_normalized, vehicle_count_normalized")

# ── 7. Display cleaned dataset ──────────────────────────────────────────────
print("\n" + "=" * 70)
print("CLEANED & NORMALIZED DATASET")
print("=" * 70)
print(traffic.to_string())

# Save cleaned CSV
traffic.to_csv("traffic_data_cleaned.csv", index=False)
print("\n>> Saved cleaned dataset to 'traffic_data_cleaned.csv'.")
