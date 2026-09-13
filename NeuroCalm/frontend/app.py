import sys
import os

# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)


# ============================================================
# IMPORTS
# ============================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from backend.predict import (
    analyze_stress,
    convert_answer
)

from backend.report_generation.pdf_report import create_pdf


# ============================================================
# PATHS
# ============================================================

HISTORY_FILE = os.path.join(
    PROJECT_DIR,
    "dataset",
    "processed",
    "stress_history.csv"
)

DETAILS_FILE = os.path.join(
    PROJECT_DIR,
    "dataset",
    "processed",
    "latest_assessment_details.json"
)

REPORT_FILE = os.path.join(
    PROJECT_DIR,
    "reports",
    "NeuroCalm_Stress_Report.pdf"
)


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="NeuroCalm",
    page_icon="🧠",
    layout="wide"
)


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
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "result" not in st.session_state:
    st.session_state.result = None

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div style="
        padding:30px;
        border-radius:20px;
        background:linear-gradient(135deg,#2563EB,#4F46E5);
        color:white;
        margin-bottom:25px;
    ">
        <h1 style="margin:0;">🧠 NeuroCalm</h1>
        <p style="font-size:18px;">
            AI-Based Stress Analysis and Personalized Wellness Support
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":

    st.subheader("Welcome to NeuroCalm 🌿")

    st.write(
        "NeuroCalm analyzes your responses to a short stress assessment "
        "and provides an understandable stress result, contributing factors, "
        "and personalized wellness recommendations."
    )

    st.info(
        "The assessment contains 20 questions. "
        "Please answer each question honestly."
    )

    if st.button(
        "🚀 Start Stress Assessment",
        type="primary",
        use_container_width=True
    ):
        st.session_state.page = "assessment"
        st.rerun()


# ============================================================
# ASSESSMENT PAGE
# ============================================================

elif st.session_state.page == "assessment":

    st.subheader("📝 Stress Assessment")

    st.write(
        "Answer all 20 questions. Your responses will be analyzed "
        "using the NeuroCalm machine-learning pipeline."
    )
    st.markdown("### 👤 Personal Information")

    user_name = st.text_input(
        "Enter your name",
        value=st.session_state.user_name,
        placeholder="Enter your name"
    )

    st.session_state.user_name = user_name
    st.progress(
        0,
        text="0 / 20 questions answered"
    )

    answers = []

    for i, (question, options) in enumerate(
        questions
    ):

        st.markdown(
            f"### {i + 1}. {question}"
        )

        answer = st.radio(
            "Select your answer:",
            options,
            index=None,
            key=f"question_{i}",
            horizontal=True
        )

        if answer is not None:
            answer_number = options.index(answer) + 1

            answers.append(
                convert_answer(
                    features[i],
                    answer_number,
                    len(options)
                )
           )

        st.divider()


    if st.button(
        "🔍 Analyze My Stress",
        type="primary",
        use_container_width=True
    ):

        if not st.session_state.user_name.strip():
            st.warning(
                "Please enter your name before analyzing your stress."
            )

            st.stop()

        with st.spinner(
            "Analyzing your responses..."
        ):

            result = analyze_stress(
                answers
            )

        st.session_state.result = result

        st.session_state.page = "result"

        st.rerun()

        result = analyze_stress(
            answers
        )

        st.session_state.result = result

        st.session_state.page = "result"

        st.rerun()


# ============================================================
# RESULT PAGE
# ============================================================

elif st.session_state.page == "result":

    result = st.session_state.result

    if result is None:

        st.warning(
            "No assessment result available."
        )

        if st.button("Start Assessment"):
            st.session_state.page = "assessment"
            st.rerun()

        st.stop()


    stress_score = result["stress_score"]
    stress_level = result["stress_level"]
    weekly_average = result["weekly_average"]
    trend = result["trend"]
    factors = result["top_factors"]
    recommendations = result["recommendations"]


    # ========================================================
    # RESULT HEADER
    # ========================================================

    st.subheader("📊 Your NeuroCalm Result")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Stress Score",
            f"{stress_score:.0f}%"
        )

    with col2:
        st.metric(
            "Stress Level",
            stress_level
        )

    with col3:
        st.metric(
            "Weekly Average",
            f"{weekly_average:.0f}%"
        )

    with col4:
        st.metric(
            "Stress Trend",
            trend
        )



    # ========================================================
    # STRESS MESSAGE
    # ========================================================

    if stress_level == "Low":

        st.success(
            "🟢 Your responses indicate a relatively low level of stress."
        )

    elif stress_level == "Moderate":

        st.warning(
            "🟠 Your responses indicate a moderate level of stress."
        )

    else:

        st.error(
            "🔴 Your responses indicate a high level of stress."
        )


    st.progress(
        min(int(stress_score), 100)
    )


    # ========================================================
    # MAIN FACTORS
    # ========================================================

    st.markdown("## 🔎 Main Stress Factors")

    if factors:

        for i, factor in enumerate(
            factors,
            1
        ):

            st.markdown(
                f"**{i}. {factor['name']}**"
            )

            st.caption(
                factor["effect"]
            )

    else:

        st.info(
            "Factor explanation is currently unavailable."
        )


    # ========================================================
    # WHY THIS RESULT
    # ========================================================

    st.markdown("## 💡 Why This Result?")

    higher = [
        factor["name"]
        for factor in factors
        if "higher" in factor["effect"].lower()
    ]

    if higher:

        names = " and ".join(
            higher[:2]
        )

        st.write(
            f"Your result is mainly influenced by {names}. "
            f"These factors contributed to your {stress_level.lower()} stress level."
        )

    else:

        st.write(
            f"Your responses resulted in a "
            f"{stress_level.lower()} stress level based on the assessment."
        )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.markdown(
        "## 🌿 Personalized Recommendations"
    )

    for i, recommendation in enumerate(
        recommendations,
        1
    ):

        st.markdown(
            f"**{i}.** {recommendation}"
        )


    # ========================================================
    # HISTORY
    # ========================================================

    st.markdown("## 📈 Stress History")

    if os.path.exists(HISTORY_FILE):

        history_df = pd.read_csv(
            HISTORY_FILE
        )

        history_df["stress_score"] = pd.to_numeric(
            history_df["stress_score"],
            errors="coerce"
        )

        history_df = history_df.dropna(
            subset=["stress_score"]
        )

        if not history_df.empty:

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=list(
                        range(
                            1,
                            len(history_df) + 1
                        )
                    ),
                    y=history_df["stress_score"],
                    mode="lines+markers",
                    name="Stress Score"
                )
            )

            fig.add_hline(
                y=33,
                line_dash="dash"
            )

            fig.add_hline(
                y=66,
                line_dash="dash"
            )

            fig.update_layout(
                xaxis_title="Assessment",
                yaxis_title="Stress Score (%)",
                yaxis=dict(
                    range=[0, 100]
                ),
                height=400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # ========================================================
    # PDF REPORT
    # ========================================================

    st.markdown("## 📄 Stress Report")

    if st.button(
        "Generate PDF Report",
        use_container_width=True
    ):

        history_df = pd.read_csv(
            HISTORY_FILE
        )

        history_df["stress_score"] = pd.to_numeric(
            history_df["stress_score"],
            errors="coerce"
        )

        average_score = history_df[
            "stress_score"
        ].mean()

        if len(history_df) < 2:

            trend = "Not enough data"

        else:

            previous = float(
                history_df.iloc[-2]["stress_score"]
            )

            difference = stress_score - previous

            if difference > 5:
                trend = "Increasing"

            elif difference < -5:
                trend = "Decreasing"

            else:
                trend = "Stable"


        create_pdf(
            REPORT_FILE,
            stress_score,
            stress_level,
            average_score,
            trend,
            history_df,
            factors,
            recommendations,
            st.session_state.user_name
        )


        with open(
            REPORT_FILE,
            "rb"
        ) as file:

            st.download_button(
                "⬇️ Download PDF Report",
                file,
                file_name="NeuroCalm_Stress_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )


    # ========================================================
    # NEW ASSESSMENT
    # ========================================================

    st.divider()

    if st.button(
        "🔄 Take Another Assessment",
        use_container_width=True
    ):

        st.session_state.result = None
        st.session_state.page = "assessment"

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "NeuroCalm | Stress Monitoring and Wellbeing Support System"
)