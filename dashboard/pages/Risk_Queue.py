import streamlit as st
import pandas as pd
from services.api import get_risk, API_KEYS

st.title("🚨 Risk Queue")

company = st.selectbox("Company", API_KEYS.keys())
api_key = API_KEYS[company]

risk = get_risk(api_key)
df = pd.DataFrame(risk["customers"])

queue = df[
    (df.churn_risk == "HIGH") |
    ((df.churn_risk == "MEDIUM") & (df.churn_probability > 0.6))
].sort_values("churn_probability", ascending=False)

st.dataframe(queue, use_container_width=True)
