import pandas as pd
from sqlalchemy import text
from database import engine
from explanation_rules import EXPLANATION_RULES

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

def generate_explanations():
    print("🧠 Generating churn explanations...")

    df = pd.read_sql(QUERY, engine)
    explanations = {}

    for _, row in df.iterrows():
        reasons = []

        for feature, rule in EXPLANATION_RULES.items():
            if rule["condition"](row[feature]):
                reasons.append(rule["message"])

        explanations[(row.company_id, row.customer_id)] = reasons

    print("✅ Explanations generated")
    return explanations

if __name__ == "__main__":
    exps = generate_explanations()
    for k, v in list(exps.items())[:5]:
        print(k, "→", v)
