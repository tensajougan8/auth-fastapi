from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    photo_url: Optional[str] = None

class User(UserBase):
    id: UUID
    bio: Optional[str] = None
    phone: Optional[str] = None
    photo_url: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str