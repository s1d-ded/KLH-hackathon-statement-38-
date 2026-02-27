import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv("synthetic_dataset_20k.csv")

# -----------------------------
# Define Features & Target
# -----------------------------

features = [
    "soil_health_score",
    "traditional_yield_index",
    "yield_stability_score",
    "previous_repayment_score",
    "income_stability_score",
    "rainfall_deviation_percent",
    "debt_to_income_ratio"
]

X = df[features]
y = df["risk_score"]

# -----------------------------
# Train-Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Initialize XGBoost Regressor
# -----------------------------

model = XGBRegressor(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

# -----------------------------
# Evaluate Model
# -----------------------------

y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print("\nModel Performance")
print("------------------")
print("R² Score:", round(r2, 4))
print("MAE:", round(mae, 4))

# -----------------------------
# Save Model
# -----------------------------

joblib.dump(model, "agri_credit_xgb_model.pkl")
print("\nModel saved as agri_credit_xgb_model.pkl")
