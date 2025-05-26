from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    firstname: str
    lastname: str
    role: str
