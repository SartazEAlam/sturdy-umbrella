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

import importlib

# ------------------------------------------------------------------
# Import page modules (with hot-reloading support)
# ------------------------------------------------------------------
from pages import dashboard, prediction, analysis, model_comparison, about
for _mod in (dashboard, prediction, analysis, model_comparison, about):
    importlib.reload(_mod)

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

    st.divider()

    # Theme selector
    st.radio(
        "Theme",
        options=["☀️ Light", "🌙 Dark"],
        horizontal=True,
        key="app_theme",
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
# Apply Dynamic Theme Styles
# ------------------------------------------------------------------
if st.session_state.get("app_theme") == "🌙 Dark":
    st.markdown(
        """
        <style>
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #0e1117 !important;
            color: #fafafa !important;
        }
        [data-testid="stSidebar"] {
            background-color: #161a23 !important;
            border-right: 1px solid #2d323f !important;
        }
        [data-testid="stSidebar"] * {
            color: #e2e8f0;
        }
        :root, body, .stApp {
            --text-primary: #f1f3f9 !important;
            --text-secondary: #94a3b8 !important;
            --text-muted: #cbd5e1 !important;
            --card-bg: linear-gradient(135deg, #1e222b 0%, #151821 100%) !important;
            --card-border: #2d323f !important;
            --card-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
            --card-hover-shadow: 0 4px 16px rgba(0, 0, 0, 0.45) !important;
            --card-high-bg: linear-gradient(135deg, #0a2618 0%, #151821 100%) !important;
            --card-medium-bg: linear-gradient(135deg, #2b1f06 0%, #151821 100%) !important;
            --card-low-bg: linear-gradient(135deg, #2c0e14 0%, #151821 100%) !important;
            --info-bg: #151f33 !important;
            --info-text: #e2e8f0 !important;
            --banner-bg: linear-gradient(135deg, #332701 0%, #241c00 100%) !important;
            --banner-border: #856404 !important;
            --banner-text: #ffd166 !important;
            --border-color: #2d323f !important;
            --about-card-bg: #1a1e27 !important;
            --chart-container-bg: #1a1e27 !important;
        }
        </style>
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
