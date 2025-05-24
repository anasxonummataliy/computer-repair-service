from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from app.database.models.users import User
from app.schemas.auth import UserLoginRequest, UserRegisRequest
from app.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get('/register')
async def registration(
    user : UserRegisRequest,
    db : AsyncSession = Depends(get_db)
):
    pass


@router.post('/login')
async def login(
    user : UserLoginRequest,
    db : AsyncSession = Depends(get_db)
):
    smtm = select(User).where(User.email == user.email)
    result = await db.execute(smtm)
    if not smtm:
        raise HTTPException(status_code=404, detail="User not found")
    if not smtm.password == user.password:
        raise HTTPException(status_code=401, detail="Invalid password")
    return {
        "message": "Login successful",
        "user": {
            "email": smtm.email,
            "name": smtm.name
        }
    }


