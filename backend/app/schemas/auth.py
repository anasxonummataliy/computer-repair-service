from pydantic import BaseModel

class UserRegisRequest(BaseModel):
    email : str
    password : str

class UserLoginRequest(BaseModel):
    email : str
    password : str