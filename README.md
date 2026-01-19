# AI-Powered SaaS Customer Churn Prediction System

An end-to-end Machine Learning project that predicts **which SaaS customers are likely to churn**, estimates **churn probability**, and lays the foundation for **explainable, actionable retention insights**.

This project is built with a **realistic SaaS dataset** and follows **industry-style ML workflows**, not just a Kaggle notebook.

---

## 🚨 Problem Statement

SaaS companies silently lose **20–30% of users every month** due to customer churn.

Key challenges:
- Companies don’t know **who will churn**
- They don’t know **why users churn**
- They react **after revenue is already lost**

**Goal:**  
Build an AI system that predicts churn *before it happens*, enabling proactive retention.

---

## 🎯 Project Objectives

- Predict customer churn (binary classification)
- Handle real-world class imbalance
- Generate churn probabilities (risk scores)
- Build explainable, business-ready ML features
- Follow a clean, reproducible ML pipeline

---

## 🧠 ML Problem Formulation

- **Type:** Supervised Learning  
- **Task:** Binary Classification  
- **Target Variable:** `churn_flag`  
  - `1` → Customer churned  
  - `0` → Customer retained  

Accuracy is **not** the primary metric.  
We prioritize **Recall** and **ROC-AUC**, which matter more for churn prevention.

---

## 📊 Dataset Overview (SaaS-Style)

The dataset simulates a real SaaS environment with multiple tables:

- `ravenstack_accounts.csv` – Account-level customer data
- `ravenstack_subscriptions.csv` – Plan & billing information
- `ravenstack_feature_usage.csv` – Product engagement data
- `ravenstack_support_tickets.csv` – Customer friction signals
- `ravenstack_churn_events.csv` – Churn records

**Churn Rate:** ~22% (realistic SaaS churn)

---

## 🏗️ Project Structure

saas-churn-ai/
│
├── data/
│ ├── raw/ # Original datasets
│ └── processed/ # ML-ready datasets
│
├── notebooks/
│ ├── 01_data_understanding.ipynb
│ ├── 02_feature_engineering.ipynb
│ └── 03_model_training.ipynb
│
├── src/ # Modular pipeline code (WIP)
├── models/ # Saved models (WIP)
├── reports/ # Insights & analysis (WIP)
├── README.md
└── venv/

yaml
Copy code

---

## 🔧 Feature Engineering Highlights

Raw data was transformed into **behavioral signals**, including:

- Account tenure (`account_age_days`)
- Trial vs paid status
- Company size proxy (`seats`)
- One-hot encoded categorical features:
  - Industry
  - Country
  - Plan tier
  - Referral source

All features are numeric and **model-ready**.

---

## 🤖 Models Implemented (So Far)

### 1️⃣ Logistic Regression (Baseline)
- Handled class imbalance using `class_weight="balanced"`
- Demonstrated why **accuracy alone is misleading** in churn problems
- Achieved meaningful **ROC-AUC (~0.62)** despite imbalance

This baseline establishes a reference for stronger models.

---

## 📈 Evaluation Metrics

We focus on:
- **Recall (Churn = 1)** → Catch potential churners
- **ROC-AUC** → Overall ranking quality
- **Precision–Recall trade-offs** → Business impact

---

## 🔮 Current Status

✅ Data understanding completed  
✅ Feature engineering completed  
✅ Baseline model trained & evaluated  
🚧 Random Forest & advanced models (next)  
🚧 Churn probability engine  
🚧 Explainability (SHAP)  
🚧 API & dashboard (optional)

---

## 🚀 Roadmap

Planned next steps:
- Train Random Forest & compare models
- Generate churn risk scores
- Identify top churn-risk customers
- Add explainable AI (SHAP)
- Translate predictions into retention actions
- Optional: API & dashboard

---

## 🏆 Why This Project Matters

This project is designed to be:
- **Portfolio-grade**, not tutorial-level
- **Business-aware**, not just technical
- **Extendable** into a real SaaS MVP

It reflects how churn prediction systems are built in **real companies**.

---

## 📌 Tech Stack

- Python 3.10
- Pandas, NumPy
- Scikit-learn
- Jupyter Notebook
- (Planned) SHAP, FastAPI, Streamlit

---

## 👤 Author

Built as a learning + portfolio project with a focus on **real-world ML thinking**.

---

⭐ If you find this project useful or insightful, feel free to star the repo.