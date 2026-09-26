from datetime import datetime

from pydantic import BaseModel, EmailStr


class ProductSchema(BaseModel):
    Name: str
    Price: int
    Is_Sale: bool | None = False
    Inventory: int | None = 0


class TestCreate(BaseModel):
    name: str
    Fname: str | None = None
    salary: float | None = None
    createdby: str | None = "System"


class TestResponse(BaseModel):
    Id: int
    name: str
    Fname: str | None = None
    salary: float | None = None
    createdby: str

    class Config:
        from_attributes = True


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