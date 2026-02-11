from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MembershipBase(BaseModel):
    user_id: int
    status: str = "active"
    ended_at: datetime | None = None


class MembershipCreate(MembershipBase):
    pass


class MembershipUpdate(BaseModel):
    status: str | None = None
    ended_at: datetime | None = None


class MembershipRead(MembershipBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    started_at: datetime
