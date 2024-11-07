from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from prisma import Prisma
from datetime import timedelta
from uuid import uuid4, UUID

from bcms.settings import get_settings
from bcms.models.auth import Auth
from bcms.models.token import Token
from bcms.models.user import User
from bcms.models.requests.register import Register
from bcms.utils.password import verify_password, get_password_hash
from bcms.utils.token import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])
db = Prisma()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    await db.connect()  # TODO: get rid of explicit connect/disconnect

    auth = await db.auth.find_unique(
        where={"email": form_data.username},
        include={"user": True},
    )

    if not auth or not verify_password(form_data.password, auth.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(
        minutes=get_settings()["auth"]["access_token_expires"]
    )

    access_token = create_access_token(
        data={"user_id": str(auth.id), "email": auth.email, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=User)
async def register(data: Register):
    await db.connect()  # TODO: get rid of explicit connect/disconnect

    if await db.auth.find_unique(where={"email": data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = str(uuid4())

    auth = Auth(
        id=user_id,
        email=data.email,
        hashed_password=get_password_hash(data.password),
    )

    async with db.tx() as transaction:
        await transaction.auth.create(
            data={
                "id": auth.id,
                "email": auth.email,
                "hashed_password": auth.hashed_password,
                "user": {
                    "create": {
                        "id": auth.id,
                        "first_name": data.first_name,
                        "last_name": data.last_name,
                        "phone": data.phone,
                        "role": data.role,
                        "department": data.department,
                    }
                },
            }
        )

    user = await db.user.find_unique(where={"id": user_id}, include={"auth": True})

    return User.model_validate(user)
