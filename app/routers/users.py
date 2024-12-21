from typing import Annotated
from fastapi import APIRouter, Depends
from app.dependencies import get_session_token

router = APIRouter(
    prefix="/users", tags=["users"], dependencies=[Depends(get_session_token)]
)


@router.get("/test/")
async def read_test_user(session_token: Annotated[str, Depends(get_session_token)]):
    print(session_token)
    return {"session_token": session_token}
