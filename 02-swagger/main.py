from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="Api de ejemplo para documentacion",
              description="Esta es una API de ejemplo para demostrar la documentacion con Swagger",
              version="1.0.0")

class User(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="Miguel Lopez")
    email: str = Field(..., example="miguel.lopez@gmail.com")

user_db: List[User] = [
    User(id=1, name="Miguel Lopez", email="miguel.lopez@gmail.com")
]

#Ruta raiz
@app.get(
    "/users",
    response_model=List[User],
    summary="Obtener todos los usuarios",
    description="Esta ruta obtiene todos los usuarios almacenados en la base de datos",
    tags=["Usuarios"],
    responses={
        200: {
            "description": "Lista de usuarios obtenida exitosamente."
        }
    }
)
def get_users() -> List[User]:
    return user_db

#Ruta para crear un usuario
@app.post(
    "/users",
    status_code=201,
    summary="Crear un nuevo usuario",
    description="Esta ruta crea un nuevo usuario y lo almacena en la base de datos",
    tags=["Usuarios"],
    responses={
        201: {
            "description": "Usuario creado exitosamente."
        },
        400: {
            "description": "Error en la solicitud. Datos inválidos."
        }
    }
)

def create_user(user: User) -> User:
    for existing_user in user_db:
        if existing_user.id == user.id:
            raise HTTPException(status_code=400, detail="El usuario con este ID ya existe.")
    user_db.append(user)
    return user


@app.put(
    "/users/{user_id}",
    response_model=User,
    summary="Actualizar un usuario existente",
    description="Esta ruta actualiza los datos de un usuario existente en la base de datos",
    tags=["Usuarios"],
    responses={
        200: {
            "description": "Usuario actualizado exitosamente."
        },
        404: {
            "description": "Usuario no encontrado."
        }
    }
)
def update_user(user_id: int, update_user: User) -> User:
    for index, existing_user in enumerate(user_db):
        if existing_user.id == user_id:
            user_db[index] = update_user
            return update_user
    raise HTTPException(status_code=404, detail="Usuario no encontrado.")