from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.permission import PermissionCreate, PermissionRead
from app.services.permission_service import create_permission, list_permissions
from app.utils.permissions import require_permissions

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.get("/", response_model=list[PermissionRead], dependencies=[Depends(require_permissions(["permission:read"]))])
async def get_permissions(db: AsyncSession = Depends(get_db)):
    return await list_permissions(db)


@router.post("/", response_model=PermissionRead, dependencies=[Depends(require_permissions(["permission:write"]))])
async def create_new_permission(payload: PermissionCreate, db: AsyncSession = Depends(get_db)):
    return await create_permission(db, payload)
