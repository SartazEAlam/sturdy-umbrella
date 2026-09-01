"""
Data Processing Utilities
==========================
Functions for loading, validating, and summarizing the student dataset.

This module keeps data handling separate from the UI layer,
making it easy to swap in real preprocessing later.
"""

import pandas as pd
import streamlit as st
import os


# ------------------------------------------------------------------
# Expected columns in the dataset
# ------------------------------------------------------------------
EXPECTED_COLUMNS = [
    "student_id",
    "attendance",
    "internal_marks",
    "assignment_marks",
    "previous_marks",
    "study_hours",
    "performance_score",
    "performance_category",
]


@st.cache_data
def load_data(filepath=None):
    """
    Load the student dataset from CSV.

    Parameters
    ----------
    filepath : str, optional
        Path to the CSV file. Defaults to data/sample_student_data.csv
        relative to the project root.

    Returns
    -------
    pd.DataFrame or None
        The loaded DataFrame, or None if the file cannot be read.
    """
    if filepath is None:
        # Resolve path relative to this file's location
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.join(base_dir, "data", "sample_student_data.csv")

    try:
        df = pd.read_csv(filepath)

        # Validate that required columns exist
        missing = [col for col in EXPECTED_COLUMNS if col not in df.columns]
        if missing:
            st.error(f"Dataset is missing columns: {', '.join(missing)}")
            return None

        # Basic type coercion — ensure numeric columns are numeric
        numeric_cols = [
            "attendance", "internal_marks", "assignment_marks",
            "previous_marks", "study_hours", "performance_score",
        ]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Drop rows that became NaN after coercion (shouldn't happen with clean data)
        df = df.dropna(subset=numeric_cols)

        if df.empty:
            st.error("The dataset contains no valid student records.")
            return None

        return df

    except FileNotFoundError:
        st.error(f"Data file not found: {filepath}")
        return None
    except pd.errors.EmptyDataError:
        st.error("The data file is empty.")
        return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None


def get_summary_stats(df):
    """
    Compute key performance indicator values from the dataset.

    Parameters
    ----------
    df : pd.DataFrame
        The student dataset.

    Returns
    -------
    dict
        Dictionary containing KPI values:
        - total_students
        - avg_attendance
        - avg_internal_marks
        - avg_study_hours
        - high_performers (count of 'High' category)
        - medium_performers
        - low_performers
    """
    if df is None or df.empty:
        return {
            "total_students": 0,
            "avg_attendance": 0.0,
            "avg_internal_marks": 0.0,
            "avg_study_hours": 0.0,
            "high_performers": 0,
            "medium_performers": 0,
            "low_performers": 0,
        }

    category_counts = df["performance_category"].value_counts()

    return {
        "total_students": len(df),
        "avg_attendance": round(float(df["attendance"].mean()), 1) if not df["attendance"].empty else 0.0,
        "avg_internal_marks": round(float(df["internal_marks"].mean()), 1) if not df["internal_marks"].empty else 0.0,
        "avg_study_hours": round(float(df["study_hours"].mean()), 1) if not df["study_hours"].empty else 0.0,
        "high_performers": int(category_counts.get("High", 0)),
        "medium_performers": int(category_counts.get("Medium", 0)),
        "low_performers": int(category_counts.get("Low", 0)),
    }


def get_correlation_matrix(df):
    """
    Compute correlation matrix for the numeric academic columns.

    Parameters
    ----------
    df : pd.DataFrame
        The student dataset.

    Returns
    -------
    pd.DataFrame
        Correlation matrix.
    """
    numeric_cols = [
        "attendance", "internal_marks", "assignment_marks",
        "previous_marks", "study_hours", "performance_score",
    ]
    return df[numeric_cols].corr().round(3)
