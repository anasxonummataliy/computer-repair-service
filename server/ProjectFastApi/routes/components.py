from fastapi import APIRouter, HTTPException, Depends
import aiosqlite
from database.connection import get_db
from models.schemas import ComponentCreate, ComponentResponse

router = APIRouter()


@router.post("/")
async def create_component(
        component_data: ComponentCreate,
        db: aiosqlite.Connection = Depends(get_db)
):
    try:
        cursor = await db.execute("""
                                  INSERT INTO components (name, description, price, quantity)
                                  VALUES (?, ?, ?, ?)
                                  """, (
                                      component_data.name,
                                      component_data.description,
                                      component_data.price,
                                      component_data.quantity
                                  ))

        await db.commit()
        component_id = cursor.lastrowid

        return {
            "message": "Component yaratildi",
            "componentId": component_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail="Serverda xatolik yuz berdi")


@router.get("/")
async def get_all_components(db: aiosqlite.Connection = Depends(get_db)):
    try:
        cursor = await db.execute("SELECT * FROM components ORDER BY created_at DESC")
        components = await cursor.fetchall()

        return [dict(component) for component in components]

    except Exception as e:
        raise HTTPException(status_code=500, detail="Serverda xatolik yuz berdi")
