import os
import numpy as np
import pandas as pd

# ============================================================
# PROJECT PATHS
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

DATA_PATH = os.path.join(
    PROJECT_DIR,
    "dataset",
    "processed",
    "multi_view_features.csv"
)

OUTPUT_PATH = os.path.join(
    PROJECT_DIR,
    "dataset",
    "processed",
    "fused_features.csv"
)

# ============================================================
# LOAD MULTI-VIEW DATA
# ============================================================

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("NEUROCALM - CROSS-ATTENTION FEATURE FUSION")
print("=" * 60)

# ------------------------------------------------------------
# Separate views
# ------------------------------------------------------------

questionnaire_cols = [
    "anxiety_level",
    "mental_health_history",
    "depression",
    "headache",
    "blood_pressure",
    "breathing_problem"
]

lifestyle_cols = [
    "sleep_quality",
    "noise_level",
    "living_conditions",
    "safety",
    "basic_needs",
    "extracurricular_activities"
]

mood_cols = [
    "self_esteem",
    "social_support"
]

academic_cols = [
    "academic_performance",
    "study_load",
    "teacher_student_relationship",
    "future_career_concerns",
    "peer_pressure",
    "bullying"
]

# ============================================================
# EXTRACT VIEWS
# ============================================================

questionnaire = df[questionnaire_cols].to_numpy(dtype=float)
lifestyle = df[lifestyle_cols].to_numpy(dtype=float)
mood = df[mood_cols].to_numpy(dtype=float)
academic = df[academic_cols].to_numpy(dtype=float)

print("\nViews loaded successfully.")

print("Questionnaire shape:", questionnaire.shape)
print("Lifestyle shape    :", lifestyle.shape)
print("Mood shape         :", mood.shape)
print("Academic shape     :", academic.shape)

# ============================================================
# VIEW REPRESENTATIONS
# ============================================================

# Mean representation for each view
questionnaire_repr = questionnaire.mean(axis=1)
lifestyle_repr = lifestyle.mean(axis=1)
mood_repr = mood.mean(axis=1)
academic_repr = academic.mean(axis=1)

# ============================================================
# CROSS-VIEW ATTENTION SCORES
# ============================================================

view_matrix = np.column_stack([
    questionnaire_repr,
    lifestyle_repr,
    mood_repr,
    academic_repr
])

# Similarity-based attention
similarity = np.abs(view_matrix)

attention_weights = (
    similarity /
    (similarity.sum(axis=1, keepdims=True) + 1e-8)
)

# ============================================================
# FUSED REPRESENTATION
# ============================================================

fused_representation = (
    view_matrix * attention_weights
).sum(axis=1)

# ============================================================
# CREATE OUTPUT
# ============================================================

fused_df = pd.DataFrame({
    "questionnaire_attention": attention_weights[:, 0],
    "lifestyle_attention": attention_weights[:, 1],
    "mood_attention": attention_weights[:, 2],
    "academic_attention": attention_weights[:, 3],
    "fused_feature": fused_representation
})

# Keep target
if "stress_level" in df.columns:
    fused_df["stress_level"] = df["stress_level"]

# ============================================================
# SAVE
# ============================================================

fused_df.to_csv(
    OUTPUT_PATH,
    index=False
)

# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\nAttention weights calculated successfully.")

print("\nFirst 5 attention-weight rows:")
print(fused_df.head())

print("\nFused Dataset Shape:")
print(fused_df.shape)

print("\nSaved to:")
print(OUTPUT_PATH)

print("\n✅ Cross-Attention Feature Fusion completed!")