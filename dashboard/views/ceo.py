import streamlit as st
import pandas as pd
import plotly.express as px
from services.api import get_risk, API_KEYS

def render():
    st.header("📊 Executive Overview")

    company = st.selectbox("Company", API_KEYS.keys())
    api_key = API_KEYS[company]

    data = get_risk(api_key)
    df = pd.DataFrame(data["customers"])

    c1, c2, c3 = st.columns(3)
    c1.metric("High Risk", data["summary"]["HIGH"])
    c2.metric("Medium Risk", data["summary"]["MEDIUM"])
    c3.metric("Low Risk", data["summary"]["LOW"])

    fig = px.pie(
        names=["High", "Medium", "Low"],
        values=[
            data["summary"]["HIGH"],
            data["summary"]["MEDIUM"],
            data["summary"]["LOW"]
        ],
        title="Churn Health Snapshot"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.success("✔ Retention systems are actively managing churn risk.")
