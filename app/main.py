# pylint: disable=E0401

"""
FastAPI API application
"""

# imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.Routes import post_routes, user_routes, auth_routes, vote_routes

# Init API
app = FastAPI()

# CORS Policy
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routes
app.include_router(post_routes.router)
app.include_router(user_routes.router)
app.include_router(auth_routes.router)
app.include_router(vote_routes.router)

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
    return "Health OK"
