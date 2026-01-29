# lifecycle.py

LIFECYCLE_STAGES = {
    "trial": {
        "days": (0, 5),
        "event_multiplier": 1.5,  # High activity during setup
        "churn_risk": 0.02        # Low risk early on
    },
    "active": {
        "days": (6, 15),
        "event_multiplier": 1.0,  # Standard usage
        "churn_risk": 0.01
    },
    "adopted": {
        "days": (16, 25),
        "event_multiplier": 1.2,  # Power users do more
        "churn_risk": 0.005
    },
    "stagnant": {
        "days": (26, 40),
        "event_multiplier": 0.2,  # Activity drops significantly
        "churn_risk": 0.20        # Danger zone!
    },
    "churned": {
        "days": (41, 999),
        "event_multiplier": 0.0,
        "churn_risk": 1.0
    }
}