import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()
FIREBASE_CREDS_PATH = os.getenv("FIREBASE_CREDS_PATH")

# Initialize Firestore DB
cred = credentials.Certificate(FIREBASE_CREDS_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()
