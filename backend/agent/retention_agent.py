from sqlalchemy import text
from database import engine
from agent.policy import decide_execution
from playbooks.engine import generate_playbook

def run_agent(company_id, limit=20):
    print(f"🤖 Running Retention Agent for {company_id}")

    # 1️⃣ Fixed Indentation and Use 2.0 Connection
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT customer_id, churn_probability, churn_risk 
            FROM churn_predictions 
            WHERE company_id = :cid
            LIMIT :limit
        """), {"cid": company_id, "limit": limit})
        
        # Use mappings() to avoid 'AttributeError' on rows
        risk_rows = result.mappings().all()

        for r in risk_rows:
            # 2️⃣ Fetch SHAP explanations (using the active connection 'conn')
            shap_result = conn.execute(text("""
                SELECT feature, shap_value
                FROM churn_shap_explanations
                WHERE company_id = :company_id
                  AND customer_id = :customer_id
                ORDER BY ABS(shap_value) DESC
                LIMIT 5;
            """), {
                "company_id": company_id,
                "customer_id": r["customer_id"] # Fixed: dictionary access
            })
            
            shap_rows = shap_result.mappings().all()

            shap_explanations = [
                {
                    "feature": s["feature"],
                    "impact": float(s["shap_value"]),
                    "direction": "increases churn" if s["shap_value"] > 0 else "reduces churn"
                }
                for s in shap_rows
            ]

            # 3️⃣ Generate playbooks
            playbooks = generate_playbook(
                customer_risk=r["churn_risk"], # Fixed: dictionary access
                shap_explanations=shap_explanations
            )

            # 4️⃣ Decide & execute
            for pb in playbooks:
                decision = decide_execution(pb, r["churn_risk"])
                status = "EXECUTED" if decision == "EXECUTE_NOW" else "QUEUED"

                # Use 'conn' for the INSERT as well
                conn.execute(text("""
                    INSERT INTO retention_agent_logs (
                        company_id, customer_id, action, execution_mode, 
                        urgency, confidence, status
                    )
                    VALUES (
                        :company_id, :customer_id, :action, :execution_mode, 
                        :urgency, :confidence, :status
                    );
                """), {
                    "company_id": company_id,
                    "customer_id": r["customer_id"],
                    "action": pb["action"],
                    "execution_mode": pb["execution"],
                    "urgency": pb["urgency"],
                    "confidence": pb["confidence"],
                    "status": status
                })
        
        # Fixed: Explicitly commit the changes to the DB
        conn.commit() 

    print("✅ Retention Agent run completed")