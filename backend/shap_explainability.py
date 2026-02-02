import shap
import joblib
import pandas as pd
from sqlalchemy import text
from database import engine

MODEL_PATH = "../models/churn_model.pkl"

FEATURE_COLUMNS = [
    "events_7d",
    "events_14d",
    "active_days_7d",
    "days_since_last_event",
    "value_events_14d"
]

# 1️⃣ Load model
model = joblib.load(MODEL_PATH)

# 2️⃣ Load latest features
QUERY = """
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

df = pd.read_sql(QUERY, engine)
X = df[FEATURE_COLUMNS]

# 3️⃣ Build SHAP explainer
explainer = shap.LinearExplainer(model, X, feature_perturbation="interventional")
shap_values = explainer.shap_values(X)

# 4️⃣ Convert to long format
records = []

for i, row in df.iterrows():
    for j, feature in enumerate(FEATURE_COLUMNS):
        records.append({
            "company_id": row.company_id,
            "customer_id": row.customer_id,
            "feature": feature,
            "shap_value": float(shap_values[i][j])
        })

shap_df = pd.DataFrame(records)

# 5️⃣ Store in DB
shap_df.to_sql(
    "churn_shap_explanations",
    engine,
    if_exists="replace",
    index=False
)

print("✅ SHAP explanations generated and stored")
