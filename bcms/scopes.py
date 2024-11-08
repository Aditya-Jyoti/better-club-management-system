from functools import lru_cache

from prisma.enums import Roles


# Overall scopes for the application
@lru_cache
def get_scopes() -> dict[str, str]:
    return {
        "user:read": "Read user information",
        "user:write": "Write/Update user information",
        "user:delete": "Delete user information",
        "roles:user:write": "Write/Update a users roles",
        "scopes:user:write": "Write/Update a users scopes",
        "department:user:write": "Write/Update a users department",
    }


# default scopes
@lru_cache
def get_default_scopes(role: Roles) -> list[str]:
    default_scopes = {
        Roles.MEMBER: ["user:read"],
        Roles.JUNIOR_DEPARTMENT_LEAD: ["user:write"],
        Roles.DEPARTMENT_LEAD: ["scopes:user:write"],
        Roles.UPPER_MANAGEMENT: [
            "user:delete",
            "roles:user:write",
            "department:user:write",
        ],
    }

    role_hierarchy = {
        Roles.MEMBER: [Roles.MEMBER],
        Roles.JUNIOR_DEPARTMENT_LEAD: [Roles.MEMBER, Roles.JUNIOR_DEPARTMENT_LEAD],
        Roles.DEPARTMENT_LEAD: [
            Roles.MEMBER,
            Roles.JUNIOR_DEPARTMENT_LEAD,
            Roles.DEPARTMENT_LEAD,
        ],
        Roles.UPPER_MANAGEMENT: [
            Roles.MEMBER,
            Roles.JUNIOR_DEPARTMENT_LEAD,
            Roles.DEPARTMENT_LEAD,
            Roles.UPPER_MANAGEMENT,
        ],
    }

    return [
        scope for role in role_hierarchy[role] for scope in default_scopes.get(role, [])
    ]
