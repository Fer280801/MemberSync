from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.invoice import Invoice
from app.models.payment import Payment


async def monthly_summary(db: AsyncSession, year: int, month: int) -> dict:
    invoices_stmt = select(func.coalesce(func.sum(Invoice.total), 0)).where(
        func.extract("year", Invoice.issued_at) == year,
        func.extract("month", Invoice.issued_at) == month,
    )
    payments_stmt = select(func.coalesce(func.sum(Payment.amount), 0)).where(
        func.extract("year", Payment.paid_at) == year,
        func.extract("month", Payment.paid_at) == month,
    )

    invoices_total = (await db.execute(invoices_stmt)).scalar_one()
    payments_total = (await db.execute(payments_stmt)).scalar_one()
    return {
        "year": year,
        "month": month,
        "invoices_total": float(invoices_total),
        "payments_total": float(payments_total),
    }


async def pending_invoices(db: AsyncSession) -> list[Invoice]:
    result = await db.execute(select(Invoice).where(Invoice.status == "issued"))
    return list(result.scalars().all())
