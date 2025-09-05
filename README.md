#  Sistema de Reservas de Hotel — FastAPI

> Proyecto base listo para clonar, ejecutar y entregar el **Parcial 1 – Aplicaciones y Servicios Web**.

---

##  Descripción General

API RESTful básica para gestionar un **sistema de reservas de hotel** con tres recursos principales:

* **Rooms (Habitaciones):** estándar, suite y premium, con tarifa por noche.
* **Guests (Huéspedes):** datos de contacto.
* **Reservations (Reservas):** crear (reservar), cancelar y **calcular el costo total** de la estadía.

La API permite **CRUD completo** de los tres recursos, incluye **path parameters**, **query parameters**, **body JSON**, **validaciones**, **códigos HTTP correctos**, autodocumentación con **Swagger (/docs)** y **ReDoc (/redoc)**.

---

##  Estructura del repositorio

```
.
├── 01-apis/
│   └── main.py              # API básica con CRUD
├── 02-swagger/
│   └── main.py              # API con documentación Swagger
├── 03-ReservasHotel/
│   ├── app/
│   │   ├── main.py          # Punto de entrada (orquesta los routers)
│   │   └── models.py        # Modelos (Pydantic y datos en memoria)
│   └── endpoints/
│       ├── rooms.py         # Endpoints de habitaciones
│       ├── guests.py        # Endpoints de huéspedes
│       └── reservations.py  # Endpoints de reservas
├── requirements.txt
└── README.md
```

> **Nota:** Para simplificar la evaluación del parcial, el almacenamiento es **en memoria** (diccionarios). Puedes migrar fácilmente a una base de datos más adelante (SQLModel/SQLAlchemy) manteniendo las rutas.

---

##  Proyectos Incluidos

Este repositorio contiene tres proyectos de ejemplo:

1. **01-apis/**: API básica con operaciones CRUD simples
2. **02-swagger/**: API con documentación automática usando Swagger
3. **03-ReservasHotel/**: Sistema completo de reservas de hotel (proyecto principal)

---

##  Requisitos de Instalación

* **Python** 3.10+
* Dependencias (archivo `requirements.txt`):

```txt
fastapi
uvicorn
pydantic
python-dateutil
```

---

## ▶ Instrucciones de Ejecución

1. Crear y activar un entorno virtual (opcional pero recomendado).
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar el servidor:

```bash
# Para el proyecto de reservas de hotel:
cd 03-ReservasHotel
uvicorn app.main:app --reload

# Para otros ejemplos:
# cd 01-apis && uvicorn main:app --reload
# cd 02-swagger && uvicorn main:app --reload
```

4. Probar documentación automática:

* **Swagger UI:** http://127.0.0.1:8000/docs
* **ReDoc:** http://127.0.0.1:8000/redoc

---

##  Objetivo del proyecto

- Desarrollar un sistema completo de reservas de hotel
- Implementar operaciones CRUD para habitaciones, huéspedes y reservas
- Explorar documentación automática con Swagger
- Usar Pydantic para validación de datos
- Calcular costos totales de estadías

---

##  Autores / Integrantes del Grupo

* Miguel Ángel Lopez Perdomo — miguellopez265477@correo.itm.edu.co
* Isabella Ramirez Ciro — isabellaramirez1116480@correo.itm.edu.co

---
