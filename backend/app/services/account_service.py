from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.account import Account
from app.schemas.account import AccountCreate


async def get_account(db: AsyncSession, account_id: int) -> Account | None:
    result = await db.execute(select(Account).where(Account.id == account_id))
    return result.scalar_one_or_none()


async def list_accounts(db: AsyncSession) -> list[Account]:
    result = await db.execute(select(Account))
    return list(result.scalars().all())


async def create_account(db: AsyncSession, payload: AccountCreate) -> Account:
    account = Account(user_id=payload.user_id, balance=payload.initial_balance)
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account
