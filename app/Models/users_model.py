# pylint: disable=E0401, E0611, W0703, R0903

"""
Schema for incoming post requests data
"""

# from datetime import datetime
import sqlalchemy
from fastapi import HTTPException, status

from app.Utils import crypt
from app.schemas.users_schema import User
from app.Exceptions.post_exceptions import SomethingWentWrongException

# ---------------------------------------------------------------------------- #
#                                 DB Operations                                #
# ---------------------------------------------------------------------------- #


def get_user(user_id, database):
    """
    Get a user with given post_id

    Args:
        user_id (int): User id

    Returns:
        dict: User details
    """
    user = database.query(User).filter(User.id == user_id).first()

    if user:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")


def get_user_by_email(creds, database):
    """
    Get a user using email and validate the password

    Args:
        user_id (UserLogin): User credentials

    Returns:
        dict: User details
    """
    try:
        return database.query(User).filter(User.email == creds.username).first()

    except Exception as error:
        print("ERROR while getting user by email")
        print(f"MSG ==> {get_user_by_email}")
        raise SomethingWentWrongException(error) from error


def create_user(user, database):
    """
    Create a new post

    Args:
        post (Post): New post data

    Returns:
        dict: Update post data
    """
    try:
        user.password = crypt.hash_password(user.password)
        inserted_user = User(**user.dict())

        database.add(inserted_user)
        database.commit()
        database.refresh(inserted_user)

        if inserted_user:
            return inserted_user
        return None

    except sqlalchemy.exc.IntegrityError as error:
        print(f'User with "email={user.email}" already exists!')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists!",
        ) from error
