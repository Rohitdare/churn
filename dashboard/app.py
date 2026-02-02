import streamlit as st

st.set_page_config(page_title="SaaS Churn Intelligence", layout="wide")

st.title("📉 SaaS Churn Intelligence Platform")
st.caption("Predict • Explain • Act")

role = st.selectbox(
    "Select your role",
    ["CEO / Founder", "Head of Customer Success", "CS Manager"]
)

st.session_state["role"] = role

st.markdown(
    """
    👈 Use the sidebar to navigate between sections.
    
    This dashboard adapts insights based on your role.
    """
)
