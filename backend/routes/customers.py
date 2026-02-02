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


@router.get("/risk-queue")
def get_risk_queue(
    company_id: str = Depends(verify_api_key)
):
    from risk_queue import build_risk_queue
    queue = build_risk_queue()

    return {
        "company_id": company_id,
        "queue": queue[:50]  # top 50 only
    }


@router.get("/shap/{customer_id}")
def shap_explanation(
    customer_id: str,
    company_id: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT
            feature,
            shap_value
        FROM churn_shap_explanations
        WHERE company_id = :company_id
          AND customer_id = :customer_id
        ORDER BY ABS(shap_value) DESC
        LIMIT 5;
    """)

    rows = db.execute(query, {
        "company_id": company_id,
        "customer_id": customer_id
    }).fetchall()

    return {
        "customer_id": customer_id,
        "shap_explanations": [
            {
                "feature": r.feature,
                "impact": round(float(r.shap_value), 4),
                "direction": "increases churn" if r.shap_value > 0 else "reduces churn"
            }
            for r in rows
        ]
    }


@router.get("/playbooks/{customer_id}")
def get_playbooks(
    customer_id: str,
    company_id: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    # Get risk
    risk_row = db.execute(text("""
        SELECT churn_risk
        FROM churn_predictions
        WHERE company_id = :company_id
          AND customer_id = :customer_id
        ORDER BY prediction_date DESC
        LIMIT 1;
    """), {"company_id": company_id, "customer_id": customer_id}).fetchone()

    # Get SHAP
    shap_rows = db.execute(text("""
        SELECT feature, shap_value
        FROM churn_shap_explanations
        WHERE company_id = :company_id
          AND customer_id = :customer_id
        ORDER BY ABS(shap_value) DESC
        LIMIT 5;
    """), {"company_id": company_id, "customer_id": customer_id}).fetchall()

    shap_explanations = [
        {
            "feature": r.feature,
            "impact": float(r.shap_value),
            "direction": "increases churn" if r.shap_value > 0 else "reduces churn"
        }
        for r in shap_rows
    ]

    from playbooks.engine import generate_playbook

    playbooks = generate_playbook(
        customer_risk=risk_row.churn_risk,
        shap_explanations=shap_explanations
    )

    return {
        "customer_id": customer_id,
        "risk": risk_row.churn_risk,
        "playbooks": playbooks
    }


@router.get("/agent/logs")
def agent_logs(
    company_id: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    rows = db.execute(text("""
        SELECT
            customer_id,
            action,
            execution_mode,
            urgency,
            status,
            executed_at
        FROM retention_agent_logs
        WHERE company_id = :company_id
        ORDER BY executed_at DESC
        LIMIT 50;
    """), {"company_id": company_id}).fetchall()

    return {
        "logs": [
            {
                "customer_id": r.customer_id,
                "action": r.action,
                "execution_mode": r.execution_mode,
                "urgency": r.urgency,
                "status": r.status,
                "executed_at": r.executed_at.isoformat()
            }
            for r in rows
        ]
    }
