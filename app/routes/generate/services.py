from app.routes.generate.schemas import DictionaryResponse
from core.openai import openai
from app.routes.generate.system_prompts import words_loopup


def generate_response(prompt: str, prefered_language: str) -> DictionaryResponse:
    response = openai.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": words_loopup(prefered_language)},
            {"role": "user", "content": prompt},
        ],
        response_format=DictionaryResponse,
    )
    return response.choices[0].message.parsed


def get_from_db():
    pass
