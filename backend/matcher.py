def calculate_ats_score(resume_skills, job_description):

    # Convert JD to lowercase
    jd = job_description.lower()

    matched_skills = []
    missing_skills = []

    for skill in resume_skills:

        if skill.lower() in jd:
            matched_skills.append(skill)

    # Find missing skills
    required_skills = [
        "Python",
        "Java",
        "SQL",
        "AWS",
        "Docker",
        "Machine Learning",
        "Deep Learning",
        "React",
        "Angular",
        "JavaScript",
        "TypeScript",
        "MySQL"
    ]

    for skill in required_skills:

        if skill.lower() in jd and skill not in matched_skills:
            missing_skills.append(skill)

    # Calculate ATS Score
    total_required = len(matched_skills) + len(missing_skills)

    if total_required == 0:
        ats_score = 0
    else:
        ats_score = int((len(matched_skills) / total_required) * 100)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "ats_score": ats_score
    }