from pydantic import BaseModel, EmailStr
from uuid import UUID

from prisma.enums import Roles, Departments

from bcms.models.auth import Auth


class User(BaseModel):
    id: UUID
    email: EmailStr
    auth: Auth | None

    first_name: str
    last_name: str
    phone: str

    role: Roles
    department: Departments

    class Config:
        from_attributes = True
