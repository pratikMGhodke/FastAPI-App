# pylint: disable=E0401, E0611, W0703, R0903, E0213

"""
Schema for incoming post requests data
"""

# Imports
from fastapi import HTTPException, status
from pydantic import BaseModel, validator

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column, ForeignKey, Integer

from app.Database import db
from app.Models.users_model import User

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


# ---------------------------------------------------------------------------- #
#                                 DB Operations                                #
# ---------------------------------------------------------------------------- #


def update_vote(vote: VoteRequest, database: Session, current_user: User):
    """
    Update a vote for post

    Args:
        vote (VoteRequest): New post data
        database (Session): Database session
        current_user (User): Current User object with info like ID

    Returns:
        dict: User details
    """
    post_id = vote.post_id
    user_id = current_user.id

    vote_query = database.query(Vote).filter(
        Vote.post_id == post_id, Vote.user_id == user_id
    )

    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Cannot vote already voted post!"
            )

        new_vote = Vote(post_id=post_id, user_id=user_id)
        database.add(new_vote)
        database.commit()
        return {"message": "Added Vote!"}

    if not found_vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cannot Down Vote a not voted this post!"
        )

    vote_query.delete(synchronize_session=False)
    database.commit()
    return {"message": "Removed Vote!"}
