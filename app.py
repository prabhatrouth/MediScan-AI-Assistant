import streamlit as st
import google.generativeai as genai
from utils import extract_text_from_pdf

# --- 1. API Configuration ---
# Your API Key is hardcoded for your convenience, 
# but will check Streamlit Secrets first for security.
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    API_KEY = "AIzaSyBgfAPft_XrZqsDtSDAx5p6DcdEu1QO6f4"

genai.configure(api_key=API_KEY)

# Modern 2026 Model IDs
# We try Gemini 3 first, then fallback to 2.5 if 3 is restricted.
MODEL_IDS = [
    "gemini-3-flash-preview", 
    "gemini-3.1-flash-lite-preview",
    "gemini-2.5-flash",
    "gemini-1.5-flash-latest"
]

# --- 2. Page Setup ---
st.set_page_config(page_title="MediScan AI Assistant", layout="wide", page_icon="🔬")

st.markdown("""
    <style>
    .stApp { background-color: #f1f4f9; }
    .welcome-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border-left: 10px solid #004aad;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .header-text { color: #004aad; font-family: 'Segoe UI'; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Dashboard Layout ---
col_welcome, col_analysis = st.columns([1, 1.5], gap="large")

with col_welcome:
    st.markdown('<div class="welcome-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="header-text">Welcome, User! 👋</h1>', unsafe_allow_html=True)
    st.write("---")
    st.markdown("""
    ### **MediScan AI Assistant**
    **Your health data, simplified.**
    
    1. **Upload** your medical report (PDF).
    2. **Paste** text if you have digital notes.
    3. **Analyze** to get a jargon-free summary.
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", width=150)
    st.markdown('</div>', unsafe_allow_html=True)

with col_analysis:
    st.header("Medical Analysis Engine")
    
    input_choice = st.radio("Select Input Method:", ["📄 Upload PDF", "✍️ Paste Text"], horizontal=True)
    
    report_content = ""
    
    if input_choice == "📄 Upload PDF":
        uploaded_file = st.file_uploader("Upload Medical Report", type=["pdf"])
        if uploaded_file:
            report_content = extract_text_from_pdf(uploaded_file)
            st.success("PDF Content Loaded Successfully!")
    else:
        report_content = st.text_area("Paste report text here:", height=250)

    if st.button("Analyse Report 🔬"):
        if not report_content:
            st.warning("Please provide a report for analysis.")
        else:
            success = False
            with st.spinner("Connecting to Gemini AI Engine..."):
                for model_id in MODEL_IDS:
                    try:
                        model = genai.GenerativeModel(model_id)
                        prompt = f"""
                        Acting as a professional medical interpreter, analyze this report:
                        {report_content}
                        
                        Provide:
                        1. A 2-sentence summary.
                        2. A list of key values that seem abnormal.
                        3. Simplified definitions of medical terms used.
                        4. Three questions to ask the doctor.
                        
                        Include a disclaimer that this is not a diagnosis.
                        """
                        response = model.generate_content(prompt)
                        
                        st.markdown(f"### 📋 Analysis Results (via {model_id})")
                        st.markdown(response.text)
                        success = True
                        break # Stop loop if successful
                    except Exception:
                        continue # Try next model if 404 occurs
                
                if not success:
                    st.error("Connection Error: All models returned a 404. Check your API key permissions in AI Studio.")
