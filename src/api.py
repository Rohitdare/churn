from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import joblib

from .predict import predict_churn

app = FastAPI(title="SaaS Churn Prediction API")

# -------- LOAD MODEL & DATA ONCE --------
model = joblib.load("models/churn_model.pkl")

background = pd.read_csv("data/processed/account_features.csv")
background_X = background.drop(columns=["account_id", "churn_flag"]).astype(float)

# -------- SCHEMA --------
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

# -------- ENDPOINTS --------
@app.post("/predict")
def predict(account: AccountFeatures):
    return predict_churn(account.dict())

@app.post("/predict/batch")
def predict_batch(accounts: List[AccountFeatures]):
    return [predict_churn(acc.dict()) for acc in accounts]

@app.get("/metrics")
def metrics():
    probs = model.predict_proba(background_X)[:, 1]

    df = background_X.copy()
    df["churn_probability"] = probs
    df["risk"] = df["churn_probability"].apply(
        lambda x: "High" if x >= 0.7 else "Medium" if x >= 0.4 else "Low"
    )

    return {
        "avg_churn_probability": float(df["churn_probability"].mean()),
        "high_risk_customers": int((df["risk"] == "High").sum()),
        "medium_risk_customers": int((df["risk"] == "Medium").sum()),
        "low_risk_customers": int((df["risk"] == "Low").sum())
    }

@app.get("/health")
def health():
    return {"status": "ok"}
