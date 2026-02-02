#from catalog import PLAYBOOK_CATALOG
from playbooks.mappings import SHAP_TO_PLAYBOOK
from playbooks.catalog import PLAYBOOK_CATALOG

RISK_PRIORITY = {
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1
}

def generate_playbook(customer_risk, shap_explanations):
    """
    shap_explanations: list of {feature, impact, direction}
    """

    action_scores = {}

    for shap in shap_explanations:
        feature = shap["feature"]
        direction = shap["direction"]

        # Only act on churn-increasing signals
        if direction != "increases churn":
            continue

        actions = SHAP_TO_PLAYBOOK.get(feature, [])

        for action in actions:
            action_scores[action] = action_scores.get(action, 0) + abs(shap["impact"])

    # Rank actions
    ranked_actions = sorted(
        action_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    playbooks = []

    for action, score in ranked_actions:
        meta = PLAYBOOK_CATALOG[action]

        urgency = "IMMEDIATE" if customer_risk == "HIGH" else "NORMAL"

        playbooks.append({
            "action": action,
            "description": meta["description"],
            "execution": meta["execution"],
            "expected_impact": meta["impact"],
            "cost": meta["cost"],
            "urgency": urgency,
            "confidence": round(score, 3)
        })

    return playbooks
