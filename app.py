import streamlit as st
import google.generativeai as genai
from utils import extract_text_from_pdf

# --- 1. API Configuration ---
# Pulling the key securely from Streamlit Secrets
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    # Fallback for local testing
    API_KEY = "AIzaSyBgfAPft_XrZqsDtSDAx5p6DcdEu1QO6f4"

genai.configure(api_key=API_KEY)

# Use the specific 2026 model ID
# gemini-3-flash is the standard for the current high-speed API
MODEL_ID = "gemini-3-flash"

# --- 2. Page Setup ---
st.set_page_config(page_title="MediScan AI Dashboard", layout="wide", page_icon="🔬")

# --- 3. Custom CSS Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .welcome-section {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        border-left: 8px solid #004aad;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .header-text { color: #004aad; font-family: 'Helvetica'; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. Dashboard Layout ---
col_left, col_right = st.columns([1, 1.5], gap="large")

with col_left:
    st.markdown('<div class="welcome-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="header-text">Welcome, Prabhat! 👋</h1>', unsafe_allow_html=True)
    st.write("---")
    st.info("""
    ### **MediScan AI Assistant**
    **Steps:**
    1. Upload a **PDF** or paste **Text**.
    2. Click **Analyse Report**.
    3. AI will simplify the medical data for you.
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/822/822118.png", width=120)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.header("Report Analysis Center")
    input_type = st.radio("Select input format:", ["📄 Upload PDF", "✍️ Paste Text"], horizontal=True)
    
    report_data = ""
    if input_type == "📄 Upload PDF":
        uploaded_file = st.file_uploader("Upload Medical PDF", type=["pdf"])
        if uploaded_file:
            with st.spinner("Extracting text from PDF..."):
                report_data = extract_text_from_pdf(uploaded_file)
                st.success("PDF Content Loaded!")
    else:
        report_data = st.text_area("Paste medical notes here:", height=300)

    if st.button("Analyse Report 🔬"):
        if not report_data:
            st.warning("Please provide a report.")
        else:
            with st.spinner(f"Analyzing with {MODEL_ID}..."):
                try:
                    # Explicitly using the Gemini 3 model
                    model = genai.GenerativeModel(MODEL_ID)
                    
                    prompt = f"""
                    You are a professional medical report interpreter. 
                    Analyze this medical report and simplify it for a patient: 
                    
                    {report_data}
                    
                    Provide a summary, explain key terms, and suggest 3 questions for their doctor.
                    """
                    
                    response = model.generate_content(prompt)
                    
                    st.markdown("### 📋 Analysis Results")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Analysis Error: {e}")
                    st.info("If you see a 404, please ensure your API key has access to Gemini 3 models in AI Studio.")
