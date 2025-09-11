from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID
from enum import Enum as PyEnum

from sqlalchemy import Column, String, DateTime, Date, ForeignKey
from sqlalchemy.sql import func, text
from sqlalchemy.dialects import postgresql
from app.database import Base


# =========================
# Enums (Pydantic / Python)
# =========================
class DocumentType(PyEnum):
    ID = "ID"
    PASSPORT = "PASSPORT"
    DRIVER_LICENSE = "DRIVER_LICENSE"
    OTHER = "OTHER"


# =========================
# SQLAlchemy model (guests)
# =========================
class Guest(Base):
    __tablename__ = "guests"
    __table_args__ = {"extend_existing": True}

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(postgresql.CITEXT, nullable=True, unique=False)
    phone = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    document_kind = Column(
        postgresql.ENUM(DocumentType, name="document_type", create_type=True),
        nullable=True,
    )
    document_no = Column(String, nullable=True)
    user_id = Column(postgresql.UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), unique=True, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    address_line = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(postgresql.UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by = Column(postgresql.UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)


# =========================
# Pydantic models
# =========================
class GuestBase(BaseModel):
    first_name: str = Field(..., min_length=1, description="Nombre(s) del huésped")
    last_name: str = Field(..., min_length=1, description="Apellido(s) del huésped")
    email: Optional[EmailStr] = Field(None, description="Correo electrónico del huésped")
    phone: Optional[str] = Field(None, min_length=5, max_length=30, description="Teléfono del huésped")
    birth_date: Optional[date] = Field(None, description="Fecha de nacimiento")
    document_kind: Optional[DocumentType] = Field(None, description="Tipo de documento")
    document_no: Optional[str] = Field(None, description="Número de documento")
    country: Optional[str] = Field(None, description="País")
    city: Optional[str] = Field(None, description="Ciudad")
    address_line: Optional[str] = Field(None, description="Dirección")


class GuestCreate(GuestBase):
    pass


class GuestUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=5, max_length=30)
    birth_date: Optional[date] = None
    document_kind: Optional[DocumentType] = None
    document_no: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    address_line: Optional[str] = None


class GuestResponse(GuestBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True