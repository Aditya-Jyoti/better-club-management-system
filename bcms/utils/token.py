import jwt
import os

from datetime import datetime, timedelta, timezone

from bcms.settings import get_settings

AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, AUTH_SECRET_KEY, algorithm=get_settings()["auth"]["algorithm"]
    )

    return encoded_jwt