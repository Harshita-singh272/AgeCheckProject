# Day 3 Activity Log

Date: 26 June 2026

## Developer A

* Integrated DeepFace age estimation model.
* Implemented `predict_age()`.
* Tested age prediction on sample images.
* Verified model inference works correctly.

## Developer B

* Implemented image loading and validation.
* Implemented image preprocessing pipeline.
* Added RGB conversion.
* Added image resizing (224x224).
* Added image normalization.
* Tested preprocessing on sample images.
* Verified error handling for missing files.

## Integration

* Combined preprocessing and age prediction workflows.
* Implemented `estimate_age()`.
* Created integration test.
* Successfully generated age predictions from test images.

# Day 4 Activity Log

Date: 27 June 2026

## Objectives

* Implement and verify threshold-based age validation logic.
* Test integration between age estimation and threshold comparison.
* Validate API functionality through FastAPI Swagger UI.

## Tasks Completed

### 1. Threshold Logic Verification

* Reviewed `check_threshold()` function in `services.py`.
* Verified comparison between predicted age and user-defined threshold.
* Confirmed generation of:

  * PASS / FAIL decision
  * Boolean result (`is_above_threshold`)
  * Confidence score

### 2. Unit Testing

Executed multiple test cases using local image samples and manually supplied threshold values.

Test cases included:

* Predicted age > threshold
* Predicted age < threshold
* Predicted age = threshold
* Adult image with threshold 18
* Child image with threshold 18
* Senior image with threshold 60

### 3. Integration Testing

* Used `estimate_age()` to obtain age predictions from DeepFace.
* Passed predicted ages into `check_threshold()`.
* Verified correct decision outputs.

### 4. API Validation

* Started FastAPI server using Uvicorn.
* Accessed Swagger UI (`/docs`).
* Uploaded test images through `/check_age`.
* Confirmed successful API responses.

## Observations

* DeepFace age estimation can vary significantly depending on image quality and face detection accuracy.
* Threshold logic behaved correctly for all tested scenarios.
* API successfully returned threshold decision results without exposing the raw predicted age.

## Status

Day 4 objectives completed successfully.
