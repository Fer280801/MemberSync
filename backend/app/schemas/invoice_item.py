from pydantic import BaseModel, ConfigDict


class InvoiceItemBase(BaseModel):
    description: str
    quantity: int = 1
    unit_price: float


class InvoiceItemCreate(InvoiceItemBase):
    pass


class InvoiceItemRead(InvoiceItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    total: float
