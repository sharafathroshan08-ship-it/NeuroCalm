import os
import pandas as pd
import joblib
import shap
import json

from backend.trend_analysis.stress_history import save_stress_result

from backend.recommendation.recommendation_engine import generate_recommendations
from backend.decision_layer.fuzzy_decision import fuzzy_decision

from backend.trend_analysis.trend_analyzer import (
    calculate_weekly_average,
    calculate_trend,
    load_history
)

# ============================================================
# PROJECT PATH
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "models",
    "neurocalm_random_forest.pkl"
)

model = joblib.load(MODEL_PATH)

# ============================================================
# FEATURES
# ============================================================

features = [
    "anxiety_level",
    "self_esteem",
    "mental_health_history",
    "depression",
    "headache",
    "blood_pressure",
    "sleep_quality",
    "breathing_problem",
    "noise_level",
    "living_conditions",
    "safety",
    "basic_needs",
    "academic_performance",
    "study_load",
    "teacher_student_relationship",
    "future_career_concerns",
    "social_support",
    "peer_pressure",
    "extracurricular_activities",
    "bullying"
]

# ============================================================
# USER-FRIENDLY FEATURE NAMES
# ============================================================

friendly_names = {
    "anxiety_level": "Anxiety",
    "self_esteem": "Self-esteem",
    "mental_health_history": "Mental health history",
    "depression": "Depression",
    "headache": "Headaches",
    "blood_pressure": "Blood pressure",
    "sleep_quality": "Sleep quality",
    "breathing_problem": "Breathing problems",
    "noise_level": "Noise level",
    "living_conditions": "Living conditions",
    "safety": "Safety",
    "basic_needs": "Basic needs",
    "academic_performance": "Academic performance",
    "study_load": "Study load",
    "teacher_student_relationship": "Teacher relationship",
    "future_career_concerns": "Future career concerns",
    "social_support": "Social support",
    "peer_pressure": "Peer pressure",
    "extracurricular_activities": "Extracurricular activities",
    "bullying": "Bullying / harassment"
}

# ============================================================
# QUESTIONS
# ============================================================

questions = [
    (
        "How often do you feel anxious?",
        ["Never", "Sometimes", "Often", "Almost always"]
    ),

    (
        "How would you rate your self-esteem?",
        ["Very high", "High", "Low", "Very low"]
    ),

    (
        "Have you experienced mental health difficulties before?",
        ["No", "Yes"]
    ),

    (
        "How often do you feel depressed or very low?",
        ["Never", "Sometimes", "Often", "Almost always"]
    ),

    (
        "How often do you experience headaches?",
        ["Never", "Sometimes", "Often", "Very often"]
    ),

    (
        "How would you rate your blood pressure condition?",
        ["Normal", "Slightly high", "High"]
    ),

    (
        "How would you rate your sleep quality?",
        ["Very good", "Good", "Poor", "Very poor"]
    ),

    (
        "How often do you experience breathing problems?",
        ["Never", "Sometimes", "Often", "Very often"]
    ),

    (
        "How much does noise affect your daily life?",
        ["Very little", "Little", "Moderate", "A lot"]
    ),

    (
        "How comfortable are your living conditions?",
        [
            "Very comfortable",
            "Comfortable",
            "Uncomfortable",
            "Very uncomfortable"
        ]
    ),

    (
        "How safe do you feel in your environment?",
        ["Very safe", "Safe", "Unsafe", "Very unsafe"]
    ),

    (
        "Do you have difficulty meeting your basic needs?",
        ["Never", "Sometimes", "Often", "Very often"]
    ),

    (
        "How would you rate your academic performance?",
        ["Very good", "Good", "Poor", "Very poor"]
    ),

    (
        "How heavy is your current study load?",
        ["Very light", "Light", "Heavy", "Very heavy"]
    ),

    (
        "How would you rate your relationship with teachers?",
        ["Very good", "Good", "Poor", "Very poor"]
    ),

    (
        "How worried are you about your future career?",
        [
            "Not worried",
            "Slightly worried",
            "Worried",
            "Very worried"
        ]
    ),

    (
        "How much social support do you receive?",
        ["A lot", "Good", "Little", "Very little"]
    ),

    (
        "How much peer pressure do you experience?",
        ["None", "Low", "Moderate", "High"]
    ),

    (
        "How often do you participate in extracurricular activities?",
        ["Very often", "Often", "Sometimes", "Never"]
    ),

    (
        "How often do you experience bullying or harassment?",
        ["Never", "Sometimes", "Often", "Very often"]
    )
]

# ============================================================
# ORIGINAL DATA RANGES
# ============================================================

ranges = {
    "anxiety_level": (0, 21),
    "self_esteem": (0, 30),
    "mental_health_history": (0, 1),
    "depression": (0, 27),
    "headache": (0, 5),
    "blood_pressure": (1, 3),
    "sleep_quality": (0, 5),
    "breathing_problem": (0, 5),
    "noise_level": (0, 5),
    "living_conditions": (0, 5),
    "safety": (0, 5),
    "basic_needs": (0, 5),
    "academic_performance": (0, 5),
    "study_load": (0, 5),
    "teacher_student_relationship": (0, 5),
    "future_career_concerns": (0, 5),
    "social_support": (0, 3),
    "peer_pressure": (0, 5),
    "extracurricular_activities": (0, 5),
    "bullying": (0, 5)
}

