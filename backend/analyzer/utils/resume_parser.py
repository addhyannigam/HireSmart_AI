import spacy
import PyPDF2

nlp = spacy.load("en_core_web_lg")

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages])
    return text

def extract_skills(text):
    doc = nlp(text)
    skills = []
    # Rule-based skill extraction (enhance with a predefined skill list)
    for token in doc:
        if token.text.lower() in ["python", "machine learning", "django"]:  # Expand this list
            skills.append(token.text)
    return list(set(skills))  # Remove duplicates