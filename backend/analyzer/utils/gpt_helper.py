import openai

openai.api_key = "your-api-key"

def generate_resume_summary(resume_text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a career coach. Summarize this resume professionally:"},
            {"role": "user", "content": resume_text}
        ]
    )
    return response.choices[0].message.content

def explain_skill_gap(missing_skills, job_title):
    prompt = f"""
    Explain to a candidate why they need {', '.join(missing_skills)} 
    for the role of {job_title}. Keep it encouraging and concise.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content