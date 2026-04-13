import streamlit as st
import google.generativeai as genai
from utils import extract_text_from_pdf
import os

# --- 1. API Configuration ---
# This looks for the key in Streamlit Cloud's "Secrets" menu
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    # Fallback for local testing only
    API_KEY = "AIzaSyBgfAPft_XrZqsDtSDAx5p6DcdEu1QO6f4"

genai.configure(api_key=API_KEY)

# Using 'gemini-1.5-flash' as it is the most stable and free-tier friendly
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. Page Configuration ---
st.set_page_config(
    page_title="MediScan AI | Sanpra Consultancy",
    page_icon="🔬",
    layout="wide"
)

# --- 3. Custom CSS Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f9; }
    .welcome-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #004aad;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .header-text { color: #004aad; font-family: 'Segoe UI'; font-weight: 700; }
    .stButton>button {
        background-color: #004aad;
        color: white;
        border-radius: 8px;
        width: 100%;
        height: 3em;
        font-weight: bold;
    }
    .result-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. Dashboard Layout ---
col_left, col_right = st.columns([1, 1.5], gap="large")

# --- LEFT PANEL: Welcome & Instructions ---
with col_left:
    st.markdown('<div class="welcome-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="header-text">Welcome, Prabhat! 👋</h1>', unsafe_allow_html=True)
    st.write("---")
    st.markdown("""
    ### **AI Medical Report Analyzer**
    Bridging the gap between clinical data and patient understanding.
    
    **How to use:**
    1. **Choose Input:** Select PDF upload or Text paste.
    2. **Provide Data:** Upload your report or paste the notes.
    3. **Analyze:** Get a simplified summary instantly.
    
    *Powered by Sanpra Consultancy Services*
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", width=150)
    st.warning("**Disclaimer:** This tool is for informational purposes only. It does not provide medical diagnoses.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- RIGHT PANEL: Analysis Engine ---
with col_right:
    st.header("Analysis Engine")
    
    # Input Method Selection
    input_method = st.radio("Select Input Method:", ["📄 Upload PDF Report", "✍️ Paste Clinical Text"], horizontal=True)
    
    report_text = ""

    if input_method == "📄 Upload PDF Report":
        uploaded_file = st.file_uploader("Upload Medical PDF", type=["pdf"])
        if uploaded_file:
            with st.spinner("Extracting text from PDF..."):
                report_text = extract_text_from_pdf(uploaded_file)
                st.success("PDF Content Loaded!")
    else:
        report_text = st.text_area("Paste medical report or lab results here:", height=250)

    # Analyze Button
    if st.button("Analyse Report 🔬"):
        if not report_text:
            st.error("Please provide medical data to analyze.")
        else:
            with st.spinner("AI is interpreting your report..."):
                # Professional medical prompt
                prompt = f"""
                You are a professional medical report interpreter. 
                Analyze the following data: {report_text}
                
                Please provide the response in these specific sections:
                1. **Simple Summary**: Explain the report in 2-3 sentences.
                2. **Key Findings**: Highlight any abnormal values.
                3. **Jargon Decoded**: Explain difficult medical terms in simple language.
                4. **Questions for your Doctor**: 3 specific questions the patient should ask.
                
                Always include a safety disclaimer at the end.
                """
                
                try:
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown("### 📋 Analysis Results")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Analysis Error: {e}")
                    st.info("Ensure your API key is correctly set in Streamlit Secrets.")
