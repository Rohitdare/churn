import joblib
import pandas as pd
import shap
import numpy as np


MODEL_PATH = "models/churn_model.pkl"
THRESHOLD_PATH = "models/threshold.txt"

model = joblib.load(MODEL_PATH)

# Load explainer with background data
background = pd.read_csv("data/processed/account_features.csv")
background_X = background.drop(columns=["account_id", "churn_flag"]).astype(float)

explainer = shap.Explainer(model, background_X)


with open(THRESHOLD_PATH, "r") as f:
    THRESHOLD = float(f.read())


def risk_bucket(prob):
    if prob >= 0.7:
        return "High Risk"
    elif prob >= 0.4:
        return "Medium Risk"
    else:
        return "Low Risk"
    
def explain_with_shap(df_row):
    shap_values = explainer(df_row)
    impacts = shap_values.values[0]

    explanation = (
        pd.DataFrame({
            "feature": df_row.columns,
            "impact": impacts
        })
        .sort_values(by="impact", ascending=False)
        .head(4)
    )

    return explanation["feature"].tolist()


FEATURE_TEXT = {
    "is_trial": "Customer is on a trial plan",
    "account_age_days": "Customer is relatively new",
    "seats": "Customer has a small team size",
    "plan_tier_Enterprise": "Customer is not on Enterprise plan",
    "plan_tier_Pro": "Customer is not on Pro plan",
    "country_US": "Customer is based in the US",
    "country_IN": "Customer is based in India"
}



def predict_churn(input_data: dict):
    df = pd.DataFrame([input_data]).astype(float)

    prob = model.predict_proba(df)[0][1]
    shap_features = explain_with_shap(df)

    reasons = [
        FEATURE_TEXT.get(f, f.replace("_", " "))
        for f in shap_features
        if f in FEATURE_TEXT
    ]

    return {
        "churn_probability": round(prob, 3),
        "risk_level": risk_bucket(prob),
        "will_churn": int(prob >= THRESHOLD),
        "top_reasons": reasons
    }
