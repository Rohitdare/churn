import pandas as pd
import joblib
from sqlalchemy import create_engine
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from database import engine

MODEL_OUT = "../models/churn_model.pkl"

QUERY = """
SELECT
    events_7d,
    events_14d,
    active_days_7d,
    days_since_last_event,
    value_events_14d,
    churned::int AS churned
FROM customer_features_daily;
"""

def retrain():
    print("🚀 Retraining churn model from feature store...")

    df = pd.read_sql(QUERY, engine)

    X = df.drop(columns=["churned"])
    y = df["churned"]

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    joblib.dump(model, MODEL_OUT)
    print("✅ Model retrained and saved")

if __name__ == "__main__":
    retrain()
