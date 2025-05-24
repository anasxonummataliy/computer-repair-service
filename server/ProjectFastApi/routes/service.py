from fastapi import APIRouter, HTTPException, Depends, Request
import aiosqlite
from database.connection import get_db
from models.schemas import ServiceCreate, ServiceUpdate, ServiceResponse
from utils.auth import get_current_user, require_role
from utils.password import hash_password
from utils.email import send_email
import random
import string
from datetime import datetime

router = APIRouter()


@router.post("/create")
async def create_service_request(
        service_data: ServiceCreate,
        request: Request,
        db: aiosqlite.Connection = Depends(get_db)
):
    try:
        owner = None

        # If email and fullName provided, create or find user
        if service_data.email and service_data.fullName:
            cursor = await db.execute("SELECT * FROM users WHERE email = ?", (service_data.email,))
            owner = await cursor.fetchone()

            if not owner:
                # Generate random password
                random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                hashed_password = hash_password(random_password)

                # Split fullName
                name_parts = service_data.fullName.split(" ", 1)
                firstname = name_parts[0]
                lastname = name_parts[1] if len(name_parts) > 1 else ""

                # Create new user
                cursor = await db.execute("""
                                          INSERT INTO users (email, password, firstname, lastname, role)
                                          VALUES (?, ?, ?, ?, 'user')
                                          """, (service_data.email, hashed_password, firstname, lastname))

                await db.commit()
                owner_id = cursor.lastrowid

                # Send email with credentials
                subject = "Hisobingiz yaratildi"
                text = f"Hurmatli {firstname}, siz uchun hisob yaratildi.\n\nLogin: {service_data.email}\nParol: {random_password}"
                await send_email(service_data.email, subject, text)

                owner = {"id": owner_id}
        else:
            # Get current user from token
            owner = await get_current_user(request, db)

        if not owner:
            raise HTTPException(status_code=401, detail="Foydalanuvchi topilmadi")

        # Create service request
        cursor = await db.execute("""
                                  INSERT INTO services (device_model, issue_type, problem_area, description, location,
                                                        owner_id, status)
                                  VALUES (?, ?, ?, ?, ?, ?, 'pending')
                                  """, (
                                      service_data.device_model,
                                      service_data.issue_type,
                                      service_data.problem_area,
                                      service_data.description,
                                      service_data.location,
                                      owner["id"]
                                  ))

        await db.commit()
        service_id = cursor.lastrowid

        return {
            "message": "So'rov muvaffaqiyatli yaratildi",
            "serviceId": service_id
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Serverda xatolik yuz berdi")


@router.post("/send/{service_id}")
async def send_to_master(
        service_id: int,
        user: dict = Depends(require_role("manager")),
        db: aiosqlite.Connection = Depends(get_db)
):
    try:
        # Check if service exists
        cursor = await db.execute("SELECT * FROM services WHERE id = ?", (service_id,))
        service = await cursor.fetchone()

        if not service:
            raise HTTPException(status_code=404, detail="So'rov topilmadi")

        # Find master
        cursor = await db.execute("SELECT * FROM users WHERE role = 'master' LIMIT 1")
        master = await cursor.fetchone()

        if not master:
            raise HTTPException(status_code=404, detail="Master topilmadi")

        # Update service
        await db.execute("""
                         UPDATE services
                         SET master_id  = ?,
                             status     = 'in_review',
                             updated_at = CURRENT_TIMESTAMP
                         WHERE id = ?
                         """, (master["id"], service_id))

        await db.commit()

        return {"message": "So'rov masterga yuborildi"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Serverda xatolik yuz berdi")


@router.put("/update")
async def update_service(
        service_data: ServiceUpdate,
        user: dict = Depends(require_role("master")),
        db: aiosqlite.Connection = Depends(get_db)
):
    try:
        # Check if service exists
        cursor = await db.execute("SELECT * FROM services WHERE id = ?", (service_data.requestId,))
        service = await cursor.fetchone()

        if not service:
            raise HTTPException(status_code=404, detail="Xizmat so'rovi topilmadi")

        # Check component availability and update quantities
        for comp in service_data.components:
            cursor = await db.execute("SELECT * FROM components WHERE id = ?", (comp.componentId,))
            component = await cursor.fetchone()

            if not component:
                raise HTTPException(status_code=404, detail=f"Component topilmadi: {comp.componentId}")

            used_qty = comp.quantity if comp.quantity > 0 else 1

            if component["quantity"] < used_qty:
                raise HTTPException(
                    status_code=400,
                    detail=f"Component \"{component['name']}\" uchun yetarli miqdor yo'q. Mavjud: {component['quantity']}, So'ralgan: {used_qty}"
                )

            # Update component quantity
            await db.execute("""
                             UPDATE components
                             SET quantity = quantity - ?
                             WHERE id = ?
                             """, (used_qty, comp.componentId))

            # Add to service_components
            await db.execute("""
                             INSERT INTO service_components (service_id, component_id, quantity)
                             VALUES (?, ?, ?)
                             """, (service_data.requestId, comp.componentId, used_qty))

        # Update service
        finished_at = datetime.fromisoformat(service_data.finishedAt.replace('Z', '+00:00'))

        await db.execute("""
                         UPDATE services
                         SET price       = ?,
                             finished_at = ?,
                             status      = 'completed',
                             updated_at  = CURRENT_TIMESTAMP
                         WHERE id = ?
                         """, (service_data.price, finished_at, service_data.requestId))

        await db.commit()

        return {"message": "Xizmat so'rovi muvaffaqiyatli yangilandi"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Serverda xatolik yuz berdi")


@router.get("/")
async def get_all_services(db: aiosqlite.Connection = Depends(get_db)):
    try:
        cursor = await db.execute("SELECT * FROM services ORDER BY created_at DESC")
        services = await cursor.fetchall()

        return [dict(service) for service in services]

    except Exception as e:
        raise HTTPException(status_code=500, detail="Serverda xatolik yuz berdi")
