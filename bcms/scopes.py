from functools import lru_cache

from prisma.enums import Roles


# Overall scopes for the application
@lru_cache
def get_scopes() -> dict[str, str]:
    return {
        "user:read": "Read user information",
        "user:write": "Write user information",
        "user:delete": "Delete user information",
    }


# Default scopes for each role
@lru_cache
def get_default_scopes(role: Roles) -> list[str]:
    return {
        Roles.MEMBER: ["user:read", "user:write", "user:delete"],
    }[role]
