from typing import Annotated
from fastapi import APIRouter, Depends

from app.routes.user.services import (
    decode_apple_token,
    decode_google_token,
    confirm_user,
    get_session_token,
    signout_user,
    verify_user_session,
)
from app.routes.user.schemas import SessionToken, EmailToken, ValidationResponse

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
    signed_out_user = signout_user(session_token)
    if not signed_out_user:
        return {"message": "No users signed out"}
    return {"message": f"Signed out users: {signed_out_user}"}


@router.post("/verify_session")
async def verify_session(session_token: Annotated[str, Depends(get_session_token)]):
    validation_response = verify_user_session(session_token)
    return validation_response
