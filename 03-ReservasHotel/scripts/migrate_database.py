"""Script de migración: crea tablas si faltan e inserta datos de ejemplo."""

from datetime import date
from sqlalchemy import inspect
from app.database import engine, SessionLocal, Base


def run_migration():
    """Ejecuta la migración y carga de datos de ejemplo de forma idempotente."""
    try:
        print("Iniciando migración de base de datos...")

        from app.models.guest import Guest
        from app.models.room import Room
        from app.models.reservation import Reservation

        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        if not all(table in existing_tables for table in ['guests', 'rooms', 'reservations']):
            print("Creando tablas faltantes...")
            Base.metadata.create_all(bind=engine)
            print("Tablas creadas.")
        else:
            print("Las tablas ya existen.")

        db = SessionLocal()
        try:
            if db.query(Guest).count() == 0:
                print("Insertando datos de prueba...")

                guests = [
                    Guest(name="Juan Pérez", email="juan.perez@email.com", phone="1234567890"),
                    Guest(name="María García", email="maria.garcia@email.com", phone="0987654321"),
                    Guest(name="Carlos López", email="carlos.lopez@email.com", phone="1122334455"),
                    Guest(name="Ana Martínez", email="ana.martinez@email.com", phone="5566778899"),
                ]
                db.add_all(guests)
                db.commit()

                rooms = [
                    Room(room_number="101", room_type="Single", price_per_night=50.00, is_available=True),
                    Room(room_number="102", room_type="Single", price_per_night=50.00, is_available=True),
                    Room(room_number="201", room_type="Double", price_per_night=80.00, is_available=True),
                    Room(room_number="202", room_type="Double", price_per_night=80.00, is_available=False),
                    Room(room_number="301", room_type="Suite", price_per_night=150.00, is_available=True),
                    Room(room_number="302", room_type="Suite", price_per_night=150.00, is_available=True),
                ]
                db.add_all(rooms)
                db.commit()

                from app.models.reservation import ReservationStatus
                reservations = [
                    Reservation(
                        guest_id=1,
                        room_id=1,
                        check_in_date=date(2024, 12, 1),
                        check_out_date=date(2024, 12, 3),
                        total_amount=100.00,
                        status=ReservationStatus.CONFIRMED,
                    ),
                    Reservation(
                        guest_id=2,
                        room_id=3,
                        check_in_date=date(2024, 12, 5),
                        check_out_date=date(2024, 12, 7),
                        total_amount=160.00,
                        status=ReservationStatus.CONFIRMED,
                    ),
                    Reservation(
                        guest_id=3,
                        room_id=5,
                        check_in_date=date(2024, 12, 10),
                        check_out_date=date(2024, 12, 12),
                        total_amount=300.00,
                        status=ReservationStatus.CONFIRMED,
                    ),
                    Reservation(
                        guest_id=4,
                        room_id=2,
                        check_in_date=date(2024, 12, 15),
                        check_out_date=date(2024, 12, 17),
                        total_amount=100.00,
                        status=ReservationStatus.PENDING,
                    ),
                ]
                db.add_all(reservations)
                db.commit()
                print("Datos de prueba insertados.")
            else:
                print("Datos de prueba ya existen.")

        except Exception as e:
            print(f"Error insertando datos: {e}")
            db.rollback()
            raise
        finally:
            db.close()

        print("Migración completada exitosamente.")

    except Exception as e:
        print(f"Error en la migración: {e}")
        raise
