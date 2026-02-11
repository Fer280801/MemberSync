from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.payment import PaymentCreate, PaymentRead
from app.services.payment_service import create_payment
from app.utils.permissions import require_permissions

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/", response_model=PaymentRead, dependencies=[Depends(require_permissions(["payment:write"]))])
async def record_payment(payload: PaymentCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_payment(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
