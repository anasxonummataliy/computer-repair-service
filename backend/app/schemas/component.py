from pydantic import BaseModel


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