# ============================================================
# FEATURES WHERE HIGHER VALUE = LOWER STRESS
# ============================================================

reverse_features = {
    "self_esteem",
    "sleep_quality",
    "living_conditions",
    "safety",
    "basic_needs",
    "academic_performance",
    "teacher_student_relationship",
    "social_support"
}

# ============================================================
# CONVERT USER ANSWER
# ============================================================

def convert_answer(feature, answer, option_count):

    minimum, maximum = ranges[feature]

    # Mental health history
    if feature == "mental_health_history":
        return 0 if answer == 1 else 1

    # Reverse features
    if feature in reverse_features:
        level = option_count - answer
    else:
        level = answer - 1

    if option_count == 2:
        normalized = level
    else:
        normalized = level / (option_count - 1)

    return minimum + normalized * (maximum - minimum)


# ============================================================
# QUESTIONNAIRE HELPER
# ============================================================

def run_questionnaire():
    print("=" * 60)
    print("              NEUROCALM")
    print("          STRESS ASSESSMENT")
    print("=" * 60)

    answers = []
    for i, (question, options) in enumerate(questions):
        feature = features[i]
        print(f"\n{i + 1}. {question}")
        for j, option in enumerate(options, 1):
            print(f"   {j}. {option}")
        while True:
            try:
                answer = int(input(f"Your answer (1-{len(options)}): "))
                if 1 <= answer <= len(options):
                    answers.append(convert_answer(feature, answer, len(options)))
                    break
                print(f"Please enter a number between 1 and {len(options)}.")
            except ValueError:
                print("Please enter a valid number.")

    normalized_values = []
    for feature, value in zip(features, answers):
        minimum, maximum = ranges[feature]
        normalized_values.append((value - minimum) / (maximum - minimum) if maximum != minimum else 0)
    return analyze_stress(normalized_values)


def analyze_stress(normalized_values):

    # ========================================================
    # CREATE DATAFRAME
    # ========================================================

    input_data = pd.DataFrame(
        [normalized_values],
        columns=features
    )

    # ========================================================
    # RANDOM FOREST PREDICTION
    # ========================================================

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0]

    # ========================================================
    # FUZZY DECISION
    # ========================================================

    stress_score = (
        probability[0] * 0 +
        probability[1] * 50 +
        probability[2] * 100
    )

    stress_score = round(stress_score, 0)

    stress_level, fuzzy_membership = fuzzy_decision(
        stress_score
    )

    # ========================================================
    # SAVE HISTORY
    # ========================================================

    save_stress_result(
        stress_score,
        stress_level
    )
    # ========================================================
    # UPDATE STRESS TREND
    # ========================================================

    history_df = load_history()

    weekly_average = calculate_weekly_average(history_df)
    trend = calculate_trend(history_df)

    # ========================================================
    # SHAP EXPLANATION
    # ========================================================

    try:

        explainer = shap.TreeExplainer(model)

        shap_values = explainer.shap_values(input_data)

        if isinstance(shap_values, list):

            values = shap_values[prediction][0]

        else:

            values = shap_values

            if len(values.shape) == 3:

                values = values[0, :, prediction]

            elif len(values.shape) == 2:

                values = values[0]

        factor_importance = []

        for feature, value in zip(features, values):

            factor_importance.append(
                (
                    feature,
                    float(value)
                )
            )

        factor_importance.sort(
            key=lambda x: abs(x[1]),
            reverse=True
        )

        higher_factors = [
            item
            for item in factor_importance
            if (
                (
                    item[0] not in reverse_features
                    and item[1] > 0
                )
                or
                (
                    item[0] in reverse_features
                    and item[1] < 0
                )
            )
        ]

        lower_factors = [
            item
            for item in factor_importance
            if (
                (
                    item[0] not in reverse_features
                    and item[1] < 0
                )
                or
                (
                    item[0] in reverse_features
                    and item[1] > 0
                )
            )
        ]

        top_factors = (
            higher_factors[:5]
            + lower_factors[:5]
        )[:5]

    except Exception:

        top_factors = []

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    recommendations = generate_recommendations(
        stress_level,
        top_factors,
        max_recommendations=5
    )

    # ========================================================
    # SAVE LATEST DETAILS
    # ========================================================

    details_file = os.path.join(
        PROJECT_DIR,
        "dataset",
        "processed",
        "latest_assessment_details.json"
    )

    os.makedirs(os.path.dirname(details_file), exist_ok=True)

    report_factors = []

    for feature, importance in top_factors:

        adjusted_importance = (
            -importance
            if feature in reverse_features
            else importance
        )

        report_factors.append({
            "name": friendly_names.get(
                feature,
                feature
            ),
            "effect": (
                "Contributing to higher stress"
                if adjusted_importance > 0
                else "Contributing to lower stress"
            )
        })

    details = {
        "stress_score": stress_score,
        "stress_level": stress_level,
        "top_factors": report_factors,
        "recommendations": recommendations
    }

    with open(
        details_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            details,
            file,
            indent=4
        )

    # ========================================================
    # RETURN RESULT TO WEBSITE
    # ========================================================

    return {
    "stress_score": stress_score,
    "stress_level": stress_level,
    "weekly_average": weekly_average,
    "trend": trend,
    "top_factors": report_factors,
    "recommendations": recommendations
}


if __name__ == "__main__":
    result = run_questionnaire()
    print("\nStress Score:", result["stress_score"])
    print("Stress Level:", result["stress_level"])
