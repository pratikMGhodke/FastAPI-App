# pylint: disable=E0401, W0707

"""
Routes for VOTES related operations
"""

# Imports
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter

from app.Utils import oauth2
from app.Models import votes_model
from app.Database.db import connect_to_postgres_db

# FastAPI Router
router = APIRouter(prefix="/api/vote", tags=["Votes"])

# ---------------------------------------------------------------------------- #
#                                    Routes                                    #
# ---------------------------------------------------------------------------- #


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_vote(
    vote: votes_model.VoteRequest,
    database: Session = Depends(connect_to_postgres_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Update a vote for post

    Args:
        vote (votes_model.VoteRequest): Vote info
        database (Session, optional):
            Postgres db session object. Defaults to Depends(connect_to_postgres_db).
        current_user (int): Logged in user ID
    """
    try:
        return votes_model.update_vote(vote, database, current_user)

    except HTTPException as error:
        raise error

    except Exception as error:
        print("Error:", error)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )
