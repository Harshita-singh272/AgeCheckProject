# Project 5 – Age Check with Boolean Privacy Demo
## Internship Report

**Team:** Harshita Singh, Ayesha Riyaz
**Date:** July 13, 2026

---

### 1. What We Built

We built a privacy-preserving age verification system using FastAPI, DeepFace, and
Streamlit. A user uploads an image and selects an age threshold (18+, 21+, or 60+).
DeepFace handles face detection and age estimation internally, and the predicted
age is compared against the threshold. Normal users receive only a boolean decision
(PASS/FAIL/INCONCLUSIVE) with a confidence score — never the raw predicted age.

The system has two access levels:
- **User flow:** public, boolean-only results via `/check_age`
- **Admin flow:** passkey-protected, via `/admin/login` and `/admin/check_age`,
  revealing estimated age, confidence, threshold difference, and diagnostics for
  internal model evaluation only

The admin passkey is loaded from a `.env` file (`python-dotenv`) and never hardcoded.

### 2. Approach & Implementation

We integrated the DeepFace age estimation model directly, using
`DeepFace.analyze(actions=["age"])` on the uploaded image. DeepFace handles its own
internal face detection and preprocessing before running age estimation — we did
not build a separate face-detection or image-preprocessing pipeline ourselves.

We implemented the threshold comparison logic in `check_threshold()`, which takes
the predicted age and the user-supplied threshold and returns a decision
(PASS/FAIL/INCONCLUSIVE), a boolean `is_above_threshold` flag, and a confidence
score based on how close the prediction is to the threshold. We validated the full
`/check_age` endpoint through Swagger UI to confirm upload, prediction, comparison,
and response all worked correctly — and that the response never exposed the raw
predicted age, satisfying the core privacy requirement.

We then built a Streamlit frontend so the system could be used as a real demo
rather than just an API. The interface supports image upload, an image preview,
threshold selection, and a clear PASS/FAIL/INCONCLUSIVE result display,
communicating with the FastAPI backend over HTTP. We added the passkey-protected
admin flow and activity logging on top of this working core.


- **Model:** DeepFace age estimation (`DeepFace.analyze(actions=["age"])`)

- **Face detection:** handled internally by DeepFace (no separate OpenCV step)

- **Decision logic:** PASS if predicted age ≥ threshold, FAIL if below, and
  INCONCLUSIVE if the difference is within 2 years of the threshold

- **Access control:** `admin.py` verifies the passkey against `.env` before
  granting access to diagnostics; invalid passkeys are denied without affecting
  the normal `/check_age` flow

### 3. Decision Logic: PASS / FAIL / INCONCLUSIVE

The `check_threshold()` function compares the predicted age against the
user-selected threshold and returns one of three decisions:

- **PASS** — predicted age is greater than or equal to the threshold, and the
  difference is more than 2 years (e.g. predicted age 25, threshold 21 → PASS)
- **FAIL** — predicted age is below the threshold, and the difference is more
  than 2 years (e.g. predicted age 15, threshold 18 → FAIL)
- **INCONCLUSIVE** — the predicted age is within 2 years of the threshold in
  either direction (e.g. predicted age 19 or 20 at an 18+ threshold → INCONCLUSIVE)

This margin exists because age estimation models are not perfectly precise, and
treating anything within a close range of the threshold as a hard PASS or FAIL
risks confidently returning the wrong decision. Returning INCONCLUSIVE instead
signals that the system isn't confident enough to make a binary call for that
borderline case.

Alongside the decision, the function returns:
- `is_above_threshold` — a boolean (`true`/`false`) indicating whether the
  predicted age met or exceeded the threshold
- `confidence` — a score reflecting how far the predicted age was from the
  threshold; predictions far from the threshold (in either direction) return
  higher confidence, while predictions close to the threshold return lower
  confidence, reinforcing why those cases are flagged INCONCLUSIVE


### 4. Test Results

We tested on 20 images with approximate known ages across thresholds 18, 21, and 60.

