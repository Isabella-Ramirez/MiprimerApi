from pathlib import Path
from alembic.config import Config
from alembic import command
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from app.database import SessionLocal, engine
from app.models.room import RoomType, Room, RoomStatus
from app.models.guest import Guest
from app.models.rbac import User, Role


def _get_alembic_config() -> Config:
    """Obtiene la configuración de Alembic usando el alembic.ini del proyecto."""
    project_root = Path(__file__).resolve().parents[1]  # 03-ReservasHotel/
    alembic_ini = project_root / "alembic.ini"
    cfg = Config(str(alembic_ini))
    # sqlalchemy.url se toma de env:DATABASE_URL según alembic.ini
    return cfg


def check_migrations_needed() -> bool:
    """Verifica si hay migraciones pendientes."""
    try:
        cfg = _get_alembic_config()
        script = ScriptDirectory.from_config(cfg)
        
        with engine.connect() as connection:
            context = MigrationContext.configure(connection)
            current_head = context.get_current_revision()
            script_head = script.get_current_head()
            
            # Si current_head es None, significa que no se han ejecutado migraciones
            if current_head is None:
                return True
            
            # Si son iguales, no hay migraciones pendientes
            return current_head != script_head
            
    except Exception:
        # Si hay error, asumir que necesita migraciones
        return True


def has_sample_data() -> bool:
    """Verifica si ya existen datos de ejemplo en la base de datos."""
    db = SessionLocal()
    try:
        return (db.query(Role).count() > 0 and 
                db.query(User).count() > 0 and 
                db.query(RoomType).count() > 0)
    except Exception:
        return False
    finally:
        db.close()


def run_migration(target: str = "head") -> None:
    """Aplica migraciones con Alembic hasta el target indicado (por defecto 'head')."""
    cfg = _get_alembic_config()
    print(f"Aplicando migraciones hasta: {target}...")
    command.upgrade(cfg, target)
    print("Migraciones aplicadas.")


def auto_setup_database() -> None:
    """Configura automáticamente la base de datos: ejecuta migraciones y seed si es necesario."""
    # Verificar si hay migraciones pendientes
    if check_migrations_needed():
        print("Migraciones pendientes detectadas. Ejecutando migraciones...")
        run_migration()
    else:
        print("Base de datos actualizada.")
    
    # Verificar si hay datos de ejemplo
    if not has_sample_data():
        print("No se encontraron datos de ejemplo. Ejecutando seed...")
        seed_sample_data()
    else:
        print("Datos de ejemplo ya existen.")


def rollback_migration(target: str = "-1") -> None:
    """Revierte migraciones (por defecto un paso)."""
    cfg = _get_alembic_config()
    print(f"Revirtiendo migraciones hasta: {target}...")
    command.downgrade(cfg, target)
    print("Migraciones revertidas.")


