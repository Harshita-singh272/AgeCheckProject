# Age Verification System

A web-based Age Verification System developed using **FastAPI**, **Streamlit**, and **DeepFace**. The application estimates a person's age from an uploaded image and determines whether they meet a user-defined age threshold.

---

## Team Members

- **Ayesha Riyaz**
- **Harshita Singh**

---

## Features

- Upload an image for age verification.
- AI-based age estimation using DeepFace.
- Customizable age threshold.
- PASS / FAIL / INCONCLUSIVE decision.
- Confidence score display.
- Verification activity logging.
- Modern Streamlit user interface.
- FastAPI backend for prediction.

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
│
├── demo/
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
git clone <repository-url>
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

## API Endpoint

### POST `/check_age`

Uploads an image and returns:

- Estimated Age
- Threshold
- Verification Decision
- Confidence Score

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

## Future Improvements

- User authentication
- Database integration
- Multiple face detection
- Improved confidence estimation
- Deployment on cloud platforms

---

## License

This project was developed for educational purposes.