from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=func.now(), onupdate=func.now())