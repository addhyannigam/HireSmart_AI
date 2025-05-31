import io
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pdfminer3.pdfpage import PDFPage

import re
import spacy

# Load spaCy English model (you can use 'en_core_web_sm' or 'en_core_web_md')
nlp = spacy.load("en_core_web_sm")

def pdf_reader(file_path):
    try:
        laparams = LAParams()
        with open(file_path, 'rb') as file:
            text = extract_text(file, laparams=laparams)
        return text
    except Exception as e:
        print(f"[Error] Failed to read PDF: {e}")
        return ""
    
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

def get_number_of_pages(pdf_path):
    with open(pdf_path, 'rb') as fh:
        pages = list(PDFPage.get_pages(fh))
        return len(pages)


