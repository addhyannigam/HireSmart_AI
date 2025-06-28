import pdfplumber
import spacy
import Courses as cs
from google.generativeai import configure, GenerativeModel


nlp = spacy.load("en_core_web_sm")

configure(api_key="your_api_key")
model = GenerativeModel("gemini-1.5-flash")


def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_skills(text, skill_set=None):
    if skill_set is None:
        skill_set = {
    # Programming Languages
    "python", "java", "c", "c++", "c#", "javascript", "typescript", "ruby", "go", "swift", "kotlin", "r", "scala", "bash", "php", "perl", "rust", "matlab",

    # Web Development
    "html", "css", "react", "angular", "vue", "next.js", "node.js", "django", "flask", "express", "bootstrap", "tailwindcss", "jquery",

    # Mobile Development
    "android", "ios", "flutter", "react native", "swift", "kotlin", "xamarin",

    # Databases & Data Tools
    "sql", "mysql", "postgresql", "sqlite", "mongodb", "firebase", "oracle", "redis", "cassandra", "bigquery", "dynamodb",

    # DevOps & Cloud
    "docker", "kubernetes", "jenkins", "ansible", "terraform", "aws", "azure", "gcp", "heroku", "git", "github", "bitbucket", "ci/cd", "linux", "shell scripting", "nginx",

    # Data Science & Machine Learning
    "pandas", "numpy", "scikit-learn", "tensorflow", "keras", "pytorch", "matplotlib", "seaborn", "xgboost", "lightgbm", "statsmodels", "jupyter", "mlops", "data wrangling", "data cleaning", "data visualization",

    # AI / NLP / CV
    "openai", "transformers", "llm", "huggingface", "bert", "gpt", "spacy", "nltk", "opencv", "deep learning", "reinforcement learning", "computer vision", "nlp", "speech recognition",

    # Analytics & BI Tools
    "excel", "power bi", "tableau", "looker", "superset", "google data studio", "qlikview", "snowflake",

    # Cybersecurity
    "penetration testing", "ethical hacking", "network security", "kali linux", "burpsuite", "wireshark", "nmap", "security analysis", "owasp",

    # Project & Product Management
    "jira", "trello", "asana", "monday.com", "confluence", "agile", "scrum", "kanban", "product roadmap", "user stories", "business analysis",

    # UI/UX Design
    "figma", "adobe xd", "sketch", "photoshop", "illustrator", "wireframing", "prototyping", "design thinking", "usability testing", "user research",

    # Marketing & Content
    "seo", "sem", "google analytics", "facebook ads", "google ads", "content writing", "copywriting", "email marketing", "social media", "canva", "wordpress",

    # Finance & Business
    "financial modeling", "accounting", "bookkeeping", "quickbooks", "erp", "sap", "oracle netsuite", "budgeting", "market research", "crm", "salesforce",

    # Soft Skills
    "communication", "leadership", "problem-solving", "time management", "teamwork", "adaptability", "critical thinking", "decision making", "empathy", "negotiation",

    # Other Tools & Platforms
    "notion", "zapier", "microsoft office", "google workspace", "airtable", "slack", "zoom", "obs", "notepad++", "vs code", "intellij", "pycharm",

    # Writing & Language
    "technical writing", "proofreading", "documentation", "editing", "transcription", "translation",

    # Certifications / Methodologies
    "six sigma", "pmp", "itil", "iso 27001", "devops", "dataops", "design sprint", "lean", "agile methodology",

    # Educational / Research
    "academic writing", "research methodology", "latex", "scopus", "bibliometrics",

    # Emerging Tech
    "blockchain", "web3", "smart contracts", "solidity", "metaverse", "iot", "robotics", "edge computing", "digital twin",

    # Job-specific skills
    "customer support", "sales", "hr operations", "recruitment", "training", "logistics", "supply chain", "legal research", "medical coding", "telemedicine", "business development"
}


    text = set(text.lower().split()) & skill_set
    found = set()
    for skill in skill_set:
        if skill in text:
            found.add(skill)
    return list(found)

def get_job_suggestions(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    skills = extract_skills(text)
    prompt = f"""Based on the following skill set: {skills}, suggest relevant job roles and job titles. 
    Categorize the suggestions by experience level (Entry-Level, Mid-Level, and Senior-Level). 
    For each category, include:

    - The job role
    - A list of 3-5 possible job titles under that role
    - Recommend some skills to add to resume that can increase the chance of job suitability

    Format the response clearly using bullet points or headings so it’s easy to read."""

    response = model.generate_content(prompt)
    return skills, response.text

def get_job_recommendations_with_courses(skills, job_recommendations):
    results = []

    # Mapping job roles to course lists
    course_map = {
        "Data Scientist": cs.ds_course,
        "Data Analyst": cs.ds_course,
        "Business Intelligence Analyst": cs.ds_course,
        "Web Developer": cs.web_course,
        "Full Stack Developer": cs.web_course,
        "Frontend Developer": cs.web_course,
        "Backend Developer": cs.web_course,
        "Android Developer": cs.android_course,
        "Flutter Developer": cs.android_course,
        "Mobile App Developer": cs.android_course,
        "iOS Developer": cs.ios_course,
        "Swift Developer": cs.ios_course,
        "UI/UX Designer": cs.uiux_course,
        "UX Designer": cs.uiux_course,
        "UI Designer": cs.uiux_course,
    }

    for level, jobs in job_recommendations.items():
        section = f"### {level}:\n"
        for job in jobs:
            role = job['role']
            titles = job['titles']
            section += f"\n**Job Role:** {role}\n"
            section += "**Job Titles:**\n"
            for title in titles:
                section += f"- {title}\n"

            # Add course recommendations if applicable
            if role in course_map:
                section += "\n**Recommended Courses:**\n"
                for course in course_map[role][:5]:  # Suggest top 5 courses for brevity
                    section += f"- [{course[0]}]({course[1]})\n"
            section += "\n"
        results.append(section)

    return "\n".join(results)


