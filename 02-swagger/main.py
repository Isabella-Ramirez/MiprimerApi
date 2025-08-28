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
#Ruta para eliminar un usuario

@app.delete(
    "/users/{user_id}",
    summary="Eliminar un usuario",
    description="Se elimina un usuario de la base de datos por Id",
    tags=["Usuarios"],
    responses={
        200: {"description": "Usuario eliminado correctamente"},
        404: {"description": "ID de usuario no se encontró"}
    }
)
def eliminar_usuario(user_id: int):
    for index, usuario_existente in enumerate(user_db):
        if usuario_existente.id == user_id:
            usuario_eliminado = user_db.pop(index)
            return {"mensaje": "Usuario eliminado correctamente", "usuario": usuario_eliminado}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

