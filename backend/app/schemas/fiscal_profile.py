from pydantic import BaseModel, ConfigDict


class FiscalProfileBase(BaseModel):
    user_id: int
    tax_id: str | None = None
    legal_name: str | None = None
    address: str | None = None


class FiscalProfileCreate(FiscalProfileBase):
    pass


class FiscalProfileUpdate(BaseModel):
    tax_id: str | None = None
    legal_name: str | None = None
    address: str | None = None


class FiscalProfileRead(FiscalProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
