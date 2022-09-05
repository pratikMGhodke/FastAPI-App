"""
File containing constants
"""

# Postgres
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "admin"

DATABASE = "fastapi_app"
POSTS_TABLE = "posts"
USERS_TABLE = "users"

JWT_SECRET_KEY = "super_duper_secret_key"
JWT_ALOGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
