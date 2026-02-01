import joblib
import pandas as pd
from datetime import date
from sqlalchemy import text
from database import engine

MODEL_PATH = "../models/churn_model.pkl"

FEATURE_QUERY = """
SELECT
    company_id,
    customer_id,
    events_7d,
    events_14d,
    active_days_7d,
    days_since_last_event,
    value_events_14d
FROM customer_features_daily
WHERE feature_date = (
    SELECT MAX(feature_date)
    FROM customer_features_daily
);
"""

INSERT_SQL = text("""
INSERT INTO churn_predictions (
    company_id,
    customer_id,
    prediction_date,
    churn_probability,
    churn_risk
)
VALUES (
    :company_id,
    :customer_id,
    :prediction_date,
    :churn_probability,
    :churn_risk
)
ON CONFLICT (company_id, customer_id, prediction_date)
DO UPDATE SET
    churn_probability = EXCLUDED.churn_probability,
    churn_risk = EXCLUDED.churn_risk,
    created_at = CURRENT_TIMESTAMP;
""")

def risk_bucket(prob):
    if prob >= 0.75:
        return "HIGH"
    elif prob >= 0.4:
        return "MEDIUM"
    else:
        return "LOW"

def run_churn_inference():
    print("🚀 Running churn inference...")

    model = joblib.load(MODEL_PATH)

    df = pd.read_sql(FEATURE_QUERY, engine)

    feature_cols = [
        "events_7d",
        "events_14d",
        "active_days_7d",
        "days_since_last_event",
        "value_events_14d"
    ]

    X = df[feature_cols]
    probs = model.predict_proba(X)[:, 1]

    today = date.today()

    with engine.begin() as conn:
        for i, row in df.iterrows():
            prob = float(probs[i])
            conn.execute(
                INSERT_SQL,
                {
                    "company_id": row["company_id"],
                    "customer_id": row["customer_id"],
                    "prediction_date": today,
                    "churn_probability": prob,
                    "churn_risk": risk_bucket(prob)
                }
            )

    print("✅ Churn inference completed")

if __name__ == "__main__":
    run_churn_inference()
