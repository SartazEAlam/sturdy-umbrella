"""
Model Comparison Page
======================
Displays mock ML model evaluation metrics and comparison charts.

All values are clearly labeled as prototype/sample results.
Real model training and evaluation will replace this in a later phase.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd


# ------------------------------------------------------------------
# Mock model evaluation data
# ------------------------------------------------------------------
# PROTOTYPE ONLY
# These are sample values for UI demonstration.
# They will be replaced with actual evaluation results after training.
# ------------------------------------------------------------------
MOCK_MODELS = pd.DataFrame({
    "Model": ["Logistic Regression", "Decision Tree", "Random Forest"],
    "Accuracy": [0.823, 0.794, 0.856],
    "Precision": [0.814, 0.781, 0.849],
    "Recall": [0.808, 0.776, 0.841],
    "F1-Score": [0.811, 0.778, 0.845],
})

MODEL_COLORS = {
    "Logistic Regression": "#4361ee",
    "Decision Tree": "#f72585",
    "Random Forest": "#06d6a0",
}


def render():
    """Render the Model Comparison page."""

    # --- Header ---
    st.markdown('<p class="main-header">🤖 Machine Learning Model Comparison</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="main-subtitle">'
        'Compare classification models for student performance prediction.'
        '</p>',
        unsafe_allow_html=True,
    )

    # --- Prominent prototype banner ---
    st.markdown(
        '<div class="prototype-banner">'
        '⚠️ <strong>Prototype / Sample Results</strong> — The metrics shown below are '
        'sample placeholder values for UI demonstration only. Actual model training, '
        'evaluation, and comparison will be performed in the next development phase.'
        '</div>',
        unsafe_allow_html=True,
    )

    # ================================================================
    # MODELS OVERVIEW
    # ================================================================
    st.markdown('<p class="section-header">📋 Models Under Evaluation</p>', unsafe_allow_html=True)

    model_cols = st.columns(3)

    model_info = [
        (
            "Logistic Regression",
            "A linear model that estimates probabilities using a logistic function. "
            "Suitable for linearly separable data and provides interpretable coefficients.",
            "📈",
        ),
        (
            "Decision Tree",
            "A tree-based model that splits data based on feature thresholds. "
            "Easy to interpret and visualize, but may overfit without pruning.",
            "🌳",
        ),
        (
            "Random Forest",
            "An ensemble of decision trees that reduces overfitting through bagging. "
            "Generally provides higher accuracy and robustness.",
            "🌲",
        ),
    ]

    for col, (name, desc, icon) in zip(model_cols, model_info):
        with col:
            st.markdown(
                f"""
                <div class="kpi-card" style="text-align: left; min-height: 160px;">
                    <div style="font-size: 1.4rem; margin-bottom: 0.5rem;">{icon}</div>
                    <div style="font-weight: 600; font-size: 1rem; color: #1a1a2e; margin-bottom: 0.4rem;">
                        {name}
                    </div>
                    <div style="font-size: 0.85rem; color: #6c757d; line-height: 1.5;">
                        {desc}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ================================================================
    # METRICS TABLE
    # ================================================================
    st.markdown('<p class="section-header">📊 Evaluation Metrics (Sample)</p>', unsafe_allow_html=True)

    # Format percentages for display
    display_df = MOCK_MODELS.copy()
    for col in ["Accuracy", "Precision", "Recall", "F1-Score"]:
        display_df[col] = display_df[col].apply(lambda x: f"{x:.1%} (sample)")

    st.dataframe(
        display_df,
        hide_index=True,
        column_config={
            "Model": st.column_config.TextColumn("Model", width="medium"),
            "Accuracy": st.column_config.TextColumn("Accuracy"),
            "Precision": st.column_config.TextColumn("Precision"),
            "Recall": st.column_config.TextColumn("Recall"),
            "F1-Score": st.column_config.TextColumn("F1-Score"),
        },
    )

    st.divider()

    # ================================================================
    # COMPARISON BAR CHART
    # ================================================================
    st.markdown('<p class="section-header">📈 Model Performance Comparison (Sample)</p>', unsafe_allow_html=True)

    metrics = ["Accuracy", "Precision", "Recall", "F1-Score"]

    fig_compare = go.Figure()

    for _, row in MOCK_MODELS.iterrows():
        model_name = row["Model"]
        fig_compare.add_trace(go.Bar(
            name=model_name,
            x=metrics,
            y=[row[m] for m in metrics],
            marker_color=MODEL_COLORS[model_name],
            text=[f"{row[m]:.1%}" for m in metrics],
            textposition="outside",
            textfont=dict(size=11),
        ))

    fig_compare.update_layout(
        barmode="group",
        template="plotly_white",
        height=450,
        margin=dict(t=30, b=30, l=40, r=20),
        yaxis=dict(range=[0, 1], title="Score", tickformat=".0%"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
    )
    st.plotly_chart(fig_compare)

    st.divider()

    # ================================================================
    # RADAR COMPARISON
    # ================================================================
    st.markdown('<p class="section-header">🕸️ Model Radar Comparison (Sample)</p>', unsafe_allow_html=True)

    fig_radar = go.Figure()
    for _, row in MOCK_MODELS.iterrows():
        model_name = row["Model"]
        values = [row[m] for m in metrics] + [row[metrics[0]]]  # close the polygon
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=metrics + [metrics[0]],
            name=model_name,
            line=dict(color=MODEL_COLORS[model_name], width=2),
            fill="toself",
            opacity=0.3,
        ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0.7, 0.9])),
        template="plotly_white",
        height=450,
        margin=dict(t=30, b=30, l=60, r=60),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
    )
    st.plotly_chart(fig_radar)

    st.divider()

    # ================================================================
    # FINAL MODEL SELECTION
    # ================================================================
    st.markdown('<p class="section-header">🏆 Final Model</p>', unsafe_allow_html=True)

    st.warning(
        "**Not selected** — Actual model evaluation will be performed after dataset training. "
        "The best-performing model will be selected based on evaluation metrics "
        "(Accuracy, Precision, Recall, F1-Score) computed on a held-out test set."
    )

    st.markdown(
        '<div class="info-box">'
        '<strong>Next Steps:</strong><br>'
        '1. Collect and preprocess the real student dataset.<br>'
        '2. Perform exploratory data analysis (EDA).<br>'
        '3. Split data into training and testing sets.<br>'
        '4. Train Logistic Regression, Decision Tree, and Random Forest models.<br>'
        '5. Evaluate and compare models using the metrics above.<br>'
        '6. Select and deploy the best-performing model.'
        '</div>',
        unsafe_allow_html=True,
    )
