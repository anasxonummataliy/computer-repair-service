from fastapi import APIRouter, Depends, HTTPException

from app.database.models.users import User
from app.schemas.auth import UserLoginRequest, UserRegisRequest

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get('')
async def registration():
    pass



