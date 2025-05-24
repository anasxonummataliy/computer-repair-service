from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from app.database.models.users import User
from app.schemas.auth import UserCreate, UserLogin, UserResponse
from app.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.get('/register')
async def registration(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        cursor = await db.execute("SELECT id FROM users WHERE email = ?", (user_data.email,))
        existing_user = await cursor.fetchone()

        if existing_user:
            raise HTTPException(
                status_code=409, detail="Bu email ro'yxatdan o'tgan")

        # Hash password
        hashed_password = hash_password(user_data.password)

        # Insert new user
        cursor = await db.execute("""
                                  INSERT INTO users (email, password, firstname, lastname, role)
                                  VALUES (?, ?, ?, ?, 'user')
                                  """, (user_data.email, hashed_password, user_data.firstName, user_data.lastName))

        await db.commit()
        user_id = cursor.lastrowid

        # Create token
        token = create_token({"id": user_id})

        response = JSONResponse(
            content={
                "message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi",
                "userId": user_id
            },
            status_code=201
        )

        # Set cookie
        response.set_cookie(
            key="token",
            value=token,
            httponly=True,
            max_age=30 * 24 * 60 * 60,  # 30 days
            samesite="strict",
            secure=False  # Set to True in production with HTTPS
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Serverda xatolik yuz berdi")


@router.post('/login')
async def login(
    user: UserLogin,
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


