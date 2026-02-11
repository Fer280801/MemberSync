from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.user_role import UserRole
from app.schemas.role import RoleCreate, RoleUpdate


async def get_role(db: AsyncSession, role_id: int) -> Role | None:
    result = await db.execute(select(Role).where(Role.id == role_id))
    return result.scalar_one_or_none()


async def list_roles(db: AsyncSession) -> list[Role]:
    result = await db.execute(select(Role))
    return list(result.scalars().all())


async def create_role(db: AsyncSession, payload: RoleCreate) -> Role:
    role = Role(name=payload.name, description=payload.description)
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role


async def update_role(db: AsyncSession, role: Role, payload: RoleUpdate) -> Role:
    if payload.name is not None:
        role.name = payload.name
    if payload.description is not None:
        role.description = payload.description
    await db.commit()
    await db.refresh(role)
    return role


async def delete_role(db: AsyncSession, role: Role) -> None:
    await db.delete(role)
    await db.commit()


async def set_role_permissions(db: AsyncSession, role_id: int, permission_ids: list[int]) -> None:
    await db.execute(delete(RolePermission).where(RolePermission.role_id == role_id))
    db.add_all([RolePermission(role_id=role_id, permission_id=perm_id) for perm_id in permission_ids])
    await db.commit()


async def assign_role_to_user(db: AsyncSession, user_id: int, role_id: int) -> None:
    db.add(UserRole(user_id=user_id, role_id=role_id))
    await db.commit()


async def remove_role_from_user(db: AsyncSession, user_id: int, role_id: int) -> None:
    await db.execute(
        delete(UserRole).where(UserRole.user_id == user_id, UserRole.role_id == role_id)
    )
    await db.commit()
