from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

class ConceptExplanation(BaseModel):
    """
    Schema for structured explanation of technical concepts returned by the LLM.
    """
    model_config = ConfigDict(extra="forbid")
    
    topic: str = Field(description="Name of the concept being explained")
    summary: str = Field(
        description="A concise explanation in beginner-friendly language"
    )
    difficulty: Literal["beginner", "intermediate", "advanced"]
    key_points: list[str] = Field(
        min_length=2,
        description="Important ideas the learner should remember",
    )
    example: str = Field(description="One practical example")
    confidence: float = Field(
        ge=0,
        le=1,
        description="Confidence score between 0 and 1",
    )
