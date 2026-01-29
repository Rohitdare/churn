import requests

def send_event(event, api_key, base_url):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    r = requests.post(
        f"{base_url}/v1/events/",
        json=event,
        headers=headers,
        timeout=5
    )

    if r.status_code != 200:
        print("❌ Failed:", r.status_code, r.text, "API_KEY:", api_key)
