"""
Test database connection
"""

# Imports
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.Database import db
from app.settings import settings
from app.schemas import users_schema, posts_schema
from app.Utils import oauth2

# App Settings
settings = settings.Settings()

# ---------------------------------------------------------------------------- #
#                                 Test Database                                #
# ---------------------------------------------------------------------------- #

# Constants
USER = settings.POSTGRES_USER
PASS = settings.POSTGRES_PASSWORD
HOST = settings.POSTGRES_HOST
DATABASE = settings.DATABASE

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASS}@{HOST}/{DATABASE}_test"

# Set up database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ---------------------------------------------------------------------------- #
#                                    Testing                                   #
# ---------------------------------------------------------------------------- #




@pytest.fixture()
def session():
    """Create DB session"""
    db.base.metadata.drop_all(bind=engine)
    db.base.metadata.create_all(bind=engine)
    database = testing_session_local()
    try:
        print('HERE in Session')
        yield database
    finally:
        database.close()


@pytest.fixture()
def client(session):
    def connect_to_test_postgres_db():
        """Create test postgres session"""
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[db.connect_to_postgres_db] = connect_to_test_postgres_db
    print('HERE in Client')
    yield TestClient(app)


@pytest.fixture()
def test_user(client):
    """Test create user endpoint"""
    EMAIL = "pratik3.user@gmail.com"
    PASSWORD = "secret_password"
    
    response = client.post(
        "/api/users/",
        json={"email": EMAIL, "password": PASSWORD},
    )
    response_data = response.json()
    resp_user = users_schema.UserResponse(**response_data)
    response_data["password"] = PASSWORD
    assert response.status_code == status.HTTP_201_CREATED
    assert resp_user.email == EMAIL

    return response_data

@pytest.fixture()
def test_user2(client):
    """Test create user endpoint"""
    EMAIL = "pratik31.user@gmail.com"
    PASSWORD = "secret_password"
    
    response = client.post(
        "/api/users/",
        json={"email": EMAIL, "password": PASSWORD},
    )
    response_data = response.json()
    resp_user = users_schema.UserResponse(**response_data)
    response_data["password"] = PASSWORD
    assert response.status_code == status.HTTP_201_CREATED
    assert resp_user.email == EMAIL

    return response_data


@pytest.fixture
def jwt_token(test_user):
    """Create a demo JWT token for dummy user"""
    return oauth2.create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, jwt_token):
    """Authorize dummy user"""
    client.headers = {**client.headers, "Authorization": f"Bearer {jwt_token}"}
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    """Create dummy posts"""
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user["id"],
        },
        {"title": "2nd title", "content": "2nd content", "owner_id": test_user["id"]},
        {"title": "3rd title", "content": "3rd content", "owner_id": test_user["id"]},
        {"title": "4th title", "content": "4th content", "owner_id": test_user2["id"]},
    ]

    def create_post_model(data):
        return posts_schema.Post(**data)
    
    session.add_all(list(map(create_post_model, posts_data)))
    session.commit()
    return session.query(posts_schema.Post).all()