# src/action_engine.py

from src.playbooks import PLAYBOOKS


def next_best_action(customer):
    """
    Determines the best action based on customer risk and context.
    Returns a list of action objects attached to Playbooks.
    """

    actions = []

    # -----------------------------
    # Safe extraction
    # -----------------------------
    risk_level = customer.get("risk_level", "Low Risk")
    is_trial = customer.get("is_trial", 0) == 1
    top_reasons = customer.get("top_reasons", [])
    seats = customer.get("seats", 0)

    # Normalize reasons for structured checks
    reasons_text = " ".join(top_reasons).lower()

    # -----------------------------
    # HIGH RISK (CRITICAL)
    # -----------------------------
    if risk_level == "High Risk":
        if is_trial:
            pb = PLAYBOOKS.get("early_trial_risk")
            if pb:
                actions.append({
                    "action": "Trial Rescue Protocol",
                    "priority": "Urgent",
                    "why": "High churn risk detected during trial phase",
                    "playbook_key": "early_trial_risk",
                    "playbook": pb
                })
        else:
            pb = PLAYBOOKS.get("high_risk_paid")
            if pb:
                actions.append({
                    "action": "Assign Customer Success Manager",
                    "priority": "Urgent",
                    "why": "High churn risk detected in paid account",
                    "playbook_key": "high_risk_paid",
                    "playbook": pb
                })

    # -----------------------------
    # MEDIUM RISK (PREVENTATIVE)
    # -----------------------------
    elif risk_level == "Medium Risk":
        # Seat underutilization logic
        if "seats" in reasons_text or seats > 10:
            pb = PLAYBOOKS.get("medium_risk_seats")
            if pb:
                actions.append({
                    "action": "Seat Utilization Audit",
                    "priority": "High",
                    "why": "Customer is paying for unused seats (cost-driven churn risk)",
                    "playbook_key": "medium_risk_seats",
                    "playbook": pb
                })
        else:
            pb = PLAYBOOKS.get("medium_risk_adoption")
            if pb:
                actions.append({
                    "action": "Send Engagement Nudge",
                    "priority": "High",
                    "why": "Risk trending upward – low feature adoption detected",
                    "playbook_key": "medium_risk_adoption",
                    "playbook": pb
                })

    # -----------------------------
    # LOW RISK (OPPORTUNITY)
    # -----------------------------
    else:
        pb = PLAYBOOKS.get("low_risk_upsell")
        if pb:
            actions.append({
                "action": "Propose Annual Contract",
                "priority": "Low",
                "why": "Customer healthy and suitable for expansion",
                "playbook_key": "low_risk_upsell",
                "playbook": pb
            })

    return actions
