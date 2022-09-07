# pylint: disable=E0401, E0611, W0703, R0903, E0213

"""
Schema and validators for "Votes" data
"""

# Imports
from pydantic import BaseModel, validator

from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column, ForeignKey, Integer

from app.Database import db

# ---------------------------------------------------------------------------- #
#                                 Model Schemas                                #
# ---------------------------------------------------------------------------- #

# ------------------------------ Database Schema ----------------------------- #
class Vote(db.base):
    """Schema for Posts table"""

    __tablename__ = "votes"

    # Columns
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    liked_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


# ---------------------------------------------------------------------------- #
#                          Pydantic request validators                         #
# ---------------------------------------------------------------------------- #


class VoteRequest(BaseModel):
    """Vote request validator"""

    post_id: int
    dir: int

    @validator("dir")
    def validate_vote_type(cls, val):
        """ Validate vote type """
        if val not in [0, 1]:
            raise ValueError("Vote type should be either 0 or 1!")
        return val
