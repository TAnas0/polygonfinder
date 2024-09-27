from pydantic import BaseModel, EmailStr, condecimal
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


# Schema for ServiceArea
class ServiceAreaBase(BaseModel):
    name: str
    price: condecimal(gt=0)  # Ensure price is greater than 0
    geojson: str  # You can replace this with a more complex type if needed


class ServiceAreaCreate(ServiceAreaBase):
    pass


class ServiceAreaUpdate(ServiceAreaBase):
    name: Optional[str] = None
    price: Optional[condecimal(gt=0)] = None
    geojson: Optional[str] = None


class ServiceArea(ServiceAreaBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
