from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer
import jwt
from datetime import datetime, timedelta
import aiosqlite
from database.connection import get_db
from typing import Optional

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

security = HTTPBearer()


def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=30)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("id")
    except jwt.PyJWTError:
        return None


async def get_current_user(request: Request, db: aiosqlite.Connection = Depends(get_db)):
    # Get token from cookies
    token = request.cookies.get("token")
    if not token:
        return None

    user_id = verify_token(token)
    if not user_id:
        return None

    cursor = await db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = await cursor.fetchone()

    if user:
        return dict(user)
    return None


async def require_auth(request: Request, db: aiosqlite.Connection = Depends(get_db)):
    user = await get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user


def require_role(role: str):
    def role_dependency(user: dict = Depends(require_auth)):
        if user["role"] != role:
            raise HTTPException(status_code=403, detail=f"Role {role} required")
        return user

    return role_dependency
