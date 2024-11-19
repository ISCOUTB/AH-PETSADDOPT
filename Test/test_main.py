from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_obtener_animales():
    response = client.get("/animales/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_agregar_animal():
    nuevo_animal = {
        "tipo": "Perro",
        "raza": "Labrador",
        "edad": 3,
        "vacunas": ["Rabia", "Parvovirus"]
    }
    response = client.post("/animales/", json=nuevo_animal)
    assert response.status_code == 200
    data = response.json()
    assert data["tipo"] == nuevo_animal["tipo"]
    assert data["raza"] == nuevo_animal["raza"]
    assert data["edad"] == nuevo_animal["edad"]
    assert data["vacunas"] == nuevo_animal["vacunas"]