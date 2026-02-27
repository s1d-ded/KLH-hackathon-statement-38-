import streamlit as st
import sqlite3
import joblib
import numpy as np
import os
from datetime import datetime
import time

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AgriScore",
    layout="wide",
    page_icon="🌾"
)

# -------------------------------------------------
# CUSTOM UI STYLING (UNCHANGED LOGIC)
# -------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    background-attachment: fixed;
    color: white;
}

header {visibility: hidden;}
footer {visibility: hidden;}

.stButton>button {
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 30px;
    padding: 10px 30px;
    border: none;
    font-weight: bold;
    transition: 0.3s ease;
}
.stButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0,114,255,0.5);
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    transition: 0.3s ease;
}
div[data-testid="stMetric"]:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LANGUAGE DICTIONARY
# -------------------------------------------------
languages = {
    "English": {
        "app_title": "AgriScore",
        "tagline": "Smart Credit Scoring for Indian Agriculture",
        "login": "Login",
        "register": "Register",
        "username": "Username",
        "password": "Password",
        "new_username": "New Username",
        "new_password": "New Password",
        "farmer_dashboard": "Farmer Dashboard",
        "fill_details": "Fill Farm Details",
        "soil": "Soil Health (%)",
        "rainfall": "Rainfall Deviation (%)",
        "yield_perf": "Yield Performance",
        "yield_stability": "Yield Stability",
        "repayment": "Repayment History",
        "income_history": "Income History",
        "income_3": "Income - 3 yrs ago",
        "income_2": "Income - 2 yrs ago",
        "income_last": "Income - Last year",
        "income_current": "Current Income",
        "debt": "Total Current Debt",
        "debt_ratio": "Calculated Debt-to-Income Ratio",
        "generate": "Generate Trust Score",
        "trust_score": "Trust Score",
        "high": "High Approval Chance",
        "manual": "Manual Review Required",
        "risk": "High Risk",
        "logout": "Logout",
        "invalid": "Invalid credentials",
        "exists": "Username already exists",
        "registered": "Registered successfully"
    },

    "Hindi": {
        "app_title": "एग्रीस्कोर",
        "tagline": "भारतीय कृषि के लिए स्मार्ट क्रेडिट स्कोरिंग",
        "login": "लॉगिन",
        "register": "पंजीकरण",
        "username": "यूज़रनेम",
        "password": "पासवर्ड",
        "new_username": "नया यूज़रनेम",
        "new_password": "नया पासवर्ड",
        "farmer_dashboard": "किसान डैशबोर्ड",
        "fill_details": "खेत विवरण भरें",
        "soil": "मिट्टी स्वास्थ्य (%)",
        "rainfall": "वर्षा विचलन (%)",
        "yield_perf": "उपज प्रदर्शन",
        "yield_stability": "उपज स्थिरता",
        "repayment": "भुगतान इतिहास",
        "income_history": "आय इतिहास",
        "income_3": "3 साल पहले की आय",
        "income_2": "2 साल पहले की आय",
        "income_last": "पिछले साल की आय",
        "income_current": "वर्तमान आय",
        "debt": "कुल वर्तमान ऋण",
        "debt_ratio": "ऋण-आय अनुपात",
        "generate": "विश्वास स्कोर उत्पन्न करें",
        "trust_score": "विश्वास स्कोर",
        "high": "उच्च स्वीकृति संभावना",
        "manual": "मैनुअल समीक्षा आवश्यक",
        "risk": "उच्च जोखिम",
        "logout": "लॉगआउट",
        "invalid": "गलत लॉगिन विवरण",
        "exists": "यूज़रनेम पहले से मौजूद है",
        "registered": "सफलतापूर्वक पंजीकरण हुआ"
    },

    "Telugu": {
        "app_title": "అగ్రిస్కోర్",
        "tagline": "భారతీయ వ్యవసాయానికి స్మార్ట్ క్రెడిట్ స్కోరింగ్",
        "login": "లాగిన్",
        "register": "నమోదు",
        "username": "యూజర్ పేరు",
        "password": "పాస్‌వర్డ్",
        "new_username": "కొత్త యూజర్ పేరు",
        "new_password": "కొత్త పాస్‌వర్డ్",
        "farmer_dashboard": "రైతు డ్యాష్‌బోర్డ్",
        "fill_details": "వ్యవసాయ వివరాలు నమోదు చేయండి",
        "soil": "మట్టి ఆరోగ్యం (%)",
        "rainfall": "వర్షపు వ్యత్యాసం (%)",
        "yield_perf": "పంట పనితీరు",
        "yield_stability": "పంట స్థిరత్వం",
        "repayment": "చెల్లింపు చరిత్ర",
        "income_history": "ఆదాయం చరిత్ర",
        "income_3": "3 సంవత్సరాల క్రితం ఆదాయం",
        "income_2": "2 సంవత్సరాల క్రితం ఆదాయం",
        "income_last": "గత సంవత్సరం ఆదాయం",
        "income_current": "ప్రస్తుత ఆదాయం",
        "debt": "ప్రస్తుత మొత్తం అప్పు",
        "debt_ratio": "అప్పు-ఆదాయం నిష్పత్తి",
        "generate": "నమ్మక స్కోర్ రూపొందించండి",
        "trust_score": "నమ్మక స్కోర్",
        "high": "అధిక ఆమోద అవకాశం",
        "manual": "మాన్యువల్ సమీక్ష అవసరం",
        "risk": "అధిక ప్రమాదం",
        "logout": "లాగ్ అవుట్",
        "invalid": "తప్పు వివరాలు",
        "exists": "యూజర్ ఇప్పటికే ఉంది",
        "registered": "విజయవంతంగా నమోదు అయ్యింది"
    }
}

