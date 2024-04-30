import openai
import os

from dotenv import load_dotenv

load_dotenv()

# NOTE: create a .env file and set OPENAI_API_KEY=<your key> and MODEL=<your model choice>

MODEL = os.getenv("OPENAI_MODEL")
assert MODEL in ['gpt-3.5-turbo']

API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY
