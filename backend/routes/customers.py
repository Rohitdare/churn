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
