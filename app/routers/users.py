from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import decode_apple_token, confirm_user
from app.schemas.users import SessionToken, EmailToken

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/verify-user/apple")
async def verify_user_apple(
    decoded_data: Annotated[EmailToken, Depends(decode_apple_token)]
) -> SessionToken:
    return confirm_user(
        email=decoded_data["email"], session_token=decoded_data["session_token"]
    )


@router.post("/verify-user/google")
async def verify_user_google(
    decoded_data: Annotated[EmailToken, Depends()]
) -> SessionToken:
    return confirm_user(
        email=decoded_data["email"], session_token=decoded_data["session_token"]
    )
