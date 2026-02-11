from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.account import AccountCreate, AccountRead
from app.services.account_service import create_account, get_account, list_accounts
from app.utils.permissions import require_permissions

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/", response_model=list[AccountRead], dependencies=[Depends(require_permissions(["account:read"]))])
async def get_accounts(db: AsyncSession = Depends(get_db)):
    return await list_accounts(db)


@router.post("/", response_model=AccountRead, dependencies=[Depends(require_permissions(["account:write"]))])
async def create_new_account(payload: AccountCreate, db: AsyncSession = Depends(get_db)):
    return await create_account(db, payload)


@router.get("/{account_id}", response_model=AccountRead, dependencies=[Depends(require_permissions(["account:read"]))])
async def get_account_detail(account_id: int, db: AsyncSession = Depends(get_db)):
    account = await get_account(db, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
