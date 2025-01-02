from typing import Annotated
from fastapi import APIRouter, Depends
from app.routes.user.services import get_session_token
from app.routes.generate.services import generate_response
from app.routes.generate.schemas import DictionaryResponse, UserInput, ModeEnum

router = APIRouter(prefix="/generate", tags=["generate"])


@router.post("/words")
async def generate_words(
    user_input: UserInput,
    session_token: Annotated[str, Depends(get_session_token)],
) -> DictionaryResponse:
    response = generate_response(
        ModeEnum.lookup, user_input.prompt, user_input.prefered_language
    )
    return response


@router.post("/scene")
async def generate_words(
    user_input: UserInput,
    session_token: Annotated[str, Depends(get_session_token)],
) -> DictionaryResponse:
    response = generate_response(
        ModeEnum.scene, user_input.prompt, user_input.prefered_language
    )
    return response
