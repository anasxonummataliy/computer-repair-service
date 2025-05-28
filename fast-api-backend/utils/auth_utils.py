from fastapi import Request, HTTPException
from bson import ObjectId
from typing import Optional, Dict, Any
from .jwt_utils import verify_token
from .mongodb import get_collection

class AuthManager:
    def __init__(self):
        self.users_collection = None
    
    def _get_users_collection(self):
        """Users collection ni olish"""
        if self.users_collection is None:
            self.users_collection = get_collection("users")
        return self.users_collection
    
    async def get_current_user(self, request: Request) -> Optional[Dict[str, Any]]:
        """Cookie dan current user ni olish"""
        try:
            # Cookie dan token olish
            cookie_header = request.headers.get("cookie")
            if not cookie_header:
                return None
            
            # Cookie larni parse qilish
            cookies = {}
            for cookie in cookie_header.split(";"):
                if "=" in cookie:
                    key, value = cookie.strip().split("=", 1)
                    cookies[key] = value
            
            token = cookies.get("token")
            if not token:
                return None
            
            # Token ni verify qilish
            payload = verify_token(token)
            if not payload:
                return None
            
            user_id = payload.get("sub") or payload.get("id")
            if not user_id:
                return None
            
            # User ni database dan olish
            users_collection = self._get_users_collection()
            user = await users_collection.find_one({"_id": ObjectId(user_id)})
            
            if user:
                user["_id"] = str(user["_id"])
            
            return user
            
        except Exception as e:
            print(f"get_current_user da xatolik: {e}")
            return None
    
    async def require_auth(self, request: Request) -> Dict[str, Any]:
        """Majburiy autentifikatsiya"""
        user = await self.get_current_user(request)
        if not user:
            raise HTTPException(status_code=401, detail="Avtorizatsiya talab qilinadi")
        return user
    
    async def require_role(self, request: Request, required_role: str) -> Dict[str, Any]:
        """Majburiy rol tekshiruvi"""
        user = await self.require_auth(request)
        if user.get("role") != required_role:
            raise HTTPException(status_code=403, detail=f"Faqat {required_role} roli kerak")
        return user
    
    async def require_roles(self, request: Request, required_roles: list) -> Dict[str, Any]:
        """Bir nechta roldan birini tekshirish"""
        user = await self.require_auth(request)
        if user.get("role") not in required_roles:
            raise HTTPException(status_code=403, detail=f"Quyidagi rollardan biri kerak: {', '.join(required_roles)}")
        return user

# Global auth manager instance
auth_manager = AuthManager()

async def get_current_user(request: Request) -> Optional[Dict[str, Any]]:
    """Current user ni olish"""
    return await auth_manager.get_current_user(request)

async def require_auth(request: Request) -> Dict[str, Any]:
    """Majburiy autentifikatsiya"""
    return await auth_manager.require_auth(request)

async def require_role(request: Request, required_role: str) -> Dict[str, Any]:
    """Majburiy rol tekshiruvi"""
    return await auth_manager.require_role(request, required_role)

async def require_roles(request: Request, required_roles: list) -> Dict[str, Any]:
    """Bir nechta roldan birini tekshirish"""
    return await auth_manager.require_roles(request, required_roles)
