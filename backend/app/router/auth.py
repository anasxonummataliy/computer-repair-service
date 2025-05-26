from argon2 import verify_password
from fastapi import APIRouter, Depends, HTTPException, logger
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.database.models.users import User
from app.schemas.auth import UserCreate, UserLogin, UserResponse
from app.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.untils import hash_password, 
from backend.app.core.security.jwt import create_jwt_token


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.get('/register')
async def registration(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        smtm = select(User).where(User.email == user_in.email)
        result = await db.execute(smtm)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=409, detail="Bu email ro'yxatdan o'tgan")
        
        user_in.password = hash_password(user_in.password)
        new_user = User(**user_in.model_dump())
        db.add(new_user)
        await db.commit()

        token = create_jwt_token(user_in.id)
        response = JSONResponse(
            content={
                "message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi",
                "userId": user_in.id,
            },
            status_code=201
        )
       
        response.set_cookie(
            key="token",
            value=token,
            httponly=True,
            max_age=30 * 24 * 60 * 60,  
            samesite="strict",
            secure=False  
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Serverda xatolik yuz berdi")


@router.post('/login')
async def login(
    user_in: UserLogin,
    db : AsyncSession = Depends(get_db)
):
    try:
        stmt = select(User).where(User.email == user_in.email)
        result = await db.execute(stmt)
        db_user = result.scalar_one_or_none()

        if not db_user:
            logger.warning("Bunday foydalanuvchi mavjud emas.")
            raise HTTPException(
                status_code=404, detail="Bunday foydalanuvchi mavjud emas."
            )
        if verify_password(db_user.password, user_in.password):
            logger.info("Kirish muvafaqiyatli amalga oshirildi.")
            token = create_jwt_token(db_user.id)
            return JSONResponse(content={"message": "", "token": token})
        raise HTTPException(detail="Ma'lumotlar xato")

     
    except Exception as e:
        raise HTTPException(status_code=500, detail="Serverda xatolik yuz berdi")

