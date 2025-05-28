from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime, timedelta
import random
import string
from contextlib import asynccontextmanager

from models import *
from auth import get_current_user_required, get_current_user, create_access_token, get_password_hash, verify_password
from email_service import send_email

# Global variables
db = None
users_collection = None
services_collection = None
components_collection = None

# MongoDB settings
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "service"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global db, users_collection, services_collection, components_collection
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    users_collection = db["users"]
    services_collection = db["services"]
    components_collection = db["components"]
    print("MongoDB ga ulandi")
    yield
    # Shutdown
    client.close()

app = FastAPI(title="Service Management API", version="1.0.0", lifespan=lifespan)

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

def set_cookie_response(content: str, token: str = None):
    response = Response(content=content, media_type="application/json")
    if token:
        response.set_cookie(
            key="token",
            value=token,
            max_age=30 * 24 * 60 * 60,  # 30 kun
            httponly=True,
            secure=True,
            samesite="strict"
        )
    return response

# Auth routes
@app.post("/auth/register")
async def register(user_data: UserCreate):
    # Foydalanuvchi mavjudligini tekshirish
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=409, detail="Bu email ro'yxatdan o'tgan")
    
    # Parolni hash qilish
    hashed_password = get_password_hash(user_data.password)
    
    # Yangi foydalanuvchi yaratish
    new_user = {
        "email": user_data.email,
        "password": hashed_password,
        "firstName": user_data.firstName,
        "lastName": user_data.lastName,
        "role": "user",
        "isLegalEntity": user_data.isLegalEntity,
        "companyName": user_data.companyName,
        "createdAt": datetime.utcnow()
    }
    
    result = await users_collection.insert_one(new_user)
    
    # Token yaratish
    access_token = create_access_token(data={"sub": str(result.inserted_id)})
    
    return set_cookie_response(
        '{"message": "Foydalanuvchi muvaffaqiyatli ro\'yxatdan o\'tdi"}',
        access_token
    )

@app.post("/auth/login")
async def login(user_data: UserLogin):
    # Foydalanuvchini topish
    user = await users_collection.find_one({"email": user_data.email})
    if not user:
        raise HTTPException(status_code=400, detail="Noto'g'ri email yoki parol")
    
    # Parolni tekshirish
    if not verify_password(user_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Noto'g'ri email yoki parol")
    
    # Token yaratish
    access_token = create_access_token(data={"sub": str(user["_id"])})
    
    return set_cookie_response(
        '{"message": "Kirish muvaffaqiyatli"}',
        access_token
    )

@app.post("/auth/logout")
async def logout():
    response = Response(content='{"message": "Chiqish muvaffaqiyatli amalga oshirildi"}', 
                       media_type="application/json")
    response.delete_cookie(key="token")
    return response

# User routes
@app.get("/auth/me")
async def get_auth_user(current_user: dict = Depends(get_current_user_required)):
    user_without_password = {k: v for k, v in current_user.items() if k != "password"}
    return user_without_password

@app.get("/users")
async def get_all_users(current_user: dict = Depends(get_current_user_required)):
    if current_user.get("role") != "manager":
        raise HTTPException(status_code=403, detail="Sizda ruxsat yo'q")
    
    users = []
    async for user in users_collection.find({}):
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

@app.patch("/users/me")
async def partial_update_user(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user_required)
):
    update_fields = {}
    
    if user_update.firstName and user_update.firstName != current_user.get("firstName"):
        update_fields["firstName"] = user_update.firstName
    
    if user_update.lastName and user_update.lastName != current_user.get("lastName"):
        update_fields["lastName"] = user_update.lastName
    
    if user_update.password:
        hashed_password = get_password_hash(user_update.password)
        update_fields["password"] = hashed_password
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="Hech qanday o'zgarish topilmadi")
    
    await users_collection.update_one(
        {"_id": ObjectId(current_user["_id"])},
        {"$set": update_fields}
    )
    
    return {"message": "Foydalanuvchi muvaffaqiyatli yangilandi"}

# Role creation
@app.post("/create-roles")
async def create_roles():
    roles_data = [
        {"role": "manager", "email": "manager@gmail.com", "password": "manager", "firstName": "Auto", "lastName": "Manager"},
        {"role": "master", "email": "master@gmail.com", "password": "master", "firstName": "Auto", "lastName": "Master"},
        {"role": "user", "email": "user@gmail.com", "password": "user", "firstName": "Auto", "lastName": "User"},
    ]
    
    created_users = []
    
    for role_data in roles_data:
        user = await users_collection.find_one({"email": role_data["email"]})
        
        if not user:
            hashed_password = get_password_hash(role_data["password"])
            
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
            
            await send_email(role_data["email"], subject, text)
            created_users.append(role_data["role"])
    
    if not created_users:
        return {"message": "Barcha role'lar allaqachon mavjud"}
    
    return {"message": f"Quyidagi role'lar yaratildi: {', '.join(created_users)}"}

