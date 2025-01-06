from google.cloud.firestore_v1.base_query import FieldFilter

from app.routes.generate.schemas import (
    DictionaryResponse,
    WordsPrediction,
    ModeEnum,
    Word,
)
from core.db import db
from core.openai import openai
import app.routes.generate.system_prompts as system_prompts


def generate_response(
    mode: ModeEnum, user_prompt: str, session_token: str
) -> DictionaryResponse:
    # First predict the words the user is looking for
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
    # Then lookup or generate the words
    words = []
    num_generated = 0
    for word in prediction_response.words:
        # if the word is in the dictionary, get it from the database
        word_ref = db.collection("dictionary").document(word)
        if word_ref.get().exists:
            words.append(Word(**word_ref.get().to_dict()))
            continue
        # Otherwise, generate the word and store it in the database
        definiton_response = openai.beta.chat.completions.parse(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": definiton_prompt},
                {"role": "user", "content": word},
            ],
            response_format=Word,
        )
        parsed_word = definiton_response.choices[0].message.parsed
        word_ref.set(parsed_word.model_dump())
        words.append(parsed_word)
        num_generated += 1
    # update user usage
    update_user_usage(session_token, len(words), num_generated)
    return DictionaryResponse(words=words, failed=False, failed_message="")


# Helper functions
def update_user_usage(
    session_token: str, num_searched: int, num_generated: int
) -> None:
    user_query = (
        db.collection("users")
        .where(filter=FieldFilter("session_token", "==", session_token))
        .stream()
    )
    for user in user_query:
        user.reference.update(
            {
                "num_searched": user.to_dict().get("num_searched", 0) + num_searched,
                "num_generated": user.to_dict().get("num_generated", 0) + num_generated,
            }
        )
