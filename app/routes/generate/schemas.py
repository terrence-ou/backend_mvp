from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class WordDefinition(BaseModel):
    part_of_speech: str
    meaning: str
    examples: List[str]


class WordOrigin(BaseModel):
    language: str
    meaning: str


class WordTenses(BaseModel):
    present: str
    past: str
    continuous: str
    future: str


class Word(BaseModel):
    word: str
    origin: WordOrigin
    pronunciation: str
    definitions: List[WordDefinition]
    tenses: Optional[WordTenses] = None
    synonyms: List[str]
    antonyms: List[str]
    related_terms: List[str]


class DictionaryResponse(BaseModel):
    words: List[Word]
    failed: bool
    failed_message: str


class WordsPrediction(BaseModel):
    words: List[str]
    failed: bool
    failed_message: str


class UserInput(BaseModel):
    prompt: str


class ModeEnum(str, Enum):
    lookup = "lookup"
    scene = "scene"
