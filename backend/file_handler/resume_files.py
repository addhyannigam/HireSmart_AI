import uuid
import datetime

import os, sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname("backend/"), '..'))
sys.path.append(ROOT_DIR)


from backend.database import firebase as fb


def upload_resume_to_storage(file, filename):
    blob = fb.bucket.blob(f'resumes/{filename}')
    blob.upload_from_file(file, content_type='application/pdf')
    blob.make_public()  # Optional: make it accessible by URL
    return blob.public_url

def save_resume_metadata(email, file_url):
    resume_id = str(uuid.uuid4())
    data = {
        'email': email,
        'uploaded_at': datetime.datetime.utcnow(),
        'resume_url': file_url,
        'id': resume_id
    }
    fb.db.collection('resumes').document(resume_id).set(data)
