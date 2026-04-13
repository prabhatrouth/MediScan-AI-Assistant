import PyPDF2

def extract_text_from_pdf(uploaded_file):
    """Safely extracts text from medical PDF reports."""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"
