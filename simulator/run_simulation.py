import random
from company_config import COMPANY
from personas import PERSONAS
from event_weights import EVENT_WEIGHTS
from event_builder import build_event
from send_event import send_event

def run():
    for day in range(COMPANY["simulation_days"]):
        for cust in range(COMPANY["customers"]):
            persona = random.choice(list(PERSONAS.keys()))
            events_today = random.randint(
                *PERSONAS[persona]["daily_event_range"]
            )

            for _ in range(events_today):
                event_name = random.choices(
                    list(EVENT_WEIGHTS.keys()),
                    weights=EVENT_WEIGHTS.values()
                )[0]

                event = build_event(
                    COMPANY["company_id"],
                    f"cust_{cust}",
                    f"user_{cust}_1",
                    event_name
                )

                send_event(
                    event,
                    COMPANY["api_key"],
                    COMPANY["base_url"]
                )

if __name__ == "__main__":
    run()
