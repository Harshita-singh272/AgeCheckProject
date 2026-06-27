from fastapi import FastAPI, UploadFile, File, Form
from app.schemas import HealthResponse, AgeCheckResponse
from app.services import estimate_age, check_threshold

import tempfile
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Age Check API Running"}

@app.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}

@app.post("/check_age", response_model=AgeCheckResponse)
async def check_age(
    image: UploadFile = File(...),
    threshold: int = Form(...)
):
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    ) as temp_file:
        temp_file.write(await image.read())
        temp_path = temp_file.name

    try:
        age = estimate_age(temp_path)

        result = check_threshold(
            age,
            threshold
        )

        return result

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)