"""
Generate Sample Student Data
=============================
This script creates a realistic sample dataset of 200 student records
with correlated academic features for the prototype dashboard.

Run once to generate data/sample_student_data.csv.
"""

import numpy as np
import pandas as pd
import os

def generate_sample_data(n_students=200, seed=42):
    """
    Generate n_students sample records with realistic correlations
    between academic factors and performance.
    """
    np.random.seed(seed)

    # ------------------------------------------------------------------
    # Step 1: Create a base "ability" factor that drives correlations
    # ------------------------------------------------------------------
    # Each student has an underlying ability level (0-100 scale, roughly)
    ability = np.random.normal(loc=60, scale=18, size=n_students)
    ability = np.clip(ability, 5, 100)

    # ------------------------------------------------------------------
    # Step 2: Generate correlated features from the ability base
    # ------------------------------------------------------------------
    # Attendance: higher-ability students tend to attend more
    attendance = ability * 0.7 + np.random.normal(0, 10, n_students) + 25
    attendance = np.clip(attendance, 20, 100).round(1)

    # Internal marks
    internal_marks = ability * 0.75 + np.random.normal(0, 8, n_students) + 15
    internal_marks = np.clip(internal_marks, 10, 100).round(1)

    # Assignment marks
    assignment_marks = ability * 0.7 + np.random.normal(0, 9, n_students) + 18
    assignment_marks = np.clip(assignment_marks, 12, 100).round(1)

    # Previous examination marks
    previous_marks = ability * 0.8 + np.random.normal(0, 7, n_students) + 10
    previous_marks = np.clip(previous_marks, 8, 100).round(1)

    # Study hours per day (0-12 scale)
    study_hours = (ability / 100) * 8 + np.random.normal(0, 1.2, n_students) + 0.5
    study_hours = np.clip(study_hours, 0.5, 12.0).round(1)

    # ------------------------------------------------------------------
    # Step 3: Calculate composite performance score
    # ------------------------------------------------------------------
    performance_score = (
        0.25 * attendance +
        0.25 * internal_marks +
        0.20 * assignment_marks +
        0.20 * previous_marks +
        0.10 * (study_hours / 12 * 100)
    ).round(1)

    # ------------------------------------------------------------------
    # Step 4: Assign performance categories
    # ------------------------------------------------------------------
    categories = []
    for score in performance_score:
        if score >= 75:
            categories.append("High")
        elif score >= 50:
            categories.append("Medium")
        else:
            categories.append("Low")

    # ------------------------------------------------------------------
    # Step 5: Build DataFrame
    # ------------------------------------------------------------------
    student_ids = [f"STU{str(i+1).zfill(3)}" for i in range(n_students)]

    df = pd.DataFrame({
        "student_id": student_ids,
        "attendance": attendance,
        "internal_marks": internal_marks,
        "assignment_marks": assignment_marks,
        "previous_marks": previous_marks,
        "study_hours": study_hours,
        "performance_score": performance_score,
        "performance_category": categories,
    })

    return df


if __name__ == "__main__":
    # Generate and save
    df = generate_sample_data(200)

    # Ensure output directory exists
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "sample_student_data.csv")
    df.to_csv(output_path, index=False)

    # Print summary
    print(f"Generated {len(df)} student records -> {output_path}")
    print(f"\nCategory distribution:")
    print(df["performance_category"].value_counts().to_string())
    print(f"\nSample records:")
    print(df.head(10).to_string(index=False))
