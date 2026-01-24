import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# ==========================================
# CONFIG
# ==========================================
API_URL = "http://localhost:8000"

st.set_page_config(page_title="SaaS Churn Intelligence", layout="wide")
st.title("📊 SaaS Churn Intelligence")

# ==========================================
# SAFE API FETCHER
# ==========================================
def fetch_api(endpoint):
    try:
        res = requests.get(f"{API_URL}/{endpoint}")
        if res.status_code == 200:
            return res.json()
        return None
    except:
        return None

# ==========================================
# 1. EXECUTIVE METRICS
# ==========================================
metrics = fetch_api("metrics")

if metrics:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg Churn Probability", f"{metrics['avg_churn_probability']:.2f}")
    c2.metric("High Risk Customers", metrics["high_risk_customers"])
    c3.metric("Medium Risk Customers", metrics["medium_risk_customers"])
    c4.metric(
        "Customers At Risk",
        metrics["high_risk_customers"] + metrics["medium_risk_customers"]
    )

st.divider()

# ==========================================
# 2. LOAD CUSTOMER DATA
# ==========================================
customers = fetch_api("customers/risk")

if not customers:
    st.error("Could not load customer data.")
    st.stop()

df = pd.DataFrame(customers)

# ==========================================
# 3. ANALYTICS CHARTS
# ==========================================
st.subheader("📊 Portfolio Risk Analytics")
col1, col2 = st.columns(2)

# --- Risk Distribution ---
with col1:
    st.markdown("### 📉 Risk Distribution")
    risk_counts = df["risk_level"].value_counts().reset_index()
    risk_counts.columns = ["risk_level", "count"]

    fig_risk = px.pie(
        risk_counts,
        names="risk_level",
        values="count",
        color="risk_level",
        color_discrete_map={
            "High Risk": "#ff4d4d",
            "Medium Risk": "#ffa500",
            "Low Risk": "#4caf50"
        }
    )
    st.plotly_chart(fig_risk, use_container_width=True)

# --- Churn Risk by Plan ---
with col2:
    st.markdown("### 💳 Churn Risk by Plan")
    df_plan = df.copy()
    df_plan["plan"] = "Basic"

    if "plan_tier_Pro" in df_plan.columns:
        df_plan.loc[df_plan["plan_tier_Pro"] == 1, "plan"] = "Pro"
        df_plan.loc[df_plan["plan_tier_Enterprise"] == 1, "plan"] = "Enterprise"

    fig_plan = px.box(
        df_plan,
        x="plan",
        y="churn_probability",
        color="plan"
    )
    st.plotly_chart(fig_plan, use_container_width=True)

st.divider()

# ==========================================
# 4. CUSTOMER RISK QUEUE
# ==========================================
st.subheader("🚨 Customer Risk Queue")

risk_filter = st.multiselect(
    "Filter by Risk Level",
    ["High Risk", "Medium Risk", "Low Risk"],
    default=["High Risk", "Medium Risk"]
)

df_filtered = df[df["risk_level"].isin(risk_filter)]

if df_filtered.empty:
    st.info("No customers match selected filters.")
    st.stop()

df_display = df_filtered.copy()
df_display["churn_probability"] = (
    df_display["churn_probability"] * 100
).round(1).astype(str) + "%"

st.dataframe(
    df_display[
        ["account_id", "risk_level", "churn_probability", "is_trial", "account_age_days"]
    ],
    use_container_width=True
)

# ==========================================
# 5. CUSTOMER DRILL-DOWN
# ==========================================
st.divider()
st.subheader("🔎 Inspect Customer Details")

selected = st.selectbox(
    "Select Account ID",
    df_filtered["account_id"].tolist()
)

cust = df_filtered[df_filtered["account_id"] == selected].iloc[0]

col_left, col_right = st.columns(2)

# --- Reasons & Actions ---
with col_left:
    st.markdown(f"### 🧠 Why `{selected}` is at risk")

    if cust.get("top_reasons"):
        for r in cust["top_reasons"]:
            st.write(f"• {r.replace('_', ' ')}")
    else:
        st.write("No dominant risk drivers detected.")

    st.markdown("### 🎯 Immediate Recommendation")
    if cust["risk_level"] == "High Risk":
        st.error("Immediate outreach required. Schedule a success call.")
    elif cust["risk_level"] == "Medium Risk":
        st.warning("Send targeted engagement and feature education.")
    else:
        st.success("Customer health is stable.")

# --- Risk Trend ---
with col_right:
    st.markdown("### 📈 Risk Trend (30 Days)")
    history_data = fetch_api(f"customers/{selected}/risk-history")

    if history_data and "risk_history" in history_data:
        hist_df = pd.DataFrame(history_data["risk_history"])

        fig_trend = px.line(
            hist_df,
            x="date",
            y="churn_probability",
            markers=True
        )
        fig_trend.update_yaxes(range=[0, 1])
        st.plotly_chart(fig_trend, use_container_width=True)

        delta = hist_df["churn_probability"].iloc[-1] - hist_df["churn_probability"].iloc[0]
        if delta > 0.15:
            st.error("🚨 Risk increasing rapidly")
        elif delta > 0.05:
            st.warning("⚠️ Risk trending upward")
        elif delta < -0.05:
            st.success("✅ Risk improving")
        else:
            st.info("ℹ️ Risk stable")
    else:
        st.write("No risk history available.")

# ==========================================
# 6. NEXT BEST ACTION ENGINE
# ==========================================
st.divider()
st.subheader("🎯 Next Best Actions")

actions_data = fetch_api(f"customers/{selected}/next-actions")

if actions_data:
    st.caption(f"Risk Trend: {actions_data.get('risk_trend', 'Unknown')}")

    for act in actions_data.get("recommended_actions", []):
        if act["priority"] == "Urgent":
            st.error(f"🔥 **{act['action']}** — {act['reason']}")
        elif act["priority"] == "High":
            st.warning(f"⚠️ **{act['action']}** — {act['reason']}")
        else:
            st.info(f"ℹ️ **{act['action']}** — {act['reason']}")
else:
    st.error("Could not load recommended actions.")