# Component routes
@app.post("/components")
async def create_component(component_data: ComponentCreate):
    new_component = {
        "name": component_data.name,
        "description": component_data.description,
        "price": component_data.price,
        "quantity": component_data.quantity,
        "createdAt": datetime.utcnow(),
    }
    
    result = await components_collection.insert_one(new_component)
    
    return {
        "message": "Component yaratildi",
        "componentId": str(result.inserted_id),
    }

@app.get("/components")
async def get_all_components():
    components = []
    async for component in components_collection.find({}):
        component["_id"] = str(component["_id"])
        components.append(component)
    return components

# Service routes
@app.post("/services")
async def create_service_request(
    service_data: ServiceRequestCreate,
    request: Request
):
    owner = None
    
    if service_data.email and service_data.fullName:
        owner = await users_collection.find_one({"email": service_data.email})
        
        if not owner:
            random_password = generate_random_password()
            hashed_password = get_password_hash(random_password)
            
            firstName = service_data.fullName.split(" ")[0] if service_data.fullName else service_data.fullName
            lastName = " ".join(service_data.fullName.split(" ")[1:]) if len(service_data.fullName.split(" ")) > 1 else ""
            
            new_user = {
                "email": service_data.email,
                "password": hashed_password,
                "firstName": firstName,
                "lastName": lastName,
                "role": "user",
                "createdAt": datetime.utcnow(),
            }
            
            result = await users_collection.insert_one(new_user)
            owner = {"_id": result.inserted_id, **new_user}
            
            subject = "Hisobingiz yaratildi"
            text = f"Hurmatli {firstName}, siz uchun hisob yaratildi.\n\nLogin: {service_data.email}\nParol: {random_password}"
            await send_email(service_data.email, subject, text)
    else:
        owner = await get_current_user(request)
    
    if not owner:
        raise HTTPException(status_code=401, detail="Foydalanuvchi topilmadi")
    
    owner_data = {k: v for k, v in owner.items() if k != "password"}
    
    new_service_request = {
        "device_model": service_data.device_model,
        "issue_type": service_data.issue_type,
        "problem_area": service_data.problem_area,
        "description": service_data.description,
        "location": service_data.location,
        "owner": owner_data,
        "createdAt": datetime.utcnow(),
        "status": "pending"
    }
    
    result = await services_collection.insert_one(new_service_request)
    
    return {
        "message": "So'rov muvaffaqiyatli yaratildi",
        "serviceId": str(result.inserted_id)
    }

@app.post("/services/{service_id}/send-to-master")
async def send_to_master(
    service_id: str,
    current_user: dict = Depends(get_current_user_required)
):
    if current_user.get("role") != "manager":
        raise HTTPException(status_code=403, detail="Faqat manager bu amalni bajarishi mumkin")
    
    if not ObjectId.is_valid(service_id):
        raise HTTPException(status_code=400, detail="Noto'g'ri serviceId formati")
    
    service_request = await services_collection.find_one({"_id": ObjectId(service_id)})
    if not service_request:
        raise HTTPException(status_code=404, detail="So'rov topilmadi")
    
    master = await users_collection.find_one({"role": "master"})
    if not master:
        raise HTTPException(status_code=404, detail="Master topilmadi")
    
    master_data = {k: v for k, v in master.items() if k != "password"}
    
    update_result = await services_collection.update_one(
        {"_id": ObjectId(service_id)},
        {
            "$set": {
                "master": master_data,
                "status": "in_review",
                "updatedAt": datetime.utcnow()
            }
        }
    )
    
    if update_result.modified_count == 0:
        raise HTTPException(status_code=500, detail="So'rovni yangilab bo'lmadi")
    
    return {"message": "So'rov masterga yuborildi"}

