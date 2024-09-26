from pydantic import BaseModel, EmailStr
from typing import Optional


# Schema for Provider
class ProviderBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    language: str
    currency: str


class ProviderCreate(ProviderBase):
    pass


class ProviderUpdate(ProviderBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    language: Optional[str] = None
    currency: Optional[str] = None


class Provider(ProviderBase):
    id: int

    class Config:
        orm_mode = True
