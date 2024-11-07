from pydantic import BaseModel
from prisma.enums import Roles, Departments


class Register(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: str
    password: str
    role: Roles
    department: Departments
