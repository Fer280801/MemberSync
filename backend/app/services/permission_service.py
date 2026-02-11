from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate


async def list_permissions(db: AsyncSession) -> list[Permission]:
    result = await db.execute(select(Permission))
    return list(result.scalars().all())


async def get_permission(db: AsyncSession, permission_id: int) -> Permission | None:
    result = await db.execute(select(Permission).where(Permission.id == permission_id))
    return result.scalar_one_or_none()


async def create_permission(db: AsyncSession, payload: PermissionCreate) -> Permission:
    permission = Permission(code=payload.code, description=payload.description)
    db.add(permission)
    await db.commit()
    await db.refresh(permission)
    return permission
