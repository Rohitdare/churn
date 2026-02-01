import streamlit as st
import requests
import pandas as pd

API_BASE = "http://localhost:8000"
API_KEYS = {
    "TaskFlow": "tf_test_key_123",
    "PayTrack": "pt_test_key_456"
}

st.set_page_config(page_title="SaaS Churn Intelligence", layout="wide")
st.title("📉 SaaS Churn Intelligence Dashboard")

company_name = st.selectbox("Select Company", list(API_KEYS.keys()))
api_key = API_KEYS[company_name]

headers = {
    "Authorization": f"Bearer {api_key}"
}

@st.cache_data(ttl=60)
def fetch_risk():
    r = requests.get(f"{API_BASE}/customers/risk", headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()

data = fetch_risk()

# --- Summary ---
col1, col2, col3 = st.columns(3)
col1.metric("High Risk", data["summary"]["HIGH"])
col2.metric("Medium Risk", data["summary"]["MEDIUM"])
col3.metric("Low Risk", data["summary"]["LOW"])

# --- Table ---
df = pd.DataFrame(data["customers"])
st.subheader("Customers by Churn Risk")
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# --- Optional: Filter ---
risk_filter = st.multiselect(
    "Filter by risk",
    ["HIGH", "MEDIUM", "LOW"],
    default=["HIGH", "MEDIUM"]
)

filtered = df[df["churn_risk"].isin(risk_filter)]
st.subheader("Filtered View")
st.dataframe(filtered, use_container_width=True, hide_index=True)
