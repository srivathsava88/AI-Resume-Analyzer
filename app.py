from flask import Flask, render_template, request
import os
import pdfplumber
from groq import Groq

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:
        return "No file uploaded"

    file = request.files["resume"]

    if file.filename == "":
        return "No selected file"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    text = ""

    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

    prompt = f"""
    Analyze this resume and provide:

    1. Resume Summary
    2. Technical Skills
    3. Strengths
    4. Weaknesses
    5. ATS Score out of 100
    6. Suggestions for Improvement

    Resume:
    {text}
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content

    return f"""
    <h1>AI Resume Analysis</h1>
    <pre>{result}</pre>
    """