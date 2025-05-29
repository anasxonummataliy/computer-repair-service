import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # MongoDB
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "service"

    # JWT
    secret_key: str = "your_secret_key"
    algorithm: str = "HS256"
    access_token_expire_days: int = 30

    # Email
    email_host: str = "smtp.gmail.com"
    email_port: int = 587
    email_user: str = "aummataliy@gmail.com"
    email_password: str = "wievsjqxyvqzawpp"

    class Config:
        env_file = ".env"


settings = Settings()
