# pylint: disable=E0401, E0611, W0703


"""
Database functions
"""

# imports
import fastapi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.settings import settings

# App Settings
settings = settings.Settings()

# Constants
USER = settings.POSTGRES_USER
PASS = settings.POSTGRES_PASSWORD
HOST = settings.POSTGRES_HOST
DATABASE = settings.DATABASE

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASS}@{HOST}/{DATABASE}"

# Set up database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()


def connect_to_postgres_db():
    """
    Create postgres session

    Yields:
        sqlalchemy.orm.session.Session: Postgres Session Object
    """
    database = session_local()
    try:
        yield database

    except fastapi.exceptions.HTTPException as error:
        print("Something went wrong while performing DB operation")
        print("MSG ==>", error)

    except Exception as error:
        print("Error occured ==>", error)

    finally:
        database.close()
