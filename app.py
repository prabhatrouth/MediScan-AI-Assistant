import streamlit as st
import google.generativeai as genai
from utils import extract_text_from_pdf

# --- 1. API Configuration ---
# Hardcoded API Key
API_KEY = "AIzaSyBgfAPft_XrZqsDtSDAx5p6DcdEu1QO6f4"
genai.configure(api_key=API_KEY)

# List of models to try in order of preference (Newest to most stable)
MODEL_OPTIONS = [
    "gemini-3-flash-preview", # Newest 2026 model
    "gemini-3.1-flash-lite-preview", 
    "gemini-2.5-flash",        # Highly stable backup
    "gemini-1.5-flash-latest"  # Legacy backup
]

# --- 2. Page Setup ---
st.set_page_config(page_title="MediScan AI Dashboard", layout="wide")

# --- 3. Custom CSS Styling (Fixed unsafe_allow_html) ---
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
    st.markdown('<h1 class="header-text">Welcome, User! 👋</h1>', unsafe_allow_html=True)
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
            report_data = extract_text_from_pdf(uploaded_file)
            st.success("PDF Content Loaded!")
    else:
        report_data = st.text_area("Paste medical notes here:", height=300)

    if st.button("Analyse Report 🔬"):
        if not report_data:
            st.warning("Please provide a report.")
        else:
            success = False
            with st.spinner("Finding an active AI model..."):
                for model_name in MODEL_OPTIONS:
                    try:
                        model = genai.GenerativeModel(model_name)
                        prompt = f"Summarize this medical report in simple terms for a patient: {report_data}"
                        response = model.generate_content(prompt)
                        
                        st.markdown(f"**Analysis (via {model_name})**")
                        st.markdown(response.text)
                        success = True
                        break # Exit loop if successful
                    except Exception as e:
                        continue # Try the next model in the list
                
                if not success:
                    st.error("Could not connect to any Gemini models. Please check if your API key is restricted by region or billing in AI Studio.")
