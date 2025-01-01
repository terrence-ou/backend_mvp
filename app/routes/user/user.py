from typing import Annotated

from fastapi import APIRouter, Depends

# from app.dependencies import decode_apple_token, decode_google_token, confirm_user
from app.routes.user.services import (
    decode_apple_token,
    decode_google_token,
    confirm_user,
)
from app.routes.user.schemas import SessionToken, EmailToken

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/verify-user/apple")
async def verify_user_apple(
    decoded_data: Annotated[EmailToken, Depends(decode_apple_token)]
) -> SessionToken:
    return confirm_user(
        email=decoded_data["email"], session_token=decoded_data["session_token"]
    )


@router.post("/verify-user/google")
async def verify_user_google(
    decoded_data: Annotated[EmailToken, Depends(decode_google_token)]
) -> SessionToken:
    return confirm_user(
        email=decoded_data["email"], session_token=decoded_data["session_token"]
    )
