from fastapi import APIRouter, Security, HTTPException, Depends

from prisma import Prisma
from prisma.enums import Departments, Roles
from uuid import UUID

from bcms.database import get_db

from bcms.models.user import User
from bcms.models.requests.update_user import UpdateUser

from bcms.utils.user import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", response_model=list[User])
async def get_all(
    db: Prisma = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["user:read"]),
):
    all_users = await db.user.find_many()

    if not all_users:
        raise HTTPException(status_code=404, detail="Users could not found.")

    return all_users


@router.get("/me", response_model=User)
async def get_self(
    current_user: User = Security(get_current_user, scopes=["user:read"])
):
    return current_user


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: UUID,
    db: Prisma = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["user:read"]),
):
    user = await db.user.find_unique(where={"id": str(user_id)})

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user


@router.get("/{department}", response_model=list[User])
async def get_users_by_department(
    department: Departments,
    db: Prisma = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["user:read"]),
):
    all_users = await db.user.find_many(where={"department": department})

    if not all_users:
        raise HTTPException(status_code=404, detail="Users could not found.")

    return all_users


@router.get("/{role}", response_model=list[User])
async def get_users_by_role(
    role: Roles,
    db: Prisma = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["user:read"]),
):
    all_users = await db.user.find_many(where={"role": role})

    if not all_users:
        raise HTTPException(status_code=404, detail="Users could not found.")

    return all_users


@router.put("/update/{user_id}", response_model=User)
async def update_user(
    user_id: UUID,
    user_update: UpdateUser,
    current_user: User = Security(
        get_current_user, scopes=["user:write", "roles:user:write", "scopes:user:write"]
    ),
    db: Prisma = Depends(get_db),
):
    update_data = user_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    # update a users scopes if "scopes:user:write" is in the current users scopes
    if user_update.scopes is not None:
        if not current_user.auth or "scopes:user:write" not in current_user.auth.scopes:
            raise HTTPException(
                status_code=403, detail="You do not have permission to update scopes."
            )

        await db.auth.update(
            where={"id": str(user_id)},
            data={"scopes": user_update.scopes},
        )

    # update a users role if "role:user:write" is in the current users scopes
    if user_update.role is not None:
        if not current_user.auth or "roles:user:write" not in current_user.auth.scopes:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to update the role of a member.",
            )

        await db.user.update(
            where={"id": str(user_id)},
            data={"role": user_update.role},
        )

    # update a users department if "department:user:write" is in the current users scopes
    if user_update.department is not None:
        if (
            not current_user.auth
            or "department:user:write" not in current_user.auth.scopes
        ):
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to update the department of a member.",
            )

        await db.user.update(
            where={"id": str(user_id)},
            data={"department": user_update.department},
        )

    # if only "user:write" is in scope
    user_to_update = await db.user.find_unique(where={"id": str(user_id)})

    if not user_to_update:
        raise HTTPException(status_code=404, detail="User not found.")

    fields_to_exclude = {"scopes", "role", "department"}
    update_data = {
        field: value
        for field, value in update_data.items()
        if field not in fields_to_exclude
    }

    for field, value in update_data.items():
        setattr(user_to_update, field, value)

    try:
        await db.user.update(
            where={"id": str(user_id)},
            data={
                "first_name": user_to_update.first_name,
                "last_name": user_to_update.last_name,
                "email": user_to_update.email,
                "phone": user_to_update.phone,
            },
        )

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update user details")

    return current_user


@router.delete("/delete/{user_id}", response_model=str)
async def delete_user(
    user_id: UUID,
    db: Prisma = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["user:delete"]),
):
    user_to_delete = await db.user.find_unique(where={"id": str(user_id)})

    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found.")

    await db.auth.delete(
        where={"id": str(user_id)},
    )

    return f"User {user_id} deleted successfully."
