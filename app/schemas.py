from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str

class AgeCheckResponse(BaseModel):
    decision: str
    is_above_threshold: bool
    confidence: float