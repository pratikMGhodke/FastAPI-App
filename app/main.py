# pylint: disable=E0401

"""
FastAPI API application
"""

# imports
from fastapi import FastAPI
from app.Models import posts_model
from app.Routes import post_routes, user_routes, auth_routes

# Init API
app = FastAPI()

# Create a post model/table
posts_model.init_posts_model()

# Register Routes
app.include_router(post_routes.router)
app.include_router(user_routes.router)
app.include_router(auth_routes.router)

# ---------------------------------------------------------------------------- #
#                               Universal Routes                               #
# ---------------------------------------------------------------------------- #

@app.get("/api/health")
async def health():
    """
    Health check for the API.

    Returns:
        str: OK response
    """
    print("[Health-check] Application is running!")
    return "OK"
