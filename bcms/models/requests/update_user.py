from typing import Optional
from pydantic import BaseModel
from prisma.enums import Roles, Departments


class UpdateUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[Roles] = None
    department: Optional[Departments] = None
    scopes: Optional[list[str]] = None

    class Config:
        from_attributes = True
