from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user_service import create_user, delete_user, get_user, list_users, update_user
from app.utils.permissions import require_permissions

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead], dependencies=[Depends(require_permissions(["user:read"]))])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await list_users(db)


@router.post("/", response_model=UserRead, dependencies=[Depends(require_permissions(["user:write"]))])
async def create_new_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, payload)


@router.get("/{user_id}", response_model=UserRead, dependencies=[Depends(require_permissions(["user:read"]))])
async def get_user_detail(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead, dependencies=[Depends(require_permissions(["user:write"]))])
async def update_user_detail(user_id: int, payload: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await update_user(db, user, payload)


@router.delete("/{user_id}", dependencies=[Depends(require_permissions(["user:write"]))])
async def delete_user_detail(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await delete_user(db, user)
    return {"detail": "User deleted"}
