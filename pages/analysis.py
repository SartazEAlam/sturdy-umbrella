"""
Performance Analysis Page
==========================
Exploratory data analysis using the sample dataset.
Includes distributions, box plots, correlation heatmap,
and a factor importance section.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_processing import load_data, get_correlation_matrix


# ------------------------------------------------------------------
# Shared styling constants
# ------------------------------------------------------------------
CATEGORY_COLORS = {
    "High": "#06d6a0",
    "Medium": "#ffd166",
    "Low": "#ef476f",
}
CATEGORY_ORDER = ["High", "Medium", "Low"]
CHART_TEMPLATE = "plotly_white"


def render():
    """Render the Performance Analysis page."""

    # --- Header ---
    st.markdown('<p class="main-header">🔬 Performance Analysis</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="main-subtitle">'
        'Explore relationships between academic factors and student performance '
        'using the sample dataset.'
        '</p>',
        unsafe_allow_html=True,
    )

    # --- Prototype notice ---
    st.markdown(
        '<div class="prototype-banner">'
        '⚠️ Analysis based on sample data only. '
        'These observations are for prototype demonstration and are not statistically validated findings.'
        '</div>',
        unsafe_allow_html=True,
    )

    # --- Load data ---
    df = load_data()
    if df is None or df.empty:
        st.warning("Unable to load dataset or dataset is empty.")
        return

    # ================================================================
    # 1. PERFORMANCE CATEGORY DISTRIBUTION
    # ================================================================
    st.markdown('<p class="section-header">📊 Performance Category Distribution</p>', unsafe_allow_html=True)

    cat_counts = df["performance_category"].value_counts().reindex(CATEGORY_ORDER, fill_value=0)

    fig_dist = go.Figure()
    fig_dist.add_trace(go.Bar(
        x=cat_counts.index,
        y=cat_counts.values,
        marker_color=[CATEGORY_COLORS[c] for c in cat_counts.index],
        text=cat_counts.values,
        textposition="outside",
        textfont=dict(size=14, color="#1a1a2e"),
    ))
    fig_dist.update_layout(
        template=CHART_TEMPLATE,
        height=350,
        margin=dict(t=30, b=30, l=40, r=20),
        xaxis_title="Performance Category",
        yaxis_title="Number of Students",
    )
    st.plotly_chart(fig_dist)

    # Show counts as metrics
    dist_cols = st.columns(3)
    for col, cat in zip(dist_cols, CATEGORY_ORDER):
        count = int(cat_counts.get(cat, 0))
        pct = round(count / len(df) * 100, 1) if len(df) > 0 else 0.0
        col.metric(f"{cat} Performers", f"{count} ({pct}%)")

    st.divider()

    # ================================================================
    # 2. ATTENDANCE ANALYSIS
    # ================================================================
    st.markdown('<p class="section-header">📋 Attendance Analysis</p>', unsafe_allow_html=True)

    att_col1, att_col2 = st.columns(2)

    with att_col1:
        fig_att_box = px.box(
            df,
            x="performance_category",
            y="attendance",
            color="performance_category",
            color_discrete_map=CATEGORY_COLORS,
            category_orders={"performance_category": CATEGORY_ORDER},
            labels={"attendance": "Attendance (%)", "performance_category": "Category"},
            template=CHART_TEMPLATE,
        )
        fig_att_box.update_layout(
            height=350,
            margin=dict(t=20, b=20, l=20, r=20),
            showlegend=False,
            title="Attendance Distribution by Category",
            title_font_size=14,
        )
        st.plotly_chart(fig_att_box)

    with att_col2:
        fig_att_hist = px.histogram(
            df,
            x="attendance",
            color="performance_category",
            color_discrete_map=CATEGORY_COLORS,
            category_orders={"performance_category": CATEGORY_ORDER},
            nbins=20,
            labels={"attendance": "Attendance (%)", "performance_category": "Category"},
            template=CHART_TEMPLATE,
            barmode="overlay",
            opacity=0.7,
        )
        fig_att_hist.update_layout(
            height=350,
            margin=dict(t=20, b=20, l=20, r=20),
            title="Attendance Histogram",
            title_font_size=14,
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        )
        st.plotly_chart(fig_att_hist)

    st.divider()

    # ================================================================
    # 3. STUDY HOURS ANALYSIS
    # ================================================================
    st.markdown('<p class="section-header">⏰ Study Hours Analysis</p>', unsafe_allow_html=True)

    sh_col1, sh_col2 = st.columns(2)

    with sh_col1:
        fig_sh_box = px.box(
            df,
            x="performance_category",
            y="study_hours",
            color="performance_category",
            color_discrete_map=CATEGORY_COLORS,
            category_orders={"performance_category": CATEGORY_ORDER},
            labels={"study_hours": "Study Hours (per day)", "performance_category": "Category"},
            template=CHART_TEMPLATE,
        )
        fig_sh_box.update_layout(
            height=350,
            margin=dict(t=20, b=20, l=20, r=20),
            showlegend=False,
            title="Study Hours Distribution by Category",
            title_font_size=14,
        )
        st.plotly_chart(fig_sh_box)

    with sh_col2:
        try:
            fig_sh_scatter = px.scatter(
                df,
                x="study_hours",
                y="performance_score",
                color="performance_category",
                color_discrete_map=CATEGORY_COLORS,
                category_orders={"performance_category": CATEGORY_ORDER},
                labels={
                    "study_hours": "Study Hours (per day)",
                    "performance_score": "Performance Score",
                    "performance_category": "Category",
                },
                template=CHART_TEMPLATE,
                opacity=0.7,
                trendline="ols",
            )
        except Exception:
            # Fallback without trendline if statsmodels encounters numerical singularities
            fig_sh_scatter = px.scatter(
                df,
                x="study_hours",
                y="performance_score",
                color="performance_category",
                color_discrete_map=CATEGORY_COLORS,
                category_orders={"performance_category": CATEGORY_ORDER},
                labels={
                    "study_hours": "Study Hours (per day)",
                    "performance_score": "Performance Score",
                    "performance_category": "Category",
                },
                template=CHART_TEMPLATE,
                opacity=0.7,
            )
        fig_sh_scatter.update_layout(
            height=350,
            margin=dict(t=20, b=20, l=20, r=20),
            title="Study Hours vs Performance (with trendline)",
            title_font_size=14,
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        )
        st.plotly_chart(fig_sh_scatter)

    st.divider()

    # ================================================================
    # 4. INTERNAL MARKS ANALYSIS
    # ================================================================
    st.markdown('<p class="section-header">📝 Internal Marks Analysis</p>', unsafe_allow_html=True)

    im_col1, im_col2 = st.columns(2)

    with im_col1:
        fig_im_box = px.box(
            df,
            x="performance_category",
            y="internal_marks",
            color="performance_category",
            color_discrete_map=CATEGORY_COLORS,
            category_orders={"performance_category": CATEGORY_ORDER},
            labels={"internal_marks": "Internal Marks", "performance_category": "Category"},
            template=CHART_TEMPLATE,
        )
        fig_im_box.update_layout(
            height=350,
            margin=dict(t=20, b=20, l=20, r=20),
            showlegend=False,
            title="Internal Marks Distribution by Category",
            title_font_size=14,
        )
        st.plotly_chart(fig_im_box)

    with im_col2:
        fig_im_violin = px.violin(
            df,
            x="performance_category",
            y="internal_marks",
            color="performance_category",
            color_discrete_map=CATEGORY_COLORS,
            category_orders={"performance_category": CATEGORY_ORDER},
            labels={"internal_marks": "Internal Marks", "performance_category": "Category"},
            template=CHART_TEMPLATE,
            box=True,
        )
        fig_im_violin.update_layout(
            height=350,
            margin=dict(t=20, b=20, l=20, r=20),
            showlegend=False,
            title="Internal Marks Violin Plot",
            title_font_size=14,
        )
        st.plotly_chart(fig_im_violin)

    st.divider()

    # ================================================================
    # 5. CORRELATION MATRIX
    # ================================================================
    st.markdown('<p class="section-header">🔗 Correlation Matrix</p>', unsafe_allow_html=True)

    corr_matrix = get_correlation_matrix(df)

    # Rename for display
    display_labels = {
        "attendance": "Attendance",
        "internal_marks": "Internal Marks",
        "assignment_marks": "Assignment Marks",
        "previous_marks": "Previous Marks",
        "study_hours": "Study Hours",
        "performance_score": "Performance Score",
    }
    corr_display = corr_matrix.rename(index=display_labels, columns=display_labels)

    fig_heatmap = px.imshow(
        corr_display,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        template=CHART_TEMPLATE,
        labels=dict(color="Correlation"),
    )
    fig_heatmap.update_layout(
        height=500,
        margin=dict(t=30, b=20, l=20, r=20),
    )
    st.plotly_chart(fig_heatmap)

    st.divider()

    # ================================================================
    # 6. FACTORS ASSOCIATED WITH PERFORMANCE
    # ================================================================
    st.markdown(
        '<p class="section-header">🎯 Factors Associated with Student Performance</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="info-box">'
        '<strong>Note:</strong> The following analysis is based on the sample dataset '
        'and shows observed correlations, not proven causal relationships. '
        'These results are for prototype demonstration purposes only.'
        '</div>',
        unsafe_allow_html=True,
    )

    # Extract correlations with performance_score (excluding self)
    perf_corr = corr_matrix["performance_score"].drop("performance_score").sort_values(ascending=False).fillna(0)

    factor_display_names = {
        "attendance": "Attendance",
        "internal_marks": "Internal Marks",
        "assignment_marks": "Assignment Marks",
        "previous_marks": "Previous Marks",
        "study_hours": "Study Hours",
    }

    fig_factors = go.Figure()
    colors = ["#06d6a0" if v > 0 else "#ef476f" for v in perf_corr.values]
    fig_factors.add_trace(go.Bar(
        x=perf_corr.values,
        y=[factor_display_names.get(col, col) for col in perf_corr.index],
        orientation="h",
        marker_color=colors,
        text=[f"{v:.3f}" for v in perf_corr.values],
        textposition="outside",
    ))
    fig_factors.update_layout(
        template=CHART_TEMPLATE,
        height=300,
        margin=dict(t=20, b=20, l=10, r=50),
        xaxis_title="Correlation with Performance Score",
        xaxis=dict(range=[-1, 1]),
    )
    st.plotly_chart(fig_factors)

    # Summary interpretation
    if not perf_corr.empty:
        top_factor = factor_display_names.get(perf_corr.index[0], perf_corr.index[0])
        st.info(
            f"📌 **Strongest observed association:** {top_factor} shows the highest "
            f"correlation ({perf_corr.values[0]:.3f}) with overall performance score "
            f"in the sample dataset."
        )
