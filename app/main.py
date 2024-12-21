from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from fastapi import FastAPI
from app.routers import users

load_dotenv()
FIREBASE_CREDS_PATH = os.getenv("FIREBASE_CREDS_PATH")

# Initialize Firestore DB
cred = credentials.Certificate(FIREBASE_CREDS_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

doc_ref = db.collection("users").document("alovelace")
doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})

users_ref = db.collection("users")
docs = users_ref.stream()

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")

app = FastAPI()
app.include_router(users.router)
