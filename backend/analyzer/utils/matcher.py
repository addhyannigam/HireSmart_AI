from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(candidate_skills, job_skills):
    # Convert skills to strings for TF-IDF
    candidate_text = " ".join(candidate_skills)
    job_text = " ".join(job_skills)
    
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([candidate_text, job_text])
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(similarity * 100, 2)  # Convert to percentage