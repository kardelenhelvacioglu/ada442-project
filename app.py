# Import necessary libraries
import streamlit as st  # For creating the Streamlit web app
import pandas as pd     # For handling dataframes
from streamlit_router import StreamlitRouter  # For page routing within Streamlit
import pickle  # For loading the trained model from a file

# Function to load the machine learning model (cached to avoid reloading every time)
@st.cache_resource()
def load_model():
    with open("best_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

# Load the model once and store it
model = load_model()

# === FUNCTION TO CREATE PREDICTION FORM PAGE ===
def create_interface():
    # Sidebar content with project and team details
    with st.sidebar:
        st.markdown("""
            <div style="background-color:#e0e0e0; padding:20px; border-radius:10px;">
                <h2 style="color:#b03b6b; font-size:24px;">🎓 ADA442 Project</h2>
                <p style="font-size:16px;">Welcome to the Term Deposit Predictor App</p>
                <hr style="border:1px solid #f0b7cd;">
                <h4 style="margin-top:20px; color:#7a2c4f;">👥 Group Members:</h4>
                <ul style="padding-left: 20px; font-size:16px; line-height:1.8;">
                    <li>İdil Yakut</li>
                    <li>Helin Kahraman</li>
                    <li>Kardelen Helvacıoğlu</li>
                </ul>
                <hr style="border:1px dashed #f3a6c0;">
                <p style="font-style: italic; font-size:15px; color:#5e3a47;">
                    💡 "Predict the future, one input at a time."
                </p>
            </div>
        """, unsafe_allow_html=True)

    # General styling for the prediction page using custom CSS
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
            html, body, [class*="css"] {
                font-family: 'Poppins', sans-serif;
                background-color: #ffe4ec;
                color: #3d2f1b;
            }
            .main-title {
                font-size: 32px;
                font-weight: 700;
                color: #2e230a;
                text-align: center;
                margin-bottom: 25px;
            }
            .section {
                background-color: #fddde6;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 12px;
                box-shadow: 0px 1px 8px rgba(220, 100, 140, 0.08);
                border: 1px solid #f7c7d9;
                max-width: 800px;
                margin-left: auto;
                margin-right: auto;
            }
            .section h4 {
                color: #4b3832;
                font-size: 24px;
                font-weight: 700;
                text-align: center;
                margin-bottom: 18px;
                border-bottom: 2px dashed #e0c98f;
                padding-bottom: 6px;
            }
            label {
                font-weight: 500 !important;
                color: #4e3a1e !important;
            }
            .stButton > button {
                background-color: #ec94b8;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                height: 45px;
                width: 100%;
                transition: 0.3s;
                border: none;
                box-shadow: 0px 2px 4px rgba(200, 80, 120, 0.2);
            }
            .stButton > button:hover {
                background-color: #e279a5;
                transform: scale(1.02);
            }
            .block-container {
                max-width: 900px !important;
                padding-left: 2rem;
                padding-right: 2rem;
                margin-left: auto;
                margin-right: auto;
            }
        </style>
    """, unsafe_allow_html=True)

    # Title of the form
    st.markdown('<div class="main-title">📈 Bank Term Deposit Prediction</div>', unsafe_allow_html=True)

    # Create the prediction input form
    with st.form("prediction_form"):
        # Section: Personal Info
        st.markdown('<div class="section"><h4>👤 Personal Information</h4>', unsafe_allow_html=True)
        age = st.number_input("Age", min_value=18, max_value=100)
        job = st.selectbox("Job", [...])
        marital = st.selectbox("Marital Status", [...])
        education = st.selectbox("Education Level", [...])
        st.markdown("</div>", unsafe_allow_html=True)

        # Section: Financial
        st.markdown('<div class="section"><h4>💳 Financial Status</h4>', unsafe_allow_html=True)
        default = st.selectbox("Credit Default?", [...])
        housing = st.selectbox("Housing Loan?", [...])
        loan = st.selectbox("Personal Loan?", [...])
        st.markdown("</div>", unsafe_allow_html=True)

        # Section: Contact Info
        st.markdown('<div class="section"><h4>📞 Contact Information</h4>', unsafe_allow_html=True)
        contact_type = st.selectbox("Contact Type", [...])
        month = st.selectbox("Month of Contact", [...])
        day_of_week = st.selectbox("Day of the Week", [...])
        st.markdown("</div>", unsafe_allow_html=True)

        # Section: Campaign Info
        st.markdown('<div class="section"><h4>📊 Campaign Details</h4>', unsafe_allow_html=True)
        duration = st.number_input("Duration of Last Contact (seconds)", 0)
        campaign = st.number_input("Number of Contacts During Campaign", 0)
        pdays = st.number_input("Days Since Last Contact", 0, value=999)
        previous = st.number_input("Number of Contacts Before Campaign", 0)
        st.markdown("</div>", unsafe_allow_html=True)

        # Section: Previous Campaign
        st.markdown('<div class="section"><h4>📁 Previous Campaign Outcome</h4>', unsafe_allow_html=True)
        poutcome = st.selectbox("Outcome of Previous Campaign", [...])
        st.markdown("</div>", unsafe_allow_html=True)

        # Section: Economic Indicators
        st.markdown('<div class="section"><h4>📈 Economic Indicators</h4>', unsafe_allow_html=True)
        emp_var_rate = st.number_input("Employment Variation Rate", format="%.2f")
        cons_price_idx = st.number_input("Consumer Price Index", format="%.2f")
        cons_conf_idx = st.number_input("Consumer Confidence Index", step=0.1, format="%.2f")
        euribor3m = st.number_input("Euribor 3 Month Rate", format="%.3f")
        nr_employed = st.number_input("Number of Employees", step=1)
        st.markdown("</div>", unsafe_allow_html=True)

        # Submit button to run the prediction
        submitted = st.form_submit_button("🔮 Predict")

        # If form submitted, generate prediction
        if submitted:
            # Prepare data for prediction
            data = {
                'age': [age], 'duration': [duration], 'campaign': [campaign],
                'pdays': [pdays], 'previous': [previous],
                'emp.var.rate': [emp_var_rate], 'cons.price.idx': [cons_price_idx],
                'cons.conf.idx': [cons_conf_idx], 'euribor3m': [euribor3m],
                'nr.employed': [nr_employed],

                # One-hot encoding for categorical features
                **{f'job_{j}': [1 if job == j else 0] for j in [...]},
                **{f'marital_{m}': [1 if marital == m else 0] for m in [...]},
                **{f'education_{e}': [1 if education == e else 0] for e in [...]},
                'default_unknown': [1 if default == 'unknown' else 0],
                'default_yes': [1 if default == 'yes' else 0],
                'housing_unknown': [1 if housing == 'unknown' else 0],
                'housing_yes': [1 if housing == 'yes' else 0],
                'loan_unknown': [1 if loan == 'unknown' else 0],
                'loan_yes': [1 if loan == 'yes' else 0],
                'contact_telephone': [1 if contact_type == 'telephone' else 0],
                **{f'month_{m}': [1 if month == m else 0] for m in [...]},
                **{f'day_of_week_{d}': [1 if day_of_week == d else 0] for d in [...]},
                'poutcome_nonexistent': [1 if poutcome == 'nonexistent' else 0],
                'poutcome_success': [1 if poutcome == 'success' else 0]
            }

            # Convert data to DataFrame for model
            input_df = pd.DataFrame(data)

            # Predict using the model
            prediction = model.predict(input_df)[0]

            # Show result based on prediction
            if prediction == 1:
                st.markdown("""
                    <div style='background-color:#d4edda; padding:20px; border-radius:10px; border: 2px solid #a0d5a0; margin-top:20px;'>
                        <h3 style='color:#155724; text-align:center; font-size:28px;'>✅ Prediction: Subscribed (Yes)</h3>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='background-color:#f8d7da; padding:20px; border-radius:10px; border: 2px solid #e8a4a7; margin-top:20px;'>
                        <h3 style='color:#721c24; text-align:center; font-size:28px;'>❌ Prediction: Not Subscribed (No)</h3>
                    </div>
                """, unsafe_allow_html=True)

# === FUNCTION FOR THE WELCOME PAGE ===
def welcome_page(router):
    # Style for welcome page
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
            html, body, [class*="css"] {
                font-family: 'Poppins', sans-serif;
                background-color: #e0f0ff;
                color: #2f2f2f;
            }
            .main-title {
                font-size: 56px;
                font-weight: 800;
                color: #1e3a5f;
                text-align: center;
                margin-top: 50px;
                margin-bottom: 20px;
            }
            .subtitle {
                font-size: 28px;
                color: #315475;
                text-align: center;
                margin-bottom: 30px;
            }
            .member-list {
                font-size: 22px;
                text-align: center;
                color: #3c3c3c;
                line-height: 2.2;
                margin-bottom: 40px;
            }
            .predict-instruction {
                font-size: 20px;
                text-align: center;
                color: #555;
                margin-bottom: 20px;
            }
            .stButton > button {
                background-color: #70b8ff;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border-radius: 12px;
                height: 55px;
                width: 100%;
                margin-top: 10px;
                transition: 0.3s;
                border: none;
                box-shadow: 0px 3px 6px rgba(80, 120, 180, 0.3);
            }
            .stButton > button:hover {
                background-color: #51a5ec;
                transform: scale(1.04);
            }
        </style>
    """, unsafe_allow_html=True)

    # Display welcome content
    st.markdown('<div class="main-title">🎓 ADA442 Project</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Welcome to the Term Deposit Predictor App</div>', unsafe_allow_html=True)
    st.markdown('<div class="member-list">Group Members:<br>İdil Yakut<br>Helin Kahraman<br>Kardelen Helvacıoğlu</div>', unsafe_allow_html=True)
    st.markdown('<div class="predict-instruction">To start your prediction, please click the button below:</div>', unsafe_allow_html=True)

    # Button to navigate to prediction form
    if st.button("🚀 Begin Prediction"):
        router.redirect("/data_input")

# === PAGE ROUTER SETUP ===
router = StreamlitRouter()
router.register(welcome_page, "/")            # Register welcome page
router.register(create_interface, "/data_input")  # Register prediction input page
router.serve()  # Start the router







