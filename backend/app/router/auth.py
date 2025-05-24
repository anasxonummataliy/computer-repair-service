from fastapi import APIRouter, Depends, HTTPException

from app.database.models.users import User
from app.schemas.auth import UserLoginRequest, UserRegisRequest
from app.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get('')
async def registration(
    user : UserRegisRequest,
    db : AsyncSession = Depends(get_db)
):
    pass



