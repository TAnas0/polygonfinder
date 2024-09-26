from pydantic import BaseModel, EmailStr


# Schema for Provider
class ProviderBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    language: str
    currency: str
