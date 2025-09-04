from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """Función simple para probar la conexión a la base de datos."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Conexión a la base de datos exitosa.")
        return True
    except Exception as e:
        print(f"Error de conexión a la base de datos: {e}")
        return False