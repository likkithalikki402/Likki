import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

ENV_FILE = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_FILE, override=True)


def generate_response(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.6-flash").strip()

    if not api_key or api_key in {
        "YOUR_API_KEY",
        "paste_your_api_key_here",
    }:
        raise ValueError("Set GEMINI_API_KEY in the .env file.")

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )

        answer = (response.text or "").strip()

        if not answer:
            raise ValueError("The Gemini response is empty.")

        return answer

    except Exception as error:
        raise RuntimeError(f"Gemini API error: {error}") from error


def ask_gemini(prompt: str) -> str:
    return generate_response(prompt)
