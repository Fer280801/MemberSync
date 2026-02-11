from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.report_service import monthly_summary, pending_invoices
from app.utils.permissions import require_permissions

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/monthly-summary", dependencies=[Depends(require_permissions(["report:read"]))])
async def get_monthly_summary(
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    db: AsyncSession = Depends(get_db),
):
    return await monthly_summary(db, year, month)


@router.get("/pending-invoices", dependencies=[Depends(require_permissions(["report:read"]))])
async def get_pending_invoices(db: AsyncSession = Depends(get_db)):
    invoices = await pending_invoices(db)
    return [{"id": invoice.id, "user_id": invoice.user_id, "total": float(invoice.total)} for invoice in invoices]
