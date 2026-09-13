import os
import csv
from datetime import datetime


# ============================================================
# NEUROCALM - STRESS HISTORY
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

HISTORY_FILE = os.path.join(
    PROJECT_DIR,
    "dataset",
    "processed",
    "stress_history.csv"
)


# ============================================================
# CREATE HISTORY FILE
# ============================================================

def create_history_file():

    os.makedirs(
        os.path.dirname(HISTORY_FILE),
        exist_ok=True
    )

    if not os.path.exists(HISTORY_FILE):

        with open(
            HISTORY_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "date",
                "time",
                "stress_score",
                "stress_level"
            ])


# ============================================================
# SAVE STRESS RESULT
# ============================================================

def save_stress_result(
    stress_score,
    stress_level
):

    create_history_file()

    now = datetime.now()

    with open(
        HISTORY_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            round(stress_score, 2),
            stress_level
        ])


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    save_stress_result(
        50,
        "Moderate"
    )

    print("=" * 60)
    print("NEUROCALM - STRESS HISTORY")
    print("=" * 60)

    print("\n✅ Stress result saved successfully!")

    print("\nSaved to:")
    print(HISTORY_FILE)