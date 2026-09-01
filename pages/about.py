"""
About Project Page
===================
Project information, objectives, technology stack,
and methodology overview.
"""

import streamlit as st


def render():
    """Render the About Project page."""

    # --- Header ---
    st.markdown('<p class="main-header">ℹ️ About This Project</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="main-subtitle">'
        'Learn about the Student Performance Prediction & Analysis System.'
        '</p>',
        unsafe_allow_html=True,
    )

    # ================================================================
    # PROJECT TITLE
    # ================================================================
    st.markdown(
        """
        <div class="kpi-card kpi-blue" style="text-align: left; margin-bottom: 1.5rem;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #1a1a2e; margin-bottom: 0.3rem;">
                🎓 Student Performance Prediction & Analysis System
            </div>
            <div style="font-size: 0.95rem; color: #6c757d;">
                Capstone Project — B.Tech Computer Science & Engineering
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ================================================================
    # OBJECTIVE
    # ================================================================
    st.markdown('<p class="section-header">🎯 Objective</p>', unsafe_allow_html=True)
    st.markdown(
        """
        The system aims to **analyze student academic information** and **predict 
        performance categories** using machine learning techniques. By examining key 
        academic factors such as attendance, examination marks, and study habits, the 
        system classifies students into performance levels to help educators identify 
        students who may need additional support.
        """
    )

    # ================================================================
    # TWO-COLUMN LAYOUT: Input Factors + Categories
    # ================================================================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-header">📥 Input Factors</p>', unsafe_allow_html=True)
        factors = [
            ("📋", "Attendance Percentage"),
            ("📝", "Internal Examination Marks"),
            ("📄", "Assignment Marks"),
            ("📊", "Previous Examination Marks"),
            ("⏰", "Study Hours per Day"),
        ]
        for icon, name in factors:
            st.markdown(f"&nbsp;&nbsp;&nbsp;{icon}&nbsp;&nbsp;**{name}**")

    with col2:
        st.markdown('<p class="section-header">🏷️ Performance Categories</p>', unsafe_allow_html=True)
        st.markdown("&nbsp;&nbsp;&nbsp;🔴&nbsp;&nbsp;**Low** — Below average performance")
        st.markdown("&nbsp;&nbsp;&nbsp;🟡&nbsp;&nbsp;**Medium** — Average performance")
        st.markdown("&nbsp;&nbsp;&nbsp;🟢&nbsp;&nbsp;**High** — Above average performance")

    st.divider()

    # ================================================================
    # ML ALGORITHMS
    # ================================================================
    st.markdown('<p class="section-header">🤖 Machine Learning Algorithms</p>', unsafe_allow_html=True)

    algo_cols = st.columns(3)
    algorithms = [
        ("📈", "Logistic Regression", "Linear classification model suitable for multi-class prediction."),
        ("🌳", "Decision Tree", "Tree-based model for interpretable, rule-based classification."),
        ("🌲", "Random Forest", "Ensemble method combining multiple decision trees for robust predictions."),
    ]

    for col, (icon, name, desc) in zip(algo_cols, algorithms):
        with col:
            st.markdown(
                f"""
                <div class="kpi-card" style="text-align: left; min-height: 130px;">
                    <div style="font-size: 1.3rem; margin-bottom: 0.4rem;">{icon}</div>
                    <div style="font-weight: 600; color: #1a1a2e; margin-bottom: 0.3rem;">{name}</div>
                    <div style="font-size: 0.85rem; color: #6c757d; line-height: 1.5;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # ================================================================
    # EVALUATION METRICS
    # ================================================================
    st.markdown('<p class="section-header">📏 Evaluation Metrics</p>', unsafe_allow_html=True)

    metric_cols = st.columns(4)
    eval_metrics = [
        ("🎯", "Accuracy", "Proportion of correct predictions among total predictions."),
        ("🔍", "Precision", "Ratio of true positives to all predicted positives."),
        ("📡", "Recall", "Ratio of true positives to all actual positives."),
        ("⚖️", "F1-Score", "Harmonic mean of precision and recall."),
    ]

    for col, (icon, name, desc) in zip(metric_cols, eval_metrics):
        with col:
            st.markdown(
                f"""
                <div class="kpi-card" style="text-align: left; min-height: 120px;">
                    <div style="font-size: 1.2rem; margin-bottom: 0.3rem;">{icon}</div>
                    <div style="font-weight: 600; color: #1a1a2e; margin-bottom: 0.2rem;">{name}</div>
                    <div style="font-size: 0.82rem; color: #6c757d; line-height: 1.4;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # ================================================================
    # TECHNOLOGY STACK
    # ================================================================
    st.markdown('<p class="section-header">🛠️ Technology Stack</p>', unsafe_allow_html=True)

    tech_cols = st.columns(3)

    tech_groups = [
        (
            "Core Language",
            [("🐍", "Python", "Primary programming language")],
        ),
        (
            "Libraries",
            [
                ("📊", "Pandas", "Data manipulation and analysis"),
                ("🔢", "NumPy", "Numerical computing"),
                ("📈", "Plotly", "Interactive visualizations"),
                ("📐", "Statsmodels", "Statistical modeling & trendlines"),
                ("🤖", "Scikit-learn", "ML models (next phase)"),
            ],
        ),
        (
            "Framework",
            [("🌐", "Streamlit", "Interactive web dashboard")],
        ),
    ]

    for col, (group_name, techs) in zip(tech_cols, tech_groups):
        with col:
            st.markdown(f"**{group_name}**")
            for icon, name, desc in techs:
                st.markdown(f"&nbsp;&nbsp;{icon} **{name}** — {desc}")

    st.divider()

    # ================================================================
    # PROJECT WORKFLOW
    # ================================================================
    st.markdown('<p class="section-header">🔄 Project Workflow</p>', unsafe_allow_html=True)

    workflow_steps = [
        ("1️⃣", "Data Collection", "Gather student academic data"),
        ("2️⃣", "Data Preprocessing", "Clean and prepare the dataset"),
        ("3️⃣", "Exploratory Data Analysis", "Analyze relationships and patterns"),
        ("4️⃣", "Train/Test Split", "Divide data for training and evaluation"),
        ("5️⃣", "Model Training", "Train LR, DT, and RF classifiers"),
        ("6️⃣", "Model Evaluation", "Compare using Accuracy, Precision, Recall, F1"),
        ("7️⃣", "Best Model Selection", "Select the highest-performing model"),
        ("8️⃣", "Prediction & Dashboard", "Deploy interactive Streamlit dashboard"),
    ]

    # Display as a visual flow
    flow_cols = st.columns(4)
    for i, (icon, title, desc) in enumerate(workflow_steps):
        with flow_cols[i % 4]:
            st.markdown(
                f"""
                <div style="text-align: center; padding: 0.8rem 0.3rem; margin-bottom: 0.5rem;">
                    <div style="font-size: 1.5rem;">{icon}</div>
                    <div style="font-weight: 600; font-size: 0.85rem; color: #1a1a2e; margin: 0.2rem 0;">{title}</div>
                    <div style="font-size: 0.75rem; color: #6c757d;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # ================================================================
    # PROTOTYPE STATUS
    # ================================================================
    st.markdown('<p class="section-header">📌 Current Status</p>', unsafe_allow_html=True)

    st.info(
        "**Phase 1 — Prototype Complete** ✅\n\n"
        "The current version is a functional UI/UX prototype using sample data and "
        "rule-based prediction logic. Machine learning model training and integration "
        "will be implemented in Phase 2."
    )
