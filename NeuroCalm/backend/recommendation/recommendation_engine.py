recommendation_cases = {

    "anxiety_level": [
        "Try 3–5 minutes of slow deep breathing.",
        "Practice a short mindfulness or meditation session.",
        "Take a short break when you feel overwhelmed."
    ],

    "sleep_quality": [
        "Maintain a regular sleep and wake-up time.",
        "Reduce screen use before bedtime.",
        "Try a short relaxation exercise before sleeping."
    ],

    "depression": [
        "Spend some time doing an activity you enjoy.",
        "Stay connected with trusted friends or family.",
        "Use journaling to record your thoughts and feelings."
    ],

    "study_load": [
        "Break large tasks into smaller steps.",
        "Use a simple study timetable.",
        "Take regular short breaks while studying."
    ],

    "academic_performance": [
        "Set small achievable academic goals.",
        "Focus on one task at a time.",
        "Ask a teacher or mentor for support when needed."
    ],

    "future_career_concerns": [
        "Write down your short-term career goals.",
        "Discuss career plans with a teacher or mentor.",
        "Focus on one practical step you can take this week."
    ],

    "peer_pressure": [
        "Spend time with people who support your wellbeing.",
        "Practice saying no to uncomfortable situations.",
        "Talk to someone you trust when peer pressure becomes difficult."
    ],

    "social_support": [
        "Talk openly with someone you trust.",
        "Stay connected with supportive friends or family.",
        "Avoid isolating yourself when you feel stressed."
    ],

    "headache": [
        "Take regular breaks from prolonged screen or study sessions.",
        "Stay hydrated and maintain regular meals.",
        "Use relaxation techniques when tension builds."
    ],

    "noise_level": [
        "Use a quieter place for study or relaxation.",
        "Take short breaks from noisy environments.",
        "Use calming music when appropriate."
    ],

    "living_conditions": [
        "Create a comfortable area for rest and study.",
        "Keep your study space organized.",
        "Spend some time in a calm environment each day."
    ],

    "teacher_student_relationship": [
        "Discuss academic difficulties with a trusted teacher.",
        "Ask for clarification when coursework feels difficult.",
        "Use constructive communication when problems arise."
    ],

    "bullying": [
        "Talk to a trusted teacher, parent, or responsible adult.",
        "Avoid handling repeated harassment completely alone.",
        "Seek appropriate support if the situation continues."
    ]
}


def generate_recommendations(
    stress_level,
    top_factors,
    max_recommendations=5
):
    recommendations = []

    for factor, _ in top_factors:

        if factor in recommendation_cases:

            for recommendation in recommendation_cases[factor]:

                if recommendation not in recommendations:
                    recommendations.append(recommendation)

                if len(recommendations) >= max_recommendations:
                    return recommendations

    if not recommendations:

        if stress_level == "High":

            recommendations = [
                "Try a short breathing or relaxation exercise.",
                "Take regular breaks from study or work.",
                "Maintain a regular sleep routine.",
                "Talk with someone you trust if stress continues."
            ]

        elif stress_level == "Moderate":

            recommendations = [
                "Take regular breaks during study or work.",
                "Maintain a healthy sleep routine.",
                "Try relaxation or breathing exercises.",
                "Stay connected with supportive people."
            ]

        else:

            recommendations = [
                "Continue your healthy daily routine.",
                "Maintain good sleep and regular physical activity.",
                "Keep spending time on activities you enjoy."
            ]

    return recommendations[:max_recommendations]