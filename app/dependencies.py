from dotenv import load_dotenv
import os
from fastapi import Header, HTTPException
from firebase_admin import auth
import jwt

import requests

load_dotenv()
APPLE_CLIENT_ID = os.getenv("APPLE_CLIENT_ID")
APPLE_KEYS_URL = os.getenv("APPLE_KEYS_URL")


def decode_apple_token(apple_identity_token: str = Header(...)):

    # Fetch Apple's public keys
    response = requests.get(APPLE_KEYS_URL)
    response.raise_for_status()
    apple_keys = response.json()["keys"]

    # Extract the `kid` from the token header
    headers = jwt.get_unverified_header(apple_identity_token)
    matching_key = next(
        (key for key in apple_keys if key["kid"] == headers["kid"]), None
    )

    if not matching_key:
        raise ValueError("No matching public key found for token")

    # Convert the key to RSA public key
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(matching_key)
    # Decode the token
    decoded_token = jwt.decode(
        apple_identity_token,
        public_key,
        algorithms=["RS256"],  # Ensure this matches the header's `alg`
        audience=APPLE_CLIENT_ID,
        issuer="https://appleid.apple.com",
    )
    return decoded_token["email"]


def get_user():
    pass
