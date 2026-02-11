from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.transaction import TransactionCreate, TransactionRead
from app.services.transaction_service import create_transaction, list_transactions
from app.utils.permissions import require_permissions

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/", response_model=list[TransactionRead], dependencies=[Depends(require_permissions(["transaction:read"]))])
async def get_transactions(account_id: int | None = Query(default=None), db: AsyncSession = Depends(get_db)):
    return await list_transactions(db, account_id=account_id)


@router.post("/", response_model=TransactionRead, dependencies=[Depends(require_permissions(["transaction:write"]))])
async def create_new_transaction(payload: TransactionCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_transaction(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
