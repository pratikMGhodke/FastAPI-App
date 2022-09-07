# pylint: disable=E0401, W0707

"""
Routes for USERS related operations
"""

# Imports
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.Utils import crypt, oauth2
from app.Models import users_model
from app.schemas import users_schema
from app.Database.db import connect_to_postgres_db
from app.Exceptions.post_exceptions import SomethingWentWrongException


# FastAPI Router
router = APIRouter(tags=["Authentication"])

# ---------------------------------------------------------------------------- #
#                                    Routes                                    #
# ---------------------------------------------------------------------------- #


@router.post("/api/login", response_model=users_schema.AuthToken)
def login(
    creds: OAuth2PasswordRequestForm = Depends(),
    database: Session = Depends(connect_to_postgres_db)
):
    """
    Login user and return a JWT access token

    Args:
        creds (OAuth2PasswordRequestForm): User creds - username, password
        [above requires data as form fields]

        database (Session, optional):
            Postgres db session object. Defaults to Depends(connect_to_postgres_db).

    Raises:
        HTTPException: HTTP_403_FORBIDDEN
        HTTPException: HTTP_500_INTERNAL_SERVER_ERROR

    Returns:
        str: JWT access Token
    """
    try:
        # Get user
        user = users_model.get_user_by_email(creds, database)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
            )

        # Verify password
        if not crypt.verify(creds.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
            )

        # Create a JWT Token
        access_token = oauth2.create_access_token(data = {"user_id": user.id})
        # access_token = "this is token"
        return {"access_token": access_token, "token_type": "bearer"}

    except SomethingWentWrongException as error:
        print("Error in routes:", error)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )
