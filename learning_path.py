from ai_client import ask_gemini


def recommend(topic: str) -> str:
    prompt = (
        "Create a learning path for this topic. Include Beginner, "
        "Intermediate, and Advanced stages. Give an estimated timeline, "
        "important concepts, and useful resource types. "
        "Do not invent specific URLs. Topic: "
        + topic
    )
    return ask_gemini(prompt)