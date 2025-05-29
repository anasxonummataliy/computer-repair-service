from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class EmailRequest(BaseModel):
    email: EmailStr
    subject: str
    text: str


class MessageResponse(BaseModel):
    message: str
