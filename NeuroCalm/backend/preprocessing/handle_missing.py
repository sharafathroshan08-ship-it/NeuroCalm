import os
import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

INPUT_DIR = os.path.join(PROJECT_DIR, "dataset", "processed")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "dataset", "processed")

files = [
    "StressLevelDataset.csv",
    "Stress_Dataset.csv",
    "academic Stress level - maintainance 1.csv",
    "Student Stress Factors.csv",
    "Student Stress Factors (2).csv"
]

for file in files:

    print("=" * 60)
    print(file)

    path = os.path.join(INPUT_DIR, file)

    df = pd.read_csv(path)

    print("Missing Before:", df.isnull().sum().sum())

    # Fill numeric columns with median
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    # Fill text columns with mode
    object_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in object_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].mode()[0])

    print("Missing After :", df.isnull().sum().sum())

    df.to_csv(path, index=False)

print("\n✅ Missing value handling completed!")