# Age Verification System

A web-based Age Verification System developed using **FastAPI**, **Streamlit**, and **DeepFace**. The application estimates a person's age from an uploaded image and determines whether they meet a user-defined age threshold.

---

## Team Members

- **Ayesha Riyaz**
- **Harshita Singh**

---

## Features

- Upload an image for age verification
- AI-based age estimation using DeepFace
- Configurable age thresholds (18+, 21+, 25+, 50+, 60+)
- Boolean PASS / FAIL / INCONCLUSIVE verification
- Confidence score visualization
- Separate User and Admin interfaces
- Admin authentication using passkey
- Detailed administrator diagnostics
- Verification activity logging
- Verification statistics dashboard
- Threshold-wise analytics using Plotly
- FastAPI REST API backend
- Streamlit-based interactive frontend
---

## Tech Stack

### Frontend
- Streamlit

### Backend
- FastAPI
- Uvicorn

### AI Model
- DeepFace

### Language
- Python 3.11

---

## Project Structure

```
AgeCheckProject/
│
├── app/
│   ├── admin.py
│   ├── config.py
│   ├── main.py
│   ├── schemas.py
│   ├── services.py
│   ├── storage.py
│
├── data/
│   └── test_images/
|
├── assets/
|    └── Screenshots of ui/
├── tests/
│
├── app_ui.py
├── requirements.txt
├── README.md
└── report.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/Harshita-singh272/AgeCheckProject
cd AgeCheckProject
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

Windows

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Backend

```bash
python -m uvicorn app.main:app --reload
```

The FastAPI server starts at:

```
http://127.0.0.1:8000
```

---

## Running the Frontend

Open a new terminal and activate the virtual environment.

Run:

```bash
streamlit run app_ui.py
```

The Streamlit application opens automatically in your browser.

---

## API Endpoints

### GET `/`

Returns a welcome message indicating that the API is running.

**Response**

```json
{
  "message": "Age Check API Running"
}
```

---

### GET `/health`

Checks whether the API is healthy.

**Response**

```json
{
  "status": "ok"
}
```

---

### GET `/version`

Returns the current API version.

**Response**

```json
{
  "module": "age_check",
  "version": "0.1.0"
}
```

---

### POST `/check_age`

Performs age verification for a normal user.

**Request**

- Image (multipart/form-data)
- Threshold (form field)

**Response**

- Decision (PASS / FAIL / INCONCLUSIVE)
- Threshold
- Confidence Score

---

### POST `/admin/login`

Authenticates an administrator.

**Request**

```json
{
  "passkey": "your_admin_passkey"
}
```

**Response**

```json
{
  "authenticated": true,
  "message": "Admin access granted"
}
```

---

### POST `/admin/check_age`

Performs administrator verification.

**Request**

- Admin passkey
- Image
- Threshold

**Response**

Returns additional diagnostic information:

- Estimated Age
- Threshold
- Difference from Threshold
- Decision
- Confidence
- Latency
- Model Name
---

## Verification Decisions

| Decision | Meaning |
|----------|---------|
| PASS | Estimated age is above the threshold |
| FAIL | Estimated age is below the threshold |
| INCONCLUSIVE | Prediction confidence is low |

---

## Dependencies

- FastAPI
- Streamlit
- DeepFace
- TensorFlow
- Pillow
- OpenCV
- NumPy
- Requests

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---
## 🔑 Admin Panel Access

The project includes an administrator panel that provides additional diagnostic information such as the estimated age, confidence score, model details, verification history, and analytics. This functionality is intended for evaluation and learning purposes only.

The actual `.env` file is not included in this repository.

### Demo Passkey

For evaluation, use the following administrator passkey:

```text
admin123
```

Create a `.env` file in the project root with:

```env
ADMIN_PASSKEY=admin123
```

You may replace `admin123` with any custom passkey if you wish.

---
## Future Improvements

- User authentication
- Database integration
- Multiple face detection
- Improved confidence estimation
- Deployment on cloud platforms

---

## License

This project was developed for educational purposes.