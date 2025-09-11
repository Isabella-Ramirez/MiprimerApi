from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, date
from uuid import UUID
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Date,
    Numeric,
    ForeignKey,
    Boolean,
    SmallInteger,
    CheckConstraint,
)
from sqlalchemy.sql import func, text
from sqlalchemy.dialects import postgresql
from app.database import Base


# =========================
# Enums (Python + PostgreSQL)
# =========================
class ReservationStatus(PyEnum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"


class PaymentStatus(PyEnum):
    PENDING = "PENDING"
    PAID = "PAID"
    REFUNDED = "REFUNDED"
    FAILED = "FAILED"


# =========================
# SQLAlchemy models
# =========================
class Reservation(Base):
    __tablename__ = "reservations"
    __table_args__ = (
        CheckConstraint("checkout_date > checkin_date", name="chk_res_dates"),
        {"extend_existing": True},
    )

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    code = Column(String, unique=True, nullable=False)
    status = Column(
        postgresql.ENUM(ReservationStatus, name="reservation_status", create_type=True),
        nullable=False,
        server_default=ReservationStatus.PENDING.value,
    )
    checkin_date = Column(Date, nullable=False)
    checkout_date = Column(Date, nullable=False)
    channel = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(postgresql.UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by = Column(postgresql.UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)


class ReservationGuest(Base):
    __tablename__ = "reservation_guests"
    __table_args__ = {"extend_existing": True}

    reservation_id = Column(postgresql.UUID(as_uuid=True), ForeignKey("reservations.id", ondelete="CASCADE"), primary_key=True)
    guest_id = Column(postgresql.UUID(as_uuid=True), ForeignKey("guests.id", ondelete="RESTRICT"), primary_key=True)
    is_primary = Column(Boolean, nullable=False, server_default=text("false"))


class ReservationRoom(Base):
    __tablename__ = "reservation_rooms"
    __table_args__ = (
        CheckConstraint("end_date > start_date", name="chk_rr_dates"),
        {"extend_existing": True},
    )

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    reservation_id = Column(postgresql.UUID(as_uuid=True), ForeignKey("reservations.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(postgresql.UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True)
    room_type_id = Column(postgresql.UUID(as_uuid=True), ForeignKey("room_types.id", ondelete="RESTRICT"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    nightly_rate = Column(Numeric(12, 2), nullable=False, server_default=text("0.00"))
    adults = Column(SmallInteger, nullable=False, server_default=text("1"))
    children = Column(SmallInteger, nullable=False, server_default=text("0"))
    notes = Column(String, nullable=True)


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = {"extend_existing": True}

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    reservation_id = Column(postgresql.UUID(as_uuid=True), ForeignKey("reservations.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), nullable=False, server_default=text("'USD'"))
    method = Column(String, nullable=False)
    status = Column(
        postgresql.ENUM(PaymentStatus, name="payment_status", create_type=True),
        nullable=False,
        server_default=PaymentStatus.PENDING.value,
    )
    paid_at = Column(DateTime(timezone=True), nullable=True)
    reference = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(postgresql.UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by = Column(postgresql.UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)


# =========================
# Pydantic models
# =========================
class ReservationBase(BaseModel):
    code: str = Field(..., description="Localizador/PNR único")
    checkin_date: date = Field(..., description="Fecha de entrada")
    checkout_date: date = Field(..., description="Fecha de salida")
    channel: Optional[str] = Field(None, description="Canal de reserva")
    notes: Optional[str] = Field(None, description="Notas")

    @validator("checkout_date")
    def _validate_dates(cls, v, values):
        if "checkin_date" in values and v <= values["checkin_date"]:
            raise ValueError("La fecha de salida debe ser posterior a la fecha de entrada")
        return v


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(BaseModel):
    code: Optional[str] = None
    checkin_date: Optional[date] = None
    checkout_date: Optional[date] = None
    channel: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[ReservationStatus] = None


class ReservationResponse(ReservationBase):
    id: UUID
    status: ReservationStatus = ReservationStatus.PENDING
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True