"""
Test votes operations
"""

# Imports
from pprint import pprint
from fastapi import status
import pytest

from app.schemas import posts_schema, votes_schema

# ---------------------------------------------------------------------------- #
#                                   Fixtures                                   #
# ---------------------------------------------------------------------------- #


@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = votes_schema.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()


# ---------------------------------------------------------------------------- #
#                                     Tests                                    #
# ---------------------------------------------------------------------------- #


def test_vote_on_own_post(authorized_client, test_posts):
    """Test voting on your own post"""
    response = authorized_client.post(
        "/api/vote/", json={"post_id": test_posts[0].id, "dir": 1}
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_vote_on_elses_post(authorized_client, test_posts):
    """Test voting on someone else's post"""
    response = authorized_client.post(
        "/api/vote/", json={"post_id": test_posts[3].id, "dir": 1}
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_vote_twice(authorized_client, test_posts, test_vote):
    """Test voting twice on a post"""
    response = authorized_client.post(
        "/api/vote/", json={"post_id": test_posts[3].id, "dir": 1}
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_down_vote(authorized_client, test_posts, test_vote):
    """Test down voting a post"""
    response = authorized_client.post(
        "/api/vote/", json={"post_id": test_posts[3].id, "dir": 0}
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_down_vote_on_non_voted_post(authorized_client, test_posts):
    """Test down voting a non voted post"""
    response = authorized_client.post(
        "/api/vote/", json={"post_id": test_posts[3].id, "dir": 0}
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_vote_on_non_voted_post(authorized_client):
    """Test voting a non exisitng post"""
    response = authorized_client.post("/api/vote/", json={"post_id": 12321, "dir": 1})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_vote_unauthorized_user(client, test_posts):
    """Test voting a non exisitng post"""
    response = client.post("/api/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
