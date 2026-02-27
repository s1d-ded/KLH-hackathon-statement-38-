import numpy as np
import pandas as pd

np.random.seed(42)

# 🔥 Increase sample size
n_samples = 20000   # you can change to 5000 if needed

# -----------------------------
# Generate Features (Within Constraints)
# -----------------------------

soil = np.random.uniform(20, 100, n_samples)

yield_index = np.random.uniform(30, 100, n_samples)

yield_stability = np.random.uniform(0.2, 1.0, n_samples)

repayment = np.random.randint(0, 3, n_samples)

income_stability = np.random.uniform(0, 1, n_samples)

rainfall = np.random.uniform(0, 50, n_samples)

debt_ratio = np.random.uniform(0, 1, n_samples)

# -----------------------------
# Normalize
# -----------------------------

soil_norm = soil / 100
yield_norm = yield_index / 100
rainfall_norm = rainfall / 50
repayment_norm = repayment / 2

# -----------------------------
# Hidden Risk Formula
# -----------------------------

risk_score = (
    0.30 * (1 - repayment_norm)
    + 0.20 * debt_ratio
    + 0.15 * (1 - soil_norm)
    + 0.15 * (1 - yield_stability)
    + 0.10 * rainfall_norm
    + 0.05 * (1 - yield_norm)
    + 0.05 * (1 - income_stability)
)

# Add slight noise
# Add controlled noise
risk_score += np.random.normal(0, 0.05, n_samples)

# Keep within 0-1
risk_score = np.clip(risk_score, 0, 1)

# -----------------------------
# Create DataFrame
# -----------------------------

df = pd.DataFrame({
    "soil_health_score": soil,
    "traditional_yield_index": yield_index,
    "yield_stability_score": yield_stability,
    "previous_repayment_score": repayment,
    "income_stability_score": income_stability,
    "rainfall_deviation_percent": rainfall,
    "debt_to_income_ratio": debt_ratio,
    "risk_score": risk_score
})

# Save CSV
df.to_csv("synthetic_agri_credit_data_10k.csv", index=False)

print("Dataset generated successfully.")
print("Shape:", df.shape)
print(df.head())
