from pydantic import BaseModel, EmailStr, constr
from datetime import date
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(BaseModel):
    password: str

class User(BaseModel):
    id: int
    email: EmailStr
    avatar_url: Optional[str] = None
    is_verified: bool

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    
class ContactBase(BaseModel):
    first_name: constr(min_length=1)
    last_name: constr(min_length=1)
    email: EmailStr
    phone: str
    bithday: date
    additional_info: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: Optional[constr(min_length=1)]
    last_name: Optional[constr(min_length=1)]
    email: Optional[EmailStr]
    phone: Optional[str]
    bithday: Optional[date]
    additional_info: Optional[str] = None

class ContactInDB(ContactBase):
    id: int

    class Config:
        orm_mode = True