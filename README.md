# KLH-hackathon-statement-38-
predict or guesstimate the credit score of a farmer for loan based on non traditional crop history and soil health data
firsts download require🌾 KrishiScore
Smart Agricultural Credit Risk Assessment System
📌 Overview

AgriScore is an AI-powered agricultural credit evaluation system designed to assist lenders in assessing farmer creditworthiness using both traditional and non-traditional agricultural indicators.

The system leverages:

Soil health data

Yield performance and stability

Income consistency

Rainfall deviation

Debt exposure

Loan repayment history

An XGBoost machine learning model predicts risk probability, which is converted into a Trust Score (0–100) to help lenders make faster and fairer decisions.

🚀 Key Features

🔐 User Authentication (Login / Register)

🌱 Farm Data Input Interface

🤖 ML-Based Risk Prediction (XGBoost)

📊 Trust Score Calculation (0–100 scale)

🧾 Risk Breakdown for Explainability

💾 SQLite Database Storage

🧠 Income Stability & Debt Ratio Auto-Calculation

🏗 System Architecture
User (Farmer)
        │
        ▼
Streamlit UI
        │
        ▼
Application Logic (app.py)
        │
        ├── SQLite Database
        └── XGBoost Model (.pkl)
                │
                ▼
        Risk Probability (0–1)
                │
                ▼
        Trust Score (0–100)
📊 Machine Learning Model
Algorithm Used

XGBoost Regressor / Binary Logistic Model

Input Features (7 Total)

Soil Health Score (%)

Traditional Yield Index

Yield Stability Score

Previous Repayment Score

Income Stability Score

Rainfall Deviation (%)

Debt-to-Income Ratio

📐 Trust Score Formula

The model predicts:

risk ∈ [0, 1]

Credit Score is calculated as:

Credit Score = 100 × (1 − risk)

Interpretation:

Risk	Credit Score
0.0	100
0.5	50
1.0	0

Decision Bands:

> 65 → High Approval Chance

40–65 → Manual Review

< 40 → High Risk

📈 Income Stability Calculation

Income stability is calculated using the standard deviation of the past 4 years’ income:

variation_ratio = std(income) / mean(income)

Classification:

< 15% → Stable (0.9)

15–30% → Moderate (0.6)

30% → Unstable (0.3)

💰 Debt-to-Income Ratio
Debt Ratio = Total Debt / Current Income

Clipped to maximum 1.0 for stability.

🗄 Database Structure
Table: users
Column	Type
id	INTEGER
username	TEXT
password	TEXT
Table: applications
Column	Description
username	Applicant
soil_health_score	Soil %
traditional_yield_index	Yield category score
yield_stability_score	Stability score
previous_repayment_score	Repayment category
income_stability_score	Calculated score
rainfall_deviation_percent	Rainfall %
debt_to_income_ratio	Calculated ratio
predicted_risk	Model output
credit_score	Final trust score
decision	Risk band
timestamp	Submission time
📂 Project Structure
credit_score_predicter/
│
├── app.py
├── agri_credit.db
├── agri_credit_xgb_model.pkl
├── synthetic_dataset_20k.csv
└── README.md
⚙ Installation & Setup
1️⃣ Clone Repository
git clone <repo-url>
cd credit_score_predicter
2️⃣ Install Dependencies
pip install streamlit numpy pandas scikit-learn xgboost joblib
3️⃣ Run Application
streamlit run app.py
🔄 Application Flow
User Login/Register
        ↓
Enter Farm Details
        ↓
Income Stability & Debt Ratio Calculated
        ↓
Feature Vector Created (7 Features)
        ↓
Model Predicts Risk
        ↓
Trust Score Generated
        ↓
Result Displayed + Saved to DB
🧠 Why This Matters

Traditional agricultural credit scoring often relies on:

Collateral

Formal financial history

KrishiScore introduces:

Climate sensitivity

Income consistency analysis

Agricultural performance indicators

Data-driven fairness

This improves:

Credit access

Risk transparency

Decision speed

⚠ Limitations

Uses synthetic training data

No external API integration (weather/soil validation)

No document verification system

Simplified financial modeling assumptions

🔮 Future Improvements

Real-time weather API integration

SHAP-based explainability visualization

Loan amount recommendation engine

Multi-role dashboard (Farmer / Lender)

Secure password hashing

Production deployment with FastAPI backend

🏁 Conclusion

KrishiScore demonstrates how machine learning can assist agricultural finance by transforming complex risk indicators into a transparent and interpretable Trust Score.

It provides a scalable foundation for modern agri-fintech systems.
