from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Definición del modelo Animal
class Animal(BaseModel):
    id: int
    tipo: str
    raza: str
    edad: int
    vacunas: List[str] = []

# Simulando una base de datos de usuarios
usuarios_db = {
    "admin": {"contraseña": "admin123", "rol": "admin"},
    "cliente": {"contraseña": "cliente123", "rol": "usuario"},
}

animales_db = []

# Ruta para iniciar sesión
@app.post("/iniciar_sesion/")
def iniciar_sesion(usuario: str, contrasena: str):
    user = usuarios_db.get(usuario)
    if user and user["contraseña"] == contrasena:
        return {"rol": user["rol"]}
    else:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

# Rutas para manejar los animales
@app.get("/animales/")
def obtener_animales():
    return animales_db

@app.post("/animales/")
def agregar_animal(animal: Animal):
    animal.id = len(animales_db) + 1
    animales_db.append(animal.dict())
    return {"message": "Animal agregado exitosamente"}

@app.delete("/animales/{animal_id}")
def eliminar_animal(animal_id: int):
    global animales_db
    animales_db = [animal for animal in animales_db if animal["id"] != animal_id]
    return {"message": "Animal eliminado exitosamente"}


