import json
import re
import logging
from typing import Optional

from app.core.constants import FALLBACK_RESPONSE, MIN_SCORE, MAX_SCORE

logger = logging.getLogger(__name__)


def _clamp_score(value: int) -> int:
    """Clamp a score between MIN_SCORE and MAX_SCORE."""
    return max(MIN_SCORE, min(MAX_SCORE, int(value)))


def parse_evaluation_response(raw_text: str) -> dict:
    """
    Parse GPT's raw text response into a structured evaluation dict.

    Handles:
    - Clean JSON responses
    - JSON wrapped in markdown code blocks
    - Partial/malformed JSON with fallback

    Args:
        raw_text: Raw string response from GPT

    Returns:
        Dict with correctness, depth, clarity, feedback keys
    """
    if not raw_text or not raw_text.strip():
        logger.warning("Received empty response from GPT")
        return FALLBACK_RESPONSE.copy()

    text = raw_text.strip()

    # Attempt 1: Direct JSON parse
    parsed = _try_direct_parse(text)
    if parsed:
        return _validate_and_normalize(parsed)

    # Attempt 2: Extract JSON from markdown code block
    parsed = _try_extract_from_codeblock(text)
    if parsed:
        return _validate_and_normalize(parsed)

    # Attempt 3: Find JSON object with regex
    parsed = _try_regex_extract(text)
    if parsed:
        return _validate_and_normalize(parsed)

    logger.error("All JSON parsing attempts failed. Raw response: %s", text[:200])
    return FALLBACK_RESPONSE.copy()


def _try_direct_parse(text: str) -> Optional[dict]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _try_extract_from_codeblock(text: str) -> Optional[dict]:
    """Extract JSON from ```json ... ``` or ``` ... ``` blocks."""
    pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    match = re.search(pattern, text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    return None


def _try_regex_extract(text: str) -> Optional[dict]:
    """Find first {...} block in the text and attempt to parse it."""
    pattern = r"\{[\s\S]*?\}"
    match = re.search(pattern, text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return None


def _validate_and_normalize(data: dict) -> dict:
    """
    Validate parsed dict has required keys with correct types.
    Apply clamping and type coercion where needed.
    """
    required_keys = {"correctness", "depth", "clarity", "feedback"}

    if not required_keys.issubset(data.keys()):
        missing = required_keys - data.keys()
        logger.warning("GPT response missing keys: %s", missing)
        return FALLBACK_RESPONSE.copy()

    try:
        return {
            "correctness": _clamp_score(data["correctness"]),
            "depth": _clamp_score(data["depth"]),
            "clarity": _clamp_score(data["clarity"]),
            "feedback": str(data["feedback"]).strip()
        }
    except (TypeError, ValueError) as e:
        logger.error("Error normalizing GPT response: %s", e)
        return FALLBACK_RESPONSE.copy()
