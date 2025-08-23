from fastapi import FastAPI
app = FastAPI()

#Ruta raiz
@app.get("/")
def read_root():
    return {"message": "Hello World"}

#Ruta para obtener un saludo personalizado
@app.get("/saludo/{nombre}")
def saludo(nombre: str):
    return {"message": f"Hola {nombre}"}

