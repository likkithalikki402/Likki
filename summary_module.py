from ai_client import ask_gemini


def summarize(text: str) -> str:
    prompt = (
        "Summarize this study material in simple language. "
        "Keep all important facts. Use short bullet points. Material:\n"
        + text
    )
    return ask_gemini(prompt)