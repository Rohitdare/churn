from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import joblib
import shap
from datetime import datetime, timedelta
import numpy as np

# Import the new logic engine
from src.action_engine import next_best_action

from .predict import predict_churn

app = FastAPI(title="SaaS Churn Prediction API")

# -------- LOAD MODEL & DATA --------
model = joblib.load("models/churn_model.pkl")
background = pd.read_csv("data/processed/account_features.csv")
background_X = background.drop(columns=["account_id", "churn_flag"]).astype(float)
explainer = shap.Explainer(model, background_X) 

# -------- HELPER FUNCTIONS --------
def generate_risk_history(current_prob):
    history = []
    prob = current_prob
    for i in range(30):
        noise = np.random.normal(0, 0.05)
        prev_prob = max(0.0, min(1.0, prob + noise))
        history.append({"days_ago": i, "churn_probability": prob})
        prob = prev_prob
    return history

def get_risk_trend(history):
    if not history: return "Stable"
    # Compare latest (index 0 in generated list is 'today' if reversed, but our logic appended backwards)
    # Actually, history[0] is 'today' (days_ago=0) in the generation loop.
    # Wait, the generation loop appends 0 days ago first.
    # So history[0] is today, history[-1] is 30 days ago.
    
    delta = history[0]["churn_probability"] - history[-1]["churn_probability"]

    if delta > 0.15: return "Rapidly Increasing"
    elif delta > 0.05: return "Increasing"
    elif delta < -0.05: return "Decreasing"
    else: return "Stable"

# -------- ENDPOINTS --------
@app.get("/customers/risk")
def customer_risk_queue():
    df = background.copy()
    X = df.drop(columns=["account_id", "churn_flag"]).astype(float)
    probs = model.predict_proba(X)[:, 1]
    df["churn_probability"] = probs
    df["risk_level"] = df["churn_probability"].apply(lambda x: "High Risk" if x >= 0.7 else "Medium Risk" if x >= 0.4 else "Low Risk")
    
    shap_values = explainer(X)
    
    # Extract top reasons for everyone
    def top_reasons(idx):
        if hasattr(shap_values, 'values'): impacts = shap_values.values[idx]
        else: impacts = shap_values[idx]
        top_idx = impacts.argsort()[::-1][:3]
        return [X.columns[i] for i in top_idx]

    df["top_reasons"] = [top_reasons(i) for i in range(len(df))]

    return df[[
        "account_id", "churn_probability", "risk_level", "is_trial", 
        "account_age_days", "top_reasons", "plan_tier_Enterprise", "plan_tier_Pro"
    ]].sort_values(by="churn_probability", ascending=False).to_dict(orient="records")

@app.get("/customers/{account_id}/risk-history")
def customer_risk_history(account_id: str):
    df = background.copy()
    row = df[df["account_id"] == account_id]
    if row.empty: return {"error": "Customer not found"}

    X = row.drop(columns=["account_id", "churn_flag"]).astype(float)
    current_prob = model.predict_proba(X)[0][1]
    
    history_objs = generate_risk_history(current_prob)
    
    # Format for chart
    today = datetime.today()
    timeline = []
    for h in history_objs:
        date_str = (today - timedelta(days=h["days_ago"])).strftime("%Y-%m-%d")
        timeline.append({"date": date_str, "churn_probability": h["churn_probability"]})
    
    return {"account_id": account_id, "risk_history": sorted(timeline, key=lambda x: x["date"])}

@app.get("/customers/{account_id}/next-actions")
def customer_next_actions(account_id: str):
    # 1. Re-calculate customer state (In a real app, you'd fetch from DB)
    df = background.copy()
    row = df[df["account_id"] == account_id]
    if row.empty: return {"error": "Customer not found"}
    
    X = row.drop(columns=["account_id", "churn_flag"]).astype(float)
    
    # Risk
    prob = model.predict_proba(X)[0][1]
    risk_level = "High Risk" if prob >= 0.7 else "Medium Risk" if prob >= 0.4 else "Low Risk"
    
    # Trend
    history_objs = generate_risk_history(prob)
    trend = get_risk_trend(history_objs)
    
    # Reasons
    shap_val = explainer(X)
    if hasattr(shap_val, 'values'): impacts = shap_val.values[0]
    else: impacts = shap_val[0]
    top_cols = [X.columns[i] for i in impacts.argsort()[::-1][:3]]

    # Build State Object
    customer_state = {
        "account_id": account_id,
        "risk_level": risk_level,
        "risk_trend": trend,
        "top_reasons": top_cols,
        # Add other fields if logic needs them
        "seats": row.iloc[0]["seats"]
    }

    # 2. Get Actions
    actions = next_best_action(customer_state)

    return {
        "account_id": account_id,
        "risk_level": risk_level,
        "risk_trend": trend,
        "recommended_actions": actions
    }

@app.get("/metrics")
def metrics():
    # (Keep your existing metrics code here)
    probs = model.predict_proba(background_X)[:, 1]
    df = background_X.copy()
    df["churn_probability"] = probs
    df["risk"] = df["churn_probability"].apply(lambda x: "High" if x >= 0.7 else "Medium" if x >= 0.4 else "Low")
    return {
        "avg_churn_probability": float(df["churn_probability"].mean()),
        "high_risk_customers": int((df["risk"] == "High").sum()),
        "medium_risk_customers": int((df["risk"] == "Medium").sum()),
        "low_risk_customers": int((df["risk"] == "Low").sum())
    }