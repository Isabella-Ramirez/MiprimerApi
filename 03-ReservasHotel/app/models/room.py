from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Numeric
from sqlalchemy.sql import func
from app.database import Base

# SQLAlchemy model
class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    room_number = Column(String(10), nullable=False, unique=True)
    room_type = Column(String(50), nullable=False)
    price_per_night = Column(Numeric(10, 2), nullable=False)
    is_available = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Pydantic models
class RoomBase(BaseModel):
    room_number: str = Field(..., min_length=1, max_length=10, description="Número de habitación")
    room_type: str = Field(..., min_length=3, max_length=50, description="Tipo de habitación (individual, doble, suite)")
    price_per_night: float = Field(..., gt=0, description="Precio por noche")
    is_available: bool = Field(True, description="Disponibilidad de la habitación")

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseModel):
    room_number: Optional[str] = Field(None, min_length=1, max_length=10, description="Número de habitación")
    room_type: Optional[str] = Field(None, min_length=3, max_length=50, description="Tipo de habitación")
    price_per_night: Optional[float] = Field(None, gt=0, description="Precio por noche")
    is_available: Optional[bool] = Field(None, description="Disponibilidad de la habitación")

class RoomResponse(RoomBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True