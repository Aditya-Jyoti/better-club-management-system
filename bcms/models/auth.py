from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID, uuid4


class Auth(BaseModel):
    id: str = Field(default_factory=uuid4)
    email: EmailStr

    created_at: datetime = Field(default_factory=datetime.now)
    last_login: datetime | None = None
    hashed_password: str
    scopes: list[str]

    class Config:
        from_attributes = True
