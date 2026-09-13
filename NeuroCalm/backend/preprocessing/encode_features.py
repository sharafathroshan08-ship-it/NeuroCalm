import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder

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

    print("Text columns before encoding:")

    text_cols = df.select_dtypes(
        include=["object", "string"]
    ).columns.tolist()

    print(text_cols)

    for col in text_cols:
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col].astype(str))

    print("Text columns after encoding:")
    print(df.select_dtypes(
        include=["object", "string"]
    ).columns.tolist())

    df.to_csv(path, index=False)

    print("Encoding completed.")

print("\n✅ Feature encoding completed!")