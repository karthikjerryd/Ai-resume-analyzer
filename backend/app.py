from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import os

from matcher import calculate_ats_score
from skills import extract_skills
from s3_upload import upload_to_s3

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/')
def home():
    return "AI Resume Analyzer Backend Running"


@app.route('/upload', methods=['POST'])
def upload_resume():

    # Check if file exists
    if 'resume' not in request.files:
        return jsonify({
            "error": "No file uploaded"
        }), 400

    file = request.files['resume']
    job_description = request.form.get('job_description', '')

    # Save file temporarily
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:

        # Upload file to AWS S3
        with open(filepath, "rb") as data:
            s3_url = upload_to_s3(data, file.filename)

        # Extract text from PDF
        text = ""

        with pdfplumber.open(filepath) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted + "\n"

        # Extract skills
        skills = extract_skills(text)

        # Calculate ATS score
        ats_result = calculate_ats_score(
            skills,
            job_description
        )

        # Return response
        return jsonify({
            "success": True,
            "resume_text": text,
            "skills": skills,
            "s3_url": s3_url,
            "matched_skills": ats_result["matched_skills"],
            "missing_skills": ats_result["missing_skills"],
            "ats_score": ats_result["ats_score"]
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })


if __name__ == '__main__':
    app.run(debug=True)