"""
Task 1 – Student Academic Data Cleaning
========================================
Use AI assistance to generate a Python script that cleans and prepares
a student academic dataset for analysis.

Steps:
  1. Handle missing values in marks, attendance, and department.
  2. Remove duplicate student records based on student ID.
  3. Standardize text fields such as department names.
  4. Encode categorical variables like gender and department.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

# ── 1. Create sample student dataset ──────────────────────────────────────────
np.random.seed(42)

raw_data = {
    "student_id":  [101, 102, 103, 104, 105, 106, 107, 108, 103, 109],
    "name":        ["Alice", "Bob", "Charlie", "Diana", "Eve",
                    "Frank", "Grace", "Hank", "Charlie", "Ivy"],
    "gender":      ["Female", "Male", "Male", "Female", "Female",
                    "Male", "Female", "Male", "Male", "Female"],
    "department":  ["computer science", "Computer Science", "  Physics",
                    "MATHEMATICS", "physics", "Comp. Sci.", np.nan,
                    "Mathematics", "physics", "computer science"],
    "marks":       [85, np.nan, 72, 90, np.nan, 65, 78, np.nan, 72, 88],
    "attendance":  [92, 85, np.nan, 88, 76, np.nan, 95, 80, np.nan, 91],
}

data = pd.DataFrame(raw_data)

# Save raw CSV for reference
data.to_csv("students.csv", index=False)

print("=" * 60)
print("ORIGINAL DATASET")
print("=" * 60)
print(data)
print(f"\nShape : {data.shape}")
print(f"Nulls :\n{data.isnull().sum()}")
print(f"Duplicates (student_id): {data.duplicated(subset='student_id').sum()}")

# ── 2. Remove duplicate records based on student_id ──────────────────────────
data = data.drop_duplicates(subset="student_id", keep="first").reset_index(drop=True)
print(f"\n>> Removed duplicates. New shape: {data.shape}")

# ── 3. Standardize department names ──────────────────────────────────────────
# Strip whitespace, convert to title case, and unify common abbreviations
dept_map = {
    "comp. sci.": "Computer Science",
    "computer science": "Computer Science",
    "physics": "Physics",
    "mathematics": "Mathematics",
}

data["department"] = (
    data["department"]
    .str.strip()
    .str.lower()
    .map(dept_map)
)
print(">> Standardized department names.")

# ── 4. Handle missing values ────────────────────────────────────────────────
# Fill missing marks & attendance with column median
data["marks"] = data["marks"].fillna(data["marks"].median())
data["attendance"] = data["attendance"].fillna(data["attendance"].median())

# Fill missing department with the mode (most frequent department)
data["department"] = data["department"].fillna(data["department"].mode()[0])

print(">> Filled missing values (median for numeric, mode for categorical).")

# ── 5. Encode categorical variables ─────────────────────────────────────────
le_gender = LabelEncoder()
le_dept   = LabelEncoder()

data["gender_encoded"]     = le_gender.fit_transform(data["gender"])
data["department_encoded"] = le_dept.fit_transform(data["department"])

print(">> Encoded 'gender' and 'department'.")
print(f"   Gender mapping  : {dict(zip(le_gender.classes_, le_gender.transform(le_gender.classes_)))}")
print(f"   Dept mapping    : {dict(zip(le_dept.classes_, le_dept.transform(le_dept.classes_)))}")

# ── 6. Display cleaned dataset ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("CLEANED & ENCODED DATASET")
print("=" * 60)
print(data)
print(f"\nShape : {data.shape}")
print(f"Nulls :\n{data.isnull().sum()}")

# Save cleaned CSV
data.to_csv("students_cleaned.csv", index=False)
print("\n>> Saved cleaned dataset to 'students_cleaned.csv'.")
