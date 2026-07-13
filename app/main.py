from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from app.schemas import HealthResponse, AgeCheckResponse, AdminLoginRequest, AdminLoginResponse, AdminAgeResponse
from app.services import estimate_age, check_threshold
from app.storage import save_verification_log
from app.admin import verify

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


@app.get("/version")
def version():
    return {"module": "age_check", "version": "0.1.0"}


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


@app.post(
    "/admin/login",
    response_model=AdminLoginResponse
)
def admin_login(request: AdminLoginRequest):
    if verify(request.passkey):

        return {
            "authenticated": True,
            "message": "Admin access granted"
        }
    
    return {
        "authenticated": False,
        "message": "Invalid passkey"
    }


@app.post("/admin/check_age", response_model=AdminAgeResponse)
async def admin_check_age(
    passkey: str = Form(...),
    image: UploadFile = File(...),
    threshold: int = Form(...)
):
    if not verify(passkey):

        raise HTTPException( 
        status_code = 401,
        detail = "Invalid Admin Passkey"
        )
    
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

        return {

        "estimated_age": round(age,2),

        "threshold": threshold,

        "difference": round(age-threshold,2),

        "decision": result["decision"],

        "confidence": result["confidence"],

        "latency_ms": latency_ms,

        "model_name":"DeepFace"

        }
    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)
            
          

