import streamlit as st
import pickle
import numpy as np
from io import BytesIO
from fpdf import FPDF
from fpdf import FPDF # Still kept for backward if needed, but we will use fpdf2
try:
    from fpdf import FPDF as FPDF2 # Try to import fpdf2 if installed as fpdf
except:
    from fpdf import FPDF
import os
import base64
from datetime import datetime
from auth import AuthManager
from health_assistant import get_medical_advice

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(page_title="Checkup Buddy", layout="wide", page_icon="🧫")

# Initialize Auth
auth = AuthManager()

# Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# ──────────────────────────────────────────────
# Authentication Page
# ──────────────────────────────────────────────

def login_page():
    st.markdown("""
        <style>
        .main {
            background-color: #f0f2f6;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #1f77b4;
            color: white;
        }
        .login-container {
            max-width: 400px;
            margin: auto;
            padding: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🩺 Checkup Buddy - Secure Portal")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Welcome Back")
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login"):
                success, message = auth.authenticate_user(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Welcome, {username}!")
                    st.rerun()
                else:
                    st.error(message)
                    
        with tab2:
            st.subheader("Create Account")
            new_user = st.text_input("Username", key="signup_user")
            new_email = st.text_input("Email", key="signup_email")
            new_pass = st.text_input("Password", type="password", key="signup_pass")
            confirm_pass = st.text_input("Confirm Password", type="password", key="signup_confirm")
            
            if st.button("Register"):
                if not new_user or not new_pass:
                    st.warning("Username and Password are required.")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match.")
                else:
                    success, message = auth.create_user(new_user, new_pass, new_email)
                    if success:
                        st.success(message)
                        st.info("Please switch to the Login tab.")
                    else:
                        st.error(message)

# ──────────────────────────────────────────────
# Main Application Content
# ──────────────────────────────────────────────

@st.cache_resource
def load_models():
    # Helper to safely load models
    files = {
        "heart": 'Saved_Models/heart_disease_model.sav',
        "heart_scaler": 'Saved_Models/scaler_heart.sav',
        "diabetes": 'Saved_Models/diabetes_model.sav',
        "diabetes_scaler": 'Saved_Models/scaler_diabetes.sav',
        "parkinsons": 'Saved_Models/parkinsons_model.sav',
        "parkinsons_scaler": 'Saved_Models/scaler_parkinsons.sav'
    }
    models = {}
    for key, path in files.items():
        if os.path.exists(path):
            models[key] = pickle.load(open(path, 'rb'))
        else:
            st.error(f"Missing model file: {path}")
    return models

def main_app():
    models = load_models()
    
    # Check if models were loaded
    if not models:
        st.stop()

    with st.sidebar:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if os.path.exists("Images/Logo 1.png"):
                st.image("Images/Logo 1.png", width=200)
            else:
                st.title("🩺 Checkup Buddy")
        
        st.markdown(f"### Logged in as: **{st.session_state.username}**")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
            
        st.markdown("---")
        st.markdown("## Navigation")
        selection = st.radio("Go to", ["Home", "Heart Disease", "Diabetes", "Parkinson's Disease", "About"])
        st.markdown("---")
        st.caption("✅ For educational use only.")

    # PDF Class using FPDF2 for better support
    class PDF(FPDF):
        def __init__(self):
            super().__init__()
            self.set_auto_page_break(auto=True, margin=15)
            # Use a standard font that supports some symbols or just sanitize
        def sanitize_text(self, text):
            # FPDF1/2 standard fonts only support latin-1
            if not text: return ""
            return str(text).encode('latin-1', 'replace').decode('latin-1')
            
        def header(self):
            logo_path = "Images/Logo 1.png"
            if os.path.exists(logo_path): 
                self.image(logo_path, x=10, y=8, w=25)
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, "Health Diagnosis Report - Checkup Buddy", ln=True, align='C')
            self.ln(5)
            
        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Page {self.page_no()} | User: {st.session_state.username}", align='C')

    def generate_pdf(name, disease_name, result_text, advice, inputs_dict, analysis, recs=None):
        pdf = PDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", "B", 18)
        pdf.set_text_color(31, 119, 180) # Blue color
        pdf.cell(0, 15, pdf.sanitize_text(f"{disease_name} - Analysis Report"), ln=True, align='C')
        pdf.ln(5)
        
        # Patient Info
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(95, 8, f"Patient Name: {pdf.sanitize_text(name)}", ln=0)
        pdf.cell(95, 8, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1, align='R')
        pdf.ln(10)
        
        # Metrics Table
        pdf.set_fill_color(240, 242, 246)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Recorded Health Metrics:", ln=True)
        pdf.set_font("Arial", "", 10)
        for label, value in inputs_dict.items():
            pdf.cell(80, 8, pdf.sanitize_text(label), border=1, fill=True)
            pdf.cell(110, 8, pdf.sanitize_text(value), border=1, ln=True)
        pdf.ln(10)
        
        # Assessment
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Medical Assessment:", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.set_fill_color(255, 255, 255)
        
        status_color = (255, 0, 0) if "RISK" in result_text.upper() or "POSITIVE" in result_text.upper() else (0, 128, 0)
        pdf.set_text_color(*status_color)
        pdf.multi_cell(0, 8, f"Status: {pdf.sanitize_text(result_text)}")
        pdf.set_text_color(0, 0, 0)
        
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Risk Analysis:", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, pdf.sanitize_text(analysis))
        
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Advice:", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, pdf.sanitize_text(advice))
        
        # AI Recommendations Section
        if recs:
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.set_text_color(31, 119, 180)
            pdf.cell(0, 15, "Personalized Medical Recommendations", ln=True, align='C')
            pdf.ln(5)
            
            pdf.set_text_color(0,0,0)
            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 10, "Medicine Prescriptions & AI Advice:", ln=True)
            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(0, 6, pdf.sanitize_text(recs['prescription_advice']))
            pdf.ln(10)
            
            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 10, "Nearby Medical Shops:", ln=True)
            pdf.set_font("Arial", "", 10)
            for shop in recs['medical_shops']:
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 7, pdf.sanitize_text(shop['name']), ln=True)
                pdf.set_font("Arial", "", 9)
                pdf.multi_cell(0, 5, pdf.sanitize_text(shop['snippet']))
                pdf.set_text_color(0, 0, 255)
                pdf.cell(0, 5, "Link: " + pdf.sanitize_text(shop['link']), ln=True)
                pdf.set_text_color(0, 0, 0)
                pdf.ln(3)
                
            pdf.ln(5)
            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 10, "Nearby Recommended Hospitals:", ln=True)
            pdf.set_font("Arial", "", 10)
            for hospital in recs["hospitals"]:
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 7, pdf.sanitize_text(hospital['name']), ln=True)
                pdf.set_font("Arial", "", 9)
                pdf.multi_cell(0, 5, pdf.sanitize_text(hospital['snippet']))
                pdf.set_text_color(0, 0, 255)
                pdf.cell(0, 5, "Link: " + pdf.sanitize_text(hospital['link']), ln=True)
                pdf.set_text_color(0, 0, 0)
                pdf.ln(3)

        pdf_output = pdf.output(dest='S')
        pdf_bytes = pdf_output.encode('latin-1') if isinstance(pdf_output, str) else bytes(pdf_output)
        b64 = base64.b64encode(pdf_bytes).decode('utf-8')
        return f'<a href="data:application/pdf;base64,{b64}" download="Health_Report.pdf" style="display:inline-block;padding:10px 20px;background:#1f77b4;color:white;border-radius:8px;text-decoration:none;font-weight:bold;">📄 Download PDF Report</a>'

    def get_analysis(disease_type, features, result):
        insights = []
        if disease_type == "heart":
            if result == 1:
                if features[3] > 140: insights.append(f"• Elevated Blood Pressure: {features[3]} mmHg")
                if features[4] > 240: insights.append(f"• High Cholesterol: {features[4]} mg/dL")
            else: insights.append("• Vital signs within recommended ranges.")
        elif disease_type == "diabetes":
            if result == 1:
                if features[1] > 140: insights.append(f"• Elevated Glucose: {features[1]} mg/dL")
                if features[5] > 30: insights.append(f"• BMI shows obesity risk: {features[5]:.1f}")
            else: insights.append("• Blood sugar levels are stable.")
        elif disease_type == "parkinsons":
            if result == 1: insights.append("• Dysphonic vocal indicators detected (high jitter/shimmer).")
            else: insights.append("• Voice biomarkers appear within healthy thresholds.")
        return "\n".join(insights) if insights else "Analysis successful."

    # Routing
    if selection == "Home":
        st.title("🩺 Checkup Buddy - Home")
        st.markdown(f"### 👋 Welcome, {st.session_state.username}!")
        st.markdown("Select a module from the sidebar to begin your health assessment.")
        col1, col2, col3 = st.columns(3)
        with col1: st.info("🫀 **Heart Assessment**")
        with col2: st.info("🩸 **Diabetes Screening**")
        with col3: st.info("🧠 **Parkinson's Analysis**")

    elif selection == "Heart Disease":
        st.header("🫀 Heart Disease Prediction")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Patient Name")
            age = st.slider("Age", 1, 100, 45)
            sex = st.selectbox("Sex", ["Male", "Female"])
            cp = st.selectbox("Chest Pain Type", ["Typical Angina", "Atypical Angina", "Non-Anginal", "Asymptomatic"])
            trestbps = st.number_input("Resting BP (mmHg)", 80, 200, 120)
            chol = st.number_input("Cholesterol (mg/dL)", 100, 500, 200)
            fbs = st.selectbox("Fasting Sugar > 120 mg/dL", ["No", "Yes"])
        with col2:
            restecg = st.selectbox("ECG Results", ["Normal", "Abnormality", "Hypertrophy"])
            thalach = st.number_input("Max Heart Rate", 60, 220, 150)
            exang = st.selectbox("Exercise Angina", ["No", "Yes"])
            oldpeak = st.number_input("ST Depression", 0.0, 6.0, 1.0)
            slope = st.selectbox("ST Slope", ["Upsloping", "Flat", "Downsloping"])
            ca = st.selectbox("Vessels Colored (0-3)", ["0", "1", "2", "3"])
            thal = st.selectbox("Thalassemia", ["Normal", "Fixed Defect", "Reversible Defect"])
            area = st.text_input("Your Location/Area (for nearby recommendations)", "New Delhi")

        if st.button("Run Diagnose"):
            sex_v = 0 if sex == "Male" else 1
            cp_v = ["Typical Angina", "Atypical Angina", "Non-Anginal", "Asymptomatic"].index(cp)
            fbs_v = 1 if fbs == "Yes" else 0
            ecg_v = ["Normal", "Abnormality", "Hypertrophy"].index(restecg)
            ex_v = 1 if exang == "Yes" else 0
            sl_v = ["Upsloping", "Flat", "Downsloping"].index(slope)
            th_v = {"Normal": 1, "Fixed Defect": 2, "Reversible Defect": 3}[thal]
            
            features = [age, sex_v, cp_v, trestbps, chol, fbs_v, ecg_v, thalach, ex_v, oldpeak, sl_v, int(ca), th_v]
            result = models["heart"].predict(models["heart_scaler"].transform([features]))[0]
            
            res_t = "HIGH RISK" if result == 1 else "LOW RISK"
            advice = "Consult a specialist for further testing." if result == 1 else "Maintain your healthy lifestyle."
            analysis = get_analysis("heart", features, result)
            
            if result == 1: st.error(f"Assessment: {res_t}")
            else: st.success(f"Assessment: {res_t}")
            st.info(f"Advice: {advice}")
            
            with st.spinner("Fetching AI recommendations..."):
                recs = get_medical_advice("Heart Disease", res_t, area)
                
            st.subheader("💊 Medicine Prescriptions & AI Advice")
            st.write(recs['prescription_advice'])
            
            col_shop, col_hosp = st.columns(2)
            with col_shop:
                st.subheader("🏪 Nearby Medical Shops")
                for shop in recs['medical_shops']:
                    st.markdown(f"**[{shop['name']}]({shop['link']})**")
                    st.caption(shop['snippet'])
            
            with col_hosp:
                st.subheader("🏥 Nearby Hospitals")
                for hosp in recs['hospitals']:
                    st.markdown(f"**[{hosp['name']}]({hosp['link']})**")
                    st.caption(hosp['snippet'])

            st.markdown(generate_pdf(name, "Heart Disease", res_t, advice, {"Age": str(age), "BP": str(trestbps), "Location": area}, analysis, recs), unsafe_allow_html=True)

    elif selection == "Diabetes":
        st.header("🩸 Diabetes Screening")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Patient Name")
            age = st.slider("Age", 1, 100, 30)
            preg = st.number_input("Pregnancies", 0, 20, 0)
            gluc = st.number_input("Glucose", 0, 300, 100)
        with col2:
            bp = st.number_input("BP", 0, 150, 72)
            skin = st.number_input("Skinfold", 0, 100, 20)
            ins = st.number_input("Insulin", 0, 900, 79)
            bmi = st.number_input("BMI", 0.0, 70.0, 25.0)
            dpf = st.number_input("Diabetes Pedigree", 0.0, 3.0, 0.3)
            area = st.text_input("Your Location/Area (for nearby recommendations)", "New Delhi")

        if st.button("Run Screen"):
            features = [preg, gluc, bp, skin, ins, bmi, dpf, age]
            result = models["diabetes"].predict(models["diabetes_scaler"].transform([features]))[0]
            res_t = "RISK DETECTED" if result == 1 else "NO RISK"
            advice = "Check blood sugar levels regularly." if result == 1 else "Keep up the good habits."
            if result == 1: st.error(res_t)
            else: st.success(res_t)
            st.info(f"Advice: {advice}")

            with st.spinner("Fetching AI recommendations..."):
                recs = get_medical_advice("Diabetes", res_t, area)
                
            st.subheader("💊 Medicine Prescriptions & AI Advice")
            st.write(recs['prescription_advice'])
            
            col_shop, col_hosp = st.columns(2)
            with col_shop:
                st.subheader("🏪 Nearby Medical Shops")
                for shop in recs['medical_shops']:
                    st.markdown(f"**[{shop['name']}]({shop['link']})**")
                    st.caption(shop['snippet'])
            
            with col_hosp:
                st.subheader("🏥 Nearby Hospitals")
                for hosp in recs['hospitals']:
                    st.markdown(f"**[{hosp['name']}]({hosp['link']})**")
                    st.caption(hosp['snippet'])

            st.markdown(generate_pdf(name, "Diabetes", res_t, advice, {"Glucose": str(gluc), "BMI": f"{bmi:.1f}", "Location": area}, get_analysis("diabetes", features, result), recs), unsafe_allow_html=True)

    elif selection == "Parkinson's Disease":
        st.header("🧠 Parkinson's Analysis")
        col1, col2 = st.columns(2)
        with col1:
            fo = st.number_input("MDVP:Fo (Hz)", 50.0, 300.0, 150.0)
            fhi = st.number_input("MDVP:Fhi (Hz)", 50.0, 600.0, 200.0)
            flo = st.number_input("MDVP:Flo (Hz)", 50.0, 300.0, 100.0)
            jit = st.number_input("Jitter (%)", 0.0, 1.0, 0.005, format="%.5f")
        with col2:
            shim = st.number_input("Shimmer", 0.0, 1.0, 0.03, format="%.5f")
            nhr = st.number_input("NHR", 0.0, 1.0, 0.02, format="%.5f")
            hnr = st.number_input("HNR", 0.0, 50.0, 20.0)
            ppe = st.number_input("PPE", 0.0, 1.0, 0.2, format="%.5f")
            area = st.text_input("Your Location/Area (for nearby recommendations)", "New Delhi")

        if st.button("Analyze Voice"):
            # Minimal feature set for demonstration, but ensuring all 22 are passed to scaler
            full_features = [fo, fhi, flo, jit, 0.0, 0.0, 0.0, 0.0, shim, 0.0, 0.0, 0.0, 0.0, 0.0, nhr, hnr, 0.0, 0.0, 0.0, 0.0, 0.0, ppe]
            result = models["parkinsons"].predict(models["parkinsons_scaler"].transform([full_features]))[0]
            res_t = "DETECTION: POSITIVE" if result == 1 else "DETECTION: NEGATIVE"
            if result == 1: st.error(res_t)
            else: st.success(res_t)

            with st.spinner("Fetching AI recommendations..."):
                recs = get_medical_advice("Parkinson's Disease", res_t, area)
                
            st.subheader("💊 Medicine Prescriptions & AI Advice")
            st.write(recs['prescription_advice'])
            
            col_shop, col_hosp = st.columns(2)
            with col_shop:
                st.subheader("🏪 Nearby Medical Shops")
                for shop in recs['medical_shops']:
                    st.markdown(f"**[{shop['name']}]({shop['link']})**")
                    st.caption(shop['snippet'])
            
            with col_hosp:
                st.subheader("🏥 Nearby Hospitals")
                for hosp in recs['hospitals']:
                    st.markdown(f"**[{hosp['name']}]({hosp['link']})**")
                    st.caption(hosp['snippet'])

            st.markdown(generate_pdf(st.session_state.username, "Parkinson's Disease", res_t, "Consult with a neurologist.", {"MDVP:Fo": str(fo), "Location": area}, get_analysis("parkinsons", full_features, result), recs), unsafe_allow_html=True)

    elif selection == "About":
        st.title("ℹ️ About Checkup Buddy")
        st.markdown("""
        ### AI-Driven Predictive Analytics for Disease Outbreaks
        **Checkup Buddy** is an advanced health diagnostic tool designed to provide preliminary health assessments using Machine Learning. 
        
        #### Key Features:
        - **ML Diagnostics**: Specialized models for Heart Disease, Diabetes, and Parkinson's.
        - **AI Recommendations**: Powered by **Gemini 2.5 Flash** for personalized medical advice and prescriptions.
        - **Real-time Search**: Powered by **Tavily AI** to locate nearby medical shops and hospitals based on your area.
        - **Comprehensive Reports**: Generate and download detailed health reports in PDF format.
        
        #### Our Mission:
        To leverage the power of Artificial Intelligence to make health screening more accessible and informative for everyone.
        
        *Disclaimer: This tool is for educational purposes and should not be used as a substitute for professional medical advice.*
        """)

# Boot
if st.session_state.logged_in:
    main_app()
else:
    login_page()
