import os
import pandas as pd
from datetime import datetime

# ============================================================
# PROJECT PATHS
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

HISTORY_DIR = os.path.join(
    PROJECT_DIR,
    "dataset",
    "history"
)

HISTORY_FILE = os.path.join(
    HISTORY_DIR,
    "stress_history.csv"
)

os.makedirs(HISTORY_DIR, exist_ok=True)

# ============================================================
# SAVE CURRENT ASSESSMENT
# ============================================================

def save_assessment(stress_score, stress_level):

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    new_record = pd.DataFrame({
        "date": [current_time],
        "stress_score": [stress_score],
        "stress_level": [stress_level]
    })

    if os.path.exists(HISTORY_FILE):

        history = pd.read_csv(HISTORY_FILE)

        history = pd.concat(
            [history, new_record],
            ignore_index=True
        )

    else:

        history = new_record

    history.to_csv(
        HISTORY_FILE,
        index=False
    )

    return history


# ============================================================
# ANALYZE STRESS TREND
# ============================================================

def analyze_trend(history):

    if len(history) < 2:

        return {
            "trend": "No previous data",
            "change": 0.0,
            "average_score": round(
                history["stress_score"].mean(),
                2
            )
        }

    previous_score = float(
        history.iloc[-2]["stress_score"]
    )

    current_score = float(
        history.iloc[-1]["stress_score"]
    )

    change = current_score - previous_score

    average_score = float(
        history["stress_score"].mean()
    )

    if change > 5:

        trend = "Increasing"

    elif change < -5:

        trend = "Improving"

    else:

        trend = "Stable"

    return {
        "trend": trend,
        "change": round(change, 2),
        "average_score": round(average_score, 2)
    }


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("NEUROCALM - TEMPORAL BEHAVIOUR MODELING")
    print("=" * 60)

    # Test assessment
    test_score = 62
    test_level = "High"

    history = save_assessment(
        test_score,
        test_level
    )

    result = analyze_trend(history)

    print("\nAssessment History:")
    print(history)

    print("\nTemporal Analysis:")
    print(
        "Current Trend:",
        result["trend"]
    )

    print(
        "Score Change:",
        result["change"],
        "%"
    )

    print(
        "Average Stress Score:",
        result["average_score"],
        "%"
    )

    print("\nSaved to:")
    print(HISTORY_FILE)

    print("\n✅ Temporal Behaviour Modeling completed!")