from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission


ROLE_PERMISSIONS = {
    "ADMIN": [
        "user:read",
        "user:write",
        "role:read",
        "role:write",
        "permission:read",
        "permission:write",
        "membership:read",
        "membership:write",
        "account:read",
        "account:write",
        "transaction:read",
        "transaction:write",
        "invoice:read",
        "invoice:write",
        "payment:write",
        "report:read",
    ],
    "OPERATIVO": [
        "user:read",
        "membership:read",
        "membership:write",
        "account:read",
        "transaction:read",
        "transaction:write",
        "invoice:read",
        "invoice:write",
        "payment:write",
        "report:read",
    ],
    "SOCIO": [
        "user:read",
        "account:read",
        "transaction:read",
        "invoice:read",
        "payment:write",
    ],
}


async def seed_roles_permissions(db: AsyncSession) -> None:
    permission_codes = {code for codes in ROLE_PERMISSIONS.values() for code in codes}

    existing_permissions = await db.execute(select(Permission))
    existing_by_code = {perm.code: perm for perm in existing_permissions.scalars().all()}

    for code in permission_codes:
        if code not in existing_by_code:
            perm = Permission(code=code)
            db.add(perm)
    await db.commit()

    existing_permissions = await db.execute(select(Permission))
    permissions_by_code = {perm.code: perm for perm in existing_permissions.scalars().all()}

    existing_roles = await db.execute(select(Role))
    roles_by_name = {role.name: role for role in existing_roles.scalars().all()}

    for role_name in ROLE_PERMISSIONS:
        if role_name not in roles_by_name:
            db.add(Role(name=role_name))
    await db.commit()

    existing_roles = await db.execute(select(Role))
    roles_by_name = {role.name: role for role in existing_roles.scalars().all()}

    for role_name, codes in ROLE_PERMISSIONS.items():
        role = roles_by_name[role_name]
        for code in codes:
            permission = permissions_by_code[code]
            exists = await db.execute(
                select(RolePermission)
                .where(RolePermission.role_id == role.id)
                .where(RolePermission.permission_id == permission.id)
            )
            if exists.scalar_one_or_none() is None:
                db.add(RolePermission(role_id=role.id, permission_id=permission.id))

    await db.commit()