| Threshold | Correct Decisions | Inconclusive | Mean Absolute Error  |
|-----------|-------------------|--------------|----------------------|
| 18+       | 20/20              | 0            | 10.05 years         |
| 21+       | 18/20              | 2            | 10.05 years         |
| 60+       | 17/20              | 0            | 10.05 years         |

Average confidence: ~95% at 18+, ~88% at 21+, ~100% at 60+.

*(MAE reflects overall age-prediction accuracy and stays the same across all three
rows, since it measures how far predicted age was from actual age, independent of
which threshold is being checked.)*

**Notable finding:** predicted ages showed a strong tendency to cluster in a
narrow lower range regardless of the input image, alongside a broader pattern of
underestimation for older adults. All 3 incorrect decisions occurred at the 60+
threshold — individuals with actual ages 61, 65, and 69 were all predicted under
60 and incorrectly returned FAIL. This shows the underestimation issue isn't just
a raw-accuracy concern; it can directly flip real decisions near a threshold
boundary.

### 5. Privacy & Access Design Rationale

Two principles guided the design:

1. **Data minimization** — the public endpoint never returns estimated age, only
   a threshold-relative decision and confidence, consistent with how real-world
   age-gating systems only need "above/below a line."
2. **Role separation** — diagnostic data (raw age, confidence breakdown) is gated
   behind an authenticated admin route so normal users' privacy guarantee stays
   intact while we retain visibility for model evaluation.

### 6. Known Limitations

- During testing, we observed that predicted ages clustered consistently in a
  narrow range regardless of the input image, alongside underestimation that was
  especially pronounced for older adults. Investigating this, we traced a likely
  cause to how we call DeepFace: our `predict_age()` function uses
  `enforce_detection=False`, which allows inference to proceed even when a face
  isn't cleanly detected. This means the model may be running on a poorly
  isolated face region — or a fallback — rather than a properly detected face on
  every call, which would explain the clustering behavior we observed.
- This is a valuable finding in itself: `enforce_detection=False` is convenient
  for avoiding crashes on bad inputs, but it can silently degrade prediction
  quality rather than failing loudly — a tradeoff worth being explicit about when
  using DeepFace. The fix would be to set `enforce_detection=True` and add
  explicit face-count validation at the API level, rejecting images with zero or
  multiple detected faces before running age estimation.
- Due to project time constraints, we were not able to re-run the full 20-image
  test set with `enforce_detection=True` to fully confirm this fix, but we flag
  it as the most likely root cause and the first change we would make going
  forward.
- The passkey check is a simple shared-secret comparison — fine for a local
  learning demo, but not production-grade (no hashing, sessions, rate limiting).
- Evaluated on a modest sample (20 images), not large enough for firm
  conclusions about bias across broader demographics, even after the above fix.

### 7. Edge Cases Handled

- **Threshold near predicted age** → returns INCONCLUSIVE instead of a
  potentially wrong PASS/FAIL
- **Invalid admin passkey** → returns HTTP 401, access denied, no diagnostic
  data leaked
- **Temporary file cleanup** → uploaded images are written to a temp file for
  processing and deleted immediately after, regardless of success or failure
  (via `finally`), so no uploaded image persists on disk

**Not currently handled:** no-face and multiple-face detection are not
explicitly validated in our implementation — since `enforce_detection=False` is
used, DeepFace does not raise an error for these cases and instead proceeds
with whatever it can infer. This is directly related to the age-clustering
issue discussed in Known Limitations, and explicit face-count validation
(rejecting images with zero or multiple faces before calling `estimate_age()`)
is one of our identified next improvements.

### 8. Next Improvements

- Set `enforce_detection=True` in `predict_age()` and re-run the full test set to
  confirm whether this resolves the age-clustering and underestimation issue
- Compare DeepFace against InsightFace's age module for accuracy
- Widen the inconclusive margin for higher thresholds (e.g. 60+), given the
  larger observed error in that range
- Test for bias across lighting conditions and age groups with a larger sample
- Build the activity log dashboard in Streamlit
- Add rate limiting on repeated failed passkey attempts

---

*This project was developed as part of the ByoSync Internship Program for
educational purposes. It is not intended for production deployment and does
not claim compliance with commercial privacy, biometric, or regulatory
standards.*