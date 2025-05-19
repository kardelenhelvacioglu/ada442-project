import streamlit as st
import pandas as pd
from streamlit_router import StreamlitRouter
import pickle


@st.cache_resource()
def load_model():
    with open("best_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

def create_interface():
    
    st.title("ADA442 Final Project")

    st.header("Personal Information")
    age = st.slider("Age", min_value=18, max_value=100)
    
    st.header("Campaign Information")
    duration = st.number_input("Duration", min_value=0)
    campaign = st.number_input("Campaign", min_value=0)
    pdays = st.number_input("Pdays", min_value=0, value=999)
    previous = st.number_input("Previous", min_value=0)
    
    st.header("Employment and Economic Indicators")
    emp_var_rate = st.number_input("Employment Variation Rate", format="%.2f")
    cons_price_idx = st.number_input("Consumer Price Index", format="%.2f")
    cons_conf_idx = st.number_input("Consumer Confidence Index", step=0.1, format="%.2f")
    euribor3m = st.number_input("3 Month Euribor Rate", format="%.3f")
    nr_employed = st.number_input("Number of Employees", step=1)
    
    st.header("Job Information")
    job_mapping = {
        'Blue Collar': 'blue-collar', 
        'Entrepreneur': 'entrepreneur', 
        'Housemaid': 'housemaid', 
        'Management': 'management', 
        'Retired': 'retired', 
        'Self-employed': 'self-employed', 
        'Services': 'services', 
        'Student': 'student', 
        'Technician': 'technician', 
        'Unemployed': 'unemployed', 
        'Unknown': 'unknown'
    }
    job_display = st.selectbox("Job", list(job_mapping.keys()))
    job = job_mapping[job_display]
    
    st.header("Marital Status")
    marital_mapping = {
        'Married': 'married', 
        'Single': 'single', 
        'Unknown': 'unknown'
    }
    marital_display = st.selectbox("Marital Status", list(marital_mapping.keys()))
    marital = marital_mapping[marital_display]

    st.header("Education")
    education_mapping = {
        'Basic 6 years': 'basic.6y', 
        'Basic 9 years': 'basic.9y', 
        'High School': 'high.school',
        'Illiterate': 'illiterate', 
        'Professional Course': 'professional.course',
        'University Degree': 'university.degree', 
        'Unknown': 'unknown'
    }
    education_display = st.selectbox("Education Level", list(education_mapping.keys()))
    education = education_mapping[education_display]
    
    st.header("Default, Housing, and Loan")
    default_mapping = {
        'Unknown': 'unknown', 
        'Yes': 'yes', 
        'No': 'no'
    }
    default_display = st.selectbox("Default", list(default_mapping.keys()))
    default = default_mapping[default_display]

    housing_display = st.selectbox("Housing Loan", list(default_mapping.keys()))
    housing = default_mapping[housing_display]

    loan_display = st.selectbox("Loan", list(default_mapping.keys()))
    loan = default_mapping[loan_display]
    
    st.header("Contact Communication Type")
    contact_mapping = {
        'Cellular': 'cellular', 
        'Telephone': 'telephone'
    }
    contact_display = st.selectbox("Contact", list(contact_mapping.keys()))
    contact_type = contact_mapping[contact_display]
    
    st.header("Campaign Month")
    month_mapping = {
        'January': 'jan',
        'February': 'feb',
        'March': 'mar',
        'April': 'apr',
        'May': 'may',
        'June': 'jun',
        'July': 'jul',
        'August': 'aug',
        'September': 'sep',
        'October': 'oct',
        'November': 'nov',
        'December': 'dec'
    }
    month_display = st.selectbox("Month", list(month_mapping.keys()))
    month = month_mapping[month_display] 

    st.header("Day of the Week")
    day_of_week_mapping = {
        'Monday': 'mon', 
        'Tuesday': 'tue', 
        'Wednesday': 'wed', 
        'Thursday': 'thu', 
        'Friday': 'fri'
    }
    day_of_week_display = st.selectbox("Day of the Week", list(day_of_week_mapping.keys()))
    day_of_week = day_of_week_mapping[day_of_week_display]
    
    st.header("Previous Outcome")
    poutcome_mapping = {
        'Failure': 'failure', 
        'Nonexistent': 'nonexistent', 
        'Success': 'success'
    }
    poutcome_display = st.selectbox("Previous Outcome", list(poutcome_mapping.keys()))
    poutcome = poutcome_mapping[poutcome_display]
    
    if st.button("Predict"):
        # Create the input data frame
        data = {
            'age': [age], 
            'duration': [duration], 
            'campaign': [campaign],
            'pdays': [pdays], 
            'previous': [previous],
            'emp.var.rate': [emp_var_rate], 
            'cons.price.idx': [cons_price_idx], 
            'cons.conf.idx': [cons_conf_idx],
            'euribor3m': [euribor3m], 
            'nr.employed': [nr_employed], 
            'job_blue-collar': [1 if job == 'blue-collar' else 0],
            'job_entrepreneur': [1 if job == 'entrepreneur' else 0],
            'job_housemaid': [1 if job == 'housemaid' else 0],
            'job_management': [1 if job == 'management' else 0],
            'job_retired': [1 if job == 'retired' else 0],
            'job_self-employed': [1 if job == 'self-employed' else 0],
            'job_services': [1 if job == 'services' else 0],
            'job_student': [1 if job == 'student' else 0],
            'job_technician': [1 if job == 'technician' else 0],
            'job_unemployed': [1 if job == 'unemployed' else 0],
            'job_unknown': [1 if job == 'unknown' else 0],
            'marital_married': [1 if marital == 'married' else 0],
            'marital_single': [1 if marital == 'single' else 0],
            'marital_unknown': [1 if marital == 'unknown' else 0],
            'education_basic.6y': [1 if education == 'basic.6y' else 0],
            'education_basic.9y': [1 if education == 'basic.9y' else 0],
            'education_high.school': [1 if education == 'high.school' else 0],
            'education_illiterate': [1 if education == 'illiterate' else 0],
            'education_professional.course': [1 if education == 'professional.course' else 0],
            'education_university.degree': [1 if education == 'university.degree' else 0],
            'education_unknown': [1 if education == 'unknown' else 0],
            'default_unknown': [1 if default == 'unknown' else 0],
            'default_yes': [1 if default == 'yes' else 0],
            'housing_unknown': [1 if housing == 'unknown' else 0],
            'housing_yes': [1 if housing == 'yes' else 0],
            'loan_unknown': [1 if loan == 'unknown' else 0],
            'loan_yes': [1 if loan == 'yes' else 0],
            'contact_telephone': [1 if contact_type == 'telephone' else 0],
            'month_aug': [1 if month == 'aug' else 0],
            'month_dec': [1 if month == 'dec' else 0],
            'month_jul': [1 if month == 'jul' else 0],
            'month_jun': [1 if month == 'jun' else 0],
            'month_mar': [1 if month == 'mar' else 0],
            'month_may': [1 if month == 'may' else 0],
            'month_nov': [1 if month == 'nov' else 0],
            'month_oct': [1 if month == 'oct' else 0],
            'month_sep': [1 if month == 'sep' else 0],
            'day_of_week_mon': [1 if day_of_week == 'mon' else 0],
            'day_of_week_thu': [1 if day_of_week == 'thu' else 0],
            'day_of_week_tue': [1 if day_of_week == 'tue' else 0],
            'day_of_week_wed': [1 if day_of_week == 'wed' else 0],
            'poutcome_nonexistent': [1 if poutcome == 'nonexistent' else 0],
            'poutcome_success': [1 if poutcome == 'success' else 0]
        }
        input_df = pd.DataFrame(data)
        
        # Make a prediction
        prediction = model.predict(input_df)[0]
        
        # Display the result
        st.write(f"Prediction (Subscribed): {'yes' if prediction == 1 else 'no'}")
        

# Function to create the welcome page
def welcome_page(router):
    st.markdown(
    """
    <style>
    button {
    height: auto;
    padding-top: 10px !important;
    padding-bottom: 10px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )
    st.title("ADA442 Final Project")
    st.write("## Group 5")
    st.write("")
    
    st.write("""
             
             #### Members:
                - Hakan Uca
                - Deniz Polat
                - Burak Güçlü
                - Emirhan Eyidoğan
             
             """)
   
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.write("")

    with col2:
        if st.button("Start Prediction"):
            router.redirect("/data_input")

    with col3:
        st.write("")

router = StreamlitRouter()
router.register(welcome_page, "/")
router.register(create_interface, "/data_input")

router.serve()