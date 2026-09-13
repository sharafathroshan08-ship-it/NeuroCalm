import os
import pandas as pd


# ============================================================
# NEUROCALM - STRESS TREND ANALYZER
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
# LOAD STRESS HISTORY
# ============================================================

def load_history():

    if not os.path.exists(HISTORY_FILE):
        return pd.DataFrame(
            columns=[
                "date",
                "time",
                "stress_score",
                "stress_level"
            ]
        )

    df = pd.read_csv(HISTORY_FILE)

    if df.empty:
        return df

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["stress_score"] = pd.to_numeric(
        df["stress_score"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["date", "stress_score"]
    )

    return df


# ============================================================
# WEEKLY AVERAGE
# ============================================================

def calculate_weekly_average(df):

    if df.empty:
        return 0

    today = pd.Timestamp.today().normalize()

    week_start = today - pd.Timedelta(days=6)

    weekly_data = df[
        df["date"].between(
            week_start,
            today
        )
    ]

    if weekly_data.empty:
        return 0

    return round(
        weekly_data["stress_score"].mean(),
        2
    )


# ============================================================
# STRESS TREND
# ============================================================

def calculate_trend(df):

    if len(df) < 2:
        return "Not enough data"

    recent = df.tail(2)

    previous_score = recent.iloc[0]["stress_score"]
    latest_score = recent.iloc[1]["stress_score"]

    difference = latest_score - previous_score

    if difference > 5:
        return "Stress is increasing ↗️"

    elif difference < -5:
        return "Stress is decreasing ↘️"

    else:
        return "Stress is stable →"


# ============================================================
# DISPLAY TREND REPORT
# ============================================================

def display_trend():

    df = load_history()

    print("=" * 60)
    print("       NEUROCALM - STRESS TREND ANALYSIS")
    print("=" * 60)

    if df.empty:

        print("\n❌ No stress history available.")

        print(
            "\nComplete at least one stress assessment "
            "to generate trend information."
        )

        return

    # --------------------------------------------------------
    # WEEKLY AVERAGE
    # --------------------------------------------------------

    weekly_average = calculate_weekly_average(df)

    print(
        f"\n📊 WEEKLY AVERAGE : "
        f"{weekly_average:.0f}%"
    )

    # --------------------------------------------------------
    # RECENT RESULTS
    # --------------------------------------------------------

    print("\n📅 RECENT RESULTS")
    print("-" * 45)

    recent_results = df.tail(7)

    for _, row in recent_results.iterrows():

        date = row["date"].strftime("%Y-%m-%d")

        score = row["stress_score"]

        level = row["stress_level"]

        print(
            f"{date} → "
            f"{score:.0f}% → "
            f"{level}"
        )

    # --------------------------------------------------------
    # TREND
    # --------------------------------------------------------

    trend = calculate_trend(df)

    print("\n📈 TREND")
    print("-" * 45)

    print(trend)

    print("\n" + "=" * 60)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    display_trend()