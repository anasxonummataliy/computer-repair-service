from fastapi import APIRouter, HTTPException, Depends
import aiosqlite
from database.connection import get_db
from utils.password import hash_password
from utils.email import send_email

router = APIRouter()


@router.get("/create")
async def create_roles(db: aiosqlite.Connection = Depends(get_db)):
    try:
        roles_data = [
            {"role": "manager", "email": "manager@gmail.com", "password": "manager", "firstname": "Auto",
             "lastname": "Manager"},
            {"role": "master", "email": "master@gmail.com", "password": "master", "firstname": "Auto",
             "lastname": "Master"},
            {"role": "user", "email": "user@gmail.com", "password": "user", "firstname": "Auto", "lastname": "User"},
        ]

        created_users = []

        for role_data in roles_data:
            # Check if user already exists
            cursor = await db.execute("SELECT id FROM users WHERE email = ?", (role_data["email"],))
            existing_user = await cursor.fetchone()

            if not existing_user:
                # Hash password
                hashed_password = hash_password(role_data["password"])

                # Create user
                await db.execute("""
                                 INSERT INTO users (email, password, firstname, lastname, role)
                                 VALUES (?, ?, ?, ?, ?)
                                 """, (
                                     role_data["email"],
                                     hashed_password,
                                     role_data["firstname"],
                                     role_data["lastname"],
                                     role_data["role"]
                                 ))

                # Send email
                subject = f"{role_data['role'].capitalize()} akkaunti yaratildi"
                text = f"Hurmatli {role_data['firstname']}, siz uchun {role_data['role']} akkaunti yaratildi.\n\nLogin: {role_data['email']}\nParol: {role_data['password']}"

                await send_email(role_data["email"], subject, text)

                created_users.append(role_data["role"])

        await db.commit()

        if not created_users:
            return {"message": "Barcha role'lar allaqachon mavjud"}

        return {"message": f"Quyidagi role'lar yaratildi: {', '.join(created_users)}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Serverda xatolik yuz berdi")
