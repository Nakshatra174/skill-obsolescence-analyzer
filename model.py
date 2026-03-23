import joblib
import pandas as pd

# -------------------------------
# Load ML Model
# -------------------------------
ml_model = joblib.load("skill_obsolescence_model.pkl")

# -------------------------------
# Load Dataset
# -------------------------------
data = pd.read_csv("dataset.csv")

# Add lowercase skill column once (handle missing safely)
data["skill_lower"] = data["skill"].astype(str).str.lower()

# -------------------------------
# Rule-based Obsolescence Logic
# -------------------------------
def predict_obsolescence_by_skill(skill_name):
    # ✅ Clean input
    skill_name = skill_name.strip().lower()

    # ❗ Handle empty input
    if not skill_name:
        return None, None, None

    # ✅ PARTIAL MATCH (case-insensitive, safe)
    matched_rows = data[data["skill_lower"].str.contains(skill_name, na=False)]

    # ❗ If no match found
    if matched_rows.empty:
        return None, None, None

    # Take first matching row
    row = matched_rows.iloc[0]

    # -------------------------------
    # Score Calculation
    # -------------------------------
    score = (
        row["automation_risk"] * 0.4 +
        (10 - row["demand_score"]) * 0.3 +
        (10 - row["learning_trend"]) * 0.3
    )

    # -------------------------------
    # Risk Classification
    # -------------------------------
    if score >= 6:
        risk = "High Risk of Skill Obsolescence"
    elif score >= 4:
        risk = "Medium Risk of Skill Obsolescence"
    else:
        risk = "Low Risk of Skill Obsolescence"

    # -------------------------------
    # Details
    # -------------------------------
    details = {
        "years_experience": int(row.get("years_experience", 0)),
        "demand_score": int(row.get("demand_score", 0)),
        "automation_risk": int(row.get("automation_risk", 0)),
        "learning_trend": int(row.get("learning_trend", 0))
    }

    return round(score, 2), risk, details


# -------------------------------
# Skill Analysis Wrapper
# -------------------------------
def get_skill_analysis(skill_name):
    score, risk, details = predict_obsolescence_by_skill(skill_name)

    if score is None:
        return None

    return {
        "name": skill_name,
        "score": score,
        "risk": risk,
        "details": details
    }


# -------------------------------
# Skill Recommendation Engine
# -------------------------------
def recommend_skills(skill_name):
    skill_name = skill_name.lower()

    recommendations = {
        "cobol": ["Python", "Java", "Cloud Computing", "Data Engineering"],
        "manual testing": ["Automation Testing", "Selenium", "Python"],
        "data entry": ["Data Analysis", "SQL", "Excel", "Power BI"],
        "php": ["JavaScript", "Node.js", "React"],
        "python": ["Machine Learning", "AI Engineering", "Data Science"],
        "sql": ["Data Engineering", "Database Administration", "Big Data"]
    }

    return recommendations.get(
        skill_name,
        ["Python", "Cloud Computing", "Data Analysis"]
    )


# -------------------------------
# ML Prediction Function
# -------------------------------
def predict_risk_ml(years, demand, automation, trend):
    try:
        prediction = ml_model.predict([[years, demand, automation, trend]])
        return prediction[0]
    except Exception:
        return "Unknown"


# -------------------------------
# Feature Importance (Explainable AI)
# -------------------------------
def get_feature_importance():
    try:
        importances = ml_model.feature_importances_
        features = ['Experience', 'Demand', 'Automation', 'Learning']
        return dict(zip(features, importances))
    except Exception:
        return {}