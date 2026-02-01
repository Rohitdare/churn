import random
import threading
from company_config import COMPANIES
from personas import PERSONAS
from event_weights import EVENT_WEIGHTS
from event_builder import build_event
from send_event import send_event
from lifecycle import LIFECYCLE_STAGES

print("COMPANIES CONFIG LOADED:", [c['company_id'] for c in COMPANIES])

def simulate_company(company):
    """Function to run simulation for a single company in its own thread."""
    print(f"🚀 [START] {company['company_id']} ({company['churn_profile']} churn profile)")

    # Initialize state for this company's customers
    customers = {
        f"{company['company_id']}_c{c}": {
            "stage": "trial",
            "days_active": 0,
            "churned": False,
            "persona": random.choice(list(PERSONAS.keys()))
        } for c in range(company["customers"])
    }

    for day in range(company["simulation_days"]):
        # Log progress every 5 days
        if day % 5 == 0:
            print(f"📊 {company['company_id']} - Progress: Day {day}/{company['simulation_days']}")

        for cust_id, state in customers.items():
            if state["churned"]:
                continue

            # 1. Update Lifecycle State
            state["days_active"] += 1
            for stage, cfg in LIFECYCLE_STAGES.items():
                if cfg["days"][0] <= state["days_active"] <= cfg["days"][1]:
                    state["stage"] = stage

            # 2. Process Churn Logic
            current_stage = state["stage"]
            base_risk = LIFECYCLE_STAGES[current_stage]["churn_risk"]
            mod = 1.5 if company["churn_profile"] == "high" else 0.7

            if random.random() < (base_risk * mod):
                state["churned"] = True
                state["stage"] = "churned"
                
                try:
                    event = build_event(company["company_id"], cust_id, f"{cust_id}_u1", "cancel_subscription")
                    send_event(event, company["api_key"], company["base_url"])
                except Exception as e:
                    print(f"⚠️ {company['company_id']} failed to send churn event: {e}")
                continue

            # 3. Generate Daily Events
            persona_range = PERSONAS[state["persona"]]["daily_event_range"]
            multiplier = LIFECYCLE_STAGES[current_stage]["event_multiplier"]
            event_count = max(0, int(random.randint(*persona_range) * multiplier))

            # Feature Drop-off Logic
            available_events = list(EVENT_WEIGHTS.keys())
            if current_stage == "stagnant":
                available_events = [e for e in available_events if e not in ["export_report", "invite_user"]]

            for _ in range(event_count):
                event_name = random.choice(available_events)
                try:
                    event = build_event(company["company_id"], cust_id, f"{cust_id}_u1", event_name)
                    send_event(event, company["api_key"], company["base_url"])
                except Exception:
                    pass # Keep moving if an individual POST fails

    print(f"🏁 [FINISH] {company['company_id']} simulation complete.")

def run():
    threads = []

    # Step 3 — Run companies in parallel
    for company in COMPANIES:
        t = threading.Thread(target=simulate_company, args=(company,))
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()

    print("\n✅ All company simulations completed.")

if __name__ == "__main__":
    run()