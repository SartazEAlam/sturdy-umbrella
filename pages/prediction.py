"""
Student Prediction Page
========================
Input form for student academic data, rule-based prediction,
result display with score breakdown and radar chart.
"""

import streamlit as st
import plotly.graph_objects as go
from utils.prediction import predict_performance


# ------------------------------------------------------------------
# Category styling
# ------------------------------------------------------------------
CATEGORY_STYLES = {
    "High": {"color": "#06d6a0", "emoji": "🟢", "bg": "#f0fdf4"},
    "Medium": {"color": "#ffa600", "emoji": "🟡", "bg": "#fffbeb"},
    "Low": {"color": "#ef476f", "emoji": "🔴", "bg": "#fef2f2"},
}


def render():
    """Render the Student Prediction page."""

    # --- Header ---
    st.markdown('<p class="main-header">🎯 Predict Student Performance</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="main-subtitle">'
        'Enter academic information to estimate the student\'s performance category.'
        '</p>',
        unsafe_allow_html=True,
    )

    # --- Prototype notice ---
    st.markdown(
        '<div class="prototype-banner">'
        '⚠️ Prototype Mode — Using rule-based prediction. '
        'ML models will be integrated in the next phase.'
        '</div>',
        unsafe_allow_html=True,
    )

    # ================================================================
    # INPUT FORM
    # ================================================================
    st.markdown('<p class="section-header">📝 Student Information</p>', unsafe_allow_html=True)

    with st.form("prediction_form"):
        # Row 1: Student ID
        student_id = st.text_input(
            "Student ID",
            value="",
            placeholder="e.g., STU001",
            help="Enter a unique student identifier.",
        )

        # Row 2: Attendance and Internal Marks
        col1, col2 = st.columns(2)
        with col1:
            attendance = st.slider(
                "Attendance (%)",
                min_value=0,
                max_value=100,
                value=75,
                step=1,
                help="Student's attendance percentage (0–100).",
            )
        with col2:
            internal_marks = st.slider(
                "Internal Examination Marks",
                min_value=0,
                max_value=100,
                value=65,
                step=1,
                help="Internal exam marks (0–100).",
            )

        # Row 3: Assignment and Previous Marks
        col3, col4 = st.columns(2)
        with col3:
            assignment_marks = st.slider(
                "Assignment Marks",
                min_value=0,
                max_value=100,
                value=70,
                step=1,
                help="Assignment marks (0–100).",
            )
        with col4:
            previous_marks = st.slider(
                "Previous Examination Marks",
                min_value=0,
                max_value=100,
                value=60,
                step=1,
                help="Previous exam marks (0–100).",
            )

        # Row 4: Study Hours
        study_hours = st.slider(
            "Study Hours per Day",
            min_value=0.0,
            max_value=12.0,
            value=3.5,
            step=0.5,
            help="Average daily study hours (0–12).",
        )

        # Submit button
        submitted = st.form_submit_button(
            "🔍 Predict Performance",
            width="stretch",
        )

    # ================================================================
    # PREDICTION RESULT
    # ================================================================
    if submitted:
        # --- Run prediction ---
        category, score, details = predict_performance(
            attendance, internal_marks, assignment_marks,
            previous_marks, study_hours,
        )

        style = CATEGORY_STYLES[category]
        sid_display = student_id.strip() if student_id and student_id.strip() else "—"

        st.markdown("<br>", unsafe_allow_html=True)

        # ---- Result Card ----
        st.markdown(
            f"""
            <div class="result-card {category.lower()}">
                <div class="result-label">Predicted Performance</div>
                <div class="result-value {category.lower()}">{style['emoji']} {category.upper()}</div>
                <div class="result-score">Overall Score: {score} / 100</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ---- Score Breakdown ----
        st.markdown('<p class="section-header">📊 Score Breakdown</p>', unsafe_allow_html=True)

        metric_cols = st.columns(6)
        metric_items = [
            ("Student ID", sid_display),
            ("Attendance", f"{details['attendance']}%"),
            ("Internal Marks", str(details["internal_marks"])),
            ("Assignment Marks", str(details["assignment_marks"])),
            ("Previous Marks", str(details["previous_marks"])),
            ("Study Hours", f"{details['study_hours']} hrs"),
        ]

        for col, (label, val) in zip(metric_cols, metric_items):
            col.metric(label, val)

        # ---- Interpretation ----
        st.markdown('<p class="section-header">💡 Performance Summary</p>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="info-box">{details["interpretation"]}</div>',
            unsafe_allow_html=True,
        )

        # ================================================================
        # VISUALIZATION — Radar Chart
        # ================================================================
        st.markdown('<p class="section-header">📈 Student Profile Visualization</p>', unsafe_allow_html=True)

        viz_col1, viz_col2 = st.columns([3, 2])

        with viz_col1:
            # Radar chart of academic factors
            categories_list = ["Attendance", "Internal Marks", "Assignment Marks", "Previous Marks", "Study Hours (scaled)"]
            values = [
                attendance,
                internal_marks,
                assignment_marks,
                previous_marks,
                details["study_hours_normalized"],
            ]
            # Close the radar polygon
            categories_list_closed = categories_list + [categories_list[0]]
            values_closed = values + [values[0]]

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=values_closed,
                theta=categories_list_closed,
                fill="toself",
                fillcolor=f"rgba({_hex_to_rgb(style['color'])}, 0.15)",
                line=dict(color=style["color"], width=2),
                marker=dict(size=6, color=style["color"]),
                name="Student",
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100]),
                ),
                showlegend=False,
                template="plotly_white",
                height=400,
                margin=dict(t=40, b=40, l=60, r=60),
            )
            st.plotly_chart(fig_radar)

        with viz_col2:
            # Weighted contribution bar chart
            st.markdown("**Weighted Contributions**")

            contributions = details["weighted_contributions"]
            fig_contrib = go.Figure()
            fig_contrib.add_trace(go.Bar(
                x=list(contributions.values()),
                y=list(contributions.keys()),
                orientation="h",
                marker_color=[
                    "#4361ee", "#4361ee", "#4895ef", "#4895ef", "#7209b7"
                ],
                text=[f"{v:.1f}" for v in contributions.values()],
                textposition="outside",
            ))
            fig_contrib.update_layout(
                template="plotly_white",
                height=400,
                margin=dict(t=20, b=20, l=10, r=40),
                xaxis_title="Contribution to Score",
                xaxis=dict(range=[0, 30]),
            )
            st.plotly_chart(fig_contrib)


def _hex_to_rgb(hex_color):
    """Convert hex color string to comma-separated RGB values."""
    try:
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 6:
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            return f"{r}, {g}, {b}"
    except Exception:
        pass
    return "67, 97, 238"
