import streamlit as st
import google.generativeai as genai
from utils import extract_text_from_pdf

# --- 1. API Configuration ---
# Securely fetching the key from Streamlit Secrets
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    # Local backup
    API_KEY = "AIzaSyBgfAPft_XrZqsDtSDAx5p6DcdEu1QO6f4"

genai.configure(api_key=API_KEY)

# --- 2. Page Setup ---
st.set_page_config(page_title="MediScan AI Dashboard", layout="wide", page_icon="🔬")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .stApp { background-color: #f1f4f9; }
    .main-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        border-left: 10px solid #004aad;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }
    .header-style { color: #004aad; font-family: 'Arial'; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. UI Layout ---
col_welcome, col_main = st.columns([1, 1.5], gap="large")

with col_welcome:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="header-style">Welcome, Prabhat! 👋</h1>', unsafe_allow_html=True)
    st.write("---")
    st.markdown("""
    ### **MediScan AI**
    **Simplify Your Health Data**
    1. **Upload** your medical report (PDF).
    2. **Paste** text if you have notes.
    3. **Analyze** to get a clear summary.
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", width=150)
    st.caption("Powered by Sanpra Consultancy Services")
    st.markdown('</div>', unsafe_allow_html=True)

with col_main:
    st.header("Report Analysis Engine")
    
    tab_pdf, tab_text = st.tabs(["📄 PDF Upload", "✍️ Manual Text"])
    
    report_content = ""
    
    with tab_pdf:
        uploaded_file = st.file_uploader("Upload Medical PDF", type=["pdf"])
        if uploaded_file:
            report_content = extract_text_from_pdf(uploaded_file)
            st.success("PDF Content Extracted!")

    with tab_text:
        text_area = st.text_area("Paste medical notes here:", height=200)
        if text_area:
            report_content = text_area

    if st.button("Run AI Analysis 🔬"):
        if not report_content:
            st.warning("Please provide a report to analyze.")
        else:
            with st.spinner("Connecting to Gemini AI..."):
                # LIST OF MODELS TO TRY (Fixes the 404 Error)
                # We try the most likely stable aliases for 2026
                models_to_try = [
                    "gemini-3-flash-preview", 
                    "gemini-3-flash", 
                    "gemini-2.5-flash", 
                    "gemini-1.5-flash"
                ]
                
                analysis_success = False
                
                for model_id in models_to_try:
                    try:
                        model = genai.GenerativeModel(model_id)
                        prompt = f"""
                        Interpret this medical report for a patient. 
                        Use simple language. Explain key values and suggest 
                        3 questions for their doctor. 
                        Data: {report_content}
                        """
                        response = model.generate_content(prompt)
                        
                        st.markdown(f"### 📋 Analysis Results (via {model_id})")
                        st.markdown(response.text)
                        st.info("**Disclaimer:** This is an AI interpretation and not a diagnosis.")
                        analysis_success = True
                        break # Exit loop if a model works
                    except Exception:
                        continue # Try the next model if 404 or error
                
                if not analysis_success:
                    st.error("Connection Error: All Gemini models returned a 404 or busy status. Please check your API key permissions in Google AI Studio.")
