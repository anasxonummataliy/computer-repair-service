from typing import List, Optional
from pydantic import BaseModel, EmailStr


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
