import bcrypt
from typing import Union

class PasswordHasher:
    def __init__(self, rounds: int = 10):
        self.rounds = rounds
    
    def hash_password(self, password: str) -> str:
        """Parolni hash qilish"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def compare_password(self, plain_password: str, hashed_password: str) -> bool:
        """Parolni tekshirish"""
        try:
            password_bytes = plain_password.encode('utf-8')
            hashed_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception:
            return False

# Global hasher instance
password_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    return password_hasher.hash_password(password)

def compare_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.compare_password(plain_password, hashed_password)
