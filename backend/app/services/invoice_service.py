from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.schemas.invoice import InvoiceCreate


async def get_invoice(db: AsyncSession, invoice_id: int) -> Invoice | None:
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    return result.scalar_one_or_none()


async def list_invoices(db: AsyncSession) -> list[Invoice]:
    result = await db.execute(select(Invoice))
    return list(result.scalars().all())


async def create_invoice(db: AsyncSession, payload: InvoiceCreate) -> Invoice:
    invoice = Invoice(user_id=payload.user_id)
    db.add(invoice)
    await db.flush()

    total = 0.0
    for item in payload.items:
        line_total = item.quantity * item.unit_price
        total += line_total
        db.add(
            InvoiceItem(
                invoice_id=invoice.id,
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total=line_total,
            )
        )

    invoice.total = total
    await db.commit()
    await db.refresh(invoice)
    return invoice


async def cancel_invoice(db: AsyncSession, invoice: Invoice) -> Invoice:
    invoice.status = "cancelled"
    invoice.cancelled_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(invoice)
    return invoice
