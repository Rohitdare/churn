import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# ==========================================
# CONFIG
# ==========================================
API_URL = "http://localhost:8000"
st.set_page_config(page_title="SaaS Churn Intelligence", layout="wide")

st.title("📊 SaaS Churn Intelligence Platform")

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
# 1. EXECUTIVE OVERVIEW
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
    st.error("❌ Could not load customer data.")
    st.stop()

df = pd.DataFrame(customers)

# ==========================================
# 3. PORTFOLIO ANALYTICS
# ==========================================
st.subheader("📊 Portfolio Risk Analytics")
col1, col2 = st.columns(2)

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

with col2:
    st.markdown("### 💳 Churn Risk by Plan")
    df_plan = df.copy()
    df_plan["plan"] = "Basic"
    if "plan_tier_Pro" in df_plan.columns:
        df_plan.loc[df_plan["plan_tier_Pro"] == 1, "plan"] = "Pro"
        df_plan.loc[df_plan["plan_tier_Enterprise"] == 1, "plan"] = "Enterprise"

    fig_plan = px.box(df_plan, x="plan", y="churn_probability", color="plan")
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
st.subheader("🔎 Inspect Customer")

selected = st.selectbox("Select Account ID", df_filtered["account_id"].tolist())
cust = df_filtered[df_filtered["account_id"] == selected].iloc[0]

col_left, col_right = st.columns(2)

with col_left:
    st.markdown(f"### 🧠 Why `{selected}` is at risk")
    for r in cust.get("top_reasons", []):
        st.write(f"• {r.replace('_', ' ')}")

with col_right:
    st.markdown("### 📈 Risk Trend (30 Days)")
    history = fetch_api(f"customers/{selected}/risk-history")
    if history:
        hist_df = pd.DataFrame(history["risk_history"])
        fig_trend = px.line(hist_df, x="date", y="churn_probability", markers=True)
        fig_trend.update_yaxes(range=[0, 1])
        st.plotly_chart(fig_trend, use_container_width=True)

st.divider()

# ==========================================
# 6. NEXT BEST ACTION ENGINE (ENTERPRISE SAFE)
# ==========================================
st.subheader("🎯 Recommended Actions & Playbooks")

actions_data = fetch_api(f"customers/{selected}/next-actions")

if not actions_data:
    st.error("❌ Could not load action recommendations.")
    st.stop()

st.caption(f"Risk Trend: {actions_data.get('risk_trend', 'Unknown')}")

for act in actions_data.get("recommended_actions", []):
    priority = act.get("priority", "Low")
    action_name = act.get("action", "Unnamed Action")
    why = act.get("why", "No explanation provided")

    if priority == "Urgent":
        st.error(f"🔥 **{action_name}**")
    elif priority == "High":
        st.warning(f"⚠️ **{action_name}**")
    else:
        st.info(f"ℹ️ **{action_name}**")

    st.write(f"**Why:** {why}")

    pb = act.get("playbook")

    if isinstance(pb, dict):
        pb_name = pb.get("name", "Unnamed Playbook")
        pb_desc = pb.get("description", "No description provided")
        pb_owner = pb.get("owner", "Unassigned")
        pb_steps = pb.get("steps", [])
        pb_impact = pb.get("expected_impact", "Impact not quantified")

        with st.expander(f"📘 Playbook: {pb_name}"):
            st.write(f"**Description:** {pb_desc}")
            st.write(f"**Owner:** {pb_owner}")
            if pb_steps:
                st.write("**Steps:**")
                for step in pb_steps:
                    st.write("•", step)
            st.success(f"Expected Impact: {pb_impact}")

st.divider()

# ==========================================
# 7. AGENT SIMULATION
# ==========================================
st.header("🤖 AI Retention Agent – Today’s Action Plan")

if st.button("Simulate Agent Plan"):
    plan = fetch_api("agent/daily-plan")

    if not plan:
        st.error("❌ Agent simulation failed.")
        st.stop()

    summary = plan["plan"]["summary"]
    c1, c2, c3 = st.columns(3)
    c1.metric("Urgent Accounts", summary["urgent_customers"])
    c2.metric("Bulk Engagement", summary["bulk_customers"])
    c3.metric("Deferred", summary["deferred_customers"])

    st.subheader("🚨 Priority Actions")
    for act in plan["plan"]["priority_actions"]:
        st.error(
            f"🔥 {act['account_id']} ({act['churn_probability']*100:.1f}%)\n\n"
            f"Action: {act['recommended_action']}"
        )

    st.subheader("📣 Bulk Actions")
    for act in plan["plan"]["bulk_actions"]:
        st.warning(f"{act['action']} → {act['customer_count']} customers")

    st.info(plan["note"])
