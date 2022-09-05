# pylint: disable=E0401, w0611

"""
Methods related to hashing
"""

# Imports
from passlib.context import CryptContext

# Default hashing algorithm to use
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """
    Hash the password

    Args:
        password (str): Plain password string

    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def verify(plain_pass, hashed_pass):
    """
    Verify plain password matches db user password

    Args:
        plain_pass (str): Plain request input password
        hashed_pass (str): Password from the DB

    Returns:
        bool: Does both password hash matches
    """
    return pwd_context.verify(plain_pass, hashed_pass)
