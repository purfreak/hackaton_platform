from datetime import datetime, timedelta
from typing import TypedDict

from jose import jwt
from ninja.security import HttpBearer
from passlib.context import CryptContext

from hackathon.settings import APP_EXPIRE_TOKEN, APP_SECRET_KEY, APP_ALGORITHM

crypto_manager = CryptContext(schemes=["bcrypt"], deprecated="auto")

JwtPayload = TypedDict("JwtPayload", {"user_id": int, "exp": datetime})


def get_password_hash(password: str) -> str:
    """Get hash of the provided password.

    Args:
        password (str): password

    Returns:
        str: password hash
    """
    return crypto_manager.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against given hashed password.

    Args:
        plain_password (str): unhashed password
        hashed_password (str): hashed password

    Returns:
        bool: True if passwords are verified, else False
    """
    return crypto_manager.verify(plain_password, hashed_password)


def create_access_token(user_id: int, expires_delta: int = APP_EXPIRE_TOKEN) -> str:
    """Create JWT access token.

    Args:
        user_id (int): user ID
        expires_delta (timedelta, optional): JWT token expiration time in seconds. Defaults to APP_EXPIRE_TOKEN.

    Returns:
        str: JWT access token
    """
    expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    payload: JwtPayload = {"user_id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(claims=payload, key=APP_SECRET_KEY, algorithm=APP_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> JwtPayload:
    """Decode JWT access token and get JWT payload.

    Args:
        token (str): JWT access token

    Returns:
        JwtPayload: JWT payload with user ID and expiration time
    """
    payload = jwt.decode(token=token, key=APP_SECRET_KEY, algorithms=APP_ALGORITHM)
    return payload
