from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from app.schemas.component import ComponentUsed



class ServiceStatus(str, Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    COMPLETED = "completed"

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
