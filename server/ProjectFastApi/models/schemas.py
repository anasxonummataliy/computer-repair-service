from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    firstName: str
    lastName: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    firstname: str
    lastname: str
    role: str

# Service schemas
class ServiceCreate(BaseModel):
    device_model: str
    issue_type: str
    problem_area: str
    description: str
    location: str
    email: Optional[EmailStr] = None
    fullName: Optional[str] = None

class ComponentUsage(BaseModel):
    componentId: int
    quantity: int

class ServiceUpdate(BaseModel):
    requestId: int
    price: float
    finishedAt: str
    components: List[ComponentUsage]

class ServiceResponse(BaseModel):
    id: int
    device_model: str
    issue_type: str
    problem_area: str
    description: str
    location: str
    owner_id: int
    master_id: Optional[int] = None
    price: Optional[float] = None
    status: str
    created_at: str

# Component schemas
class ComponentCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

class ComponentResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int
    created_at: str
