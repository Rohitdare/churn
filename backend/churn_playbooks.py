from sqlalchemy import text
from database import engine
from explanation_rules import EXPLANATION_RULES
from playbook_rules import PLAYBOOK_RULES

QUERY = """
SELECT
    cf.company_id,
    cf.customer_id,
    cf.events_7d,
    cf.events_14d,
    cf.active_days_7d,
    cf.days_since_last_event,
    cf.value_events_14d,
    cp.churn_probability,
    cp.churn_risk
FROM customer_features_daily cf
JOIN churn_predictions cp
  ON cf.company_id = cp.company_id
 AND cf.customer_id = cp.customer_id
WHERE cf.feature_date = (
    SELECT MAX(feature_date)
    FROM customer_features_daily
)
AND cp.prediction_date = (
    SELECT MAX(prediction_date)
    FROM churn_predictions
);
"""

def generate_playbooks():
    # FIX: Use a connection block for SQLAlchemy 2.0 compatibility
    with engine.connect() as conn:
        result = conn.execute(text(QUERY))
        # fetchall() returns a list of Row objects
        rows = result.fetchall()
    
    results = {}

    for r in rows:
        reasons = []

        # Convert row to a dictionary for easier lookup with getattr-like behavior
        # In SQLAlchemy 2.0, rows are mapping-compatible
        row_dict = r._asdict()

        for feature, rule in EXPLANATION_RULES.items():
            # Check if feature exists in our query results
            if feature in row_dict:
                if rule["condition"](row_dict[feature]):
                    reasons.append(rule["message"])

        actions = []
        for reason in reasons:
            actions.extend(PLAYBOOK_RULES.get(reason, []))

        # remove duplicates while preserving order
        actions = list(dict.fromkeys(actions))

        results[(row_dict['company_id'], row_dict['customer_id'])] = {
            "risk": row_dict['churn_risk'],
            "churn_probability": float(row_dict['churn_probability']),
            "reasons": reasons,
            "recommended_actions": actions
        }

    return results

if __name__ == "__main__":
    data = generate_playbooks()
    for k, v in list(data.items())[:3]:
        print(f"Company/Customer: {k}")
        print(f"Data: {v}\n")