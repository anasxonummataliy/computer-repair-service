from sqlalchemy import Column, Integer, String, Float

from app.database.base import Base


class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    in_stock = Column(Integer, default=0)
    price = Column(Float, nullable=True)