"""
Tests for out API application
"""

from pprint import pprint
from fastapi import status

from app.schemas.users_schema import UserResponse
from .database import client, session

# ---------------------------------------------------------------------------- #

EMAIL = "pratik3.user@gmail.com"
PASSWORD = "secret_password"


def test_health(client):
    """Test health endpoint"""
    response = client.get("/api/health")
    assert 200 == response.status_code
    assert "OK" == response.json()


def test_create_user(client):
    """Test create user endpoint"""
    response = client.post(
        "/api/users/",
        json={"email": EMAIL, "password": PASSWORD},
    )
    response_data = response.json()
    print("Error Message!")
    pprint(response_data)
    resp_user = UserResponse(**response_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert resp_user.email == EMAIL
