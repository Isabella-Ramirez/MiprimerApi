"""Modelos de huésped: SQLAlchemy y esquemas Pydantic."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Guest(Base):
    """Modelo SQLAlchemy que representa a un huésped."""

    __tablename__ = "guests"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(15), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class GuestBase(BaseModel):
    """Esquema base para datos de huésped."""

    name: str = Field(..., min_length=2, max_length=100, description="Nombre del huésped")
    email: str = Field(..., description="Correo electrónico del huésped")
    phone: str = Field(..., min_length=10, max_length=15, description="Teléfono del huésped")


class GuestCreate(GuestBase):
    """Esquema para creación de huésped."""

    pass


class GuestUpdate(BaseModel):
    """Esquema para actualización parcial de huésped."""

    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Nombre del huésped")
    email: Optional[str] = Field(None, description="Correo electrónico del huésped")
    phone: Optional[str] = Field(None, min_length=10, max_length=15, description="Teléfono del huésped")


class GuestResponse(GuestBase):
    """Esquema de respuesta de huésped."""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True