<div align="center">

<br>
  <img src="https://img.shields.io/badge/🔮_RETENTION-AI_Decision_Systems-702963?style=for-the-badge&labelColor=1a1a2e" alt="Retention AI"/>
<br>

<br>
<h1 align="center">
  📉 SaaS Churn Intelligence Platform
</h1>
<br>

<h3 align="center">
  AI-Powered Customer Retention & Decision System
</h3>

<br>

<p align="center">
  <strong>From Passive Prediction to Proactive Intervention</strong>
  <br>
  <i>Stop wondering "Who will churn?" and start asking "What can we do today?"</i>
</p>

<br>

<p align="center">
  <a href="#-executive-summary"><img src="https://img.shields.io/badge/📊-Executive_Summary-2196F3?style=flat-square" alt="Summary"/></a>
  <a href="#-system-architecture"><img src="https://img.shields.io/badge/🏗️-Architecture-FF9800?style=flat-square" alt="Architecture"/></a>
  <a href="#-quick-start"><img src="https://img.shields.io/badge/🚀-Quick_Start-4CAF50?style=flat-square" alt="Quick Start"/></a>
  <a href="#-core-features"><img src="https://img.shields.io/badge/🧠-Features-9C27B0?style=flat-square" alt="Features"/></a>
</p>

<br>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-High_Performance-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/SHAP-Explainable_AI-FF6B35?style=for-the-badge&logo=google-cloud&logoColor=white" alt="SHAP"/>
</p>

</div>

---

## 📊 Executive Summary

<table>
<tr>
<td width="60%">

### The Real SaaS Problem
SaaS businesses silently lose **20–30%** of customers annually. Most churn models stop at prediction (*"73% chance of churn"*), which is useless for operational teams.

### Our Solution
This project is an **end-to-end Decision Intelligence System**. It combines Machine Learning with Operational Playbooks to answer:
1.  **Who** is at risk?
2.  **Why** (Explainability)?
3.  **What action** to take today?
4.  **Who** owns that action?

It bridges the gap between **Data Science** (Models) and **Customer Success** (Revenue).

</td>
<td width="40%" align="center">

### 🎯 Platform Goals

| Metric | Target Outcome |
|:------|:-----|
| **Churn Prediction** | High Precision Binary Classification |
| **Explainability** | 100% White-box (SHAP) |
| **Response Time** | Daily Action Plans |
| **User Trust** | Context-aware Reasons |
| **Workflow** | Automated SOP Assignment |

</td>
</tr>
</table>

---

## 🏗️ System Architecture

