from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func, text
from enum import Enum as PyEnum
from app.database import Base


class RoomStatus(PyEnum):
    AVAILABLE = "AVAILABLE"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"
    CLEANING = "CLEANING"
    OCCUPIED = "OCCUPIED"


class RoomType(Base):
    __tablename__ = "room_types"
    __table_args__ = {"extend_existing": True}

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    capacity_adults = Column(postgresql.SMALLINT, nullable=False)
    capacity_children = Column(postgresql.SMALLINT, nullable=False)
    base_rate = Column(postgresql.NUMERIC(12, 2), nullable=False, server_default=text("0.00"))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(postgresql.UUID(as_uuid=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by = Column(postgresql.UUID(as_uuid=True), nullable=True)


class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = {"extend_existing": True}

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    room_number = Column(String, unique=True, nullable=False)
    floor = Column(String, nullable=True)
    room_type_id = Column(postgresql.UUID(as_uuid=True), ForeignKey("room_types.id", ondelete="RESTRICT"), nullable=False)
    status = Column(
        postgresql.ENUM(RoomStatus, name="room_status", create_type=False),
        nullable=False,
        server_default=RoomStatus.AVAILABLE.value,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(postgresql.UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_by = Column(postgresql.UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)


# Pydantic models
class RoomTypeBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    capacity_adults: int
    capacity_children: int
    base_rate: float


class RoomTypeCreate(RoomTypeBase):
    pass


class RoomTypeUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    capacity_adults: Optional[int] = None
    capacity_children: Optional[int] = None
    base_rate: Optional[float] = None


class RoomTypeResponse(RoomTypeBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RoomBase(BaseModel):
    room_number: str
    floor: Optional[str] = None
    room_type_id: UUID
    status: RoomStatus = RoomStatus.AVAILABLE


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    room_number: Optional[str] = None
    floor: Optional[str] = None
    room_type_id: Optional[int] = None
    status: Optional[RoomStatus] = None


class RoomResponse(RoomBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True