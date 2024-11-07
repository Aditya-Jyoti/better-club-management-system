import os
import jwt

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from prisma import Prisma
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from uuid import UUID
from jwt import InvalidTokenError
from datetime import datetime, timezone
from pydantic import ValidationError

from bcms.settings import get_settings, get_scopes
from bcms.models.user import User
from bcms.models.token import TokenData

from bcms.routes.auth import router as auth_router

from prisma.enums import Roles, Departments

load_dotenv()

# Set the environment variables
AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Scopes

db = Prisma()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", scopes=get_scopes())


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    try:
        yield
    finally:
        await db.disconnect()


app = FastAPI(lifespan=lifespan, title=get_settings()["club_details"]["name"])


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
) -> User:

    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(
            token, AUTH_SECRET_KEY, algorithms=get_settings()["auth"]["algorithm"]
        )

        user_id: str = payload.get("user_id")
        email: str = payload.get("email")

        if user_id is None or email is None:
            raise credentials_exception

        token_scopes = payload.get("scopes", [])

        token_data = TokenData(id=UUID(user_id), email=email, scopes=token_scopes)

    except (InvalidTokenError, ValidationError):
        raise credentials_exception

    else:
        user = await db.user.find_unique(
            where={"id": str(token_data.id)}, include={"auth": True}
        )

        if user is None or user.auth is None:
            raise credentials_exception

        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )

        await db.auth.update(
            where={"id": user.auth.id},
            data={"last_login": datetime.now(timezone.utc)},
        )

    return User.model_validate(user)


@app.get("/")
async def root():
    return {"message": "I am alive"}


app.include_router(auth_router)
