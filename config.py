import logging
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.models.request_models import EvaluationRequest, EvaluationResponse, ErrorResponse
from app.services.evaluator import evaluate_answer

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/evaluate",
    response_model=EvaluationResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluate a candidate's answer",
    description=(
        "Accepts a question and a candidate answer, sends them to GPT for evaluation, "
        "and returns structured scores with feedback."
    ),
    responses={
        200: {"model": EvaluationResponse, "description": "Successful evaluation"},
        422: {"description": "Validation error (empty/short inputs)"},
        503: {"description": "GPT API unavailable or rate-limited"},
        500: {"description": "Internal server error"},
    }
)
async def evaluate_endpoint(request: EvaluationRequest) -> EvaluationResponse:
    """
    Evaluate a candidate answer using GPT.

    - **question**: The question being answered
    - **answer**: The candidate's response to evaluate
    """
    try:
        result = evaluate_answer(request)
        return result
    except ValueError as e:
        logger.warning("Validation error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except RuntimeError as e:
        error_msg = str(e)
        logger.error("Evaluation runtime error: %s", error_msg)

        if "rate limit" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=error_msg
            )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=error_msg
        )
    except Exception as e:
        logger.exception("Unexpected error during evaluation")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )


@router.get(
    "/health",
    summary="Health check",
    description="Returns the health status of the API."
)
async def health_check():
    return {"status": "ok", "service": "GPT Answer Evaluator"}
