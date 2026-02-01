EXPLANATION_RULES = {
    "days_since_last_event": {
        "condition": lambda v: v > 7,
        "message": "Customer has been inactive recently"
    },
    "active_days_7d": {
        "condition": lambda v: v <= 2,
        "message": "Low engagement in the last 7 days"
    },
    "value_events_14d": {
        "condition": lambda v: v == 0,
        "message": "No usage of core value features"
    },
    "events_7d": {
        "condition": lambda v: v < 3,
        "message": "Overall activity is declining"
    }
}