def seed_sample_data() -> None:
    """Inserta datos de ejemplo en el orden correcto: roles, users, room_types, rooms, guests."""
    db = SessionLocal()
    try:
        print("Iniciando seed de datos de ejemplo...")
        
        # 1. Crear roles primero
        if db.query(Role).count() == 0:
            roles = [
                Role(code="ADMIN", name="Administrador"),
                Role(code="RECEPTIONIST", name="Recepcionista"),
                Role(code="GUEST", name="Huésped")
            ]
            db.add_all(roles)
            db.flush()
            print(f"Creados {len(roles)} roles")

        # 2. Crear usuarios básicos
        if db.query(User).count() == 0:
            # Obtener roles para asignar
            admin_role = db.query(Role).filter(Role.code == "ADMIN").first()
            receptionist_role = db.query(Role).filter(Role.code == "RECEPTIONIST").first()
            
            users = [
                User(
                    email="admin@hotel.com",
                    password_hash="$2b$12$dummy.hash.for.testing.purposes.only",
                    full_name="Administrador Sistema",
                    role_id=admin_role.id,
                    is_active=True
                ),
                User(
                    email="recepcion@hotel.com", 
                    password_hash="$2b$12$dummy.hash.for.testing.purposes.only",
                    full_name="Personal Recepción",
                    role_id=receptionist_role.id,
                    is_active=True
                )
            ]
            db.add_all(users)
            db.flush()
            print(f"Creados {len(users)} usuarios")

        # 3. Crear tipos de habitación
        if db.query(RoomType).count() == 0:
            room_types = [
                RoomType(
                    code="STD-KING", 
                    name="Standard King", 
                    description="Habitación estándar con cama king size",
                    capacity_adults=2, 
                    capacity_children=1, 
                    base_rate=80.00
                ),
                RoomType(
                    code="DLX-QUEEN", 
                    name="Deluxe Queen", 
                    description="Habitación deluxe con cama queen size",
                    capacity_adults=2, 
                    capacity_children=2, 
                    base_rate=120.00
                ),
                RoomType(
                    code="SUITE", 
                    name="Suite Ejecutiva", 
                    description="Suite ejecutiva con sala de estar",
                    capacity_adults=4, 
                    capacity_children=2, 
                    base_rate=200.00
                )
            ]
            db.add_all(room_types)
            db.flush()
            print(f"Creados {len(room_types)} tipos de habitación")

        # 4. Crear habitaciones
        if db.query(Room).count() == 0:
            # Obtener los tipos de habitación para asignar
            std_type = db.query(RoomType).filter(RoomType.code == "STD-KING").first()
            dlx_type = db.query(RoomType).filter(RoomType.code == "DLX-QUEEN").first()
            suite_type = db.query(RoomType).filter(RoomType.code == "SUITE").first()
            
            rooms = [
                # Piso 1 - Standard
                Room(room_number="101", floor="1", room_type_id=std_type.id, status=RoomStatus.AVAILABLE),
                Room(room_number="102", floor="1", room_type_id=std_type.id, status=RoomStatus.AVAILABLE),
                Room(room_number="103", floor="1", room_type_id=std_type.id, status=RoomStatus.CLEANING),
                
                # Piso 2 - Deluxe
                Room(room_number="201", floor="2", room_type_id=dlx_type.id, status=RoomStatus.AVAILABLE),
                Room(room_number="202", floor="2", room_type_id=dlx_type.id, status=RoomStatus.AVAILABLE),
                Room(room_number="203", floor="2", room_type_id=dlx_type.id, status=RoomStatus.OCCUPIED),
                
                # Piso 3 - Suites
                Room(room_number="301", floor="3", room_type_id=suite_type.id, status=RoomStatus.AVAILABLE),
                Room(room_number="302", floor="3", room_type_id=suite_type.id, status=RoomStatus.OUT_OF_SERVICE),
            ]
            db.add_all(rooms)
            db.flush()
            print(f"Creadas {len(rooms)} habitaciones")

        # 5. Crear huéspedes
        if db.query(Guest).count() == 0:
            guests = [
                Guest(
                    first_name="Juan Carlos",
                    last_name="Pérez González",
                    email="juan.perez@example.com",
                    phone="+1-555-0101",
                    country="España",
                    city="Madrid"
                ),
                Guest(
                    first_name="María Elena",
                    last_name="García Rodríguez",
                    email="maria.garcia@example.com",
                    phone="+1-555-0102",
                    country="México",
                    city="Ciudad de México"
                ),
                Guest(
                    first_name="Ana Sofía",
                    last_name="Martínez López",
                    email="ana.martinez@example.com",
                    phone="+1-555-0103",
                    country="Colombia",
                    city="Bogotá"
                ),
                Guest(
                    first_name="Carlos Alberto",
                    last_name="Ruiz Hernández",
                    email="carlos.ruiz@example.com",
                    phone="+1-555-0104",
                    country="Argentina",
                    city="Buenos Aires"
                ),
                Guest(
                    first_name="Laura Patricia",
                    last_name="Sánchez Vargas",
                    phone="+1-555-0105",
                    country="Chile",
                    city="Santiago"
                )
            ]
            db.add_all(guests)
            db.flush()
            print(f"Creados {len(guests)} huéspedes")

        # Confirmar todos los cambios
        db.commit()
        print("Seed de datos completado exitosamente")
        
    except Exception as e:
        db.rollback()
        print(f"Error en seed: {e}")
        raise
    finally:
        db.close()
