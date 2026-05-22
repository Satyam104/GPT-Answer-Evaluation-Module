from app.core.constants import EVALUATION_SYSTEM_PROMPT, EVALUATION_USER_TEMPLATE
from app.core.config import settings


def build_evaluation_prompt(question: str, answer: str) -> list[dict]:
    """
    Builds the messages payload for the OpenAI ChatCompletion API.

    Args:
        question: The interview/assessment question
        answer: The candidate's answer

    Returns:
        List of message dicts for the API call
    """
    # Truncate answer if it exceeds max length to avoid token overflow
    truncated_answer = answer
    if len(answer) > settings.MAX_ANSWER_LENGTH:
        truncated_answer = answer[:settings.MAX_ANSWER_LENGTH] + "... [truncated]"

    user_message = EVALUATION_USER_TEMPLATE.format(
        question=question.strip(),
        answer=truncated_answer.strip()
    )

    return [
        {"role": "system", "content": EVALUATION_SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]
