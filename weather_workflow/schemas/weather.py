from pydantic import BaseModel, Field

class WeatherToolInput(BaseModel):
    """
    Schema for validating weather tool input arguments from the LLM.
    """
    location: str = Field(
        description="Name of the city, for example Kolkata or Paris"
    )
