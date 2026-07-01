from fastapi import FastAPI, UploadFile, File, Form
from app.schemas import HealthResponse, AgeCheckResponse
from app.services import estimate_age, check_threshold
from app.storage import save_verification_log

import tempfile
import os
import uuid
import time
from datetime import datetime

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
    start_time = time.perf_counter()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    ) as temp_file:
        temp_file.write(await image.read())
        temp_path = temp_file.name

    try:
        age = estimate_age(temp_path)

        result = check_threshold(age, threshold)

        latency_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2
        )

        log_data = {
            "event_id": f"evt_{uuid.uuid4().hex[:8]}",
            "timestamp": datetime.now().isoformat(),
            "threshold": threshold,
            "predicted_age": round(age, 2),
            "decision": result["decision"],
            "confidence": result["confidence"],
            "latency_ms": latency_ms,
            "model_name": "DeepFace",
            "image_filename": image.filename
        }

        save_verification_log(log_data)

        return result

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)