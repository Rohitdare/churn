import streamlit as st
import pandas as pd
from services.api import (
    get_risk, get_shap, get_playbooks, API_KEYS
)

def render():
    st.header("👤 Customer Intelligence")

    company = st.selectbox("Company", API_KEYS.keys())
    api_key = API_KEYS[company]

    risk = get_risk(api_key)
    df = pd.DataFrame(risk["customers"])

    customer_id = st.selectbox("Customer", df["customer_id"])

    shap = get_shap(api_key, customer_id)
    playbooks = get_playbooks(api_key, customer_id)

    st.subheader("🧠 Why at risk")
    for s in shap["shap_explanations"]:
        st.warning(f"{s['feature']} → {s['impact']:.3f}")

    st.subheader("🛠️ Recommended Actions")
    for p in playbooks["playbooks"]:
        st.info(
            f"{p['action']} | Urgency: {p['urgency']} | Confidence: {p['confidence']}"
        )
