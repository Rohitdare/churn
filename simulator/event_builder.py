from datetime import datetime

def build_event(company_id, customer_id, user_id, event_name):
    return {
        "company_id": company_id,
        "customer_id": customer_id,
        "user_id": user_id,
        "event_name": event_name,
        "properties": {},
        "timestamp": datetime.utcnow().isoformat()
    }
