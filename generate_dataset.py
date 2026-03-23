import pandas as pd
import random

skills = [
    "Python","Java","C++","C","JavaScript","TypeScript","SQL","NoSQL",
    "React","Angular","Vue","Node.js","Django","Flask","Spring Boot",
    "Machine Learning","Deep Learning","Data Science","AI Engineer",
    "NLP","Computer Vision","TensorFlow","PyTorch",
    "Cloud Computing","AWS","Azure","Google Cloud",
    "Docker","Kubernetes","DevOps","CI/CD",
    "Cybersecurity","Ethical Hacking","Blockchain",
    "Big Data","Hadoop","Spark","Data Engineering",
    "Power BI","Tableau","Excel",
    "Manual Testing","Automation Testing","Selenium",
    "UI/UX Design","Figma","Adobe XD",
    "Mobile Development","Android","iOS","Flutter",
    "Game Development","Unity","Unreal Engine"
]

rows = []

for i in range(300):
    skill = random.choice(skills)
    years = random.randint(1, 12)
    demand = random.randint(1, 10)
    automation = random.randint(1, 10)
    learning = random.randint(1, 10)

    score = automation*0.4 + (10-demand)*0.3 + (10-learning)*0.3

    if score >= 6:
        risk = "High"
    elif score >= 4:
        risk = "Medium"
    else:
        risk = "Low"

    rows.append([skill, years, demand, automation, learning, risk])

df = pd.DataFrame(rows, columns=[
    "skill","years_experience","demand_score",
    "automation_risk","learning_trend","risk_level"
])

# ✅ IMPORTANT: force save
df.to_csv("dataset.csv", index=False)

print("✅ Dataset created successfully!")