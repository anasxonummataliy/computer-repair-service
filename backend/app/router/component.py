from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.database.models.components import Component
from app.schemas.component import ComponentCreate, ComponentResponse


router = APIRouter()


@router.post("/")
async def create_component(
        component_data: ComponentCreate,
        db: AsyncSession = Depends(get_db)
):
    try:
        new_component = await db.execute()

        await db.commit()
        component_id = cursor.lastrowid

        return {
            "message": "Component yaratildi",
            "componentId": component_id
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Serverda xatolik yuz berdi")


@router.get("/")
async def get_all_components(db: AsyncSession = Depends(get_db)):
    try:
        cursor = await db.execute("SELECT * FROM components ORDER BY created_at DESC")
        components = await cursor.fetchall()

        return [dict(component) for component in components]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Serverda xatolik yuz berdi")
