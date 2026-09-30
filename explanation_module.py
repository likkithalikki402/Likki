from ai_client import ask_gemini


def explain(topic: str) -> str:
    prompt = (
        "Explain this topic in simple language. "
        "Give a short definition, one easy example, and 3 key points. "
        "Use the same language as the input. Topic: "
        + topic
    )
    return ask_gemini(prompt)