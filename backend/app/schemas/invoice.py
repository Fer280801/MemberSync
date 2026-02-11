from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.invoice_item import InvoiceItemCreate, InvoiceItemRead


class InvoiceBase(BaseModel):
    user_id: int


class InvoiceCreate(InvoiceBase):
    items: list[InvoiceItemCreate]


class InvoiceRead(InvoiceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    total: float
    issued_at: datetime
    cancelled_at: datetime | None
    items: list[InvoiceItemRead] = []
