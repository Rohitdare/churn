import streamlit as st
import pandas as pd
from services.api import get_risk, get_agent_logs, API_KEYS

st.title("🤖 AI Retention Agent")

company = st.selectbox("Company", API_KEYS.keys())
api_key = API_KEYS[company]

risk = get_risk(api_key)
df = pd.DataFrame(risk["customers"])

urgent = df[df.churn_risk == "HIGH"]
bulk = df[df.churn_risk == "MEDIUM"]
deferred = df[df.churn_risk == "LOW"]

c1, c2, c3 = st.columns(3)
c1.metric("🚨 Urgent", len(urgent))
c2.metric("📣 Bulk", len(bulk))
c3.metric("⏳ Deferred", len(deferred))

st.subheader("🔥 Top Priority Accounts")
st.dataframe(urgent.head(10), use_container_width=True)

st.subheader("📜 Agent Execution Log")
logs = get_agent_logs(api_key)

with st.expander("View recent actions"):
    for log in logs:
        st.write(
            f"{log['executed_at']} → {log['customer_id']} → {log['action']} ({log['status']})"
        )
