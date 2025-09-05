from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.reservation import Reservation, ReservationCreate, ReservationUpdate, ReservationResponse, ReservationStatus
from app.models.room import Room
from app.models.guest import Guest

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)

# Crear reserva
@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    # Validar huésped
    guest = db.query(Guest).filter(Guest.id == reservation.guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Huésped no encontrado")

    # Validar habitación
    room = db.query(Room).filter(Room.id == reservation.room_id, Room.is_available == True).first()
    if not room:
        raise HTTPException(status_code=400, detail="Habitación no disponible")

    # Calcular costo total automáticamente
    nights = (reservation.check_out_date - reservation.check_in_date).days
    if nights <= 0:
        raise HTTPException(status_code=400, detail="Las fechas de reserva no son válidas")

    total = nights * float(room.price_per_night)

    new_reservation = Reservation(
        guest_id=reservation.guest_id,
        room_id=reservation.room_id,
        check_in_date=reservation.check_in_date,
        check_out_date=reservation.check_out_date,
        total_amount=total,
        status=ReservationStatus.CONFIRMED
    )

    # Marcar habitación como no disponible
    room.is_available = False

    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)

    return new_reservation


# Listar reservas
@router.get("/", response_model=list[ReservationResponse])
def get_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).all()


# Obtener reserva por ID
@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reservation


# Cancelar reserva (cambiar estado a CANCELLED y liberar habitación)
@router.put("/{reservation_id}/cancel", response_model=ReservationResponse)
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    if reservation.status == ReservationStatus.CANCELLED:
        raise HTTPException(status_code=400, detail="La reserva ya está cancelada")

    reservation.status = ReservationStatus.CANCELLED

    # Liberar la habitación
    room = db.query(Room).filter(Room.id == reservation.room_id).first()
    if room:
        room.is_available = True

    db.commit()
    db.refresh(reservation)
    return reservation


# Actualizar reserva (ejemplo: cambiar fechas)
@router.put("/{reservation_id}", response_model=ReservationResponse)
def update_reservation(reservation_id: int, reservation_update: ReservationUpdate, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    for key, value in reservation_update.dict(exclude_unset=True).items():
        setattr(reservation, key, value)

    # Recalcular total si cambian fechas
    if reservation.check_in_date and reservation.check_out_date:
        nights = (reservation.check_out_date - reservation.check_in_date).days
        if nights <= 0:
            raise HTTPException(status_code=400, detail="Las fechas de reserva no son válidas")
        room = db.query(Room).filter(Room.id == reservation.room_id).first()
        if room:
            reservation.total_amount = nights * float(room.price_per_night)

    db.commit()
    db.refresh(reservation)
    return reservation


# Eliminar reserva
@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    # Liberar habitación si estaba confirmada
    if reservation.status == ReservationStatus.CONFIRMED:
        room = db.query(Room).filter(Room.id == reservation.room_id).first()
        if room:
            room.is_available = True

    db.delete(reservation)
    db.commit()
    return None
