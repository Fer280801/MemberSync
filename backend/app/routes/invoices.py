from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.invoice import InvoiceCreate, InvoiceRead
from app.services.invoice_service import cancel_invoice, create_invoice, get_invoice, list_invoices
from app.utils.permissions import require_permissions

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("/", response_model=list[InvoiceRead], dependencies=[Depends(require_permissions(["invoice:read"]))])
async def get_invoices(db: AsyncSession = Depends(get_db)):
    return await list_invoices(db)


@router.post("/", response_model=InvoiceRead, dependencies=[Depends(require_permissions(["invoice:write"]))])
async def create_new_invoice(payload: InvoiceCreate, db: AsyncSession = Depends(get_db)):
    return await create_invoice(db, payload)


@router.post("/{invoice_id}/cancel", response_model=InvoiceRead, dependencies=[Depends(require_permissions(["invoice:write"]))])
async def cancel_invoice_detail(invoice_id: int, db: AsyncSession = Depends(get_db)):
    invoice = await get_invoice(db, invoice_id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return await cancel_invoice(db, invoice)
