import os
import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler

# Project paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

INPUT_DIR = os.path.join(PROJECT_DIR, "dataset", "processed")
MODEL_DIR = os.path.join(PROJECT_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)

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

    # Select numeric columns
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    # Do not normalize target column
    if "stress_level" in numeric_cols:
        numeric_cols.remove("stress_level")

    # Normalize numeric columns
    if len(numeric_cols) > 0:

        scaler = MinMaxScaler()

        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

        print("Numeric columns normalized:", len(numeric_cols))

        # Save scaler for the primary dataset
        if file == "StressLevelDataset.csv":

            scaler_path = os.path.join(
                MODEL_DIR,
                "neurocalm_scaler.pkl"
            )

            joblib.dump(scaler, scaler_path)

            print("Scaler saved successfully!")
            print("Scaler:", scaler_path)

    # Save processed dataset
    df.to_csv(path, index=False)

print("\n✅ Min-Max normalization completed!")