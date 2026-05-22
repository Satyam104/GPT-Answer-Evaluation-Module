from pydantic import BaseModel, Field, field_validator
from typing import Optional


class EvaluationRequest(BaseModel):
    question: str = Field(..., description="The question to evaluate the answer against")
    answer: str = Field(..., description="The candidate's answer to evaluate")

    @field_validator("question")
    @classmethod
    def question_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Question must not be empty or whitespace")
        if len(v) < 3:
            raise ValueError("Question is too short (minimum 3 characters)")
        return v

    @field_validator("answer")
    @classmethod
    def answer_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Answer must not be empty or whitespace")
        if len(v) < 3:
            raise ValueError("Answer is too short (minimum 3 characters)")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "Explain FastAPI",
                "answer": "FastAPI is a Python framework used for building APIs."
            }
        }
    }


class EvaluationResponse(BaseModel):
    correctness: int = Field(..., ge=0, le=10, description="Factual accuracy score (0-10)")
    depth: int = Field(..., ge=0, le=10, description="Answer depth/thoroughness score (0-10)")
    clarity: int = Field(..., ge=0, le=10, description="Clarity and structure score (0-10)")
    feedback: str = Field(..., description="Constructive feedback for the candidate")

    model_config = {
        "json_schema_extra": {
            "example": {
                "correctness": 8,
                "depth": 6,
                "clarity": 7,
                "feedback": "Good basic explanation, but missing async support and automatic API documentation."
            }
        }
    }


class ErrorResponse(BaseModel):
    detail: str
    error_type: Optional[str] = None
