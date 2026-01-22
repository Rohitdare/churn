import streamlit as st
import requests

st.set_page_config(page_title="SaaS Churn Predictor", layout="centered")

st.title("📉 SaaS Customer Churn Risk")
st.write("Check if a customer is at risk of leaving and understand why.")

# Input section
st.header("Customer Details")

seats = st.slider("Team size", 1, 100, 10)
is_trial = st.checkbox("Is trial user?")
account_age = st.slider("Account age (days)", 1, 1000, 60)

industry = st.selectbox("Industry", ["EdTech", "FinTech", "DevTools", "HealthTech"])
country = st.selectbox("Country", ["US", "IN", "UK", "CA", "DE", "FR"])
plan = st.selectbox("Plan Tier", ["Basic", "Pro", "Enterprise"])
referral = st.selectbox("Referral Source", ["organic", "event", "partner", "other"])

# Build API payload
payload = {
    "seats": seats,
    "is_trial": int(is_trial),
    "account_age_days": account_age,

    "industry_DevTools": industry == "DevTools",
    "industry_EdTech": industry == "EdTech",
    "industry_FinTech": industry == "FinTech",
    "industry_HealthTech": industry == "HealthTech",

    "country_US": country == "US",
    "country_IN": country == "IN",
    "country_UK": country == "UK",
    "country_CA": country == "CA",
    "country_DE": country == "DE",
    "country_FR": country == "FR",

    "plan_tier_Enterprise": plan == "Enterprise",
    "plan_tier_Pro": plan == "Pro",

    "referral_source_organic": referral == "organic",
    "referral_source_event": referral == "event",
    "referral_source_partner": referral == "partner",
    "referral_source_other": referral == "other"
}

if st.button("Predict Churn Risk"):
    response = requests.post("http://127.0.0.1:8000/predict", json=payload)
    result = response.json()

    st.subheader("📊 Prediction Result")

    st.metric("Churn Probability", f"{result['churn_probability'] * 100:.1f}%")
    st.metric("Risk Level", result["risk_level"])

    st.subheader("🔍 Why this customer is at risk")
    for reason in result["top_reasons"]:
        st.write("•", reason)
