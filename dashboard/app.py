import streamlit as st
import pandas as pd
import requests

# 1. Define where the API lives
API_URL = "http://localhost:8000"

# --- Header ---
st.title("🚨 Customer Risk Queue")

# 2. Fetch data
try:
    response = requests.get(f"{API_URL}/customers/risk")
    
    # Check if the request was successful
    if response.status_code == 200:
        customers = response.json()
        df = pd.DataFrame(customers)
    else:
        st.error(f"Failed to fetch data. Status code: {response.status_code}")
        # Stop execution here so we don't use an undefined 'df' later
        st.stop()

except requests.exceptions.ConnectionError:
    st.error(f"❌ Could not connect to API at {API_URL}. Is your backend server running?")
    st.stop()

# --- 🔍 Filters ---
# Allowing the user to focus on specific risk categories
risk_filter = st.multiselect(
    "Filter by Risk Level",
    ["High Risk", "Medium Risk", "Low Risk"],
    default=["High Risk", "Medium Risk"]
)

# Apply the filter to the dataframe
if not df.empty:
    df = df[df["risk_level"].isin(risk_filter)]

# --- 📊 Queue Table ---
st.subheader("Customers Needing Attention")

# Prepare display dataframe (formatting churn prob as %)
if not df.empty:
    df_display = df.copy()
    df_display["churn_probability"] = (df_display["churn_probability"] * 100).round(1).astype(str) + "%"

    st.dataframe(
        df_display[[
            "account_id",
            "risk_level",
            "churn_probability",
            "is_trial",
            "account_age_days"
        ]],
        use_container_width=True
    )
else:
    st.info("No customers found.")

st.markdown("---")

# --- 🔎 Customer Drill-Down ---
# Contextual inspection of a single customer
st.subheader("Inspect Customer Details")

if not df.empty:
    selected = st.selectbox(
        "Select Account ID",
        df["account_id"].tolist()
    )

    # Get the single customer row
    cust = df[df["account_id"] == selected].iloc[0]

    # --- 🧠 Explanation Panel ---
    st.subheader(f"🧠 Why {selected} is at risk")
    
    # Check if list exists to avoid errors
    if "top_reasons" in cust and cust["top_reasons"]:
        for reason in cust["top_reasons"]:
            st.write("•", reason.replace("_", " "))
    else:
        st.write("No specific risk factors flagged.")

    # --- 🎯 Recommended Actions ---
    st.subheader("🎯 Recommended Actions")
    
    if cust["risk_level"] == "High Risk":
        st.error("Immediate intervention required")
        st.write("• Assign Customer Success Manager")
        st.write("• Offer onboarding or upgrade assistance")
        
    elif cust["risk_level"] == "Medium Risk":
        st.warning("Monitor and engage")
        st.write("• Send usage tips")
        st.write("• Trigger feature adoption nudges")
        
    else:
        st.success("Customer healthy - No immediate action needed")

else:
    st.info("No customers match the selected filters.")