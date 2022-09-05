# pylint: disable=E0401, R0903

"""
Setting and configuration for the App
"""

# Imports
from pydantic import BaseSettings

class Settings(BaseSettings):
    """ Setting validation for the App """

    # DB Creds
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    
    # Database
    DATABASE: str
    POSTS_TABLE: str
    USERS_TABLE: str
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALOGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        """ Configuration for env file """
        env_file = "app/settings/.env"
