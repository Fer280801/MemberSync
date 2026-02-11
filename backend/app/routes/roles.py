from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.role import RoleCreate, RoleRead, RoleUpdate
from app.services.role_service import (
    assign_role_to_user,
    create_role,
    delete_role,
    get_role,
    list_roles,
    remove_role_from_user,
    set_role_permissions,
    update_role,
)
from app.utils.permissions import require_permissions

router = APIRouter(prefix="/roles", tags=["roles"])


class RolePermissionsUpdate(BaseModel):
    permission_ids: list[int]


@router.get("/", response_model=list[RoleRead], dependencies=[Depends(require_permissions(["role:read"]))])
async def get_roles(db: AsyncSession = Depends(get_db)):
    return await list_roles(db)


@router.post("/", response_model=RoleRead, dependencies=[Depends(require_permissions(["role:write"]))])
async def create_new_role(payload: RoleCreate, db: AsyncSession = Depends(get_db)):
    return await create_role(db, payload)


@router.put("/{role_id}", response_model=RoleRead, dependencies=[Depends(require_permissions(["role:write"]))])
async def update_role_detail(role_id: int, payload: RoleUpdate, db: AsyncSession = Depends(get_db)):
    role = await get_role(db, role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return await update_role(db, role, payload)


@router.delete("/{role_id}", dependencies=[Depends(require_permissions(["role:write"]))])
async def delete_role_detail(role_id: int, db: AsyncSession = Depends(get_db)):
    role = await get_role(db, role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    await delete_role(db, role)
    return {"detail": "Role deleted"}


@router.put("/{role_id}/permissions", dependencies=[Depends(require_permissions(["role:write"]))])
async def update_role_permissions(role_id: int, payload: RolePermissionsUpdate, db: AsyncSession = Depends(get_db)):
    role = await get_role(db, role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    await set_role_permissions(db, role_id, payload.permission_ids)
    return {"detail": "Permissions updated"}


@router.post("/{role_id}/users/{user_id}", dependencies=[Depends(require_permissions(["role:write"]))])
async def add_user_role(role_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    await assign_role_to_user(db, user_id, role_id)
    return {"detail": "Role assigned"}


@router.delete("/{role_id}/users/{user_id}", dependencies=[Depends(require_permissions(["role:write"]))])
async def remove_user_role(role_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    await remove_role_from_user(db, user_id, role_id)
    return {"detail": "Role removed"}
