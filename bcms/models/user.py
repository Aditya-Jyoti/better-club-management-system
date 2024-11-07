from pydantic import BaseModel, EmailStr
from uuid import UUID

from prisma.enums import Roles, Departments

from bcms.models.auth import Auth


class User(BaseModel):
    id: UUID
    auth: Auth | None = None

    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None

    role: Roles | None = None
    department: Departments | None = None

    class Config:
        from_attributes = True