```mermaid
graph TD
    A[Customer Data] -->|ETL Process| B(Churn Prediction Model)
    B --> C{Explainability Engine SHAP}
    C --> D[Risk Scoring & Segmentation]
    D --> E[Action Engine: Rules + Context]
    E --> F[Playbooks: Operational SOPs]
    F --> G((AI Retention Agent))
    G --> H[Executive & Ops Dashboard]
🚀 Quick StartPrerequisitesBash# 1. Clone the repository
git clone [https://github.com/yourusername/saas-churn-ai.git](https://github.com/yourusername/saas-churn-ai.git)

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate    # Mac/Linux
# venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt
⚡ Run the PlatformLaunch the dashboard to view the Executive Overview and Action Queue:Bashstreamlit run dashboard/app.py
🧠 Run the Pipelines (Notebooks)To retrain models or simulate agent behavior manually:Bashcd notebooks
# Run "03_model_training.ipynb" to generate new pickles
🗂️ Project StructurePlaintextsaas-churn-ai/
│
├── 📂 data/                      # Data Ingestion Layer
│   ├── raw/
│   └── processed/
│
├── 📂 models/                    # Serialized ML Artifacts
│   └── churn_model.pkl
│
├── 📂 src/                       # Core Logic
│   ├── predict.py                # Inference Engine
│   ├── action_engine.py          # Rule-based Decision Layer
│   ├── playbooks.py              # Operational SOP Definitions
│   └── agent_simulator.py        # AI Agent Logic
│
├── 📂 dashboard/                 # Frontend
│   └── app.py                    # Streamlit Entry Point
│
├── 📂 notebooks/                 # Experiments
│   ├── 01_data_understanding.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training.ipynb
│
├── api.py                        # FastAPI Backend
└── README.md                     # Documentation
🔍 Core Features1️⃣ The Intelligence Layer (ML + SHAP)Goal: Accurate prediction with total transparency.Technique: Scikit-learn Classifier + SHAP (SHapley Additive exPlanations).Output: Probability score + Top 3 contributing factors per customer.Example: "Risk High due to: Low Login Frequency (-40%) and Expiring Card."2️⃣ The Action Engine (Decision Intelligence)Goal: Convert "Risk Scores" into "To-Do Lists".Logic: Combines Risk Level + Account Status (Trial/Paid) + Usage Signals.Output: Assigns specific protocols.Trial Rescue ProtocolAnnual Contract ProposalEngagement Nudge3️⃣ AI Retention Agent (Simulation)Goal: Manage capacity and prioritize work.Function: The agent scans the risk queue, respects daily human capacity (e.g., 10 calls/day), and prioritizes the highest value actions.Result: A generated Daily Action Plan for the CS team.💡 Operational Playbooks (Real-World Use)<table><tr><td width="33%" valign="top">🚨 High Risk: TrialSignal: 3 days left, 0 active seats.Action: Trial Rescue Protocol.Playbook: Send "Founder Outreach" email template -> Offer 7-day extension -> Schedule Setup Call.</td><td width="33%" valign="top">⚠️ Medium Risk: PaidSignal: Usage dropped 15% MoM.Action: Engagement Nudge.Playbook: CSM to review "Value Gap" -> Send "Feature Highlight" video relevant to their industry.</td><td width="33%" valign="top">✅ Low Risk: UpsellSignal: 95% License Utilization.Action: Expansion Drive.Playbook: Propose Annual Contract with 10% discount for early renewal.</td></tr></table>🛠️ Technology Stack<p align="center"><img src="https://www.google.com/search?q=https://img.shields.io/badge/Backend-Python-3776AB%3Fstyle%3Dfor-the-badge%26logo%3Dpython%26logoColor%3Dwhite" alt="Python"/><img src="https://img.shields.io/badge/ML-Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-learn"/><img src="https://www.google.com/search?q=https://img.shields.io/badge/Viz-Plotly-3F4F75%3Fstyle%3Dfor-the-badge%26logo%3Dplotly%26logoColor%3Dwhite" alt="Plotly"/><img src="https://www.google.com/search?q=https://img.shields.io/badge/API-FastAPI-009688%3Fstyle%3Dfor-the-badge%26logo%3Dfastapi%26logoColor%3Dwhite" alt="FastAPI"/><img src="https://www.google.com/search?q=https://img.shields.io/badge/Data-Pandas-150458%3Fstyle%3Dfor-the-badge%26logo%3Dpandas%26logoColor%3Dwhite" alt="Pandas"/></p>🚧 Future RoadmapPhaseFeatureTech Stack1LLM ExplainerOpenAI/LangChain2"What-If" SimulationMonte Carlo / Streamlit3Reinforcement LearningStable Baselines34Multi-tenant DeployDocker + AWS🎯 Use Cases & Audience<p align="center"><strong>SaaS Startups</strong>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<strong>Customer Success Teams</strong>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<strong>Growth Engineers</strong></p>📜 LicenseThis project is open-source and available under the MIT License.<p align="center"><img src="https://www.google.com/search?q=https://img.shields.io/badge/Built_for-SaaS_Growth-FF9933%3Fstyle%3Dfor-the-badge" alt="SaaS"/><img src="https://www.google.com/search?q=https://img.shields.io/badge/Maintained%253F-yes-green.svg%3Fstyle%3Dfor-the-badge" alt="Maintained"/></p>