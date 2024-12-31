from fastapi import FastAPI
from app.routers import users

# doc_ref = db.collection("users").document("alovelace")
# doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})

# users_ref = db.collection("users")
# docs = users_ref.stream()

# for doc in docs:
# print(f"{doc.id} => {doc.to_dict()}")

app = FastAPI()
app.include_router(users.router)
