from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.transaction import TransactionType


class TransactionBase(BaseModel):
    account_id: int
    amount: float
    type: TransactionType


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
