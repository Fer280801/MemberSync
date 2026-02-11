from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.invoice import Invoice
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate


async def create_payment(db: AsyncSession, payload: PaymentCreate) -> Payment:
    result = await db.execute(select(Invoice).where(Invoice.id == payload.invoice_id))
    invoice = result.scalar_one_or_none()
    if invoice is None:
        raise ValueError("Invoice not found")

    payment = Payment(
        invoice_id=payload.invoice_id,
        amount=payload.amount,
        method=payload.method,
    )
    db.add(payment)

    if float(payload.amount) >= float(invoice.total):
        invoice.status = "paid"

    await db.commit()
    await db.refresh(payment)
    return payment
