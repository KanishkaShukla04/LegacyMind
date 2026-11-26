
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini API key not found in .env file")

client = genai.Client(api_key=API_KEY)


def generate_answer(context):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=context
    )

    return response.text
