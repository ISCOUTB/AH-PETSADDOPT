import psycopg2
from psycopg2 import sql

# Establecer conexión con PostgreSQL
conn = psycopg2.connect(
    dbname="nombre_de_tu_base_de_datos", 
    user="tu_usuario", 
    password="tu_contraseña", 
    host="localhost", 
    port="5432"
)

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
conn.close()

# Insertar datos de ejemplo en la tabla animales
cur.execute("""
INSERT INTO animales (especie, raza, edad, sexo, historial_clinico, fotos, necesidades_especiales)
VALUES 
('Perro', 'Labrador', 5, 'Macho', 'Vacunas al día', ARRAY['labrador1.jpg', 'labrador2.jpg'], 'Ninguna'),
('Gato', 'Siames', 3, 'Hembra', 'Vacunas al día', ARRAY['siames1.jpg', 'siames2.jpg'], 'Requiere dieta especial');
""")

# Insertar datos de ejemplo en la tabla familias
cur.execute("""
INSERT INTO familias (nombre, direccion, telefono, email, composicion_familiar, estilo_de_vida)
VALUES 
('Juan Pérez', 'Calle Falsa 123', '555-1234', 'juan@example.com', 'Padre, Madre, 2 Hijos', 'Activos'),
('María López', 'Calle Verdadera 456', '555-5678', 'maria@example.com', 'Solo', 'Tranquila');
""")

# Confirmar los cambios
conn.commit()
