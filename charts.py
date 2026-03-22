import matplotlib
matplotlib.use("Agg")  # Required for Flask (no GUI)

import os
import pandas as pd
import matplotlib.pyplot as plt

# ------------------ CONSTANTS ------------------

DATASET_PATH = "dataset.csv"
CHART_DIR = os.path.join("static", "charts")

os.makedirs(CHART_DIR, exist_ok=True)

# ------------------ HELPER: LOAD DATA SAFELY ------------------

def load_dataset():
    return pd.read_csv(DATASET_PATH)

def add_obsolete_column(df):
    """
    Create 'obsolete' column safely.
    Rule:
    If risk_level == 'High' -> obsolete = 1
    Else -> obsolete = 0
    """
    if "risk_level" in df.columns:
        df["obsolete"] = df["risk_level"].apply(
            lambda x: 1 if str(x).strip().lower() == "high" else 0
        )
    else:
        df["obsolete"] = 0  # fallback
    return df

# ------------------ CHART 1: OBSOLESCENCE DISTRIBUTION ------------------

def generate_obsolescence_distribution():
    df = load_dataset()
    df = add_obsolete_column(df)

    counts = df["obsolete"].value_counts()

    plt.figure(figsize=(8, 5))
    bars = plt.bar(counts.index.astype(str), counts.values)

    for bar in bars:
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            int(bar.get_height()),
            ha="center",
            va="bottom"
        )

    plt.title("Skill Obsolescence Distribution")
    plt.xlabel("Obsolete (1 = Yes, 0 = No)")
    plt.ylabel("Number of Skills")
    plt.tight_layout()

    path = os.path.join(CHART_DIR, "obsolescence_distribution.png")
    plt.savefig(path)
    plt.close()

    return "charts/obsolescence_distribution.png"

# ------------------ CHART 2: SKILL DEMAND TREND ------------------

def generate_skill_demand_trend():
    years = ["2019", "2020", "2021", "2022", "2023"]
    demand = [4.2, 4.8, 5.5, 6.1, 6.9]

    plt.figure(figsize=(8, 5))
    plt.plot(years, demand, marker="o")
    plt.xlabel("Year")
    plt.ylabel("Demand Level")
    plt.title("Skill Demand Trend")

    path = os.path.join(CHART_DIR, "skill_demand_trend.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()

    return "charts/skill_demand_trend.png"

# ------------------ CHART 3: AVERAGE DISTRIBUTION (SAFE) ------------------

def generate_average_distribution():
    df = load_dataset()

    averages = {}

    if "demand" in df.columns:
        averages["Demand"] = df["demand"].mean()

    if "automation" in df.columns:
        averages["Automation"] = df["automation"].mean()

    if "learning" in df.columns:
        averages["Learning"] = df["learning"].mean()

    if not averages:
        return None  # no valid columns → no crash

    plt.figure(figsize=(8, 5))
    bars = plt.bar(averages.keys(), averages.values())

    for bar in bars:
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            round(bar.get_height(), 2),
            ha="center",
            va="bottom"
        )

    plt.title("Average Distribution of Skill Factors")
    plt.xlabel("Factors")
    plt.ylabel("Average Score")
    plt.tight_layout()

    path = os.path.join(CHART_DIR, "average_distribution.png")
    plt.savefig(path)
    plt.close()

    return "charts/average_distribution.png"

# ------------------ CHART 4: RISK LEVEL DISTRIBUTION ------------------

def generate_risk_level_distribution():
    df = load_dataset()
    df = add_obsolete_column(df)

    counts = df["obsolete"].value_counts()

    plt.figure(figsize=(8, 5))
    bars = plt.bar(counts.index.astype(str), counts.values)

    for bar in bars:
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            int(bar.get_height()),
            ha="center",
            va="bottom"
        )

    plt.title("Risk Level Distribution")
    plt.xlabel("Obsolete (1 = High Risk)")
    plt.ylabel("Number of Skills")
    plt.tight_layout()

    path = os.path.join(CHART_DIR, "risk_level_distribution.png")
    plt.savefig(path)
    plt.close()

    return "charts/risk_level_distribution.png"

# ------------------ SUMMARY COUNTS ------------------

def get_risk_summary_counts():
    df = load_dataset()
    df = add_obsolete_column(df)

    low = len(df[df["obsolete"] == 0])
    medium = 0
    high = len(df[df["obsolete"] == 1])

    return low, medium, high

# ------------------ ML RISK DISTRIBUTION ------------------

def generate_ml_risk_distribution():
    df = pd.read_csv(DATASET_PATH)

    if "risk_level" not in df.columns:
        return None

    counts = df["risk_level"].value_counts()

    plt.figure(figsize=(8, 5))
    counts.plot(kind="bar")
    plt.title("ML Risk Level Distribution")
    plt.xlabel("Risk Level")
    plt.ylabel("Number of Skills")

    path = os.path.join(CHART_DIR, "ml_risk_distribution.png")
    plt.savefig(path)
    plt.close()

    return "charts/ml_risk_distribution.png"

