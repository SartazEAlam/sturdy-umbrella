"""
Prediction Utilities
=====================
Contains the prediction function used by the Student Prediction page.

# ============================================================
# PROTOTYPE ONLY
# Replace this rule-based logic with trained ML models later.
# ============================================================
#
# In the final version, this module will:
#   1. Load a trained model (e.g., joblib/pickle file)
#   2. Accept the same input parameters
#   3. Return the same output format (category, score, details)
#
# The function signature is designed so the UI code does NOT
# need to change when the real model is plugged in.
# ============================================================
"""
import math


def predict_performance(attendance, internal_marks, assignment_marks,
                        previous_marks, study_hours):
    """
    Predict student performance category based on academic inputs.

    PROTOTYPE: Uses a weighted rule-based formula.
    FUTURE:    Will use a trained ML model (Logistic Regression / Decision Tree / Random Forest).

    Parameters
    ----------
    attendance : float
        Attendance percentage (0–100).
    internal_marks : float
        Internal examination marks (0–100).
    assignment_marks : float
        Assignment marks (0–100).
    previous_marks : float
        Previous examination marks (0–100).
    study_hours : float
        Study hours per day (0–12).

    Returns
    -------
    tuple : (category, score, details)
        category : str
            "Low", "Medium", or "High"
        score : float
            Weighted composite score (0–100 scale)
        details : dict
            Breakdown of individual weighted contributions and interpretation text.
    """

    # ------------------------------------------------------------------
    # Step 1: Validate and sanitize inputs
    # ------------------------------------------------------------------
    def _clean(val, min_v, max_v, default=0.0):
        try:
            if val is None:
                return default
            f_val = float(val)
            if math.isnan(f_val) or math.isinf(f_val):
                return default
            return max(min_v, min(max_v, f_val))
        except (ValueError, TypeError):
            return default

    attendance = _clean(attendance, 0.0, 100.0, default=75.0)
    internal_marks = _clean(internal_marks, 0.0, 100.0, default=65.0)
    assignment_marks = _clean(assignment_marks, 0.0, 100.0, default=70.0)
    previous_marks = _clean(previous_marks, 0.0, 100.0, default=60.0)
    study_hours = _clean(study_hours, 0.0, 12.0, default=3.5)

    # ------------------------------------------------------------------
    # Step 2: Calculate weighted composite score
    # ------------------------------------------------------------------
    # Weights (sum to 1.0):
    #   Attendance:        25%
    #   Internal Marks:    25%
    #   Assignment Marks:  20%
    #   Previous Marks:    20%
    #   Study Hours:       10%  (normalized to 0–100 scale)
    # ------------------------------------------------------------------
    weights = {
        "attendance": 0.25,
        "internal_marks": 0.25,
        "assignment_marks": 0.20,
        "previous_marks": 0.20,
        "study_hours": 0.10,
    }

    study_hours_normalized = (study_hours / 12) * 100

    score = (
        weights["attendance"] * attendance +
        weights["internal_marks"] * internal_marks +
        weights["assignment_marks"] * assignment_marks +
        weights["previous_marks"] * previous_marks +
        weights["study_hours"] * study_hours_normalized
    )

    score = round(score, 1)

    # ------------------------------------------------------------------
    # Step 3: Classify into performance category
    # ------------------------------------------------------------------
    if score >= 75:
        category = "High"
    elif score >= 50:
        category = "Medium"
    else:
        category = "Low"

    # ------------------------------------------------------------------
    # Step 4: Generate interpretation text
    # ------------------------------------------------------------------
    interpretations = {
        "High": (
            "The student demonstrates strong academic indicators across all "
            "measured factors. Attendance, marks, and study commitment are "
            "all at healthy levels, suggesting consistent academic engagement."
        ),
        "Medium": (
            "The student shows moderate academic performance. Some areas are "
            "performing well while others could benefit from improvement. "
            "Targeted interventions in weaker areas could help elevate overall performance."
        ),
        "Low": (
            "The student's academic indicators suggest areas of concern. "
            "Low scores across attendance, marks, or study hours may indicate "
            "the need for academic support, counseling, or resource allocation."
        ),
    }

    # ------------------------------------------------------------------
    # Step 5: Build details dictionary
    # ------------------------------------------------------------------
    details = {
        "score": score,
        "category": category,
        "attendance": attendance,
        "internal_marks": internal_marks,
        "assignment_marks": assignment_marks,
        "previous_marks": previous_marks,
        "study_hours": study_hours,
        "study_hours_normalized": round(study_hours_normalized, 1),
        "interpretation": interpretations[category],
        "weighted_contributions": {
            "Attendance": round(weights["attendance"] * attendance, 1),
            "Internal Marks": round(weights["internal_marks"] * internal_marks, 1),
            "Assignment Marks": round(weights["assignment_marks"] * assignment_marks, 1),
            "Previous Marks": round(weights["previous_marks"] * previous_marks, 1),
            "Study Hours": round(weights["study_hours"] * study_hours_normalized, 1),
        },
    }

    return category, score, details
