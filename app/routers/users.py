from typing import Annotated
from fastapi import APIRouter, Depends
from app.dependencies import decode_apple_token

router = APIRouter(
    prefix="/users", tags=["users"], dependencies=[Depends(decode_apple_token)]
)


@router.post("/verify-user/apple")
async def read_test_user(email: Annotated[str, Depends(decode_apple_token)]):
    return {"email": email}
