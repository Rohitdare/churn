import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"
st.set_page_config("SaaS Churn Intelligence", layout="wide")

st.title("📊 SaaS Churn Intelligence Dashboard")

# ---------------- METRICS ----------------
metrics = requests.get(f"{API_URL}/metrics").json()

c1, c2, c3 = st.columns(3)
c1.metric("Avg Churn Probability", f"{metrics['avg_churn_probability']:.2f}")
c2.metric("High Risk Customers", metrics["high_risk_customers"])
c3.metric("Medium Risk Customers", metrics["medium_risk_customers"])

# ---------------- INPUT ----------------
st.header("🔍 Analyze a Customer")

seats = st.slider("Team size", 1, 100, 10)
is_trial = st.checkbox("Trial user")
age = st.slider("Account age (days)", 1, 1000, 90)
country = st.selectbox("Country", ["US","IN","UK","CA","DE","FR"])
plan = st.selectbox("Plan", ["Basic","Pro","Enterprise"])
industry = st.selectbox("Industry", ["EdTech","FinTech","DevTools","HealthTech"])

payload = {
    "seats": seats,
    "is_trial": int(is_trial),
    "account_age_days": age,

    "industry_DevTools": industry=="DevTools",
    "industry_EdTech": industry=="EdTech",
    "industry_FinTech": industry=="FinTech",
    "industry_HealthTech": industry=="HealthTech",

    "country_US": country=="US",
    "country_IN": country=="IN",
    "country_UK": country=="UK",
    "country_CA": country=="CA",
    "country_DE": country=="DE",
    "country_FR": country=="FR",

    "plan_tier_Enterprise": plan=="Enterprise",
    "plan_tier_Pro": plan=="Pro",

    "referral_source_organic": True,
    "referral_source_event": False,
    "referral_source_partner": False,
    "referral_source_other": False
}

# ---------------- PREDICT ----------------
res = None

if st.button("Predict Churn Risk"):
    res = requests.post(f"{API_URL}/predict", json=payload).json()

    st.subheader("📌 Risk Assessment")
    st.metric("Churn Probability", f"{res['churn_probability']*100:.1f}%")
    st.metric("Risk Level", res["risk_level"])

    st.subheader("🧠 Why this customer is at risk")
    for reason in res["top_reasons"]:
        st.write("•", reason)

# ---------------- ACTIONS ----------------
if res:
    st.subheader("🎯 Recommended Actions")

    if res["risk_level"] == "High Risk":
        st.error("Immediate retention action recommended")
        st.write("• Offer discount or plan upgrade")
        st.write("• Assign CSM outreach")

    elif res["risk_level"] == "Medium Risk":
        st.warning("Monitor and engage")
        st.write("• Product onboarding nudges")

    else:
        st.success("Customer healthy")
