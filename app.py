from flask import Flask, render_template, request, jsonify

# -------- MODEL IMPORTS --------
from model import (
    predict_obsolescence_by_skill,
    get_skill_analysis,
    recommend_skills,
    predict_risk_ml
)

# -------- CHART / INSIGHTS IMPORTS --------
from charts import (
    generate_obsolescence_distribution,
    generate_risk_level_distribution,
    generate_average_distribution,
    generate_skill_demand_trend,
    generate_ml_risk_distribution,
    get_risk_summary_counts
)

app = Flask(__name__)

# ---------------- PAGE ROUTES (GET) ----------------

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/analyze')
def analyze():
    return render_template('index.html')


@app.route('/compare')
def compare():
    return render_template('compare.html')


@app.route('/insights')
def insights():
    # Generate charts
    generate_obsolescence_distribution()
    generate_risk_level_distribution()
    generate_average_distribution()
    generate_skill_demand_trend()
    generate_ml_risk_distribution()

    # Get summary counts
    low, medium, high = get_risk_summary_counts()

    return render_template(
        'insights.html',
        low_risk=low,
        medium_risk=medium,
        high_risk=high
    )


@app.route('/about')
def about():
    return render_template('about.html')


# ---------------- ACTION ROUTES (POST) ----------------

@app.route('/predict', methods=['POST'])
def predict():
    skill = request.form['skill']

    # -------- RULE-BASED PREDICTION --------
    score, rule_risk, details = predict_obsolescence_by_skill(skill)

    # ✅ HANDLE UNKNOWN SKILL (FIX)
    if rule_risk is None:
        return render_template(
            'result.html',
            skill=skill,
            score="N/A",
            risk="❌ Skill not found in dataset",
            details={},
            recommendations=[]
        )

    # -------- ML INPUTS --------
    years = int(request.form.get('years', 3))
    demand = int(request.form.get('demand', 5))
    automation = int(request.form.get('automation', 5))
    trend = int(request.form.get('trend', 5))

    # -------- ML PREDICTION --------
    ml_risk = predict_risk_ml(years, demand, automation, trend)

    # -------- COMBINE RESULTS --------
    risk = f"{rule_risk} (ML Prediction: {ml_risk})"

    # -------- RECOMMENDATIONS --------
    recommendations = []

    # ✅ SAFE CONDITION (FIX)
    if (rule_risk and "High" in rule_risk) or ml_risk == "High":
        recommendations = recommend_skills(skill)

    # -------- FINAL OUTPUT --------
    return render_template(
        'result.html',
        skill=skill,
        score=score,
        risk=risk,
        details=details,
        recommendations=recommendations
    )


@app.route('/compare-result', methods=['POST'])
def compare_result():
    skill1 = request.form['skill1']
    skill2 = request.form['skill2']

    result1 = get_skill_analysis(skill1)
    result2 = get_skill_analysis(skill2)

    return render_template(
        'compare_result.html',
        skill1=result1,
        skill2=result2
    )
@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('q', '').lower()

    from model import data  # access dataset

    # Get matching skills
    matches = data[data["skill_lower"].str.contains(query, na=False)]

    # Unique skill names
    suggestions = matches["skill"].unique().tolist()

    return jsonify(suggestions[:5])  # limit to 5 suggestions

# ---------------- RUN SERVER ----------------

if __name__ == '__main__':
    app.run(debug=True)
