from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.membership import MembershipCreate, MembershipRead, MembershipUpdate
from app.services.membership_service import (
    create_membership,
    delete_membership,
    get_membership,
    list_memberships,
    update_membership,
)
from app.utils.permissions import require_permissions

router = APIRouter(prefix="/memberships", tags=["memberships"])


@router.get("/", response_model=list[MembershipRead], dependencies=[Depends(require_permissions(["membership:read"]))])
async def get_memberships(db: AsyncSession = Depends(get_db)):
    return await list_memberships(db)


@router.post("/", response_model=MembershipRead, dependencies=[Depends(require_permissions(["membership:write"]))])
async def create_new_membership(payload: MembershipCreate, db: AsyncSession = Depends(get_db)):
    return await create_membership(db, payload)


@router.put("/{membership_id}", response_model=MembershipRead, dependencies=[Depends(require_permissions(["membership:write"]))])
async def update_membership_detail(membership_id: int, payload: MembershipUpdate, db: AsyncSession = Depends(get_db)):
    membership = await get_membership(db, membership_id)
    if membership is None:
        raise HTTPException(status_code=404, detail="Membership not found")
    return await update_membership(db, membership, payload)


@router.delete("/{membership_id}", dependencies=[Depends(require_permissions(["membership:write"]))])
async def delete_membership_detail(membership_id: int, db: AsyncSession = Depends(get_db)):
    membership = await get_membership(db, membership_id)
    if membership is None:
        raise HTTPException(status_code=404, detail="Membership not found")
    await delete_membership(db, membership)
    return {"detail": "Membership deleted"}
