from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import joblib
import shap
from datetime import datetime, timedelta
import numpy as np

# --- IMPORTS ---
from src.action_engine import next_best_action
from src.agent_simulator import simulate_daily_action_plan
from .predict import predict_churn

# ==============================
# CONFIG
# ==============================
HIGH_RISK = 0.7
MEDIUM_RISK = 0.4

# ==============================
# APP SETUP
# ==============================
app = FastAPI(title="SaaS Churn Intelligence API")

# ==============================
# LOAD MODEL & DATA
# ==============================
model = joblib.load("models/churn_model.pkl")
background = pd.read_csv("data/processed/account_features.csv")

background_X = background.drop(
    columns=["account_id", "churn_flag"]
).astype(float)

explainer = shap.Explainer(model, background_X)

# ==============================
# HELPER FUNCTIONS
# ==============================
def generate_risk_history(current_prob, days=30):
    history = []
    prob = current_prob

    for i in range(days, 0, -7):
        drift = np.random.uniform(-0.08, 0.08)
        prob = max(0.0, min(1.0, prob - drift))
        history.append({
            "days_ago": i,
            "churn_probability": round(prob, 3)
        })

    history.append({
        "days_ago": 0,
        "churn_probability": round(current_prob, 3)
    })

    return history


def get_risk_trend(history):
    if len(history) < 2:
        return "Stable"

    delta = history[-1]["churn_probability"] - history[0]["churn_probability"]

    if delta > 0.15:
        return "Rapidly Increasing"
    elif delta > 0.05:
        return "Increasing"
    elif delta < -0.05:
        return "Decreasing"
    else:
        return "Stable"


# ==============================
# SCHEMAS
# ==============================
class AccountFeatures(BaseModel):
    seats: int
    is_trial: int
    account_age_days: int

    industry_DevTools: bool
    industry_EdTech: bool
    industry_FinTech: bool
    industry_HealthTech: bool

    country_CA: bool
    country_DE: bool
    country_FR: bool
    country_IN: bool
    country_UK: bool
    country_US: bool

    referral_source_event: bool
    referral_source_organic: bool
    referral_source_other: bool
    referral_source_partner: bool

    plan_tier_Enterprise: bool
    plan_tier_Pro: bool


# ==============================
# HEALTH
# ==============================
@app.get("/health")
def health():
    return {"status": "ok"}


# ==============================
# METRICS
# ==============================
@app.get("/metrics")
def metrics():
    probs = model.predict_proba(background_X)[:, 1]

    df = background_X.copy()
    df["churn_probability"] = probs

    df["risk"] = df["churn_probability"].apply(
        lambda x: "High"
        if x >= HIGH_RISK
        else "Medium"
        if x >= MEDIUM_RISK
        else "Low"
    )

    return {
        "avg_churn_probability": float(df["churn_probability"].mean()),
        "high_risk_customers": int((df["risk"] == "High").sum()),
        "medium_risk_customers": int((df["risk"] == "Medium").sum()),
        "low_risk_customers": int((df["risk"] == "Low").sum())
    }


# ==============================
# CUSTOMER RISK QUEUE
# ==============================
@app.get("/customers/risk")
def customer_risk_queue():
    df = background.copy()
    X = df.drop(columns=["account_id", "churn_flag"]).astype(float)

    probs = model.predict_proba(X)[:, 1]
    df["churn_probability"] = probs

    df["risk_level"] = df["churn_probability"].apply(
        lambda x: "High Risk"
        if x >= HIGH_RISK
        else "Medium Risk"
        if x >= MEDIUM_RISK
        else "Low Risk"
    )

    shap_values = explainer(X)

    def top_reasons(idx):
        impacts = shap_values.values[idx]
        top_idx = impacts.argsort()[::-1][:3]
        return [X.columns[i] for i in top_idx]

    df["top_reasons"] = [top_reasons(i) for i in range(len(df))]

    return df[
        [
            "account_id",
            "churn_probability",
            "risk_level",
            "is_trial",
            "account_age_days",
            "top_reasons",
            "plan_tier_Enterprise",
            "plan_tier_Pro",
            "seats"
        ]
    ].sort_values(
        by="churn_probability",
        ascending=False
    ).to_dict(orient="records")


# ==============================
# CUSTOMER RISK HISTORY
# ==============================
@app.get("/customers/{account_id}/risk-history")
def customer_risk_history(account_id: str):
    row = background[background["account_id"] == account_id]

    if row.empty:
        return {"error": "Customer not found"}

    X = row.drop(columns=["account_id", "churn_flag"]).astype(float)
    current_prob = model.predict_proba(X)[0][1]

    history = generate_risk_history(current_prob)

    today = datetime.today()
    timeline = [
        {
            "date": (today - timedelta(days=h["days_ago"])).strftime("%Y-%m-%d"),
            "churn_probability": h["churn_probability"]
        }
        for h in history
    ]

    return {
        "account_id": account_id,
        "risk_history": sorted(timeline, key=lambda x: x["date"])
    }


# ==============================
# NEXT BEST ACTIONS
# ==============================
@app.get("/customers/{account_id}/next-actions")
def customer_next_actions(account_id: str):
    row = background[background["account_id"] == account_id]

    if row.empty:
        return {"error": "Customer not found"}

    X = row.drop(columns=["account_id", "churn_flag"]).astype(float)
    prob = model.predict_proba(X)[0][1]

    risk_level = (
        "High Risk" if prob >= HIGH_RISK
        else "Medium Risk" if prob >= MEDIUM_RISK
        else "Low Risk"
    )

    history = generate_risk_history(prob)
    trend = get_risk_trend(history)

    shap_val = explainer(X)
    impacts = shap_val.values[0]
    top_reasons = [X.columns[i] for i in impacts.argsort()[::-1][:3]]

    customer_state = {
        "account_id": account_id,
        "risk_level": risk_level,
        "risk_trend": trend,
        "top_reasons": top_reasons,
        "seats": int(row.iloc[0]["seats"]),
        "is_trial": int(row.iloc[0]["is_trial"]),
        "account_age_days": int(row.iloc[0]["account_age_days"]),
        "plan": (
            "Enterprise" if row.iloc[0]["plan_tier_Enterprise"]
            else "Pro" if row.iloc[0]["plan_tier_Pro"]
            else "Basic"
        )
    }

    actions = next_best_action(customer_state)

    return {
        "account_id": account_id,
        "risk_level": risk_level,
        "risk_trend": trend,
        "recommended_actions": actions
    }


# ==============================
# AGENT DAILY PLAN (SIMULATION)
# ==============================
@app.get("/agent/daily-plan")
def agent_daily_plan():
    customers = customer_risk_queue()
    plan = simulate_daily_action_plan(customers)

    return {
        "agent": "AI Retention Agent",
        "plan": plan,
        "note": "This is a simulated daily plan. No actions were executed."
    }


# ==============================
# PREDICTION (SINGLE ACCOUNT)
# ==============================
@app.post("/predict")
def predict(account: AccountFeatures):
    return predict_churn(account.dict())
