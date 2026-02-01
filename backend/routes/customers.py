from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal
from auth import verify_api_key

router = APIRouter(prefix="/customers", tags=["Customers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/risk")
def get_customer_risk(
    company_id: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT
            customer_id,
            churn_probability,
            churn_risk
        FROM churn_predictions
        WHERE company_id = :company_id
          AND prediction_date = (
              SELECT MAX(prediction_date)
              FROM churn_predictions
              WHERE company_id = :company_id
          )
        ORDER BY churn_probability DESC;
    """)

    rows = db.execute(query, {"company_id": company_id}).fetchall()

    summary = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    customers = []

    for r in rows:
        summary[r.churn_risk] += 1
        customers.append({
            "customer_id": r.customer_id,
            "churn_probability": round(float(r.churn_probability), 3),
            "churn_risk": r.churn_risk
        })

    return {
        "company_id": company_id,
        "summary": summary,
        "customers": customers
    }


@router.get("/explain/{customer_id}")
def explain_customer(
    customer_id: str,
    company_id: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT
            events_7d,
            events_14d,
            active_days_7d,
            days_since_last_event,
            value_events_14d
        FROM customer_features_daily
        WHERE company_id = :company_id
          AND customer_id = :customer_id
          AND feature_date = (
              SELECT MAX(feature_date)
              FROM customer_features_daily
          );
    """)

    row = db.execute(query, {
        "company_id": company_id,
        "customer_id": customer_id
    }).fetchone()

    if not row:
        return {"customer_id": customer_id, "reasons": []}

    reasons = []
    from explanation_rules import EXPLANATION_RULES

    for feature, rule in EXPLANATION_RULES.items():
        if rule["condition"](getattr(row, feature)):
            reasons.append(rule["message"])

    return {
        "customer_id": customer_id,
        "reasons": reasons
    }



@router.get("/intelligence/{customer_id}")
def customer_intelligence(
    customer_id: str,
    company_id: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT
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
        WHERE cf.company_id = :company_id
          AND cf.customer_id = :customer_id
          AND cf.feature_date = (
              SELECT MAX(feature_date)
              FROM customer_features_daily
          )
          AND cp.prediction_date = (
              SELECT MAX(prediction_date)
              FROM churn_predictions
          );
    """)

    row = db.execute(query, {
        "company_id": company_id,
        "customer_id": customer_id
    }).fetchone()

    if not row:
        return {"customer_id": customer_id}

    from explanation_rules import EXPLANATION_RULES
    from playbook_rules import PLAYBOOK_RULES

    reasons = []
    for feature, rule in EXPLANATION_RULES.items():
        if rule["condition"](getattr(row, feature)):
            reasons.append(rule["message"])

    actions = []
    for reason in reasons:
        actions.extend(PLAYBOOK_RULES.get(reason, []))

    actions = list(dict.fromkeys(actions))

    return {
        "customer_id": customer_id,
        "churn_probability": round(float(row.churn_probability), 3),
        "churn_risk": row.churn_risk,
        "reasons": reasons,
        "recommended_actions": actions
    }
