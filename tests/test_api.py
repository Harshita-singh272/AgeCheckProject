from fastapi.testclient import TestClient
from app.main import app
from app.config import ADMIN_PASSKEY

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_admin_login():

    response = client.post(
        "/admin/login",
        json={"passkey": ADMIN_PASSKEY}
    )

    assert response.status_code == 200
    assert response.json()["authenticated"] is True

def test_admin_login_invalid():

    response = client.post(
        "/admin/login",
        json={"passkey": "wrong_passkey"}
    )

    assert response.status_code == 200
    assert response.json()["authenticated"] is False

def test_check_age():

    with open("data/test_images/image.jpg", "rb") as image:

        response = client.post(
            "/check_age",
            files={
                "image": ("image.jpg", image, "image/jpeg")
            },
            data={
                "threshold": 18
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert "decision" in data
    assert "confidence" in data
    assert "is_above_threshold" in data

def test_admin_check_age():

    with open("data/test_images/image.jpg", "rb") as image:

        response = client.post(
            "/admin/check_age",
            files={
                "image": ("image.jpg", image, "image/jpeg")
            },
            data={
                "passkey": ADMIN_PASSKEY,
                "threshold": 18
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert "estimated_age" in data
    assert "decision" in data
    assert "confidence" in data