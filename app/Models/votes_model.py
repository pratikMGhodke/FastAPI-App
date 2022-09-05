# pylint: disable=E0401, E0611, W0703, R0903

"""
Schema for incoming post requests data
"""

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
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    liked_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )