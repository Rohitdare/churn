import streamlit as st
from ui.common import ROLE_VIEWS

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="SaaS Churn Intelligence",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("📉 SaaS Churn Intelligence Platform")
st.caption("Predict • Explain • Act")

# ---------------- ROLE SELECTION ----------------
role = st.selectbox(
    "Select your role",
    ["CEO / Founder", "Head of Customer Success", "CS Manager"]
)

st.session_state["role"] = role

# ---------------- SIDEBAR NAV ----------------
st.sidebar.header("Navigation")

allowed_views = ROLE_VIEWS[role]

selected_view = st.sidebar.radio(
    "Go to",
    allowed_views
)

# ---------------- VIEW ROUTING ----------------
if selected_view == "Executive Overview":
    from views.ceo import render
    render()

elif selected_view == "Retention Agent":
    from views.retention_agent import render
    render()

elif selected_view == "Risk Queue":
    from views.risk_queue import render
    render()

elif selected_view == "Customer Intelligence":
    from views.customer_intelligence import render
    render()
