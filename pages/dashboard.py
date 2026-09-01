"""
Dashboard Page
===============
Main overview page showing KPI cards, performance charts,
and a recent student records table.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processing import load_data, get_summary_stats


# ------------------------------------------------------------------
# Color palette used across charts
# ------------------------------------------------------------------
CATEGORY_COLORS = {
    "High": "#06d6a0",
    "Medium": "#ffd166",
    "Low": "#ef476f",
}

CHART_TEMPLATE = "plotly_white"


def render():
    """Render the Dashboard page."""

    # --- Header ---
    st.markdown('<p class="main-header">📊 Student Performance Prediction & Analysis</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="main-subtitle">'
        'Analyze academic factors and predict student performance using machine learning.'
        '</p>',
        unsafe_allow_html=True,
    )

    # --- Load data ---
    df = load_data()
    if df is None:
        st.warning("Unable to load the student dataset. Please check the data file.")
        return

    stats = get_summary_stats(df)

    # ================================================================
    # KPI CARDS
    # ================================================================
    kpi_cols = st.columns(5)

    kpi_data = [
        ("👥", "Total Students", str(stats["total_students"]), "kpi-blue"),
        ("📋", "Avg Attendance", f"{stats['avg_attendance']}%", "kpi-green"),
        ("📝", "Avg Internal Marks", str(stats["avg_internal_marks"]), "kpi-orange"),
        ("⏰", "Avg Study Hours", f"{stats['avg_study_hours']} hrs", "kpi-purple"),
        ("🏆", "High Performers", str(stats["high_performers"]), "kpi-teal"),
    ]

    for col, (icon, label, value, css_class) in zip(kpi_cols, kpi_data):
        with col:
            st.markdown(
                f"""
                <div class="kpi-card {css_class}">
                    <div class="kpi-icon">{icon}</div>
                    <div class="kpi-value">{value}</div>
                    <div class="kpi-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ================================================================
    # CHARTS — Row 1 (two columns)
    # ================================================================
    chart_col1, chart_col2 = st.columns(2)

    # ---- Chart 1: Performance Distribution (Donut) ----
    with chart_col1:
        st.markdown('<p class="section-header">Performance Distribution</p>', unsafe_allow_html=True)

        category_counts = df["performance_category"].value_counts().reindex(["High", "Medium", "Low"])
        fig_donut = go.Figure(data=[go.Pie(
            labels=category_counts.index,
            values=category_counts.values,
            hole=0.5,
            marker=dict(colors=[CATEGORY_COLORS[cat] for cat in category_counts.index]),
            textinfo="label+percent",
            textfont=dict(size=13),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
        )])
        fig_donut.update_layout(
            template=CHART_TEMPLATE,
            height=380,
            margin=dict(t=20, b=20, l=20, r=20),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # ---- Chart 2: Attendance vs Performance ----
    with chart_col2:
        st.markdown('<p class="section-header">Attendance vs Performance</p>', unsafe_allow_html=True)

        fig_scatter1 = px.scatter(
            df,
            x="attendance",
            y="performance_score",
            color="performance_category",
            color_discrete_map=CATEGORY_COLORS,
            category_orders={"performance_category": ["High", "Medium", "Low"]},
            labels={
                "attendance": "Attendance (%)",
                "performance_score": "Performance Score",
                "performance_category": "Category",
            },
            template=CHART_TEMPLATE,
            opacity=0.7,
        )
        fig_scatter1.update_layout(
            height=380,
            margin=dict(t=20, b=20, l=20, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        )
        fig_scatter1.update_traces(marker=dict(size=8))
        st.plotly_chart(fig_scatter1, use_container_width=True)

    # ================================================================
    # CHARTS — Row 2 (two columns)
    # ================================================================
    chart_col3, chart_col4 = st.columns(2)

    # ---- Chart 3: Study Hours vs Performance ----
    with chart_col3:
        st.markdown('<p class="section-header">Study Hours vs Performance</p>', unsafe_allow_html=True)

        fig_scatter2 = px.scatter(
            df,
            x="study_hours",
            y="performance_score",
            color="performance_category",
            color_discrete_map=CATEGORY_COLORS,
            category_orders={"performance_category": ["High", "Medium", "Low"]},
            labels={
                "study_hours": "Study Hours (per day)",
                "performance_score": "Performance Score",
                "performance_category": "Category",
            },
            template=CHART_TEMPLATE,
            opacity=0.7,
        )
        fig_scatter2.update_layout(
            height=380,
            margin=dict(t=20, b=20, l=20, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        )
        fig_scatter2.update_traces(marker=dict(size=8))
        st.plotly_chart(fig_scatter2, use_container_width=True)

    # ---- Chart 4: Academic Factors by Category ----
    with chart_col4:
        st.markdown('<p class="section-header">Academic Factors by Category</p>', unsafe_allow_html=True)

        # Compute mean of each factor per category
        factor_cols = ["attendance", "internal_marks", "assignment_marks", "previous_marks", "study_hours"]
        factor_labels = {
            "attendance": "Attendance",
            "internal_marks": "Internal Marks",
            "assignment_marks": "Assignment Marks",
            "previous_marks": "Previous Marks",
            "study_hours": "Study Hours (×10)",
        }

        grouped = df.groupby("performance_category")[factor_cols].mean()
        grouped = grouped.reindex(["High", "Medium", "Low"])
        # Scale study_hours ×10 for visual comparability
        grouped["study_hours"] = grouped["study_hours"] * 10

        fig_bar = go.Figure()
        for category in ["High", "Medium", "Low"]:
            fig_bar.add_trace(go.Bar(
                name=category,
                x=[factor_labels[col] for col in factor_cols],
                y=grouped.loc[category].values,
                marker_color=CATEGORY_COLORS[category],
            ))

        fig_bar.update_layout(
            barmode="group",
            template=CHART_TEMPLATE,
            height=380,
            margin=dict(t=20, b=20, l=20, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            yaxis_title="Average Value",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ================================================================
    # RECENT STUDENT RECORDS
    # ================================================================
    st.markdown('<p class="section-header">Recent Student Records</p>', unsafe_allow_html=True)

    # Display first 10 records with formatted columns
    display_df = df.head(10).copy()
    display_df.columns = [
        "Student ID", "Attendance (%)", "Internal Marks", "Assignment Marks",
        "Previous Marks", "Study Hours", "Performance Score", "Performance"
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Attendance (%)": st.column_config.NumberColumn(format="%.1f%%"),
            "Study Hours": st.column_config.NumberColumn(format="%.1f hrs"),
            "Performance Score": st.column_config.NumberColumn(format="%.1f"),
            "Performance": st.column_config.TextColumn(),
        },
    )
