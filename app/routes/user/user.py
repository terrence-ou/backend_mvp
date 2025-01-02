from typing import Annotated
from fastapi import APIRouter, Depends

# from app.dependencies import decode_apple_token, decode_google_token, confirm_user
from app.routes.user.services import (
    decode_apple_token,
    decode_google_token,
    confirm_user,
    get_session_token,
    signout_user,
)
from app.routes.user.schemas import SessionToken, EmailToken

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/signin/apple")
async def verify_user_apple(
    decoded_data: Annotated[EmailToken, Depends(decode_apple_token)]
) -> SessionToken:
    return confirm_user(
        email=decoded_data["email"], session_token=decoded_data["session_token"]
    )


@router.post("/signin/google")
async def verify_user_google(
    decoded_data: Annotated[EmailToken, Depends(decode_google_token)]
) -> SessionToken:
    return confirm_user(
        email=decoded_data["email"], session_token=decoded_data["session_token"]
    )


@router.post("/signout")
async def signout(session_token: Annotated[str, Depends(get_session_token)]) -> None:
    signed_out_users = signout_user(session_token)
    if len(signed_out_users) == 0:
        return {"message": "No users signed out"}
    return {"message": f"Signed out users: {" ".join(signed_out_users)}"}
