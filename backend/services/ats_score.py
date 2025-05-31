import pdfplumber
import re
import time

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def evaluate_resume_sections(resume_text):
    resume_score = 0
    resume_text = resume_text.lower()

    #
    # Section weights and indicative keywords
    sections = {
        "Objective": {"weight": 10, "keywords": ["objective", "summary"]},
        "Education": {"weight": 15, "keywords": ["education", "academic background"]},
        "Experience": {"weight": 20, "keywords": ["experience", "work history", "employment"]},
        "Internship": {"weight":5,"keywords":["Internship","internship"]},
        "Projects": {"weight": 15, "keywords": ["projects", "portfolio"]},
        "Certifications": {"weight": 10, "keywords": ["certifications", "licenses"]},
        "Skills": {"weight": 10, "keywords": ["skills", "technologies"]},
        "Achievements": {"weight": 10, "keywords": ["achievements", "awards", "honors"]},
        "Interests": {"weight": 5, "keywords": ["hobbies", "interests"]},
        "Contact": {"weight": 5, "keywords": ["phone", "email", "linkedin"]},
    }

    def section_found(keywords):
        return any(re.search(rf"\b{re.escape(word)}\b", resume_text) for word in keywords)

    for section, config in sections.items():
        if section_found(config["keywords"]):
            resume_score += config["weight"]

    # Simulated progress
    for _ in range(0, resume_score + 1, 10):
        time.sleep(0.02)

    return resume_score
