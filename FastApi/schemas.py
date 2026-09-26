from datetime import datetime

from pydantic import BaseModel, EmailStr


# Request Schema: For user registration or request payloads
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Response Schema: Returned to clients (excludes sensitive password)
class UserOut(BaseModel):
    id: int
    email: EmailStr
    modified_Dt: datetime | None = None

    class Config:
        from_attributes = True  # Enables ORM model conversion in Pydantic v2