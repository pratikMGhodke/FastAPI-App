# pylint: disable=E0401, E0611, W0703, R0903

"""
Schema for incoming post requests data
"""

from datetime import datetime
from typing import Dict, List
from pydantic import BaseModel
from fastapi import HTTPException, status

from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import Session, relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.Database import db
from app.Models.users_model import UserResponse, User

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
        database.query(Post)
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
    post = database.query(Post).filter(Post.id == post_id).first()

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
