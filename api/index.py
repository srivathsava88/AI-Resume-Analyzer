from flask import Flask, render_template, request
import pdfplumber
from groq import Groq
import os

app = Flask(__name__, template_folder="../templates")

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

@app.route("/", methods=["GET", "POST"])
def home():

    analysis = ""

    if request.method == "POST":

        file = request.files["resume"]

        if file:

            filepath = "temp_resume.pdf"
            file.save(filepath)

            text = ""

            with pdfplumber.open(filepath) as pdf:

                for page in pdf.pages:
                    text += page.extract_text()

            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "user",
                        "content": f"Analyze this resume and give feedback: {text}"
                    }
                ]
            )

            analysis = response.choices[0].message.content

            os.remove(filepath)

    return render_template(
        "index.html",
        analysis=analysis
    )

if __name__ == "__main__":
    app.run(debug=True)