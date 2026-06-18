from flask import Flask, render_template, request
import PyPDF2
import re

app = Flask(__name__)

# -------------------------------
# Resume text extract
# -------------------------------
def extract_text(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# -------------------------------
# Skills list
# -------------------------------
skills_list = ["python", "java", "html", "css", "javascript", "sql"]

# -------------------------------
# Better skill extraction
# -------------------------------
def extract_skills(text):
    found = []
    words = re.findall(r'\b\w+\b', text)  # clean words

    for skill in skills_list:
        if skill in words:
            found.append(skill)

    return found

# -------------------------------
# Correct score calculation
# -------------------------------
def calculate_score(resume_skills, job_skills):
    if not job_skills:
        return 0

    match_count = 0
    for skill in job_skills:
        if skill in resume_skills:
            match_count += 1

    score = (match_count / len(job_skills)) * 100
    return round(score, 2)

# -------------------------------
# Routes
# -------------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['resume']
    job_role = request.form['job']

    text = extract_text(file)
    resume_skills = extract_skills(text)

    # Job roles
    if job_role == "web":
        job_skills = ["html", "css", "javascript"]
    elif job_role == "data":
        job_skills = ["python", "sql"]
    elif job_role == "java":
        job_skills = ["java"]
    else:
        job_skills = []

    # Score
    score = calculate_score(resume_skills, job_skills)

    # Matched & Missing
    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    # Message
    if score > 70:
        message = "Strong Match ✅"
    elif score > 40:
        message = "Average Match ⚠️"
    else:
        message = "Low Match ❌"

    # Debug (optional)
    print("Resume Skills:", resume_skills)
    print("Job Skills:", job_skills)
    print("Score:", score)

    return render_template('result.html',
                           skills=resume_skills,
                           score=score,
                           matched=matched,
                           missing=missing,
                           message=message)

# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)