def next_best_action(customer):
    """
    Determines the best action based on risk level, trend, and top factors.
    Returns a list of actions with priority.
    """
    actions = []
    
    risk_level = customer.get("risk_level", "Low Risk")
    trend = customer.get("risk_trend", "Stable")
    top_reasons = customer.get("top_reasons", [])
    
    # --- 1. CRITICAL INTERVENTIONS (High Risk) ---
    if risk_level == "High Risk":
        if trend == "Rapidly Increasing":
            actions.append({
                "action": "Executive Outreach",
                "priority": "Urgent",
                "reason": "Risk spiked >15% in 30 days. Needs VP/Director touch."
            })
        
        actions.append({
            "action": "Schedule Business Review",
            "priority": "Urgent",
            "reason": "High probability of churn. Lock in renewal discussion."
        })

    # --- 2. PREVENTATIVE (Medium Risk) ---
    elif risk_level == "Medium Risk":
        if "seats" in top_reasons:
            actions.append({
                "action": "Seat Utilization Audit",
                "priority": "High",
                "reason": "Customer is paying for unused seats."
            })
        
        actions.append({
            "action": "Send 'Pro' Feature Guide",
            "priority": "High",
            "reason": "Drive adoption of sticky features."
        })

    # --- 3. UPSELL (Low Risk) ---
    else: # Low Risk
        if trend == "Decreasing" or trend == "Stable":
            actions.append({
                "action": "Propose Annual Contract",
                "priority": "Medium",
                "reason": "Customer is healthy and stable."
            })

    # --- 4. FALLBACK ---
    if not actions:
        actions.append({
            "action": "Monitor Health Score",
            "priority": "Low",
            "reason": "No immediate alerts."
        })
        
    return actions