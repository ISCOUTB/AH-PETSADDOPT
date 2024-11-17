from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Datos primarios para el ejemplo
animales = [
    {"id": 1, "tipo": "Perro", "raza": "Labrador", "edad": 5, "vacunas": ["Rabia", "VIH"], "fotos": ["labrador1.jpg", "labrador2.jpg"]},
    {"id": 2, "tipo": "Gato", "raza": "Siames", "edad": 3, "vacunas": ["Rabia", "VIH"], "fotos": ["siames1.jpg", "siames2.jpg"]},
]

usuarios = []
credenciales = {"admin": "admin1"}

class Animal(BaseModel):
    id: int
    tipo: str
    raza: str
    edad: int
    vacunas: List[str]
    fotos: List[str]

class Usuario(BaseModel):
    nombre: str
    direccion: str
    telefono: str
    email: str
    composicion_familiar: str
    estilo_de_vida: str

@app.get("/animales/", response_model=List[Animal])
def obtener_animales():
    return animales

@app.post("/registrar/")
def registrar_usuario(usuario: Usuario):
    usuarios.append(usuario)
    return {"mensaje": "Usuario registrado exitosamente"}

@app.post("/iniciar_sesion/")
def iniciar_sesion(usuario: str, contrasena: str):
    if credenciales.get(usuario) == contrasena:
        return {"mensaje": "Inicio de sesión exitoso", "rol": "admin" if usuario == "admin" else "usuario"}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")

@app.post("/animales/")
def agregar_animal(animal: Animal):
    if any(a["id"] == animal.id for a in animales):
        raise HTTPException(status_code=400, detail="El ID del animal ya existe")
    animales.append(animal.dict())
    return {"mensaje": "Animal agregado exitosamente"}
