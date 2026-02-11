from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AccountBase(BaseModel):
    user_id: int


class AccountCreate(AccountBase):
    initial_balance: float = 0


class AccountRead(AccountBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    balance: float
    created_at: datetime
