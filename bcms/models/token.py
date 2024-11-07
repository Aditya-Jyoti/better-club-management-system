from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[UUID] = None
    email: Optional[str] = None
    scopes: list[str] = []