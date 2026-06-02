from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import PyPDF2
import pymysql

app = Flask(__name__)
CORS(app)

# -----------------------------
# AWS S3 CONFIGURATION
# -----------------------------

BUCKET_NAME = "ai-resume-analyzer-project"

s3 = boto3.client(
    's3',
    aws_access_key_id='AKIAT3H7RDDM4XW4IREH',
    aws_secret_access_key='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',
    region_name='eu-north-1'
)

# -----------------------------
# RDS DATABASE CONNECTION
# -----------------------------

def get_db_connection():

    return pymysql.connect(
        host="resume-analyzer-db.cl0igecm6h52.eu-north-1.rds.amazonaws.com",
        user="admin",
        password="admin123456",
        database="resumeanalyzer_db"
    )



# -----------------------------
# CREATE TABLE
# -----------------------------


#connection = get_db_connection()
#cursor = connection.cursor()



 

#connection.commit()

# -----------------------------
# SKILLS DATABASE
# -----------------------------

skills_list = [

    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "React",
    "Angular",
    "Node.js",
    "Flask",
    "Django",
    "SQL",
    "MySQL",
    "MongoDB",
    "AWS",
    "EC2",
    "S3",
    "Docker",
    "Kubernetes",
    "Terraform",
    "Ansible",
    "Jenkins",
    "Git",
    "Linux",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "HTML",
    "CSS",
    "Bootstrap",
    "Tailwind",
    "Data Structures",
    "OOPS",
    "DBMS"

]

# -----------------------------
# EXTRACT SKILLS
# -----------------------------

def extract_skills(text):

    detected_skills = []

    for skill in skills_list:

        if skill.lower() in text.lower():

            detected_skills.append(skill)

    return detected_skills

# -----------------------------
# CALCULATE ATS SCORE
# -----------------------------

def calculate_ats_score(resume_skills, job_description):

    matched_skills = []
    missing_skills = []

    job_description_lower = job_description.lower()

    for skill in skills_list:

        if skill.lower() in job_description_lower:

            if skill in resume_skills:

                matched_skills.append(skill)

            else:

                missing_skills.append(skill)

    total_skills = len(matched_skills) + len(missing_skills)

    if total_skills > 0:

        ats_score = int(
            (len(matched_skills) / total_skills) * 100
        )

    else:

        ats_score = 0

    return {

        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "ats_score": ats_score

    }

# -----------------------------
# HOME ROUTE
# -----------------------------

@app.route('/')

def home():

    return "AI Resume Analyzer Backend Running"

# -----------------------------
# UPLOAD ROUTE
# -----------------------------

@app.route('/upload', methods=['POST'])

@app.route('/upload', methods=['POST'])
def upload_resume():

    try:

        # Get uploaded file
        file = request.files['resume']

        # Get job description
        job_description = request.form.get(
            'job_description',
            ''
        )

        # File name
        filename = file.filename

        file_content = file.read()

        import io

        # Upload to S3
        s3.upload_fileobj(
            io.BytesIO(file_content),
            BUCKET_NAME,
            filename
        )

        # S3 URL
        s3_url = f"https://{BUCKET_NAME}.s3.eu-north-1.amazonaws.com/{filename}"

        # Reset file pointer
        file.seek(0)

        # Read PDF
        pdf_reader = PyPDF2.PdfReader(
            io.BytesIO(file_content)
        )

        text = ""

        for page in pdf_reader.pages:

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

        # Store result in RDS

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO ats_results
            (filename, ats_score, matched_skills, missing_skills)
            VALUES (%s, %s, %s, %s)
            """,
            (
                filename,
                ats_result["ats_score"],
                ",".join(ats_result["matched_skills"]),
                ",".join(ats_result["missing_skills"])
             )
        )

        connection.commit()
        cursor.close()
        connection.close()

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
# ----------------------------# RUN APP
# -----------------------------

@app.route('/history', methods=['GET'])
def get_history():

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            pymysql.cursors.DictCursor
        )

        cursor.execute("""
            SELECT
                id,
                filename,
                ats_score,
                matched_skills,
                missing_skills,
                created_at
            FROM ats_results
            ORDER BY created_at DESC
        """)

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(results)

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })
if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
