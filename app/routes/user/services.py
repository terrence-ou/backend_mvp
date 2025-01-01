from dotenv import load_dotenv
import os
from fastapi import Header, HTTPException
from google.cloud.firestore_v1.base_query import FieldFilter
import jwt
from typing import List
import random
from core.db import db
from app.utils.names import literature_giants
import requests

from app.routes.user.schemas import EmailToken, SessionToken

load_dotenv()
APPLE_CLIENT_ID = os.getenv("APPLE_CLIENT_ID")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
APPLE_KEYS_URL = os.getenv("APPLE_KEYS_URL")
GOOGLE_KEYS_URL = os.getenv("GOOGLE_KEYS_URL")


def decode_apple_token(identity_token: str = Header(...)) -> EmailToken:
    # Decode the Apple Identity Token
    decoded_data = decode_token(
        token=identity_token,
        public_url=APPLE_KEYS_URL,
        issuer="https://appleid.apple.com",
        client_id=APPLE_CLIENT_ID,
    )
    return decoded_data


def decode_google_token(identity_token: str = Header(...)) -> EmailToken:
    # Decode the Google Identity Token
    decoded_data = decode_token(
        token=identity_token,
        public_url=GOOGLE_KEYS_URL,
        issuer="https://accounts.google.com",
        client_id=GOOGLE_CLIENT_ID,
    )
    return decoded_data


def get_session_token(session_token: str = Header(...)) -> str:
    return session_token


def signout_user(session_token: str) -> List[str]:
    query = db.collection("users").where(
        filter=FieldFilter("session_token", "==", session_token)
    )
    users = query.stream()
    signed_out_users = []
    for user in users:
        signed_out_users.append(user.to_dict()["email"])
        user.reference.update({"session_token": None})
    return signed_out_users


# Helper function


# Decode the token using the public key
def decode_token(
    token: str, public_url: str, issuer: str, client_id: str
) -> EmailToken:
    # Fetch Apple's public keys
    response = requests.get(public_url)
    response.raise_for_status()
    apple_keys = response.json()["keys"]

    # Extract the `kid` from the token header
    headers = jwt.get_unverified_header(token)
    matching_key = next(
        (key for key in apple_keys if key["kid"] == headers["kid"]), None
    )

    if not matching_key:
        raise HTTPException(
            status_code=401, detail="No matching public key found for token"
        )

    # Convert the key to RSA public key
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(matching_key)
    # Decode the token
    decoded_token = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],  # Ensure this matches the header's `alg`
        audience=client_id,
        issuer=issuer,
    )

    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid Identity Token")

    return {"email": decoded_token["email"], "session_token": decoded_token["sub"]}


# create or update user info on firebase
def confirm_user(email: str, session_token: str) -> SessionToken:
    user_ref = db.collection("users").document(email)
    user = user_ref.get()
    if not user.exists:
        giant = random.choice(literature_giants)
        user_ref.set(
            {
                "email": email,
                "first_name": giant["first_name"],
                "last_name": giant["last_name"],
                "intro": giant["introduction"],
                "session_token": session_token,
            }
        )
    else:
        user_ref.update({"session_token": session_token})
    return {"session_token": session_token}
