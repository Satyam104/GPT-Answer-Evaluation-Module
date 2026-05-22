import logging
from openai import OpenAI, OpenAIError, RateLimitError, AuthenticationError, APIConnectionError

from app.core.config import settings
from app.services.prompt_builder import build_evaluation_prompt
from app.services.response_parser import parse_evaluation_response
from app.models.request_models import EvaluationRequest, EvaluationResponse

logger = logging.getLogger(__name__)

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    """Lazily initialize and return the OpenAI client."""
    global _client
    if _client is None:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured. Please set it in your .env file.")
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


def evaluate_answer(request: EvaluationRequest) -> EvaluationResponse:
    """
    Main evaluation pipeline:
    1. Build prompt
    2. Call GPT API
    3. Parse response
    4. Return structured evaluation

    Args:
        request: EvaluationRequest with question and answer

    Returns:
        EvaluationResponse with scores and feedback

    Raises:
        RuntimeError: on unrecoverable API or parsing failures
    """
    logger.info("Evaluating answer for question: %s...", request.question[:60])

    messages = build_evaluation_prompt(request.question, request.answer)

    raw_response = _call_gpt(messages)

    result = parse_evaluation_response(raw_response)

    logger.info("Evaluation complete — correctness=%d, depth=%d, clarity=%d",
                result["correctness"], result["depth"], result["clarity"])

    return EvaluationResponse(**result)


def _call_gpt(messages: list[dict]) -> str:
    """
    Call the OpenAI ChatCompletion API.

    Args:
        messages: List of message dicts

    Returns:
        Raw string content from the model

    Raises:
        RuntimeError: with user-friendly message on API errors
    """
    client = _get_client()

    try:
        response = client.chat.completions.create(
            model=settings.GPT_MODEL,
            messages=messages,
            temperature=settings.GPT_TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )
        content = response.choices[0].message.content
        if content is None:
            raise RuntimeError("GPT returned an empty response.")
        return content

    except AuthenticationError:
        logger.error("OpenAI authentication failed. Check your API key.")
        raise RuntimeError("Invalid OpenAI API key. Please check your configuration.")

    except RateLimitError:
        logger.error("OpenAI rate limit exceeded.")
        raise RuntimeError("OpenAI rate limit exceeded. Please try again later.")

    except APIConnectionError as e:
        logger.error("OpenAI connection error: %s", e)
        raise RuntimeError("Could not connect to OpenAI API. Check your internet connection.")

    except OpenAIError as e:
        logger.error("OpenAI API error: %s", e)
        raise RuntimeError(f"OpenAI API error: {str(e)}")
