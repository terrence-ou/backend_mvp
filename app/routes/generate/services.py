from app.routes.generate.schemas import DictionaryResponse, ModeEnum
from core.openai import openai
from app.routes.generate.system_prompts import words_loopup, scene_prediction


def generate_response(
    mode: ModeEnum, user_prompt: str, prefered_language: str
) -> DictionaryResponse:

    system_prompt = ""
    if mode == ModeEnum.scene:
        system_prompt = scene_prediction(prefered_language)
    else:
        system_prompt = words_loopup(prefered_language)

    response = openai.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format=DictionaryResponse,
    )
    return response.choices[0].message.parsed


def get_from_db():
    pass
