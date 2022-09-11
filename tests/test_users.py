"""
Tests for out API application
"""
import pytest
from jose import jwt
from pprint import pprint
from fastapi import status

from app.schemas.users_schema import UserResponse, AuthToken
from app.settings.settings import Settings

settings = Settings()

# ---------------------------------------------------------------------------- #

EMAIL = "pratik2.user@gmail.com"
PASSWORD = "secret_password"


# def test_health(client):
#     """Test health endpoint"""
#     response = client.get("/api/health")
#     assert 200 == response.status_code
#     assert "OK" == response.json()


def test_create_user(client):
    """Test create user endpoint"""
    response = client.post(
        "/api/users/",
        json={"email": EMAIL, "password": PASSWORD},
    )
    response_data = response.json()
    resp_user = UserResponse(**response_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert resp_user.email == EMAIL


def test_login_user(client, test_user):
    """Test user login feature [SUCCESS]"""
    response = client.post(
        "/api/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    token = AuthToken(**response.json())
    payload = jwt.decode(
        token.access_token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALOGORITHM
    )
    user_id = payload.get("user_id")
    assert response.status_code == status.HTTP_200_OK
    assert user_id == test_user["id"]
    assert token.token_type == "bearer"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 403),
        ("pratik@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "password123", 422),
        ("pratik@gmail.com", None, 422),
    ],
)
def test_failed_login_user(client, email, password, status_code):
    """Test user login feature [FAILED]"""
    response = client.post(
        "/api/login",
        data={
            "username": email,
            "password": password,
        },
    )
    assert response.status_code == status_code
    # assert response.json()["detail"] == "Invalid Credentials"
