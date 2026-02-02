from sqlalchemy import text
from database import engine

QUERY = """
SELECT
    customer_id,
    churn_probability,
    churn_risk
FROM churn_predictions
WHERE prediction_date = (
    SELECT MAX(prediction_date)
    FROM churn_predictions
);
"""

RISK_MULTIPLIER = {
    "HIGH": 1.5,
    "MEDIUM": 1.0,
    "LOW": 0.5
}

def build_risk_queue():
    # Fix 1: Use a connection block for SQLAlchemy 2.0
    with engine.connect() as conn:
        result = conn.execute(text(QUERY))
        # Fix 2: Convert rows to dictionaries for easier access
        rows = result.mappings().all()
    
    queue = []

    for r in rows:
        # Now we access via keys which is much more robust
        score = float(r["churn_probability"]) * RISK_MULTIPLIER.get(r["churn_risk"], 1.0)

        queue.append({
            "customer_id": r["customer_id"],
            "churn_probability": float(r["churn_probability"]),
            "risk": r["churn_risk"],
            "priority_score": round(score, 3)
        })

    queue.sort(key=lambda x: x["priority_score"], reverse=True)
    return queue

if __name__ == "__main__":
    q = build_risk_queue()
    for i in q[:5]:
        print(i)