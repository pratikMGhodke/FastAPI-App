# pylint: disable=E0401

"""
JWT auth operations
"""

# Imports
from datetime import datetime, timedelta

from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer

from app.Database import db
from app.schemas import users_schema
from app.settings import settings

# App Settings
settings = settings.Settings()

# Look on ENDPOINT for bearer tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    """
    Create a JSON web token

    Args:
        data (dict): Data to be encoded

    Returns:
        str: JWT token
    """

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALOGORITHM
    )


def verify_access_token(token: str, credentials_exceptions):
    """
    Verify a JWT access token

    Args:
        token (str): Access token
        credentials_exceptions (Exception): Exception to raise for unauthorization

    Returns:
        app.Models.users_schema.TokenData: Decoded token data (user_id)
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALOGORITHM
        )

        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exceptions

        token_data = users_schema.TokenData(id=user_id)
        return token_data

    except JWTError as error:
        print("JWT error!", error)
        raise credentials_exceptions from error


def get_current_user(
    token: str = Depends(oauth2_scheme),
    database: Session = Depends(db.connect_to_postgres_db),
):
    """
    Check if token is valid or not else raise an error

    Args:
        token (str, optional): JWT access token. Defaults to Depends(oauth2_scheme).
    """

    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exceptions)
    return (
        database.query(users_schema.User).filter(users_schema.User.id == token.id).first()
    )
