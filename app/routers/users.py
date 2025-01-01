from typing import Annotated
import random

from fastapi import APIRouter, Depends

from app.dependencies import decode_apple_token
from app.utils.db import db
from app.utils.names import literature_giants
from app.schemas.users import SessionToken, EmailToken

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/verify-user/apple")
async def verify_user_apple(
    emailToken: Annotated[EmailToken, Depends(decode_apple_token)]
) -> SessionToken:
    # Check if the user exists in the database
    email, session_token = emailToken["email"], emailToken["session_token"]
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
                "session_token": session_token,
            }
        )
    else:
        user_ref.update({"session_token": session_token})
    return {"session_token": session_token}
