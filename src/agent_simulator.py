# src/agent_simulator.py

from datetime import datetime
from src.action_engine import next_best_action

# ----------------------------------
# CONFIG (Agent Constraints)
# ----------------------------------
MAX_URGENT_ACTIONS = 5   # Simulated daily capacity


def simulate_daily_action_plan(customers):
    """
    Simulates an AI Retention Agent planning actions for the day.
    NO real actions are executed.
    """

    priority_actions = []
    bulk_actions = []
    deferred_customers = []

    # Sort customers by churn probability (descending)
    customers = sorted(
        customers,
        key=lambda x: x.get("churn_probability", 0),
        reverse=True
    )

    for cust in customers:
        if len(priority_actions) >= MAX_URGENT_ACTIONS:
            deferred_customers.append(cust["account_id"])
            continue

        actions = next_best_action(cust)

        for action in actions:
            playbook = action.get("playbook")

            # Skip no-op actions
            if not playbook:
                continue

            # ----------------------------
            # PRIORITY ACTIONS
            # ----------------------------
            if action["priority"] == "Urgent":
                priority_actions.append({
                    "account_id": cust["account_id"],
                    "churn_probability": cust.get("churn_probability", 0),
                    "recommended_action": action["action"],
                    "owner": playbook["owner"],
                    "playbook": playbook["name"],
                    "why": action["why"],
                    "timestamp": datetime.now().isoformat()
                })

            # ----------------------------
            # BULK ACTIONS
            # ----------------------------
            elif action["priority"] == "High":
                bulk_actions.append({
                    "action": action["action"],
                    "playbook": playbook["name"],
                    "channel": "Email / In-App",
                })

    # Aggregate bulk actions
    bulk_summary = {}
    for b in bulk_actions:
        key = (b["action"], b["playbook"])
        bulk_summary[key] = bulk_summary.get(key, 0) + 1

    bulk_actions_final = [
        {
            "action": k[0],
            "playbook": k[1],
            "customer_count": v
        }
        for k, v in bulk_summary.items()
    ]

    return {
        "summary": {
            "urgent_customers": len(priority_actions),
            "bulk_customers": sum(b["customer_count"] for b in bulk_actions_final),
            "deferred_customers": len(deferred_customers)
        },
        "priority_actions": priority_actions,
        "bulk_actions": bulk_actions_final,
        "deferred_accounts": deferred_customers
    }
