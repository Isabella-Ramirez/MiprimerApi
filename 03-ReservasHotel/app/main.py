from fastapi import FastAPI
from app.database import test_connection
from app.endpoints import guests, rooms, reservations
from scripts.migrate_database import auto_setup_database

app = FastAPI(
    title="Hotel Reservations API",
    description="API para manejar reservas de hotel.",
    version="1.0.0"
)



app.include_router(guests.router)
app.include_router(rooms.router)
app.include_router(reservations.router)


@app.on_event("startup")
async def startup():
    try:
        if test_connection():
            print("Conexión a la base de datos verificada.")
            auto_setup_database()
    except Exception as e:
        print(f"Error durante el inicio: {e}")
        
@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de Reservas de Hotel. Visita /docs para ver la documentación.",
        "endpoints": ["/guests", "/rooms", "/reservations"]
    }