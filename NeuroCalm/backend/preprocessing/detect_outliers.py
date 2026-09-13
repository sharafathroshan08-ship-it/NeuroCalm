import os
import pandas as pd

# ============================================================
# PROJECT PATHS
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

DATA_PATH = os.path.join(
    PROJECT_DIR,
    "dataset",
    "raw",
    "StressLevelDataset.csv"
)

# ============================================================
# LOAD PRIMARY DATASET
# ============================================================

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("NEUROCALM - IQR OUTLIER DETECTION")
print("=" * 60)

print("\nDataset Shape:", df.shape)

# Select numeric feature columns
numeric_cols = df.select_dtypes(
    include=["number"]
).columns.tolist()

# Do not check target as an input outlier
if "stress_level" in numeric_cols:
    numeric_cols.remove("stress_level")

total_outliers = 0

# ============================================================
# IQR METHOD
# ============================================================

for col in numeric_cols:

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[
        (df[col] < lower_bound) |
        (df[col] > upper_bound)
    ]

    count = len(outliers)

    total_outliers += count

    if count > 0:
        print(
            f"{col}: {count} outlier(s)"
        )

# ============================================================
# RESULT
# ============================================================

print("\n" + "-" * 60)

print(
    "Total feature-level outlier observations:",
    total_outliers
)

if total_outliers == 0:
    print("✅ No IQR outliers detected.")

else:
    print(
        "⚠️ IQR outliers detected."
    )

print("=" * 60)
print("✅ IQR outlier detection completed!")