from fastapi import FastAPI
from app.schemas import HealthResponse

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Age Check API Running"}
    
@app.get("/health" , response_model=HealthResponse)
    
def health():
    return {"status" : "ok"}