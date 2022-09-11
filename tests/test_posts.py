"""
Test posts operations
"""

# Imports
from pprint import pprint
from fastapi import status
import pytest

from app.schemas import posts_schema

# ---------------------------------------------------------------------------- #
#                                     Tests                                    #
# ---------------------------------------------------------------------------- #


def test_get_all_posts(authorized_client, test_posts):
    """Test and validate getting all posts"""
    response = authorized_client.get("/api/posts/")

    def validate_post(post):
        return posts_schema.PostResponse(**post)

    validated_posts = list(map(validate_post, response.json()))
    # pprint(validated_posts)
    assert len(response.json()) == len(test_posts)
    assert response.status_code == status.HTTP_200_OK


def test_unauthorized_get_all_posts(client):
    """Test all posts with unauthorized user"""
    response = client.get("/api/posts/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorized_get_one_post(client, test_posts):
    """Test one post with unauthorized user"""
    response = client.get(f"/api/posts/{test_posts[0].id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_post_not_exists(authorized_client):
    """Test not existing post"""
    response = authorized_client.get(f"/api/posts/123321")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_post(authorized_client, test_posts):
    """Test getting valid post"""
    response = authorized_client.get(f"/api/posts/{test_posts[0].id}")
    post = posts_schema.PostResponse(**response.json())
    assert response.status_code == status.HTTP_200_OK


# -------------------------------- Create Post ------------------------------- #


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("awesome new title", "awesome new content", True),
        ("favorite pizza", "i love pepperoni", False),
        ("tallest skyscrapers", "wahoo", True),
    ],
)
def test_create_post(authorized_client, test_user, title, content, published):
    """Test creating the post"""
    response = authorized_client.post(
        f"/api/posts/",
        json={"title": title, "content": content, "published": published},
    )
    created_post = posts_schema.Post(**response.json())
    assert response.status_code == status.HTTP_201_CREATED
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_post_default_published(authorized_client, test_user):
    """Test default published value=False"""
    title, content = "tallest skyscrapers", "wahoo"
    response = authorized_client.post(
        f"/api/posts/",
        json={"title": title, "content": content},
    )
    created_post = posts_schema.Post(**response.json())
    assert response.status_code == status.HTTP_201_CREATED
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == False
    assert created_post.owner_id == test_user["id"]


def test_unauthorized_user_create_post(client):
    """Test unauthorized user creating post"""
    title, content, published = "tallest skyscrapers", "wahoo", True
    response = client.post(
        f"/api/posts/",
        json={"title": title, "content": content, "published": published},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# -------------------------------- Delete Post ------------------------------- #


def test_unauthorized_user_delete_post(client, test_posts):
    """Test unauthorized user deleting post"""
    response = client.delete(f"/api/posts/{test_posts[0].id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_post_success(authorized_client, test_posts):
    """Test valid deletion of the post"""
    response = authorized_client.delete(f"/api/posts/{test_posts[0].id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_non_existing_post(authorized_client):
    """Test deletion of the non existing post"""
    response = authorized_client.delete(f"/api/posts/12321")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_other_users_post(authorized_client, test_posts):
    """Test deletion of the post by other user"""
    response = authorized_client.delete(f"/api/posts/{test_posts[3].id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN


# -------------------------------- Update Post ------------------------------- #
def test_update_post(authorized_client, test_posts):
    """Test updating valid post"""
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id,
    }
    response = authorized_client.put(f"/api/posts/{test_posts[0].id}", json=data)
    updated_post = posts_schema.Post(**response.json())
    assert response.status_code == status.HTTP_200_OK
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_posts):
    """Test updating other users post"""
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id,
    }
    response = authorized_client.put(f"/api/posts/{test_posts[3].id}", json=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_unauthorized_user_update_post(client, test_posts):
    """Test unauthorized user updating post"""
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id,
    }
    response = client.put(f"/api/posts/{test_posts[0].id}", json=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_non_existing_post(authorized_client, test_posts):
    """Test updation of the non existing post"""
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id,
    }
    response = authorized_client.put(f"/api/posts/123321", json=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
