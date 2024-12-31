from typing import Annotated
import random

from fastapi import APIRouter, Depends

from app.dependencies import decode_apple_token
from app.utils.db import db
from app.utils.names import literature_giants
from app.schemas.users import UserBase, EmailToken

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/verify-user/apple")
async def verify_user_apple(
    emailToken: Annotated[EmailToken, Depends(decode_apple_token)]
) -> UserBase:
    # Check if the user exists in the database
    email, identity_token = emailToken["email"], emailToken["identity_token"]
    user_ref = db.collection("users").document(emailToken["email"])
    user = user_ref.get()
    if not user.exists:
        giant = random.choice(literature_giants)
        user_ref.set(
            {
                "email": email,
                "first_name": giant["first_name"],
                "last_name": giant["last_name"],
                "intro": giant["introduction"],
                "identity_token": identity_token,
            }
        )
    else:
        user_ref.update({"identity_token": identity_token})
    user_data = user_ref.get().to_dict()
    return UserBase(**user_data)
