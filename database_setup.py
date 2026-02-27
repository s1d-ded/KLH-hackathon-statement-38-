import sqlite3

# Create database file
conn = sqlite3.connect("agri_credit.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    soil_health_score REAL,
    traditional_yield_index REAL,
    yield_stability_score REAL,
    previous_repayment_score INTEGER,
    income_stability_score REAL,
    rainfall_deviation_percent REAL,
    debt_to_income_ratio REAL,
    predicted_risk REAL,
    credit_score REAL,
    decision TEXT,
    timestamp TEXT
)
""")

conn.commit()
conn.close()

print("Database and table created successfully.")
