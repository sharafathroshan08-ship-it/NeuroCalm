import os
import pandas as pd

# Current file path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Project root (go up two folders)
PROJECT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

# Dataset folder
DATASET_DIR = os.path.join(PROJECT_DIR, "dataset", "raw")

print("Dataset Folder:", DATASET_DIR)

files = [
    "StressLevelDataset.csv",
    "Stress_Dataset.csv",
    "academic Stress level - maintainance 1.csv",
    "Student Stress Factors.csv",
    "Student Stress Factors (2).csv"
]

for file in files:
    print("\n" + "=" * 60)
    print("Loading:", file)

    file_path = os.path.join(DATASET_DIR, file)

    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        continue

    df = pd.read_csv(file_path)

    print("Shape:", df.shape)
    print("Missing Values:", df.isnull().sum().sum())
    print("Duplicate Rows:", df.duplicated().sum())
    print("Columns:")
    print(df.columns.tolist())