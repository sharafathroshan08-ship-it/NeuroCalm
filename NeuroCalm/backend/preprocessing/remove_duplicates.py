import os
import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
DATASET_DIR = os.path.join(PROJECT_DIR, "dataset", "raw")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "dataset", "processed")

os.makedirs(OUTPUT_DIR, exist_ok=True)

files = [
    "StressLevelDataset.csv",
    "Stress_Dataset.csv",
    "academic Stress level - maintainance 1.csv",
    "Student Stress Factors.csv",
    "Student Stress Factors (2).csv"
]

for file in files:
    path = os.path.join(DATASET_DIR, file)
    df = pd.read_csv(path)

    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    print(f"\n{file}")
    print(f"Before : {before}")
    print(f"After  : {after}")
    print(f"Removed: {before - after}")

    output_path = os.path.join(OUTPUT_DIR, file)
    df.to_csv(output_path, index=False)

print("\n✅ Duplicate removal completed!")