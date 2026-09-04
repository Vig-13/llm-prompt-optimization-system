# Gemini client creation

from google import genai

from app.config import GEMINI_API_KEY


MODEL_NAME = "gemini-3.5-flash-lite"


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def test_connection():

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents="Gemini connection successful"
    )

    return response.text