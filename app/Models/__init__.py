# pylint: disable=E0401, E0611, W0703, R0903, C0103

"""
Initialize and create tables in DB (postgres)
"""

# Imports
import sqlalchemy
from app.Database import db

from . import posts_model, users_model, votes_model

def init_models():
    """Initialize tables in the database"""

    try:
        db.base.metadata.create_all(bind=db.engine)
    except sqlalchemy.exc.OperationalError as err:
        print("Error while intializing the POSTS table!")
        print("MSG ==>", err)

init_models()
