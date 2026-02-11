from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PaymentBase(BaseModel):
    invoice_id: int
    amount: float
    method: str | None = None


class PaymentCreate(PaymentBase):
    pass


class PaymentRead(PaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paid_at: datetime
