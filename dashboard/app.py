import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ---------------- CONFIG ----------------
API_BASE = "http://localhost:8000"

API_KEYS = {
    "TaskFlow (High churn)": "tf_test_key_123",
    "PayTrack (Low churn)": "pt_test_key_456"
}

st.set_page_config(
    page_title="SaaS Churn Intelligence",
    layout="wide",
)

# ---------------- HELPERS ----------------
def api_headers(api_key):
    return {"Authorization": f"Bearer {api_key}"}

@st.cache_data(ttl=60)
def fetch_risk(api_key):
    r = requests.get(
        f"{API_BASE}/customers/risk",
        headers=api_headers(api_key),
        timeout=10
    )
    r.raise_for_status()
    return r.json()

@st.cache_data(ttl=60)
def fetch_intelligence(api_key, customer_id):
    r = requests.get(
        f"{API_BASE}/customers/intelligence/{customer_id}",
        headers=api_headers(api_key),
        timeout=10
    )
    r.raise_for_status()
    return r.json()

# ---------------- HEADER ----------------
st.title("📉 SaaS Churn Intelligence Platform")
st.caption("Predict • Explain • Act")

st.divider()

# ---------------- COMPANY SELECTION ----------------
company_label = st.selectbox(
    "Select Company",
    list(API_KEYS.keys())
)

api_key = API_KEYS[company_label]
risk_data = fetch_risk(api_key)

df = pd.DataFrame(risk_data["customers"])

# ---------------- KPI METRICS ----------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "🔴 High Risk Customers",
    risk_data["summary"]["HIGH"]
)
col2.metric(
    "🟠 Medium Risk Customers",
    risk_data["summary"]["MEDIUM"]
)
col3.metric(
    "🟢 Low Risk Customers",
    risk_data["summary"]["LOW"]
)

st.divider()

# ---------------- RISK DISTRIBUTION CHART ----------------
st.subheader("📊 Churn Risk Distribution")

risk_df = pd.DataFrame({
    "Risk": ["High", "Medium", "Low"],
    "Customers": [
        risk_data["summary"]["HIGH"],
        risk_data["summary"]["MEDIUM"],
        risk_data["summary"]["LOW"]
    ]
})

fig = px.pie(
    risk_df,
    values="Customers",
    names="Risk",
    color="Risk",
    color_discrete_map={
        "High": "#e74c3c",
        "Medium": "#f39c12",
        "Low": "#2ecc71"
    }
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------- CUSTOMER TABLE ----------------
st.subheader("👥 Customers Ranked by Churn Risk")

risk_filter = st.multiselect(
    "Filter by risk level",
    ["HIGH", "MEDIUM", "LOW"],
    default=["HIGH", "MEDIUM"]
)

filtered_df = df[df["churn_risk"].isin(risk_filter)]

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ---------------- CUSTOMER DRILL-DOWN ----------------
st.subheader("🔍 Customer Intelligence")

customer_ids = filtered_df["customer_id"].tolist()

selected_customer = st.selectbox(
    "Select a customer to inspect",
    customer_ids
)

if selected_customer:
    intel = fetch_intelligence(api_key, selected_customer)

    colA, colB = st.columns([1, 2])

    with colA:
        st.metric(
            "Churn Probability",
            f"{intel['churn_probability']:.2f}"
        )
        st.metric(
            "Risk Level",
            intel["churn_risk"]
        )

    with colB:
        st.markdown("### ❓ Why is this customer at risk?")
        if intel["reasons"]:
            for r in intel["reasons"]:
                st.warning(r)
        else:
            st.success("No major risk signals detected")

    st.markdown("### 🛠️ Recommended Actions")
    if intel["recommended_actions"]:
        for a in intel["recommended_actions"]:
            st.info(a)
    else:
        st.success("No immediate action required")

st.divider()

# ---------------- FOOTER ----------------
st.caption(
    "Built with real-time events, feature aggregation, ML inference, explainability, and playbooks."
)
