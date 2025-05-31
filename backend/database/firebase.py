import os
import sys

# Get absolute path to project root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname("backend/"), '..'))
sys.path.append(ROOT_DIR)

from backend.config import config
import pyrebase

import firebase_admin
from firebase_admin import credentials, firestore, storage

# Replace with path to your downloaded service account key
cred = credentials.Certificate("backend/database/hiresmart-ai-c5b3b-firebase-adminsdk-fbsvc-32c188a5c9.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
#bucket = storage.bucket()

firebase = pyrebase.initialize_app(config.load_config())
auth = firebase.auth()
rdb = firebase.database()

