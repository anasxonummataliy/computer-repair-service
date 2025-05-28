from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
import random
import string

# Import utility modules
from utils.mongodb import connect_to_mongodb, close_mongodb_connection, get_collection
from utils.auth_utils import get_current_user, require_auth, require_role, require_roles
from utils.jwt_utils import create_token
from utils.hash_utils import hash_password, compare_password
from utils.email_utils import send_to_email
from utils.response_utils import send_json, success_response, error_response, created_response
from utils.request_utils import handle_request

# Import models
from models import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongodb()
    print("FastAPI server ishga tushdi")
    yield
    # Shutdown
    await close_mongodb_connection()
    print("FastAPI server to'xtatildi")

app = FastAPI(
    title="Service Management API", 
    version="2.0.0",
    description="Utility modullar bilan yangilangan FastAPI backend",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utility functions
def generate_random_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Auth routes
@app.post("/auth/register")
async def register(request: Request):
    try:
        data = await handle_request(request)
        
        email = data.get("email")
        password = data.get("password")
        firstName = data.get("firstName")
        lastName = data.get("lastName")
        isLegalEntity = data.get("isLegalEntity", False)
        companyName = data.get("companyName")
        
        if not all([email, password, firstName, lastName]):
            return error_response("Barcha maydonlar to'ldirilishi kerak", 400)
        
        if isLegalEntity and not companyName:
            return error_response("Yuridik shaxs uchun kompaniya nomi kerak", 400)
        
        # Foydalanuvchi mavjudligini tekshirish
        users_collection = get_collection("users")
        existing_user = await users_collection.find_one({"email": email})
        if existing_user:
            return error_response("Bu email ro'yxatdan o'tgan", 409)
        
        # Yangi foydalanuvchi yaratish
        hashed_password = hash_password(password)
        new_user = {
            "email": email,
            "password": hashed_password,
            "firstName": firstName,
            "lastName": lastName,
            "role": "user",
            "isLegalEntity": isLegalEntity,
            "companyName": companyName,
            "createdAt": datetime.utcnow()
        }
        
        result = await users_collection.insert_one(new_user)
        token = create_token({"sub": str(result.inserted_id)})
        
        return created_response(
            "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi",
            {"userId": str(result.inserted_id)},
            token
        )
        
    except Exception as e:
        return error_response("Serverda xatolik", 500)

@app.post("/auth/login")
async def login(request: Request):
    try:
        data = await handle_request(request)
        
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return error_response("Email va parol kerak", 400)
        
        # Foydalanuvchini topish
        users_collection = get_collection("users")
        user = await users_collection.find_one({"email": email})
        if not user:
            return error_response("Noto'g'ri email yoki parol", 400)
        
        # Parolni tekshirish
        if not compare_password(password, user["password"]):
            return error_response("Noto'g'ri email yoki parol", 400)
        
        # Token yaratish
        token = create_token({"sub": str(user["_id"])})
        
        user_data = {
            "id": str(user["_id"]),
            "email": user["email"],
            "firstName": user.get("firstName"),
            "lastName": user.get("lastName"),
            "role": user.get("role")
        }
        
        return success_response(
            "Kirish muvaffaqiyatli",
            {"user": user_data},
            token
        )
        
    except Exception as e:
        return error_response("Serverda xatolik", 500)

@app.post("/auth/logout")
async def logout():
    return send_json(200, {"message": "Chiqish muvaffaqiyatli amalga oshirildi"})

@app.get("/auth/me")
async def get_auth_user(request: Request):
    user = await require_auth(request)
    user_without_password = {k: v for k, v in user.items() if k != "password"}
    return success_response("Foydalanuvchi ma'lumotlari", user_without_password)

@app.get("/users")
async def get_all_users(request: Request):
    await require_role(request, "manager")
    
    users_collection = get_collection("users")
    users = []
    async for user in users_collection.find({}):
        user["_id"] = str(user["_id"])
        users.append(user)
    
    return success_response("Foydalanuvchilar ro'yxati", {"users": users})

@app.patch("/users/me")
async def partial_update_user(request: Request):
    current_user = await require_auth(request)
    data = await handle_request(request)
    
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    password = data.get("password")
    
    update_fields = {}
    
    if firstName and firstName != current_user.get("firstName"):
        update_fields["firstName"] = firstName
    
    if lastName and lastName != current_user.get("lastName"):
        update_fields["lastName"] = lastName
    
    if password:
        update_fields["password"] = hash_password(password)
    
    if not update_fields:
        return error_response("Hech qanday o'zgarish topilmadi", 400)
    
    users_collection = get_collection("users")
    await users_collection.update_one(
        {"_id": ObjectId(current_user["_id"])},
        {"$set": update_fields}
    )
    
    return success_response("Foydalanuvchi muvaffaqiyatli yangilandi")

# Role creation endpoint
@app.post("/create-roles")
async def create_roles():
    roles_data = [
        {"role": "manager", "email": "manager@gmail.com", "password": "manager", "firstName": "Auto", "lastName": "Manager"},
        {"role": "master", "email": "master@gmail.com", "password": "master", "firstName": "Auto", "lastName": "Master"},
        {"role": "user", "email": "user@gmail.com", "password": "user", "firstName": "Auto", "lastName": "User"},
    ]
    
    users_collection = get_collection("users")
    created_users = []
    
    for role_data in roles_data:
        user = await users_collection.find_one({"email": role_data["email"]})
        
        if not user:
            hashed_password = hash_password(role_data["password"])
            
            new_user = {
                "email": role_data["email"],
                "password": hashed_password,
                "firstName": role_data["firstName"],
                "lastName": role_data["lastName"],
                "role": role_data["role"],
                "createdAt": datetime.utcnow(),
            }
            
            await users_collection.insert_one(new_user)
            
            subject = f"{role_data['role'].capitalize()} akkaunti yaratildi"
            text = f"Hurmatli {role_data['firstName']}, siz uchun {role_data['role']} akkaunti yaratildi.\n\nLogin: {role_data['email']}\nParol: {role_data['password']}"
            
            await send_to_email(role_data["email"], subject, text)
            created_users.append(role_data["role"])
    
    if not created_users:
        return success_response("Barcha role'lar allaqachon mavjud")
    
    return created_response(f"Quyidagi role'lar yaratildi: {', '.join(created_users)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
