from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.room import Room, RoomCreate, RoomUpdate, RoomResponse
from app.models.reservation import Reservation, ReservationStatus

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)

# Crear habitación
@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    # Validar que no se repita el número de habitación
    existing = db.query(Room).filter(Room.room_number == room.room_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="El número de habitación ya existe")

    new_room = Room(**room.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


# Listar habitaciones con filtro opcional (Query Parameters)
@router.get("/", response_model=list[RoomResponse])
def get_rooms(
    available: bool | None = Query(None, description="Filtrar por disponibilidad"),
    room_type: str | None = Query(None, description="Filtrar por tipo de habitación"),
    db: Session = Depends(get_db)
):
    query = db.query(Room)
    if available is not None:
        query = query.filter(Room.is_available == available)
    if room_type:
        query = query.filter(Room.room_type.ilike(f"%{room_type}%"))

    return query.all()


# Obtener habitación por ID (Path Parameter)
@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    return room


# Actualizar habitación
@router.put("/{room_id}", response_model=RoomResponse)
def update_room(room_id: int, room_update: RoomUpdate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")

    for key, value in room_update.dict(exclude_unset=True).items():
        setattr(room, key, value)

    db.commit()
    db.refresh(room)
    return room


# Eliminar habitación
@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")

    reservation = db.query(Reservation).filter(Reservation.room_id == room_id, Reservation.status != ReservationStatus.CANCELLED, Reservation.status != ReservationStatus.COMPLETED).first()
    
    if reservation:
        raise HTTPException(status_code=400, detail="No se puede eliminar la habitación con reservas activas")

    db.delete(room)
    db.commit()
    return JSONResponse(content={
        "detail": "Habitación eliminada correctamente"
    })
