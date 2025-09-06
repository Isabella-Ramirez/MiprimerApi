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

itemList = []

@app.post("/")
def create_item(item: dict):
    itemList.append(item)
    return item

@app.put("/{item_id}")
def update_item(item_id: int, item: dict):
    if item_id < 0 or item_id >= len(itemList):
        return {"error": "Item no encontrado"}
    itemList[item_id] = item
    return item

@app.delete("/{item_id}")
def delete_item(item_id: int):
    if item_id < 0 or item_id >= len(itemList):
        return {"error": "Item no encontrado"}
    deleted_item = itemList.pop(item_id)
    return {"message": "Item eliminado", "item": deleted_item}