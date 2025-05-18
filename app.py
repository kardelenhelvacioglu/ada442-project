#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""streamlit_app.py – Bank Term Deposit Predictor
------------------------------------------------
Author: ADA442 Project Team (İdil Yakut, Helin Kahraman, Kardelen Helvacıoğlu)
Description: Streamlit web application that loads a pickled ML model and
             predicts whether a client will subscribe to a term deposit.
"""

# =============================
# Imports
# =============================
import streamlit as st
import pandas as pd
import pickle
from streamlit_router import StreamlitRouter

# =============================
# Constants – categorical vocab
# =============================
JOB_OPTIONS = [
    "admin.", "blue-collar", "entrepreneur", "management", "retired",
    "self-employed", "services", "student", "technician", "unemployed",
    "unknown",
]

MARITAL_OPTIONS = ["single", "married", "divorced", "unknown"]
EDU_OPTIONS = ["primary", "secondary", "tertiary", "unknown"]
DEFAULT_OPTIONS = ["no", "yes", "unknown"]
HOUSING_OPTIONS = ["no", "yes", "unknown"]
LOAN_OPTIONS = ["no", "yes", "unknown"]
CONTACT_OPTIONS = ["cellular", "telephone"]
MONTH_OPTIONS = [
    "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
    "sep", "oct", "nov", "dec",
]
DOW_OPTIONS = ["mon", "tue", "wed", "thu", "fri"]
POUTCOME_OPTIONS = ["nonexistent", "failure", "success"]

# =============================
# Model loader (cached)
# =============================
@st.cache_resource()
def load_model():
    with open("best_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

# =============================
# Prediction form page
# =============================

def create_interface():
    # Sidebar – project info
    with st.sidebar:
        st.markdown(
            """
            <div style="background-color:#e0e0e0; padding:20px; border-radius:10px;">
              <h2 style="color:#b03b6b; font-size:24px;">🎓 ADA442 Project</h2>
              <p style="font-size:16px;">Term Deposit Predictor App</p>
              <hr style="border:1px solid #f0b7cd;">
              <h4 style="margin-top:20px; color:#7a2c4f;">👥 Group Members:</h4>
              <ul style="padding-left: 20px; font-size:16px; line-height:1.8;">
                  <li>İdil Yakut</li>
                  <li>Helin Kahraman</li>
                  <li>Kardelen Helvacıoğlu</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------- Styling ----------
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
        html, body, [class*="css"] {font-family:'Poppins',sans-serif; background-color:#ffe4ec; color:#3d2f1b;}
        .main-title{font-size:32px;font-weight:700;color:#2e230a;text-align:center;margin-bottom:25px;}
        .section{background-color:#fddde6;padding:20px;margin-bottom:20px;border-radius:12px;box-shadow:0 1px 8px rgba(220,100,140,.08);border:1px solid #f7c7d9;max-width:800px;margin:auto;}
        .section h4{color:#4b3832;font-size:24px;font-weight:700;text-align:center;margin-bottom:18px;border-bottom:2px dashed #e0c98f;padding-bottom:6px;}
        label{font-weight:500!important;color:#4e3a1e!important;}
        .stButton>button{background-color:#ec94b8;color:white;font-size:16px;font-weight:bold;border-radius:10px;height:45px;width:100%;border:none;transition:.3s;box-shadow:0 2px 4px rgba(200,80,120,.2);} .stButton>button:hover{background-color:#e279a5;transform:scale(1.02);}
        .block-container{max-width:900px!important;padding-left:2rem;padding-right:2rem;margin:auto;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="main-title">📈 Bank Term Deposit Prediction</div>', unsafe_allow_html=True)

    # ---------- Form ----------
    with st.form("prediction_form"):
        # Personal Info
        st.markdown('<div class="section"><h4>👤 Personal Information</h4>', unsafe_allow_html=True)
        age = st.number_input("Age", min_value=18, max_value=100)
        job = st.selectbox("Job", JOB_OPTIONS)
        marital = st.selectbox("Marital Status", MARITAL_OPTIONS)
        education = st.selectbox("Education Level", EDU_OPTIONS)
        st.markdown("</div>", unsafe_allow_html=True)

        # Financial
        st.markdown('<div class="section"><h4>💳 Financial Status</h4>', unsafe_allow_html=True)
        default = st.selectbox("Credit Default?", DEFAULT_OPTIONS)
        housing = st.selectbox("Housing Loan?", HOUSING_OPTIONS)
        loan = st.selectbox("Personal Loan?", LOAN_OPTIONS)
        st.markdown("</div>", unsafe_allow_html=True)

        # Contact Info
        st.markdown('<div class="section"><h4>📞 Contact Information</h4>', unsafe_allow_html=True)
        contact_type = st.selectbox("Contact Type", CONTACT_OPTIONS)
        month = st.selectbox("Month of Contact", MONTH_OPTIONS)
        day_of_week = st.selectbox("Day of the Week", DOW_OPTIONS)
        st.markdown("</div>", unsafe_allow_html=True)

        # Campaign Info
        st.markdown('<div class="section"><h4>📊 Campaign Details</h4>', unsafe_allow_html=True)
        duration = st.number_input("Duration of Last Contact (seconds)", 0)
        campaign = st.number_input("Number of Contacts During Campaign", 0)
        pdays = st.number_input("Days Since Last Contact", 0, value=999)
        previous = st.number_input("Number of Contacts Before Campaign", 0)
        st.markdown("</div>", unsafe_allow_html=True)

        # Previous Campaign
        st.markdown('<div class="section"><h4>📁 Previous Campaign Outcome</h4>', unsafe_allow_html=True)
        poutcome = st.selectbox("Outcome of Previous Campaign", POUTCOME_OPTIONS)
        st.markdown("</div>", unsafe_allow_html=True)

        # Economic Indicators
        st.markdown('<div class="section"><h4>📈 Economic Indicators</h4>', unsafe_allow_html=True)
        emp_var_rate = st.number_input("Employment Variation Rate", format="%.2f")
        cons_price_idx = st.number_input("Consumer Price Index", format="%.2f")
        cons_conf_idx = st.number_input("Consumer Confidence Index", step=0.1, format="%.2f")
        euribor3m = st.number_input("Euribor 3‑Month Rate", format="%.3f")
        nr_employed = st.number_input("Number of Employees", step=1)
        st.markdown("</div>", unsafe_allow_html=True)

        submitted = st.form_submit_button("🔮 Predict")

        if submitted:
            # Assemble input row
            data = {
                "age": [age],
                "duration": [duration],
                "campaign": [campaign],
                "pdays": [pdays],
                "previous": [previous],
                "emp.var.rate": [emp_var_rate],
                "cons.price.idx": [cons_price_idx],
                "cons.conf.idx": [cons_conf_idx],
                "euribor3m": [euribor3m],
                "nr.employed": [nr_employed],
                # One‑hot
                **{f"job_{j}": [1 if job == j else 0] for j in JOB_OPTIONS},
                **{f"marital_{m}": [1 if marital == m else 0] for m in MARITAL_OPTIONS},
                **{f"education_{e}": [1 if education == e else 0] for e in EDU_OPTIONS},
                "default_unknown": [1 if default == "unknown" else 0],
                "default_yes": [1 if default == "yes" else 0],
                "housing_unknown": [1 if housing == "unknown" else 0],
                "housing_yes": [1 if housing == "yes" else 0],
                "loan_unknown": [1 if loan == "unknown" else 0],
                "loan_yes": [1 if loan == "yes" else 0],
                "contact_telephone": [1 if contact_type == "telephone" else 0],
                **{f"month_{m}": [1 if month == m else 0] for m in MONTH_OPTIONS},
                **{f"day_of_week_{d}": [1 if day_of_week == d else 0] for d in DOW_OPTIONS},
                "poutcome_nonexistent": [1 if poutcome == "nonexistent" else 0],
                "poutcome_success": [1 if poutcome == "success" else 0],
            }

            input_df = pd.DataFrame(data)
            prediction = model.predict(input_df)[0]

            if prediction == 1:
                st.success("✅ Prediction: Subscribed (Yes)")
            else:
                st.error("❌ Prediction: Not Subscribed (No)")

# =============================
# Welcome page
# =============================

def welcome_page(router):
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
        html, body, [class*="css"] {font-family:'Poppins',sans-serif;background-color:#e0f0ff;color:#2f2f2f;}
        .main-title{font-size:56px;font-weight:800;color:#1e3a5f;text-align:center;margin:50px 0 20px;}
        .subtitle{font-size:28px;color:#315475;text-align:center;margin-bottom:30px;}
        .member-list{font-size:22px;text-align:center;color:#3c3c3c;line-height:2.2;margin-bottom:40px;}
        .predict-instruction{font-size:20px;text-align:center;color:#555;margin-bottom:20px;}
        .stButton>button{background-color:#70b8ff;color:white;font-size:20px;font-weight:bold;border-radius:12px;height:55px;width:100%;margin-top:10px;border:none;transition:.3s;box-shadow:0 3px 6px rgba(80,120,180,.3);} .stButton>button:hover{background-color:#51a5ec;transform:scale(1.04);}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="main-title">🎓 ADA442 Project</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Term Deposit Predictor App</div>', unsafe_allow_html=True)
    st.markdown('<div class="member-list">Group Members:<br>İdil Yakut<br>Helin Kahraman<br>Kardelen Helvacıoğlu</div>', unsafe_allow_html=True)
    st.markdown('<div class="predict-instruction">Click below to begin your prediction:</div>', unsafe_allow_html=True)

    if st.button("🚀 Begin Prediction"):
        router.redirect("/data_input")

# =============================
# Routing
# =============================

router = StreamlitRouter()
router.register(welcome_page, "/")
router.register(create_interface, "/data_input")
router.serve()


# In[ ]:




