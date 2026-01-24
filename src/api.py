from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import joblib
import shap  # <--- NEW: Import SHAP

from .predict import predict_churn

app = FastAPI(title="SaaS Churn Prediction API")

# -------- LOAD MODEL & DATA ONCE --------
model = joblib.load("models/churn_model.pkl")

background = pd.read_csv("data/processed/account_features.csv")
background_X = background.drop(columns=["account_id", "churn_flag"]).astype(float)

# -------- INITIALIZE SHAP EXPLAINER --------
# <--- NEW: Define explainer so the risk endpoint doesn't crash
# We use a generic Explainer which auto-selects the best method (Tree, Linear, etc.)
explainer = shap.Explainer(model, background_X) 

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

@app.get("/customers/risk")
def customer_risk_queue():
    df = background.copy()

    X = df.drop(columns=["account_id", "churn_flag"]).astype(float)
    probs = model.predict_proba(X)[:, 1]

    df["churn_probability"] = probs
    df["risk_level"] = df["churn_probability"].apply(
        lambda x: "High Risk" if x >= 0.7 else "Medium Risk" if x >= 0.4 else "Low Risk"
    )

    # SHAP explanations
    # This now works because 'explainer' is defined at the top
    shap_values = explainer(X)

    def top_reasons(idx):
        # Handle SHAP values structure (checking if it returns object or array)
        if hasattr(shap_values, 'values'):
            impacts = shap_values.values[idx]
        else:
            impacts = shap_values[idx]
            
        features = X.columns
        top_idx = impacts.argsort()[::-1][:3]
        return [features[i] for i in top_idx]

    df["top_reasons"] = [
        top_reasons(i) for i in range(len(df))
    ]

    return df[[
        "account_id",
        "churn_probability",
        "risk_level",
        "is_trial",
        "account_age_days",
        "top_reasons"
    ]].sort_values(by="churn_probability", ascending=False).to_dict(orient="records")