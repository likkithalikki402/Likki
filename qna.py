from ai_client import ask_gemini


def answer_question(question: str) -> str:
    prompt = (
        "Answer this question clearly and simply. "
        "Use the same language as the question. "
        "If you are unsure, say so. Question: "
        + question
    )
    return ask_gemini(prompt)