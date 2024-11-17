from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from fastapi.responses import JSONResponse
from passlib.context import CryptContext

app = FastAPI()

# Base de datos simulada
animales = [
    {"id": 1, "tipo": "Perro", "raza": "Labrador", "edad": 5, "vacunas": ["Rabia", "VIH"], "fotos": ["labrador1.jpg", "labrador2.jpg"]},
    {"id": 2, "tipo": "Gato", "raza": "Siames", "edad": 3, "vacunas": ["Rabia", "VIH"], "fotos": ["siames1.jpg", "siames2.jpg"]},
]

usuarios = []
familias = []  # Añadido para registrar las familias
credenciales = {"admin": "$2b$12$1234567890abcdefghijklmno"}  # Contraseña encriptada ("admin1")

# Configuración para encriptar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Animal(BaseModel):
    id: int
    tipo: str
    raza: str
    edad: int = Field(gt=0, description="Edad debe ser mayor a 0")
    vacunas: List[str]
    fotos: List[str]


class Usuario(BaseModel):
    nombre: str
    direccion: str
    telefono: str = Field(regex=r"^\+?\d{7,15}$", description="Número de teléfono válido con 7 a 15 dígitos")
    email: EmailStr
    composicion_familiar: str
    estilo_de_vida: str


class Familia(BaseModel):
    nombre_familia: str
    miembros: List[str]  # Lista de nombres de miembros de la familia


class Credenciales(BaseModel):
    usuario: str
    contrasena: str


# --- Endpoints de animales ---
@app.get("/animales/", response_model=List[Animal])
def obtener_animales(tipo: Optional[str] = Query(None, description="Filtrar por tipo de animal")):
    if tipo:
        return [animal for animal in animales if animal["tipo"].lower() == tipo.lower()]
    return animales


@app.post("/animales/", status_code=201)
def agregar_animal(animal: Animal):
    if any(a["id"] == animal.id for a in animales):
        raise HTTPException(status_code=400, detail="El ID del animal ya existe")
    animales.append(animal.dict())
    return {"success": True, "mensaje": "Animal agregado exitosamente"}


@app.delete("/animales/{animal_id}")
def eliminar_animal(animal_id: int):
    global animales
    animales_filtrados = [animal for animal in animales if animal["id"] != animal_id]
    if len(animales_filtrados) == len(animales):
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    animales = animales_filtrados
    return {"success": True, "mensaje": "Animal eliminado exitosamente"}


# --- Endpoints de usuarios y familias ---
@app.post("/registrar/", status_code=201)
def registrar_usuario(usuario: Usuario):
    if any(u.email == usuario.email for u in usuarios):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    usuarios.append(usuario)
    return {"success": True, "mensaje": "Usuario registrado exitosamente"}


@app.get("/usuarios/", response_model=List[Usuario])
def obtener_usuarios():
    return usuarios


@app.post("/iniciar_sesion/")
def iniciar_sesion(credenciales: Credenciales):
    contrasena_encriptada = credenciales.get(credenciales.usuario)
    if not contrasena_encriptada or not pwd_context.verify(credenciales.contrasena, contrasena_encriptada):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return {"success": True, "mensaje": "Inicio de sesión exitoso", "rol": "admin" if credenciales.usuario == "admin" else "usuario"}


# --- Endpoints de familias ---
@app.post("/familias/", status_code=201)
def registrar_familia(familia: Familia):
    familias.append(familia.dict())
    return {"success": True, "mensaje": "Familia registrada exitosamente"}


@app.get("/familias/", response_model=List[Familia])
def obtener_familias():
    return familias


@app.post("/asignar_animal/")
def asignar_animal_a_familia(animal_id: int, familia_nombre: str):
    animal = next((a for a in animales if a["id"] == animal_id), None)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")

    familia = next((f for f in familias if f["nombre_familia"] == familia_nombre), None)
    if not familia:
        raise HTTPException(status_code=404, detail="Familia no encontrada")

    animal["familia_asignada"] = familia_nombre
    return {"success": True, "mensaje": f"Animal {animal_id} asignado a la familia {familia_nombre}"}
