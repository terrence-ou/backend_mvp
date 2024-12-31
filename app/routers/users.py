from typing import Annotated
import random
from fastapi import APIRouter, Depends
from app.dependencies import decode_apple_token
from app.utils.db import db
from app.utils.names import literature_giants

from app.schemas.users import UserBase

router = APIRouter(
    prefix="/users", tags=["users"], dependencies=[Depends(decode_apple_token)]
)


@router.post("/verify-user/apple")
async def verify_user_apple(
    email: Annotated[str, Depends(decode_apple_token)]
) -> UserBase:
    # Check if the user exists in the database
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
            }
        )
    user_data = user_ref.get().to_dict()
    return UserBase(**user_data)
