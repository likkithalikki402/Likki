from gemini_client import generate_response


def ask_gemini(prompt: str) -> str:
    return generate_response(prompt)