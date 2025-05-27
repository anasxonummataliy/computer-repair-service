from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_async_session
from app.database.models.users import User

from app.database.models.components import Component