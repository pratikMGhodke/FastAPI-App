# pylint: disable=E0401, E0611, W0703, R0903

"""
Schema for incoming post requests data
"""

# from datetime import datetime
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException, status

import sqlalchemy
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column, Integer, String

from app.Utils import crypt
from app.Database import db
from app.Exceptions.post_exceptions import SomethingWentWrongException

# ---------------------------------------------------------------------------- #
#                                 Model Schemas                                #
# ---------------------------------------------------------------------------- #

# ------------------------------ Database Schema ----------------------------- #
class User(db.base):
    """Schema for Posts table"""

    __tablename__ = "users"

    # Columns
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("NULL"))


# ---------------------------------------------------------------------------- #
#                          Pydantic request validators                         #
# ---------------------------------------------------------------------------- #

class UserCreate(BaseModel):
    """CREATE User request data validator"""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """RESPONSE data validator"""

    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        """Configuration for the pydantic schema"""

        orm_mode = True  # This takes a SQLAlchemy response instead of dict[default]


class UserLogin(BaseModel):
    """LOGIN data validator"""

    email: EmailStr
    password: str


class AuthToken(BaseModel):
    """Access token data validator"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Data to create the access token validator"""

    id: Optional[str]


# # ---------------------------------------------------------------------------- #


# def init_posts_model():
#     """Initialize connection to the database"""

#     try:
#         db.base.metadata.create_all(bind=db.engine)
#     except sqlalchemy.exc.OperationalError as err:
#         print("Error while intializing the POSTS table!")
#         print("MSG ==>", err)


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

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
    )



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
        print(F"MEG ==> {get_user_by_email}")
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
