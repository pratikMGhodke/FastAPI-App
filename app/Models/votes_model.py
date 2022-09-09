# pylint: disable=E0401, E0611, W0703, R0903, E0213

"""
Schema for incoming post requests data
"""

# Imports
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.users_schema import User
from app.schemas.votes_schema import Vote, VoteRequest
from app.Models.posts_model import check_if_post_exists

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

    # Check if post exists
    post = check_if_post_exists(database, post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exists!"
        )

    vote_query = database.query(Vote).filter(
        Vote.post_id == post_id, Vote.user_id == user_id
    )

    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot vote already voted post!",
            )

        new_vote = Vote(post_id=post_id, user_id=user_id)
        database.add(new_vote)
        database.commit()
        return {"message": "Added Vote!"}

    if not found_vote:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot down-vote a not voted this post!",
        )

    vote_query.delete(synchronize_session=False)
    database.commit()
    return {"message": "Removed Vote!"}
