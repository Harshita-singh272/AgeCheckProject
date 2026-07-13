# Activity Log

## Purpose

The Age Verification System maintains an activity log to record every verification request processed by the application. The log provides a history of requests for monitoring, debugging, testing, and audit purposes.

The activity log is stored in:

```
data/activity_log.jsonl
```

Each verification request is saved as a separate JSON object (JSON Lines format).

---

# Information Logged

For every verification request, the system records:

* Timestamp of the request
* Uploaded image filename (if available)
* Estimated age
* Selected age threshold
* Verification decision (PASS or FAIL)
* Confidence score
* Request status

This information helps verify that the application is functioning correctly without storing unnecessary personal information.

---

# Logging Workflow

1. User uploads an image.
2. The image is processed by the DeepFace age estimation model.
3. The predicted age is compared with the selected threshold.
4. A verification decision is generated.
5. The request details are appended to `activity_log.jsonl`.

---

# Example Log Entry

```json
{
    "timestamp": "2026-07-13T10:45:30",
    "filename": "image.jpg",
    "estimated_age": 23,
    "threshold": 18,
    "decision": "PASS",
    "confidence": 92
}
```

---

# Purpose of Maintaining Logs

The activity log is useful for:

* Monitoring application usage
* Debugging unexpected behavior
* Verifying API responses during testing
* Tracking verification requests
* Maintaining an audit trail for development and evaluation

---

# Notes

* Log entries are stored in JSON Lines (`.jsonl`) format.
* Each request generates one log entry.
* The log is intended for development, testing, and demonstration purposes.
* Sensitive user information is not intentionally stored beyond the data required for verification records.

---

## Implementation

The logging functionality is implemented in the project backend. Whenever the `/check_age` API endpoint processes a request, the application records the verification details and appends them to `data/activity_log.jsonl`. The logging process is handled automatically and does not require any user interaction.
