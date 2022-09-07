# pylint: disable=E0401, E0611, W0703, R0903, E0213

"""
Schema and validators for "Post" data
"""

# Imports
from datetime import datetime
from pydantic import BaseModel

from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.Database import db
from app.Models.users_model import UserResponse


# ---------------------------------------------------------------------------- #
#                                 Model Schemas                                #
# ---------------------------------------------------------------------------- #

# ------------------------------ Database Schema ----------------------------- #
class Post(db.base):
    """Schema for Posts table"""

    __tablename__ = "posts"

    # Columns
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("NULL"))
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    owner = relationship("User")


# ---------------------------------------------------------------------------- #
#                          Pydantic request validators                         #
# ---------------------------------------------------------------------------- #
class PostBase(BaseModel):
    """Data validation for POSTS"""

    title: str
    content: str
    published: bool = False


class PostCreate(PostBase):
    """CREATE Post request data validator"""


class PostUpdate(PostBase):
    """UPDATE Post request data validator"""


class PostResponse(PostBase):
    """RESPONSE data validator"""

    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime | None
    owner: UserResponse

    class Config:
        """Configuration for the pydantic schema"""

        orm_mode = True  # This takes a SQLAlchemy response instead of dict[default]
