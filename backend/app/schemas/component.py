from datetime import datetime
from pydantic import BaseModel


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
