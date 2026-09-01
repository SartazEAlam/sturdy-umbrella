# Student Performance Prediction & Analysis System

A Streamlit-based web application for analyzing student academic data and predicting performance categories using machine learning.

---

## 📋 Project Overview

This system collects student academic information (attendance, examination marks, assignment scores, study hours) and:

1. **Visualizes** key academic indicators through interactive charts
2. **Predicts** student performance categories (Low / Medium / High)
3. **Analyzes** relationships between academic factors and outcomes
4. **Compares** machine learning models for classification accuracy

**Current Status:** Phase 1 — Functional UI/UX Prototype

---

## ✨ Features

| Feature | Status |
|---------|--------|
| Interactive Dashboard with KPI cards and charts | ✅ Complete |
| Student Performance Prediction (rule-based) | ✅ Prototype |
| Exploratory Data Analysis | ✅ Complete |
| Model Comparison Interface | ✅ Prototype (mock data) |
| About Project Page | ✅ Complete |
| ML Model Training & Evaluation | 🔜 Phase 2 |

---

## 🛠️ Technology Stack

- **Python** — Core programming language
- **Streamlit** — Interactive web dashboard framework
- **Pandas** — Data manipulation and analysis
- **NumPy** — Numerical computing
- **Plotly** — Interactive data visualizations
- **Scikit-learn** — Machine learning (to be integrated in Phase 2)

---

## 📁 Project Structure

```text
Student_Performance_Prediction_System/
│
├── app.py                          # Main Streamlit application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── generate_data.py                # Script to generate sample data
│
├── data/
│   └── sample_student_data.csv     # Sample dataset (200 student records)
│
├── pages/
│   ├── __init__.py
│   ├── dashboard.py                # Dashboard with KPIs and charts
│   ├── prediction.py               # Student prediction form and results
│   ├── analysis.py                 # Performance analysis and EDA
│   ├── model_comparison.py         # ML model comparison (prototype)
│   └── about.py                    # Project information
│
├── utils/
│   ├── __init__.py
│   ├── data_processing.py          # Data loading and processing utilities
│   └── prediction.py               # Prediction logic (rule-based prototype)
│
└── assets/
    └── style.css                   # Custom CSS styling
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone or download** this project:
   ```bash
   cd Student_Performance_Prediction_System
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Regenerate sample data:**
   ```bash
   python generate_data.py
   ```

---

## 🚀 How to Run

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

---

## ⚠️ Current Prototype Limitations

This is **Phase 1 — Prototype**. The following components use mock/sample data:

| Component | Current State | Phase 2 Upgrade |
|-----------|--------------|-----------------|
| Dataset | 200 sample records (generated) | Real student dataset |
| Prediction | Rule-based weighted formula | Trained ML model |
| Model Comparison | Sample placeholder metrics | Actual evaluation results |
| Analysis | Based on sample data | Based on real data with statistical validation |

**Important:** The mock evaluation metrics on the Model Comparison page are sample values for UI demonstration only. They do not represent actual model performance.

---

## 🔮 Future ML Implementation (Phase 2)

The following will be implemented in the next development phase:

1. **Data Collection** — Gather real student academic data
2. **Data Preprocessing** — Handle missing values, outliers, encoding
3. **Exploratory Data Analysis** — Statistical analysis on real data
4. **Train/Test Split** — Stratified splitting for balanced evaluation
5. **Model Training:**
   - Logistic Regression
   - Decision Tree
   - Random Forest
6. **Model Evaluation** — Accuracy, Precision, Recall, F1-Score
7. **Best Model Selection** — Based on evaluation metrics
8. **Integration** — Replace rule-based prediction with trained model

---

## 📄 License

This project is developed as an academic capstone project for B.Tech CSE.