@app.put("/services/update")
async def update_service(
    service_update: ServiceUpdate,
    current_user: dict = Depends(get_current_user_required)
):
    if current_user.get("role") != "master":
        raise HTTPException(status_code=403, detail="Faqat master bu amalni bajarishi mumkin")
    
    if not ObjectId.is_valid(service_update.requestId):
        raise HTTPException(status_code=400, detail="Noto'g'ri requestId formati")
    
    service_request = await services_collection.find_one({"_id": ObjectId(service_update.requestId)})
    if not service_request:
        raise HTTPException(status_code=404, detail="Xizmat so'rovi topilmadi")
    
    used_products = []
    
    for comp in service_update.components:
        if not ObjectId.is_valid(comp.componentId):
            raise HTTPException(status_code=400, detail=f"Noto'g'ri componentId: {comp.componentId}")
        
        component = await components_collection.find_one({"_id": ObjectId(comp.componentId)})
        if not component:
            raise HTTPException(status_code=404, detail=f"Component topilmadi: {comp.componentId}")
        
        used_products.append({
            "componentId": str(component["_id"]),
            "name": component["name"],
            "price": component["price"],
            "usedQuantity": comp.quantity,
        })
    
    update_data = {
        "price": service_update.price,
        "finishedAt": service_update.finishedAt,
        "usedProducts": used_products,
        "status": "approved",
        "updatedAt": datetime.utcnow(),
    }
    
    result = await services_collection.update_one(
        {"_id": ObjectId(service_update.requestId)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Xizmat so'rovini yangilashda xatolik yuz berdi")
    
    return {"message": "Xizmat so'rovi muvaffaqiyatli yangilandi"}

@app.get("/services")
async def get_all_services(current_user: dict = Depends(get_current_user_required)):
    filter_query = {}
    
    if current_user.get("role") == "master":
        filter_query["master._id"] = current_user["_id"]
    elif current_user.get("role") == "user":
        filter_query["owner._id"] = current_user["_id"]
    elif current_user.get("role") == "manager":
        pass  # Manager can see all services
    
    services = []
    async for service in services_collection.find(filter_query):
        service["_id"] = str(service["_id"])
        services.append(service)
    
    return services

@app.patch("/services/status")
async def update_service_status(
    status_update: ServiceStatusUpdate,
    current_user: dict = Depends(get_current_user_required)
):
    if not ObjectId.is_valid(status_update.requestId):
        raise HTTPException(status_code=400, detail="Noto'g'ri serviceId formati")
    
    service_request = await services_collection.find_one({"_id": ObjectId(status_update.requestId)})
    if not service_request:
        raise HTTPException(status_code=404, detail="So'rov topilmadi")
    
    update_data = {"updatedAt": datetime.utcnow()}
    
    if current_user.get("role") == "user":
        update_data["status"] = "in_progress"
    elif current_user.get("role") == "master":
        update_data["status"] = "approved"
    else:
        raise HTTPException(status_code=403, detail="Faqat user va master bu amalni bajarishi mumkin")
    
    await services_collection.update_one(
        {"_id": ObjectId(status_update.requestId)},
        {"$set": update_data}
    )
    
    return {"message": "yangilandi"}

@app.patch("/services/complete")
async def complete_service(service_complete: ServiceComplete):
    if not ObjectId.is_valid(service_complete.requestId):
        raise HTTPException(status_code=400, detail="Noto'g'ri serviceId formati")
    
    service_request = await services_collection.find_one({"_id": ObjectId(service_complete.requestId)})
    if not service_request:
        raise HTTPException(status_code=404, detail="So'rov topilmadi")
    
    await services_collection.update_one(
        {"_id": ObjectId(service_complete.requestId)},
        {"$set": {"status": "completed", "updatedAt": datetime.utcnow()}}
    )
    
    return {"message": "yangilandi"}

# Stats routes
@app.get("/stats/visitors")
async def get_visitor_stats(current_user: dict = Depends(get_current_user_required)):
    if current_user.get("role") != "manager":
        raise HTTPException(status_code=403, detail="Ruxsat yo'q")
    
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    pipeline = [
        {
            "$match": {
                "createdAt": {
                    "$gte": thirty_days_ago,
                    "$lte": datetime.utcnow()
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateToString": {"format": "%Y-%m-%d", "date": "$createdAt"}
                },
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "date": "$_id",
                "count": 1
            }
        },
        {
            "$sort": {"date": 1}
        }
    ]
    
    visitor_data = await users_collection.aggregate(pipeline).to_list(None)
    return visitor_data

@app.get("/stats/locations")
async def get_location_stats(current_user: dict = Depends(get_current_user_required)):
    if current_user.get("role") != "manager":
        raise HTTPException(status_code=403, detail="Ruxsat yo'q")
    
    pipeline = [
        {
            "$group": {
                "_id": "$location",
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "source": {"$ifNull": ["$_id", "Unknown"]},
                "count": 1
            }
        }
    ]
    
    location_data = await services_collection.aggregate(pipeline).to_list(None)
    return location_data

@app.get("/stats/requests")
async def get_request_stats(current_user: dict = Depends(get_current_user_required)):
    filter_query = {}
    
    if current_user.get("role") == "master":
        filter_query["master._id"] = current_user["_id"]
    elif current_user.get("role") == "user":
        filter_query["owner._id"] = current_user["_id"]
    elif current_user.get("role") == "manager":
        pass  # Manager can see all
    else:
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")
    
    total = await services_collection.count_documents(filter_query)
    pending = await services_collection.count_documents({**filter_query, "status": "pending"})
    in_progress = await services_collection.count_documents({**filter_query, "status": "in_progress"})
    completed = await services_collection.count_documents({**filter_query, "status": "completed"})
    
    return {
        "total_requests": total,
        "pending_requests": pending,
        "in_progress_requests": in_progress,
        "completed_requests": completed,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
