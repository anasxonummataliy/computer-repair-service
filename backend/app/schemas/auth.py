from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    USER = "user"
    MASTER = "master"
    MANAGER = "manager"


class UserBase(BaseModel):
    email: EmailStr
    firstName: str
    lastName: str

class UserCreate(UserBase):
    password: str
    isLegalEntity: Optional[bool] = False
    companyName: Optional[str] = None


class UserUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    password: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: str
    role: UserRole
    isLegalEntity: Optional[bool] = False
    companyName: Optional[str] = None
    createdAt: Optional[datetime] = None
