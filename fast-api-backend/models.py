from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    MASTER = "master"
    MANAGER = "manager"

class ServiceStatus(str, Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    COMPLETED = "completed"

# User models
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

# Component models
class ComponentCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

class ComponentResponse(ComponentCreate):
    id: str
    createdAt: datetime

class ComponentUsed(BaseModel):
    componentId: str
    quantity: int

# Service models
class ServiceRequestCreate(BaseModel):
    device_model: str
    issue_type: str
    problem_area: str
    description: str
    location: str
    email: Optional[EmailStr] = None
    fullName: Optional[str] = None

class ServiceUpdate(BaseModel):
    price: float
    finishedAt: datetime
    components: List[ComponentUsed]
    requestId: str

class ServiceStatusUpdate(BaseModel):
    requestId: str

class ServiceComplete(BaseModel):
    requestId: str

class ServiceResponse(BaseModel):
    id: str
    device_model: str
    issue_type: str
    problem_area: str
    description: str
    location: str
    status: ServiceStatus
    owner: dict
    master: Optional[dict] = None
    price: Optional[float] = None
    finishedAt: Optional[datetime] = None
    usedProducts: Optional[List[dict]] = None
    createdAt: datetime
    updatedAt: Optional[datetime] = None

# Stats models
class VisitorStats(BaseModel):
    date: str
    count: int

class LocationStats(BaseModel):
    source: str
    count: int

class RequestStats(BaseModel):
    total_requests: int
    pending_requests: int
    in_progress_requests: int
    completed_requests: int

# Other models
class Token(BaseModel):
    access_token: str
    token_type: str

class EmailRequest(BaseModel):
    email: EmailStr
    subject: str
    text: str

class MessageResponse(BaseModel):
    message: str
