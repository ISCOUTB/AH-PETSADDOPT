import psycopg2
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import bcrypt

# Configuración de conexión a la base de datos PostgreSQL
DATABASE_URL = "postgresql://base1:123456@db:5432/Centro_animals" 

# Crear la instancia de la API
app = FastAPI()

# Definición del modelo Pydantic para los animales
class Animal(BaseModel):
    tipo: str
    raza: str
    edad: int
    vacunas: List[str] = []

# Definición del modelo Pydantic para el usuario (login)
class Usuario(BaseModel):
    usuario: str
    contrasena: str

# Definición del modelo Pydantic para el usuario con rol
class UsuarioConRol(BaseModel):
    usuario: str
    rol: str

# Definición del modelo Pydantic para crear un usuario
class UsuarioCreate(BaseModel):
    usuario: str
    contrasena: str
    rol: str  # El rol puede ser 'admin' o 'usuario'

# Función para obtener la conexión a la base de datos
def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Función para ejecutar una consulta SQL
def execute_query(query: str, params=None):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
    finally:
        cursor.close()
        conn.close()

# Función para obtener los animales
def fetch_animals():
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM animales")
        animals = cursor.fetchall()
        return animals
    finally:
        cursor.close()
        conn.close()

# Función para verificar las credenciales de usuario y obtener el rol
def verify_user_credentials(usuario: str, contrasena: str):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT contrasena, rol FROM usuarios WHERE usuario = %s", (usuario,))
        user = cursor.fetchone()
        if user:
            hashed_password, rol = user
            if bcrypt.checkpw(contrasena.encode('utf-8'), hashed_password.encode('utf-8')):
                return rol
        return None
    finally:
        cursor.close()
        conn.close()

# Crear las tablas necesarias si no existen
def create_tables():
    # Crear tabla de usuarios
    query_usuarios = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        usuario VARCHAR(100) UNIQUE NOT NULL,
        contrasena VARCHAR(255) NOT NULL,
        rol VARCHAR(50) NOT NULL
    );
    """
    execute_query(query_usuarios)

    # Crear tabla de animales
    query_animales = """
    CREATE TABLE IF NOT EXISTS animales (
        id SERIAL PRIMARY KEY,
        tipo VARCHAR(100),
        raza VARCHAR(100),
        edad INT,
        vacunas TEXT[]
    );
    """
    execute_query(query_animales)

# Llamar a create_tables para asegurarse de que las tablas existan
create_tables()

# Función para verificar si el usuario es administrador
def is_admin(usuario: str):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT rol FROM usuarios WHERE usuario = %s", (usuario,))
        user = cursor.fetchone()
        if user and user[0] == 'admin':
            return True
        return False
    finally:
        cursor.close()
        conn.close()

# Rutas de la API

# Ruta para obtener todos los animales
@app.get("/animales/", response_model=List[Animal])
def obtener_animales():
    animals = fetch_animals()
    return [
        Animal(tipo=animal[1], raza=animal[2], edad=animal[3], vacunas=animal[4])
        for animal in animals
    ]

# Ruta para eliminar un animal por su ID
@app.delete("/animales/eliminar/{animal_id}", response_model=Animal)
def eliminar_animal(animal_id: int):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM animales WHERE id = %s", (animal_id,))
        animal = cursor.fetchone()
        if not animal:
            raise HTTPException(status_code=404, detail="Animal no encontrado")
        
        query = "DELETE FROM animales WHERE id = %s"
        cursor.execute(query, (animal_id,))
        conn.commit()
        return {"id": animal[0], "tipo": animal[1], "raza": animal[2], "edad": animal[3], "vacunas": animal[4]}
    finally:
        cursor.close()
        conn.close()

# Ruta para registrar un nuevo usuario (solo administrador)
@app.post("/usuarios/")
def crear_usuario(usuario_create: UsuarioCreate):
    
    conn = get_db()
    cursor = conn.cursor()
    try:
        # Verificar si el usuario ya existe
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario_create.usuario,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="El usuario ya existe")
        
        # Hash de la contraseña
        hashed_password = bcrypt.hashpw(usuario_create.contrasena.encode('utf-8'), bcrypt.gensalt())
        
        query = """
        INSERT INTO usuarios (usuario, contrasena, rol)
        VALUES (%s, %s, %s);
        """
        cursor.execute(query, (usuario_create.usuario, hashed_password.decode('utf-8'), usuario_create.rol))
        conn.commit()
        return {"usuario": usuario_create.usuario, "rol": usuario_create.rol}
    finally:
        cursor.close()
        conn.close()

# Ruta para iniciar sesión y devolver el rol
@app.post("/iniciar_sesion/", response_model=UsuarioConRol)
def iniciar_sesion(usuario: Usuario):
    # Verificar las credenciales en la base de datos y obtener el rol
    rol = verify_user_credentials(usuario.usuario, usuario.contrasena)
    if rol:
        return {"usuario": usuario.usuario, "rol": rol}
    else:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")