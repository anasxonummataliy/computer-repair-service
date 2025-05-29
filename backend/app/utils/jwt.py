import jwt
from datetime import datetime, timedelta
from typing import Optional, Union
from fastapi import HTTPException


class JWTManager:
    def __init__(self, secret_key: str = "your_secret_key", algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(self, payload: dict, expires_in: Union[str, timedelta] = "30d") -> str:
        """JWT token yaratish"""
        to_encode = payload.copy()

        if isinstance(expires_in, str):
            if expires_in.endswith('d'):
                days = int(expires_in[:-1])
                expire = datetime.utcnow() + timedelta(days=days)
            elif expires_in.endswith('h'):
                hours = int(expires_in[:-1])
                expire = datetime.utcnow() + timedelta(hours=hours)
            elif expires_in.endswith('m'):
                minutes = int(expires_in[:-1])
                expire = datetime.utcnow() + timedelta(minutes=minutes)
            else:
                expire = datetime.utcnow() + timedelta(days=30)
        else:
            expire = datetime.utcnow() + expires_in

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[dict]:
        """JWT token ni tekshirish"""
        try:
            payload = jwt.decode(token, self.secret_key,
                                 algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None


# Global JWT manager instance
jwt_manager = JWTManager()


def create_token(payload: dict, expires_in: Union[str, timedelta] = "30d") -> str:
    return jwt_manager.create_token(payload, expires_in)


def verify_token(token: str) -> Optional[dict]:
    return jwt_manager.verify_token(token)
