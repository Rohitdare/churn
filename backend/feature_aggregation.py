from datetime import date
from sqlalchemy import text
from database import engine

VALUE_EVENTS = (
    "export_report",
    "invite_user",
    "use_advanced_feature"
)

AGGREGATION_SQL = text("""
WITH snapshot AS (
    SELECT MAX(DATE(timestamp)) AS snapshot_date
    FROM events
),

base_events AS (
    SELECT
        e.company_id,
        e.customer_id,
        DATE(e.timestamp) AS event_date,
        e.event_name,
        e.timestamp,
        s.snapshot_date
    FROM events e
    CROSS JOIN snapshot s
    WHERE DATE(e.timestamp) <= s.snapshot_date
),

last_event AS (
    SELECT
        company_id,
        customer_id,
        MAX(timestamp) AS last_event_ts
    FROM events
    GROUP BY company_id, customer_id
)

INSERT INTO customer_features_daily (
    company_id,
    customer_id,
    feature_date,
    events_7d,
    events_14d,
    active_days_7d,
    days_since_last_event,
    value_events_14d
)
SELECT
    e.company_id,
    e.customer_id,
    e.snapshot_date AS feature_date,

    COUNT(*) FILTER (
        WHERE event_date >= e.snapshot_date - INTERVAL '7 days'
    ) AS events_7d,

    COUNT(*) FILTER (
        WHERE event_date >= e.snapshot_date - INTERVAL '14 days'
    ) AS events_14d,

    COUNT(DISTINCT event_date) FILTER (
        WHERE event_date >= e.snapshot_date - INTERVAL '7 days'
    ) AS active_days_7d,

    EXTRACT(DAY FROM e.snapshot_date - l.last_event_ts)::INT
        AS days_since_last_event,

    COUNT(*) FILTER (
        WHERE event_name IN :value_events
        AND event_date >= e.snapshot_date - INTERVAL '14 days'
    ) AS value_events_14d

FROM base_events e
JOIN last_event l
  ON e.company_id = l.company_id
 AND e.customer_id = l.customer_id

GROUP BY
    e.company_id,
    e.customer_id,
    e.snapshot_date,
    l.last_event_ts

ON CONFLICT (company_id, customer_id, feature_date)
DO UPDATE SET
    events_7d = EXCLUDED.events_7d,
    events_14d = EXCLUDED.events_14d,
    active_days_7d = EXCLUDED.active_days_7d,
    days_since_last_event = EXCLUDED.days_since_last_event,
    value_events_14d = EXCLUDED.value_events_14d,
    updated_at = CURRENT_TIMESTAMP;
""")

    
def run_daily_aggregation():
    print("🚀 Running daily feature aggregation...")
    with engine.begin() as conn:
        conn.execute(AGGREGATION_SQL, {
            "value_events": VALUE_EVENTS
        })
    print("✅ Feature aggregation completed")
       

if __name__ == "__main__":
    run_daily_aggregation()
