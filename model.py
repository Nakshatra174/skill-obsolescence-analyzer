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

# Add lowercase skill column once
data["skill_lower"] = data["skill"].str.lower()

# -------------------------------
# Rule-based Obsolescence Logic
# -------------------------------
def predict_obsolescence_by_skill(skill_name):
    skill_name = skill_name.strip().lower()

    if skill_name not in data["skill_lower"].values:
        return None, None, None

    row = data[data["skill_lower"] == skill_name].iloc[0]

    # Obsolescence score calculation (aligned with dataset)
    score = (
        row["automation_risk"] * 0.4 +
        (10 - row["demand_score"]) * 0.3 +
        (10 - row["learning_trend"]) * 0.3
    )

    # Risk classification
    if score >= 6:
        risk = "High Risk of Skill Obsolescence"
    elif score >= 4:
        risk = "Medium Risk of Skill Obsolescence"
    else:
        risk = "Low Risk of Skill Obsolescence"

    details = {
        "years_experience": int(row["years_experience"]),
        "demand_score": int(row["demand_score"]),
        "automation_risk": int(row["automation_risk"]),
        "learning_trend": int(row["learning_trend"])
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
    recommendations = {
        "cobol": ["Python", "Java", "Cloud Computing", "Data Engineering"],
        "manual testing": ["Automation Testing", "Selenium", "Python"],
        "data entry": ["Data Analysis", "SQL", "Excel", "Power BI"],
        "php": ["JavaScript", "Node.js", "React"],
        "python": ["Machine Learning", "AI Engineering", "Data Science"],
    }

    return recommendations.get(
        skill_name.lower(),
        ["Python", "Cloud Computing", "Data Analysis"]
    )


# -------------------------------
# ML Prediction Function
# -------------------------------
def predict_risk_ml(years, demand, automation, trend):
    prediction = ml_model.predict([[years, demand, automation, trend]])
    return prediction[0]
