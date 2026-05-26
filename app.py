import streamlit as st
import pdfplumber
from groq import Groq

# --------------------------------
# PAGE SETTINGS
# --------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄"
)

st.title("📄 AI Resume Analyzer")

st.write("Upload your resume and get AI feedback.")

# --------------------------------
# API KEY INPUT
# --------------------------------

api_key = st.text_input(
    "Enter Groq API Key",
    type="password"
)

# --------------------------------
# FILE UPLOAD
# --------------------------------

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# --------------------------------
# EXTRACT TEXT
# --------------------------------

def extract_text(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            content = page.extract_text()

            if content:
                text += content + "\n"

    return text

# --------------------------------
# ANALYZE RESUME
# --------------------------------

def analyze_resume(text, api_key):

    client = Groq(
        api_key=api_key
    )

    prompt = f"""
    Analyze this resume carefully.

    Give:
    1. ATS Score
    2. Technical Skills
    3. Missing Skills
    4. Strengths
    5. Weaknesses
    6. Suggestions
    7. Suitable Job Roles

    Resume:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

# --------------------------------
# MAIN LOGIC
# --------------------------------

if uploaded_file:

    st.success("✅ Resume Uploaded Successfully")

    text = extract_text(uploaded_file)

    with st.expander("View Resume Text"):

        st.write(text)

    if st.button("Analyze Resume"):

        if api_key == "":

            st.warning("Please enter Groq API Key.")

        else:

            with st.spinner("Analyzing Resume..."):

                try:

                    result = analyze_resume(
                        text,
                        api_key
                    )

                    st.subheader("📊 Resume Analysis")

                    st.write(result)

                except Exception as e:

                    st.error(f"ERROR: {e}")

else:

    st.info("Please upload a PDF resume.")