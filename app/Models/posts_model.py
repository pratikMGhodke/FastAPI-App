# pylint: disable=E0401, E0611, W0703, R0903

"""
Database operations for Posts
"""

from typing import Dict, List
from fastapi import HTTPException, status

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.Models.users_model import User
from app.schemas.posts_schema import Post
from app.schemas.votes_schema import Vote

# from app.Models.votes_model import Vote

# ---------------------------------------------------------------------------- #
#                                Helper Functions                              #
# ---------------------------------------------------------------------------- #
def check_if_post_exists(database: Session, post_id: int):
    """Check if post with given post_id exists"""
    return database.query(Post).filter(Post.id == post_id).first()


# ---------------------------------------------------------------------------- #
#                                 DB Operations                                #
# ---------------------------------------------------------------------------- #


def get_all_posts(database: Session, limit: int, skip: int, search: str) -> List[Dict]:
    """
    Fetch list of all posts

    Args:
        database (Session): Database session
        limit (int): Number of posts to return
        skip (int): Number of posts to skip
        search (str): Search query string

    Returns:
        list: Return list of posts
    """
    return (
        database.query(Post, func.count(Vote.post_id).label("votes"))
        .join(Vote, Post.id == Vote.post_id, isouter=True)
        .group_by(Post.id)
        .filter(Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )


def get_single_post(post_id: int, database: Session) -> Dict:
    """
    Get a single post with given post_id

    Args:
        post_id (int): Id of the required post
        database (Session): Database session

    Returns:
        dict: Fetched post
    """
    post = (
        database.query(Post, func.count(Vote.post_id).label("votes"))
        .join(Vote, Post.id == Vote.post_id, isouter=True)
        .group_by(Post.id)
        .filter(Post.id == post_id)
        .first()
    )

    if post:
        return post

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")


def create_post(post: Post, database: Session, current_user: User) -> Dict:
    """
    Create a new post

    Args:
        post (Post): New post data
        database (Session): Database session
        current_user (User): Current User object with info like ID

    Returns:
        dict: Update post data
    """
    inserted_post = Post(owner_id=current_user.id, **post.dict())

    database.add(inserted_post)
    database.commit()
    database.refresh(inserted_post)

    print("Post is created!")
    return inserted_post


def update_post(
    post_id: int, post: Post, database: Session, current_user: User
) -> Dict:
    """
    Update a post

    Args:
        post_id (int): Id of the post
        post (Post): Updated post data
        database (Session): Database session
        current_user (User): Current User object with info like ID

    Returns:
        dict: Updated post
    """
    post_query = database.query(Post).filter(Post.id == post_id)
    existing_post = post_query.first()

    if existing_post:
        if existing_post.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform requested operation",
            )
        post_query.update(
            {**post.dict(), **{"updated_at": "now()"}}, synchronize_session=False
        )

    database.commit()
    updated_post = post_query.first()

    if updated_post:
        return post_query.first()

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")


def delete_post(post_id: int, database: Session, current_user: User) -> bool:
    """
    Delete a post

    Args:
        post_id (int): Id of the post

    Returns:
        bool: Post is deleted?
    """
    post_query = database.query(Post).filter(Post.id == post_id)
    existing_post = post_query.first()

    if existing_post:
        if existing_post.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform requested operation",
            )

        post_query.delete(synchronize_session=False)
        database.commit()
        return True

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
