import os
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# NEUROCALM - PROFESSIONAL STRESS TREND VISUALIZER
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

HISTORY_FILE = os.path.join(
    PROJECT_DIR,
    "dataset",
    "processed",
    "stress_history.csv"
)

GRAPH_PATH = os.path.join(
    PROJECT_DIR,
    "dataset",
    "processed",
    "stress_trend.png"
)


# ============================================================
# LOAD DATA
# ============================================================

if not os.path.exists(HISTORY_FILE):

    print("❌ Stress history file not found.")
    exit()


df = pd.read_csv(HISTORY_FILE)

if df.empty:

    print("❌ No stress history available.")
    exit()


df["stress_score"] = pd.to_numeric(
    df["stress_score"],
    errors="coerce"
)

df = df.dropna(
    subset=["stress_score"]
).reset_index(drop=True)


# ============================================================
# CREATE ASSESSMENT LABELS
# ============================================================

df["assessment"] = [
    f"Test {i + 1}"
    for i in range(len(df))
]


# ============================================================
# CREATE GRAPH
# ============================================================

plt.figure(figsize=(12, 7))

plt.plot(
    df["assessment"],
    df["stress_score"],
    marker="o",
    linewidth=2.5,
    markersize=8,
    label="Stress Score"
)


# ============================================================
# STRESS LEVEL REFERENCE LINES
# ============================================================

plt.axhline(
    y=33,
    linestyle="--",
    linewidth=1.5,
    label="Low / Moderate boundary"
)

plt.axhline(
    y=66,
    linestyle="--",
    linewidth=1.5,
    label="Moderate / High boundary"
)


# ============================================================
# LABEL EACH POINT
# ============================================================

for i, row in df.iterrows():

    score = row["stress_score"]

    plt.annotate(
        f"{score:.0f}%",
        (
            row["assessment"],
            score
        ),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize=10
    )


# ============================================================
# GRAPH SETTINGS
# ============================================================

plt.title(
    "NEUROCALM - PERSONAL STRESS TREND",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel(
    "Assessment",
    fontsize=12
)

plt.ylabel(
    "Stress Score (%)",
    fontsize=12
)

plt.ylim(
    0,
    100
)

plt.yticks(
    range(0, 101, 10)
)

plt.grid(
    True,
    linestyle=":",
    alpha=0.5
)

plt.legend()

plt.tight_layout()


# ============================================================
# SAVE GRAPH
# ============================================================

plt.savefig(
    GRAPH_PATH,
    dpi=200,
    bbox_inches="tight"
)


print("=" * 60)
print("NEUROCALM - STRESS TREND VISUALIZATION")
print("=" * 60)

print("\n✅ Professional stress trend graph created!")

print("\nAssessments:", len(df))

print("\nSaved to:")
print(GRAPH_PATH)

print("\n" + "=" * 60)


plt.show()