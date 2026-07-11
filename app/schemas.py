from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str

class AgeCheckResponse(BaseModel):
    decision: str
    is_above_threshold: bool
    confidence: float


class AdminLoginRequest(BaseModel):
    passkey: str

class AdminLoginResponse(BaseModel):
    authenticated: bool
    message: str

class AdminAgeResponse(BaseModel):
    estimated_age: float
    threshold: int
    difference: float
    decision: str
    confidence: float
    latency_ms: float
    model_name: str