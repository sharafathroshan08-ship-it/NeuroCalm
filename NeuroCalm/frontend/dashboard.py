import os
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# NEUROCALM - DASHBOARD
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

HISTORY_FILE = os.path.join(
    PROJECT_DIR,
    "dataset",
    "processed",
    "stress_history.csv"
)


# ============================================================
# LOAD HISTORY
# ============================================================

if not os.path.exists(HISTORY_FILE):

    print("❌ Stress history not found.")
    exit()

df = pd.read_csv(HISTORY_FILE)

if df.empty:

    print("❌ No stress assessments available.")
    exit()


df["stress_score"] = pd.to_numeric(
    df["stress_score"],
    errors="coerce"
)

df = df.dropna(
    subset=["stress_score"]
).reset_index(drop=True)


# ============================================================
# CURRENT RESULT
# ============================================================

latest = df.iloc[-1]

latest_score = latest["stress_score"]
latest_level = latest["stress_level"]


# ============================================================
# AVERAGE
# ============================================================

average_score = df["stress_score"].mean()


# ============================================================
# TREND
# ============================================================

if len(df) < 2:

    trend = "Not enough data"

else:

    previous = df.iloc[-2]["stress_score"]

    difference = latest_score - previous

    if difference > 5:
        trend = "Increasing ↗️"

    elif difference < -5:
        trend = "Decreasing ↘️"

    else:
        trend = "Stable →"


# ============================================================
# DASHBOARD
# ============================================================

print("=" * 60)
print("              🧠 NEUROCALM DASHBOARD")
print("=" * 60)

print("\n📊 CURRENT STRESS")
print("---------------------------------------------")

print(
    f"Stress Score : {latest_score:.0f}%"
)

print(
    f"Stress Level : {latest_level}"
)

print(
    f"Average Score: {average_score:.0f}%"
)

print(
    f"Trend        : {trend}"
)


# ============================================================
# HISTORY
# ============================================================

print("\n📅 STRESS HISTORY")
print("---------------------------------------------")

for _, row in df.tail(7).iterrows():

    print(
        f"{row['date']} → "
        f"{row['stress_score']:.0f}% → "
        f"{row['stress_level']}"
    )


# ============================================================
# GRAPH
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    range(1, len(df) + 1),
    df["stress_score"],
    marker="o",
    linewidth=2
)

plt.title(
    "NeuroCalm Stress History"
)

plt.xlabel(
    "Assessment"
)

plt.ylabel(
    "Stress Score (%)"
)

plt.ylim(
    0,
    100
)

plt.grid(
    True,
    linestyle=":"
)

plt.tight_layout()

plt.show()


print("\n" + "=" * 60)
print("       ✅ DASHBOARD LOADED SUCCESSFULLY")
print("=" * 60)