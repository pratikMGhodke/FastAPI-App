# pylint: disable=E0401, E0611, W0703, R0903, E0213

"""
Schema and validators for "Users" & "JWT Token" data
"""

# from datetime import datetime
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column, Integer, String

from app.Database import db

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
