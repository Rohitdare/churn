<div align="center">

<img src="https://img.shields.io/badge/🔮_RETENTION-AI_Decision_Systems-702963?style=for-the-badge&labelColor=1a1a2e" />

# 📉 SaaS Churn Intelligence Platform  
### AI-Powered Customer Retention & Decision System

**From Passive Prediction → Proactive Intervention**

_Stop asking **“Who will churn?”**  
Start answering **“What should we do today?”**_

<br/>

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/SHAP-Explainable_AI-FF6B35?style=for-the-badge"/>

</div>

---

## 📌 Executive Summary

### The Real SaaS Problem
SaaS companies silently lose **20–30% of customers every year**.  
Most churn models stop at prediction:

> “This user has a **73% chance of churn**.”

This insight alone **does not save revenue**.

---

### Our Solution
This project is an **end-to-end Decision Intelligence Platform** that bridges the gap between **Data Science** and **Customer Operations**.

It answers four business-critical questions:

1. **Who** is at risk?
2. **Why** are they at risk? (Explainability)
3. **What action** should be taken?
4. **Who owns** that action today?

The result is **daily, prioritized action plans**, not static dashboards.

---

## 🎯 Platform Objectives

| Capability | Outcome |
|-----------|--------|
| Churn Prediction | High-precision classification |
| Explainability | 100% transparent (SHAP) |
| Decisioning | Rule + context driven |
| Execution | SOP-based playbooks |
| Trust | Human-readable reasons |

---

## 🏗️ System Architecture

```mermaid
graph TD
    A[Customer Data] -->|ETL| B[Churn Model]
    B --> C[SHAP Explainability]
    C --> D[Risk Scoring]
    D --> E[Decision Engine]
    E --> F[Operational Playbooks]
    F --> G[AI Retention Agent]
    G --> H[Ops & Executive Dashboard]
🧠 Core Capabilities
1️⃣ Intelligence Layer (ML + Explainability)
Goal: Predict churn with complete transparency

Binary classification (Churn / Retain)

Probability-based risk scoring

SHAP-based feature attribution

Example Output

Risk: HIGH (0.81)
Top Drivers:
• Low login frequency
• Expiring payment method
• No feature adoption
2️⃣ Decision Engine (Action Mapping)
Goal: Convert risk scores into concrete actions

Inputs:

Risk level

Account type (Trial / Paid)

Usage signals

Revenue potential

Output:

A specific operational protocol, not a vague alert

3️⃣ AI Retention Agent (Simulation)
Goal: Optimize human effort

Respects daily team capacity

Prioritizes highest-value actions

Generates a Daily Action Plan

📋 Operational Playbooks
Risk Scenario	Trigger	Action
🚨 High Risk – Trial	3 days left, no usage	Founder outreach + extension
⚠️ Medium Risk – Paid	Usage down 15% MoM	Value reminder + feature demo
✅ Low Risk – Healthy	High utilization	Upsell / annual renewal
🚀 Quick Start
Prerequisites
Python 3.10+

Git

Installation
git clone https://github.com/yourusername/saas-churn-ai.git
cd saas-churn-ai

python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows

pip install -r requirements.txt
Run Dashboard
streamlit run dashboard/app.py
Train / Retrain Models
cd notebooks
# Run:
03_model_training.ipynb
🗂️ Project Structure
saas-churn-ai/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   └── churn_model.pkl
│
├── src/
│   ├── predict.py
│   ├── action_engine.py
│   ├── playbooks.py
│   └── agent_simulator.py
│
├── dashboard/
│   └── app.py
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training.ipynb
│
├── api.py
└── README.md
🛠️ Technology Stack
Layer	Tools
Language	Python
Machine Learning	Scikit-Learn
Explainability	SHAP
Backend	FastAPI
Frontend	Streamlit
Data	Pandas, NumPy
Visualization	Plotly
🚧 Roadmap
Phase	Feature	Tech
1	LLM Explanation Layer	OpenAI / LangChain
2	What-If Simulations	Monte Carlo
3	Retention Policy Learning	Reinforcement Learning
4	Multi-Tenant SaaS	Docker + AWS
🎯 Target Audience
SaaS Founders

Customer Success Teams

Growth Engineers

ML Engineers building real products

📜 License
MIT License – free to use, modify, and commercialize.

<div align="center">
Built for SaaS teams that care about revenue, not just metrics.

</div> ```