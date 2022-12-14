# pylint: disable=E0401, W0707

"""
Routes for POSTS related operations
"""

# Imports
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Response, status, APIRouter

from app.Utils import oauth2
from app.Models import posts_model
from app.schemas import posts_schema
from app.Database.db import connect_to_postgres_db

# FastAPI Router
router = APIRouter(prefix="/api/posts", tags=["Posts"])

# ---------------------------------------------------------------------------- #
#                                    Routes                                    #
# ---------------------------------------------------------------------------- #


@router.get("/", response_model=list[posts_schema.PostResponse])
def get_posts(
    database: Session = Depends(connect_to_postgres_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    """
    Return all posts.

    Args:
        database (Session, optional):
            Postgres db session object. Defaults to Depends(connect_to_postgres_db).
        current_user (int): Logged in user ID
        limit (int): Number of posts to be shown
        skip (int): Number of posts to be skipped
        search (str, Optional): Search string
    Returns:
        list[dict]: all/limited posts
    """
    try:
        posts = posts_model.get_all_posts(database, limit, skip, search)
        print("[API /posts] Fetched all posts")
        return posts

    except Exception as error:
        print("Error:", error)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )


@router.get("/{post_id}", response_model=posts_schema.PostResponse)
def get_post(
    post_id: int,
    database: Session = Depends(connect_to_postgres_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Return a post content

    Args:
        post_id (int): Post id

        database (Session, optional):
            Postgres db session object. Defaults to Depends(connect_to_postgres_db).
        current_user (int): Logged in user ID

    Raises:
        HTTPException: HTTP_404_NOT_FOUND
        HTTPException: HTTP_500_INTERNAL_SERVER_ERROR

    Returns:
        dict: Post contents
    """
    try:
        post = posts_model.get_single_post(post_id, database)
        return post

    except HTTPException as error:
        raise error

    except Exception as error:
        print("Error:", error)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=posts_schema.PostData,
)
def create_post(
    new_post: posts_schema.PostCreate,
    database: Session = Depends(connect_to_postgres_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Create a new post

    Args:
        new_post (posts_schema.PostCreate): New post data contents

        database (Session, optional):
            Postgres db session object. Defaults to Depends(connect_to_postgres_db).
        current_user (int): Logged in user ID

    Raises:
        HTTPException: HTTP_500_INTERNAL_SERVER_ERROR

    Returns:
        dict: Newly created post content
    """
    try:
        inserted_post = posts_model.create_post(new_post, database, current_user)
        return inserted_post

    except HTTPException as error:
        raise error

    except Exception as error:
        print("Error:", error)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    database: Session = Depends(connect_to_postgres_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Delete a post

    Args:
        post_id (int): Post ID

        database (Session, optional):
            Postgres db session object. Defaults to Depends(connect_to_postgres_db).
        current_user (int): Logged in user ID

    Raises:
        HTTPException: HTTP_404_NOT_FOUND
        HTTPException: HTTP_500_INTERNAL_SERVER_ERROR
    """
    try:
        posts_model.delete_post(post_id, database, current_user)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException as error:
        raise error

    except Exception as error:
        print("Error in post routes:", error)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )


@router.put("/{post_id}", response_model=posts_schema.PostData)
def update_post(
    post_id: int,
    updated_post: posts_schema.PostUpdate,
    database: Session = Depends(connect_to_postgres_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Update a post.

    Args:
        post_id (int): Id of the post
        updated_post (posts_schema.PostUpdate): Post update data field(s) + original fields

        database (Session, optional):
            Postgres db session object. Defaults to Depends(connect_to_postgres_db).
        current_user (int): Logged in user ID
    Raises:
        HTTPException: HTTP_404_NOT_FOUND

    Returns:
        dict: Response for updated post
    """
    try:
        updated_post = posts_model.update_post(
            post_id, updated_post, database, current_user
        )
        return updated_post

    except HTTPException as error:
        raise error

    except Exception as error:
        print("Error:", error)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )
