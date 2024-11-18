import psycopg2
from psycopg2 import sql

try:
    # Establecer conexión con PostgreSQL
    conn = psycopg2.connect(
        dbname="Centro_animals", 
        user="base1", 
        password="123456", 
        host="localhost", 
        port="5432",
        options="-c client_encoding=utf8"
    )
    print("Conexión exitosa")

    # Crear un cursor
    cur = conn.cursor()

    # Crear tabla para Animales
    cur.execute("""
    CREATE TABLE IF NOT EXISTS animales (
        id SERIAL PRIMARY KEY,
        especie VARCHAR(50) NOT NULL,
        raza VARCHAR(50) NOT NULL,
        edad INT NOT NULL,
        sexo VARCHAR(10) NOT NULL,
        historial_clinico TEXT,
        fotos TEXT[],
        necesidades_especiales TEXT
    );
    """)

    # Crear tabla para Familias
    cur.execute("""
    CREATE TABLE IF NOT EXISTS familias (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        direccion VARCHAR(255) NOT NULL,
        telefono VARCHAR(20) NOT NULL,
        email VARCHAR(100) NOT NULL,
        composicion_familiar TEXT,
        estilo_de_vida TEXT
    );
    """)

    # Crear tabla para Adopciones
    cur.execute("""
    CREATE TABLE IF NOT EXISTS adopciones (
        id SERIAL PRIMARY KEY,
        fecha_solicitud DATE NOT NULL,
        animal_id INT REFERENCES animales(id),
        familia_id INT REFERENCES familias(id),
        fecha_adopcion DATE,
        CONSTRAINT unique_adoption UNIQUE (animal_id, familia_id)
    );
    """)

    # Confirmar los cambios
    conn.commit()

    # Cerrar cursor y conexión
    cur.close()

except Exception as e:
    print(f"Error en la conexión o ejecución: {e}")
finally:
    # Asegurarse de cerrar la conexión si fue establecida
    if 'conn' in locals():
        conn.close()
