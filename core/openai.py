import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

openai = OpenAI(api_key=OPENAI_KEY)
