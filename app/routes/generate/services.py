from app.routes.generate.schemas import (
    DictionaryResponse,
    WordsPrediction,
    ModeEnum,
    Word,
)
from core.db import db
from core.openai import openai
import app.routes.generate.system_prompts as system_prompts


def generate_response(mode: ModeEnum, user_prompt: str):
    prediction_prompt = (
        system_prompts.predict_words
        if mode == ModeEnum.lookup
        else system_prompts.predict_scene
    )
    definiton_prompt = system_prompts.words_loopup

    word_prediction = openai.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": prediction_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format=WordsPrediction,
    )
    # return failed message if failed in predicting scenes
    prediction_response = word_prediction.choices[0].message.parsed
    if prediction_response.failed:
        return DictionaryResponse(
            words=[],
            failed=True,
            failed_message=prediction_response.failed_message,
        )

    words = []

    for word in prediction_response.words:
        definiton_response = openai.beta.chat.completions.parse(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": definiton_prompt},
                {"role": "user", "content": word},
            ],
            response_format=Word,
        )
        words.append(definiton_response.choices[0].message.parsed)
    return DictionaryResponse(words=words, failed=False, failed_message="")
