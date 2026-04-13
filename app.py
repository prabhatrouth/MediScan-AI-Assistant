import streamlit as st
import google.generativeai as genai
from utils import extract_text_from_pdf

# --- 1. API Configuration ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    API_KEY = "AIzaSyBgfAPft_XrZqsDtSDAx5p6DcdEu1QO6f4"

genai.configure(api_key=API_KEY)

# --- 2. Dashboard UI ---
st.set_page_config(page_title="MediScan AI Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .welcome-card { background: white; padding: 25px; border-radius: 15px; border-left: 10px solid #004aad; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.markdown('<div class="welcome-card">', unsafe_allow_html=True)
    st.title("Welcome, Prabhat! 👋")
    st.info("Upload a medical report to simplify clinical jargon using AI.")
    st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", width=150)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.header("Report Analysis")
    uploaded_file = st.file_uploader("Upload PDF Report", type=["pdf"])
    text_input = st.text_area("Or Paste Text Here:")
    
    if st.button("Analyse Report 🔬"):
        report_content = ""
        if uploaded_file:
            report_content = extract_text_from_pdf(uploaded_file)
        elif text_input:
            report_content = text_input

        if not report_content:
            st.warning("Please provide a report.")
        else:
            with st.spinner("Analyzing..."):
                # AUTOMATIC MODEL FALLBACK LOGIC
                # We try Gemini 3 first, then fallback to 2.5
                models_to_try = ["gemini-3-flash-preview", "gemini-2.5-flash"]
                success = False
                
                for model_name in models_to_try:
                    try:
                        model = genai.GenerativeModel(model_name)
                        response = model.generate_content(f"Simplify this medical report: {report_content}")
                        st.success(f"Analysis complete (via {model_name})")
                        st.markdown(response.text)
                        success = True
                        break
                    except Exception:
                        continue
                
                if not success:
                    st.error("Model connection failed. Please check your API Key and Region in Google AI Studio.")
