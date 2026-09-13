import os
import pandas as pd

# Get backend folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Get dataset/raw folder path
DATASET_DIR = os.path.join(BASE_DIR, "..", "dataset", "raw")

files = [
    "StressLevelDataset.csv",
    "Stress_Dataset.csv",
    "academic Stress level - maintainance 1.csv",
    "Student Stress Factors.csv",
    "Student Stress Factors (2).csv"
]

for file in files:
    path = os.path.join(DATASET_DIR, file)

    print("=" * 60)
    print("Loading:", file)

    if os.path.exists(path):
        df = pd.read_csv(path)
        print("Shape:", df.shape)
        print(df.head())
    else:
        print("❌ File not found:", path)