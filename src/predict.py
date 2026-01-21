import joblib
import pandas as pd

MODEL_PATH = "models/churn_model.pkl"
THRESHOLD_PATH = "models/threshold.txt"

model = joblib.load(MODEL_PATH)

with open(THRESHOLD_PATH, "r") as f:
    THRESHOLD = float(f.read())


def risk_bucket(prob):
    if prob >= 0.7:
        return "High Risk"
    elif prob >= 0.4:
        return "Medium Risk"
    else:
        return "Low Risk"


def predict_churn(input_data: dict):
    df = pd.DataFrame([input_data])
    prob = model.predict_proba(df)[0][1]

    return {
        "churn_probability": round(prob, 3),
        "risk_level": risk_bucket(prob),
        "will_churn": int(prob >= THRESHOLD)
    }