selected_language = st.selectbox("🌐 Language", list(languages.keys()))
T = languages[selected_language]

# -------------------------------------------------
# DATABASE + MODEL (UNCHANGED)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "agri_credit.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

MODEL_PATH = os.path.join(BASE_DIR, "agri_credit_xgb_model.pkl")
model = joblib.load(MODEL_PATH)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "credit_score" not in st.session_state:
    st.session_state.credit_score = None

# -------------------------------------------------
# LOGIN PAGE
# -------------------------------------------------
if not st.session_state.logged_in:

    st.title(T["app_title"])
    st.subheader(T["tagline"])

    tab1, tab2 = st.tabs([T["login"], T["register"]])

    with tab1:
        user = st.text_input(T["username"])
        pwd = st.text_input(T["password"], type="password")

        if st.button(T["login"]):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
            if cur.fetchone():
                st.session_state.logged_in = True
                st.session_state.username = user
                st.rerun()
            else:
                st.error(T["invalid"])
            conn.close()

    with tab2:
        new_user = st.text_input(T["new_username"])
        new_pwd = st.text_input(T["new_password"], type="password")

        if st.button(T["register"]):
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO users (username,password) VALUES (?,?)",(new_user,new_pwd))
                conn.commit()
                st.success(T["registered"])
            except:
                st.error(T["exists"])
            conn.close()

# -------------------------------------------------
# DASHBOARD (100% ORIGINAL LOGIC PRESERVED)
# -------------------------------------------------
else:

    st.title(T["farmer_dashboard"])
    st.write(f"Welcome, {st.session_state.username}")

    with st.expander(T["fill_details"], expanded=True):

        soil = st.number_input(T["soil"], 0.0, 100.0)
        rainfall = st.number_input(T["rainfall"], 0.0, 100.0)

        yield_map = {"Above Average":85,"Average":60,"Below Average":40}
        yield_choice = st.selectbox(T["yield_perf"], list(yield_map.keys()))

        yield_stability_map = {
            "Very Stable": 0.9,
            "Moderately Stable": 0.6,
            "Unstable": 0.3
        }
        yield_stability_choice = st.selectbox(T["yield_stability"], list(yield_stability_map.keys()))

        repayment_map = {"Defaulted":0,"Delayed":1,"On Time":2}
        repayment_choice = st.selectbox(T["repayment"], list(repayment_map.keys()))

        st.subheader(T["income_history"])

        incomes = np.array([
            st.number_input(T["income_3"],0.0),
            st.number_input(T["income_2"],0.0),
            st.number_input(T["income_last"],0.0),
            st.number_input(T["income_current"],0.0)
        ])

        if np.mean(incomes) > 0:
            var_ratio = np.std(incomes) / np.mean(incomes)
            if var_ratio < 0.15:
                income_stability = 0.9
            elif var_ratio < 0.30:
                income_stability = 0.6
            else:
                income_stability = 0.3
        else:
            income_stability = 0.3

        total_debt = st.number_input(T["debt"], 0.0)

        if incomes[-1] > 0:
            debt_ratio = min(total_debt / incomes[-1], 1.0)
        else:
            debt_ratio = 1.0

        st.write(f"{T['debt_ratio']}: {debt_ratio:.2f}")

        if st.button(T["generate"]):

            input_data = np.array([[soil,
                                    yield_map[yield_choice],
                                    yield_stability_map[yield_stability_choice],
                                    repayment_map[repayment_choice],
                                    income_stability,
                                    rainfall,
                                    debt_ratio]])

            risk = model.predict(input_data)[0]
            risk = np.clip(risk,0,1)
            score = 100*(1-risk)

            st.session_state.credit_score = score

            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO applications (
            username,soil_health_score,traditional_yield_index,
            yield_stability_score,previous_repayment_score,
            income_stability_score,rainfall_deviation_percent,
            debt_to_income_ratio,predicted_risk,credit_score,
            decision,timestamp)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (st.session_state.username,
             soil,
             yield_map[yield_choice],
             yield_stability_map[yield_stability_choice],
             repayment_map[repayment_choice],
             income_stability,
             rainfall,
             debt_ratio,
             risk,
             score,
             "Generated",
             datetime.now()))
            conn.commit()
            conn.close()

    if st.session_state.credit_score is not None:

        st.subheader(T["trust_score"])
        st.metric("Credit Score", f"{st.session_state.credit_score:.2f}/100")

        if st.session_state.credit_score > 65:
            st.success(T["high"])
        elif st.session_state.credit_score > 40:
            st.warning(T["manual"])
        else:
            st.error(T["risk"])

    if st.button(T["logout"]):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.credit_score = None
        st.rerun()
