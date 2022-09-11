"""
Test database connection
"""

# Imports
import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.Database import db
from app.settings import settings

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


@pytest.fixture
def session():
    """Create DB session"""
    db.base.metadata.drop_all(bind=engine)
    db.base.metadata.create_all(bind=engine)
    database = testing_session_local()
    try:
        yield database
    finally:
        database.close()


@pytest.fixture
def client(session):
    def connect_to_test_postgres_db():
        """Create test postgres session"""
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[db.connect_to_postgres_db] = connect_to_test_postgres_db
    yield TestClient(app)
