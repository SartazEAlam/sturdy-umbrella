"""
Student Performance Prediction & Analysis System
==================================================
Main application entry point.

This is a Streamlit-based academic analytics dashboard that provides:
- Dashboard with KPI cards and charts
- Student performance prediction
- Exploratory data analysis
- Machine learning model comparison
- Project information

Run with: streamlit run app.py
"""

import streamlit as st
import os

# ------------------------------------------------------------------
# Page Configuration (must be the first Streamlit command)
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Student Performance Prediction & Analysis",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# Load Custom CSS
# ------------------------------------------------------------------
def load_css():
    """Load custom CSS from assets/style.css."""
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ------------------------------------------------------------------
# Import page modules
# ------------------------------------------------------------------
from pages import dashboard, prediction, analysis, model_comparison, about

# ------------------------------------------------------------------
# Sidebar Navigation
# ------------------------------------------------------------------
with st.sidebar:
    # Project title
    st.markdown(
        """
        <div style="text-align: center; padding: 1rem 0 1.5rem 0;">
            <div style="font-size: 2rem;">🎓</div>
            <div class="sidebar-title">Student Performance</div>
            <div class="sidebar-title">Prediction & Analysis</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # Navigation menu
    page = st.radio(
        "Navigation",
        options=[
            "📊 Dashboard",
            "🎯 Student Prediction",
            "🔬 Performance Analysis",
            "🤖 Model Comparison",
            "ℹ️ About Project",
        ],
        label_visibility="collapsed",
    )

    # Footer
    st.divider()
    st.markdown(
        """
        <div style="text-align: center; padding: 0.5rem 0;">
            <div style="font-size: 0.78rem; color: #adb5bd; font-weight: 600;">
                CAPSTONE PROJECT
            </div>
            <div style="font-size: 0.72rem; color: #ced4da; margin-top: 0.3rem; line-height: 1.4;">
                Student Performance<br>
                Prediction & Analysis System
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------
# Page Routing
# ------------------------------------------------------------------
if page == "📊 Dashboard":
    dashboard.render()
elif page == "🎯 Student Prediction":
    prediction.render()
elif page == "🔬 Performance Analysis":
    analysis.render()
elif page == "🤖 Model Comparison":
    model_comparison.render()
elif page == "ℹ️ About Project":
    about.render()
