import streamlit as st
import pandas as pd
import plotly.express as px
from services.api import get_risk, API_KEYS

st.title("📊 Executive Overview")

company = st.selectbox("Company", API_KEYS.keys())
api_key = API_KEYS[company]

data = get_risk(api_key)
df = pd.DataFrame(data["customers"])

# KPIs
c1, c2, c3 = st.columns(3)
c1.metric("High Risk", data["summary"]["HIGH"])
c2.metric("Medium Risk", data["summary"]["MEDIUM"])
c3.metric("Low Risk", data["summary"]["LOW"])

# Distribution chart
risk_df = pd.DataFrame({
    "Risk": ["High", "Medium", "Low"],
    "Customers": [
        data["summary"]["HIGH"],
        data["summary"]["MEDIUM"],
        data["summary"]["LOW"]
    ]
})

fig = px.pie(
    risk_df,
    values="Customers",
    names="Risk",
    title="Current Churn Health"
)

st.plotly_chart(fig, use_container_width=True)

st.success(
    "✔ The retention system is actively monitoring and mitigating churn risk."
)
