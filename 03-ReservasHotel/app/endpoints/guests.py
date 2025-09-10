"""Endpoints de gestión de huéspedes."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.guest import Guest, GuestCreate, GuestUpdate, GuestResponse
from app.models.reservation import Reservation, ReservationStatus

router = APIRouter(
    prefix="/guests",
    tags=["Guests"]
)


@router.post("/", response_model=GuestResponse, status_code=status.HTTP_201_CREATED)
def create_guest(guest: GuestCreate, db: Session = Depends(get_db)):
    """Crea un nuevo huésped si el correo no está registrado."""
    existing = db.query(Guest).filter(Guest.email == guest.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    new_guest = Guest(**guest.dict())
    db.add(new_guest)
    db.commit()
    db.refresh(new_guest)
    return new_guest


@router.get("/", response_model=list[GuestResponse])
def get_all_guests(db: Session = Depends(get_db)):
    """Devuelve la lista completa de huéspedes."""
    guests = db.query(Guest).all()
    return guests


@router.get("/{guest_id}", response_model=GuestResponse)
def get_guest(guest_id: int, db: Session = Depends(get_db)):
    """Obtiene un huésped por su identificador."""
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Huésped no encontrado")
    return guest


@router.put("/{guest_id}", response_model=GuestResponse)
def update_guest(guest_id: int, guest_update: GuestUpdate, db: Session = Depends(get_db)):
    """Actualiza los datos de un huésped existente."""
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Huésped no encontrado")

    for key, value in guest_update.dict(exclude_unset=True).items():
        setattr(guest, key, value)

    db.commit()
    db.refresh(guest)
    return guest


@router.delete("/{guest_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_guest(guest_id: int, db: Session = Depends(get_db)):
    """Elimina un huésped si no tiene reservas activas."""
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Huésped no encontrado")

    reservation = db.query(Reservation).filter(
        Reservation.guest_id == guest_id,
        Reservation.status != ReservationStatus.CANCELLED,
        Reservation.status != ReservationStatus.COMPLETED,
    ).first()

    if reservation:
        raise HTTPException(status_code=400, detail="No se puede eliminar el huésped con reservas activas")

    db.delete(guest)
    db.commit()
    return JSONResponse(content={"detail": "Huésped eliminado correctamente"})
