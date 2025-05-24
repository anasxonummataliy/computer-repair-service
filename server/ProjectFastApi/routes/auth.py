from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import JSONResponse
import aiosqlite
from database.connection import get_db
from models.schemas import UserCreate, UserLogin, UserResponse
from utils.password import hash_password, verify_password
from utils.auth import create_token
from datetime import timedelta

router = APIRouter()


@router.post("/register")
async def register(user_data: UserCreate, db: aiosqlite.Connection = Depends(get_db)):
    try:
        # Check if user already exists
        cursor = await db.execute("SELECT id FROM users WHERE email = ?", (user_data.email,))
        existing_user = await cursor.fetchone()

        if existing_user:
            raise HTTPException(status_code=409, detail="Bu email ro'yxatdan o'tgan")

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
        raise HTTPException(status_code=500, detail="Serverda xatolik")


@router.post("/login")
async def login(user_data: UserLogin, db: aiosqlite.Connection = Depends(get_db)):
    try:
        # Find user
        cursor = await db.execute("SELECT * FROM users WHERE email = ?", (user_data.email,))
        user = await cursor.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Noto'g'ri email yoki parol")

        # Verify password
        if not verify_password(user_data.password, user["password"]):
            raise HTTPException(status_code=401, detail="Noto'g'ri email yoki parol")

        # Create token
        token = create_token({"id": user["id"]})

        response = JSONResponse(
            content={
                "message": "Kirish muvaffaqiyatli",
                "user": {
                    "id": user["id"],
                    "email": user["email"],
                    "firstname": user["firstname"],
                    "lastname": user["lastname"]
                }
            }
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

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Serverda xatolik")


@router.post("/logout")
async def logout():
    response = JSONResponse(
        content={"message": "Chiqish muvaffaqiyatli amalga oshirildi"}
    )
    response.delete_cookie(key="token")
    return response
