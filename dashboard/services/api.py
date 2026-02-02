import requests

API_BASE = "http://localhost:8000"

API_KEYS = {
    "TaskFlow": "tf_test_key_123",
    "PayTrack": "pt_test_key_456"
}

def headers(api_key):
    return {"Authorization": f"Bearer {api_key}"}

def get_risk(api_key):
    return requests.get(
        f"{API_BASE}/customers/risk",
        headers=headers(api_key)
    ).json()

def get_agent_logs(api_key):
    return requests.get(
        f"{API_BASE}/customers/agent/logs",
        headers=headers(api_key)
    ).json()["logs"]

def get_shap(api_key, customer_id):
    return requests.get(
        f"{API_BASE}/customers/shap/{customer_id}",
        headers=headers(api_key)
    ).json()

def get_playbooks(api_key, customer_id):
    return requests.get(
        f"{API_BASE}/customers/playbooks/{customer_id}",
        headers=headers(api_key)
    ).json()
