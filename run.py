from app.core.config import settings


def is_answer_too_long(answer: str) -> bool:
    """Check if the answer exceeds the configured maximum length."""
    return len(answer) > settings.MAX_ANSWER_LENGTH


def is_answer_too_short(answer: str) -> bool:
    """Check if the answer is below the minimum meaningful length."""
    return len(answer.strip()) < settings.MIN_ANSWER_LENGTH


def sanitize_text(text: str) -> str:
    """Strip leading/trailing whitespace and normalize internal whitespace."""
    return " ".join(text.split())
