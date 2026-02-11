from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.account import Account
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import TransactionCreate


async def list_transactions(db: AsyncSession, account_id: int | None = None) -> list[Transaction]:
    stmt = select(Transaction)
    if account_id is not None:
        stmt = stmt.where(Transaction.account_id == account_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_transaction(db: AsyncSession, payload: TransactionCreate) -> Transaction:
    account_result = await db.execute(select(Account).where(Account.id == payload.account_id))
    account = account_result.scalar_one_or_none()
    if account is None:
        raise ValueError("Account not found")

    if payload.type == TransactionType.consumption:
        account.balance = float(account.balance) - payload.amount
    else:
        account.balance = float(account.balance) + payload.amount

    transaction = Transaction(
        account_id=payload.account_id,
        amount=payload.amount,
        type=payload.type,
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction
