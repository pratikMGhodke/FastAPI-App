# pylint: disable=E0401, W0707

"""
Routes for USERS related operations
"""

# Imports
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter

from app.Models import users_model
from app.schemas import users_schema
from app.Database.db import connect_to_postgres_db

# FastAPI Router
router = APIRouter(prefix="/api/users", tags=["Users"])

# ---------------------------------------------------------------------------- #
#                                    Routes                                    #
# ---------------------------------------------------------------------------- #


@router.get("/{user_id}", response_model=users_schema.UserResponse)
def get_user(user_id: int, database: Session = Depends(connect_to_postgres_db)):
    """Return user info

    Args:
        user_id (int): User id

        database (Session, optional):
            Postgres db session object. Defaults to Depends(connect_to_postgres_db).

    Raises:
        HTTPException: HTTP_404_NOT_FOUND
        HTTPException: HTTP_500_INTERNAL_SERVER_ERROR

    Returns:
        dict: User info
    """

    try:
        user = users_model.get_user(user_id, database)
        return user

    except HTTPException as error:
        raise error

    except Exception as error:
        print("Error in routes:", error)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=users_schema.UserResponse,
)
def create_user(
    new_user: users_schema.UserCreate,
    database: Session = Depends(connect_to_postgres_db),
):
    """
    Create a new user

    Args:
        new_user (users_schema.UserCreate): User request data validator

        database (Session, optional):
            Postgres db session object. Defaults to Depends(connect_to_postgres_db).

    Raises:
        HTTPException: HTTP_409_CONFLICT [already exists]
        HTTPException: HTTP_500_INTERNAL_SERVER_ERROR

    Returns:
        dict: Newly created user info
    """

    try:
        inserted_user = users_model.create_user(new_user, database)
        return inserted_user

    except HTTPException as error:
        raise error

    except Exception as error:
        print("Error in routes:", error)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )
