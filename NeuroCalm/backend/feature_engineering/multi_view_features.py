import os
import pandas as pd

# ============================================================
# PROJECT PATHS
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

DATA_PATH = os.path.join(
    PROJECT_DIR,
    "dataset",
    "raw",
    "StressLevelDataset.csv"
)

OUTPUT_DIR = os.path.join(
    PROJECT_DIR,
    "dataset",
    "processed"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# LOAD PRIMARY DATASET
# ============================================================

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("NEUROCALM - MULTI-VIEW FEATURE LEARNING")
print("=" * 60)

print("\nOriginal Dataset Shape:", df.shape)

# ============================================================
# VIEW DEFINITIONS
# ============================================================

questionnaire_features = [
    "anxiety_level",
    "mental_health_history",
    "depression",
    "headache",
    "blood_pressure",
    "breathing_problem"
]

lifestyle_features = [
    "sleep_quality",
    "noise_level",
    "living_conditions",
    "safety",
    "basic_needs",
    "extracurricular_activities"
]

mood_features = [
    "self_esteem",
    "social_support"
]

academic_features = [
    "academic_performance",
    "study_load",
    "teacher_student_relationship",
    "future_career_concerns",
    "peer_pressure",
    "bullying"
]

# ============================================================
# CREATE FOUR VIEWS
# ============================================================

questionnaire_view = df[questionnaire_features].copy()

lifestyle_view = df[lifestyle_features].copy()

mood_view = df[mood_features].copy()

academic_view = df[academic_features].copy()

# ============================================================
# DISPLAY VIEW SHAPES
# ============================================================

print("\nQuestionnaire View:")
print("Features:", questionnaire_view.shape[1])
print("Samples :", questionnaire_view.shape[0])

print("\nLifestyle View:")
print("Features:", lifestyle_view.shape[1])
print("Samples :", lifestyle_view.shape[0])

print("\nMood View:")
print("Features:", mood_view.shape[1])
print("Samples :", mood_view.shape[0])

print("\nAcademic View:")
print("Features:", academic_view.shape[1])
print("Samples :", academic_view.shape[0])

# ============================================================
# COMBINE VIEWS
# ============================================================

multi_view_data = pd.concat(
    [
        questionnaire_view,
        lifestyle_view,
        mood_view,
        academic_view
    ],
    axis=1
)

# Add target separately
if "stress_level" in df.columns:
    multi_view_data["stress_level"] = df["stress_level"]

# ============================================================
# SAVE MULTI-VIEW DATA
# ============================================================

output_path = os.path.join(
    OUTPUT_DIR,
    "multi_view_features.csv"
)

multi_view_data.to_csv(
    output_path,
    index=False
)

# ============================================================
# RESULT
# ============================================================

print("\nUnified Multi-View Dataset Shape:")
print(multi_view_data.shape)

print("\nSaved to:")
print(output_path)

print("\n✅ Multi-View Feature Learning completed!")