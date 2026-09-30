import json
import re

from ai_client import ask_gemini


def generate_quiz(text: str) -> list:
    prompt = (
        "Create exactly 3 multiple-choice questions from this material. "
        "Each question must have exactly 4 options and one correct answer. "
        'Return only a JSON array. Each item format: '
        '{"question":"...","options":["A","B","C","D"],"answer":"A"}. '
        "Material:\n"
        + text
    )

    answer = ask_gemini(prompt)
    answer = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        answer.strip(),
        flags=re.IGNORECASE,
    )

    try:
        questions = json.loads(answer)

        if not isinstance(questions, list) or len(questions) != 3:
            raise ValueError("The quiz must contain exactly 3 questions.")

        for question in questions:
            if (
                not isinstance(question, dict)
                or not isinstance(question.get("question"), str)
                or not isinstance(question.get("options"), list)
                or len(question["options"]) != 4
                or question.get("answer") not in question["options"]
            ):
                raise ValueError("The quiz response has an invalid format.")

        return questions

    except (json.JSONDecodeError, ValueError, TypeError) as error:
        raise ValueError(
            "Could not create a valid quiz. Please try again."
        ) from error
