# src/playbooks.py

PLAYBOOKS = {
    "early_trial_risk": {
        "name": "Early Trial Rescue",
        "description": "Prevent churn during trial by accelerating activation.",
        "owner": "Customer Success",
        "steps": [
            "Schedule onboarding call within 24 hours",
            "Walk through core value features",
            "Identify activation blockers"
        ],
        "expected_impact": "-15% churn probability"
    },

    "high_risk_paid": {
        "name": "High Risk Paid Intervention",
        "description": "Immediate human intervention for paid customers at high risk.",
        "owner": "Customer Success Manager",
        "steps": [
            "Review account usage and tickets",
            "Schedule retention call",
            "Offer plan optimization or discount if needed"
        ],
        "expected_impact": "-12% churn probability"
    },

    "medium_risk_seats": {
        "name": "Seat Utilization Audit",
        "description": "Reduce churn by aligning seat usage with billing.",
        "owner": "Customer Success",
        "steps": [
            "Analyze active vs purchased seats",
            "Recommend seat reduction or training",
            "Follow up after 7 days"
        ],
        "expected_impact": "-8% churn probability"
    },

    "medium_risk_adoption": {
        "name": "Feature Adoption Boost",
        "description": "Increase engagement before churn risk escalates.",
        "owner": "Lifecycle Marketing",
        "steps": [
            "Send feature adoption email",
            "Trigger in-app tooltip",
            "Monitor engagement for 7 days"
        ],
        "expected_impact": "-6% churn probability"
    },

    "low_risk_upsell": {
        "name": "Expansion Opportunity",
        "description": "Convert healthy customers into long-term contracts.",
        "owner": "Sales / Account Management",
        "steps": [
            "Propose annual contract",
            "Offer loyalty incentive",
            "Highlight ROI metrics"
        ],
        "expected_impact": "+10% LTV"
    }
}
