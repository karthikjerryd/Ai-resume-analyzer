SKILLS_DB = [

    "Python",
    "Java",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "TypeScript",
    "Angular",
    "React",
    "Machine Learning",
    "Deep Learning",
    "Data Structures",
    "OOPS",
    "Bootstrap",
    "AWS",
    "Flask",
    "Django",
    "TensorFlow",
    "PyTorch",
    "MySQL"
]


def extract_skills(resume_text):

    detected_skills = []

    resume_text = resume_text.lower()

    for skill in SKILLS_DB:

        if skill.lower() in resume_text.lower():
            detected_skills.append(skill)

    return list(set(detected_skills))