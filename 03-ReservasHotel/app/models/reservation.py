from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, ForeignKey, Boolean, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class ReservationStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

# SQLAlchemy model
class Reservation(Base):
    __tablename__ = "reservations"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    guest_id = Column(Integer, ForeignKey("guests.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.CONFIRMED)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Pydantic models
class ReservationBase(BaseModel):
    guest_id: int = Field(..., gt=0, description="ID del huésped")
    room_id: int = Field(..., gt=0, description="ID de la habitación")
    check_in_date: date = Field(..., description="Fecha de entrada")
    check_out_date: date = Field(..., description="Fecha de salida")
    total_amount: Optional[float] = Field(None, ge=0, description="Monto total")

    @validator('check_out_date')
    def check_out_must_be_after_check_in(cls, v, values):
        if 'check_in_date' in values and v <= values['check_in_date']:
            raise ValueError('La fecha de salida debe ser posterior a la fecha de entrada')
        return v

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(BaseModel):
    guest_id: Optional[int] = Field(None, gt=0, description="ID del huésped")
    room_id: Optional[int] = Field(None, gt=0, description="ID de la habitación")
    check_in_date: Optional[date] = Field(None, description="Fecha de entrada")
    check_out_date: Optional[date] = Field(None, description="Fecha de salida")
    total_amount: Optional[float] = Field(None, ge=0, description="Monto total")

class ReservationResponse(ReservationBase):
    id: int
    status: str = "confirmed"
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True