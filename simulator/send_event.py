import requests

def send_event(event, api_key, base_url):
    url = f"{base_url}/v1/events"
    print("POSTING TO:", url)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, json=event, headers=headers, timeout=5)

    if r.status_code != 200:
        print("❌ Failed event:", r.text)
