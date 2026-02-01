import joblib
import pandas as pd

MODEL_PATH = "../models/churn_model.pkl"

FEATURE_NAMES = [
    "events_7d",
    "events_14d",
    "active_days_7d",
    "days_since_last_event",
    "value_events_14d"
]

model = joblib.load(MODEL_PATH)

coefs = pd.DataFrame({
    "feature": FEATURE_NAMES,
    "coefficient": model.coef_[0]
}).sort_values(by="coefficient", ascending=False)

print(coefs)
