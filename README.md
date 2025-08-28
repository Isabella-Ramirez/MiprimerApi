# 🚀 Mi Primeras APIs con FastAPI

Este repositorio contiene dos proyectos de ejemplo desarrollados con **FastAPI** para aprender a crear, documentar y probar APIs REST.

---

## 📂 Estructura del repositorio

.
├── 01-apis        
│   └── main.py
├── 02-swagger     
│   └── main.py
├── .gitignore
└── README.md

---

## ⚡ Requisitos

- Python 3.8+
- FastAPI
- Uvicorn

Instala dependencias con:

pip install fastapi uvicorn

---

## 📌 01-apis

API básica con rutas CRUD (Create, Read, Update, Delete).  

### ▶️ Ejecución

uvicorn main:app --reload

### 📍 Endpoints

- GET / → Devuelve mensaje **Hello World**  
- GET /saludo/{nombre} → Devuelve un saludo personalizado  
- POST / → Crea un nuevo item en memoria  
- PUT /{item_id} → Actualiza un item por ID  
- DELETE /{item_id} → Elimina un item por ID  

Ejemplo de petición POST:

{
  "nombre": "Ejemplo",
  "valor": 123
}

---

## 📌 02-swagger

API más avanzada con validaciones usando **Pydantic** y documentación automática con **Swagger**.

### ▶️ Ejecución

uvicorn main:app --reload

### 📍 Endpoints

- GET /users → Lista todos los usuarios  
- POST /users → Crea un nuevo usuario  
- PUT /users/{user_id} → Actualiza un usuario existente  
- DELETE /users/{user_id} → Elimina un usuario por ID  

Modelo de usuario:

{
  "id": 1,
  "name": "Miguel Lopez",
  "email": "miguel.lopez@gmail.com"
}

### 📖 Documentación automática

Al ejecutar el servidor puedes acceder a:

- Swagger UI → http://127.0.0.1:8000/docs  
- ReDoc → http://127.0.0.1:8000/redoc  

---

## 🎯 Objetivo del repositorio

- Practicar creación de APIs con FastAPI  
- Implementar operaciones CRUD  
- Explorar documentación automática con Swagger  
- Usar Pydantic para validación de datos  

---



