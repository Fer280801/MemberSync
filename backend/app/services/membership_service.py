from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.membership import Membership
from app.schemas.membership import MembershipCreate, MembershipUpdate


async def get_membership(db: AsyncSession, membership_id: int) -> Membership | None:
    result = await db.execute(select(Membership).where(Membership.id == membership_id))
    return result.scalar_one_or_none()


async def list_memberships(db: AsyncSession) -> list[Membership]:
    result = await db.execute(select(Membership))
    return list(result.scalars().all())


async def create_membership(db: AsyncSession, payload: MembershipCreate) -> Membership:
    membership = Membership(
        user_id=payload.user_id,
        status=payload.status,
        ended_at=payload.ended_at,
    )
    db.add(membership)
    await db.commit()
    await db.refresh(membership)
    return membership


async def update_membership(db: AsyncSession, membership: Membership, payload: MembershipUpdate) -> Membership:
    if payload.status is not None:
        membership.status = payload.status
    if payload.ended_at is not None:
        membership.ended_at = payload.ended_at
    await db.commit()
    await db.refresh(membership)
    return membership


async def delete_membership(db: AsyncSession, membership: Membership) -> None:
    await db.delete(membership)
    await db.commit()
