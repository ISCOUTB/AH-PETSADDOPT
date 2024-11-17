import tkinter as tk
from tkinter import messagebox
import requests

API_URL = 'http://127.0.0.1:8000'

def elegir_tipo_usuario():
    clear_window()
    tk.Label(window, text="Seleccione el tipo de usuario").pack()
    tk.Button(window, text="Administrador", command=show_admin_login).pack()
    tk.Button(window, text="Cliente", command=show_client_registration).pack()

def show_admin_login():
    clear_window()
    tk.Label(window, text="Iniciar Sesión como Administrador").pack()
    tk.Label(window, text="Usuario").pack()
    admin_username_entry = tk.Entry(window)
    admin_username_entry.pack()
    tk.Label(window, text="Contraseña").pack()
    admin_password_entry = tk.Entry(window, show="*")
    admin_password_entry.pack()
    tk.Button(window, text="Login", command=lambda: admin_login(admin_username_entry.get(), admin_password_entry.get())).pack()
    tk.Button(window, text="Atrás", command=elegir_tipo_usuario).pack()

def admin_login(username, password):
    response = requests.post(f'{API_URL}/iniciar_sesion/', json={"usuario": username, "contrasena": password})
    if response.status_code == 200 and response.json()["rol"] == "admin":
        show_admin_options()
    else:
        messagebox.showerror("Error", "Credenciales inválidas")

def show_admin_options():
    clear_window()
    tk.Label(window, text="Opciones del Administrador").pack()
    tk.Button(window, text="Ver Datos de Animales", command=show_animal_data).pack()
    tk.Button(window, text="Agregar Nuevo Animal", command=show_add_animal).pack()
    tk.Button(window, text="Cerrar Sesión", command=elegir_tipo_usuario).pack()

def show_add_animal():
    clear_window()
    tk.Label(window, text="Registrar Nuevo Animal").pack()
    tk.Label(window, text="ID").pack()
    id_entry = tk.Entry(window)
    id_entry.pack()
    tk.Label(window, text="Tipo").pack()
    tipo_entry = tk.Entry(window)
    tipo_entry.pack()
    tk.Label(window, text="Raza").pack()
    raza_entry = tk.Entry(window)
    raza_entry.pack()
    tk.Label(window, text="Edad").pack()
    edad_entry = tk.Entry(window)
    edad_entry.pack()
    tk.Label(window, text="Vacunas (separadas por coma)").pack()
    vacunas_entry = tk.Entry(window)
    vacunas_entry.pack()
    tk.Label(window, text="Fotos (separadas por coma)").pack()
    fotos_entry = tk.Entry(window)
    fotos_entry.pack()
    tk.Button(window, text="Registrar", command=lambda: register_animal(id_entry.get(), tipo_entry.get(), raza_entry.get(), edad_entry.get(), vacunas_entry.get(), fotos_entry.get())).pack()
    tk.Button(window, text="Atrás", command=show_admin_options).pack()

def register_animal(id, tipo, raza, edad, vacunas, fotos):
    animal_data = {
        "id": int(id),
        "tipo": tipo,
        "raza": raza,
        "edad": int(edad),
        "vacunas": [v.strip() for v in vacunas.split(",")],
        "fotos": [f.strip() for f in fotos.split(",")]
    }
    response = requests.post(f'{API_URL}/animales/', json=animal_data)
    if response.status_code == 200:
        messagebox.showinfo("Éxito", "Animal registrado exitosamente")
        show_admin_options()
    else:
        messagebox.showerror("Error", response.json()["detail"])

def show_client_registration():
    clear_window()
    tk.Label(window, text="Registrar como Cliente").pack()
    tk.Label(window, text="Nombre").pack()
    name_entry = tk.Entry(window)
    name_entry.pack()
    tk.Label(window, text="Dirección").pack()
    address_entry = tk.Entry(window)
    address_entry.pack()
    tk.Label(window, text="Teléfono").pack()
    phone_entry = tk.Entry(window)
    phone_entry.pack()
    tk.Label(window, text="Email").pack()
    email_entry = tk.Entry(window)
    email_entry.pack()
    tk.Label(window, text="Composición Familiar").pack()
    family_entry = tk.Entry(window)
    family_entry.pack()
    tk.Label(window, text="Estilo de Vida").pack()
    lifestyle_entry = tk.Entry(window)
    lifestyle_entry.pack()
    tk.Button(window, text="Enviar", command=lambda: register_user(name_entry.get(), address_entry.get(), phone_entry.get(), email_entry.get(), family_entry.get(), lifestyle_entry.get())).pack()
    tk.Button(window, text="Atrás", command=elegir_tipo_usuario).pack()

def register_user(name, address, phone, email, family_composition, lifestyle):
    user_data = {
        "nombre": name,
        "direccion": address,
        "telefono": phone,
        "email": email,
        "composicion_familiar": family_composition,
        "estilo_de_vida": lifestyle
    }
    response = requests.post(f'{API_URL}/registrar/', json=user_data)
    if response.status_code == 200:
        messagebox.showinfo("Éxito", "Usuario registrado exitosamente")
        elegir_tipo_usuario()
    else:
        messagebox.showerror("Error", "Error en el registro")

def show_animal_data():
    clear_window()
    response = requests.get(f'{API_URL}/animales/')
    animals = response.json()
    for animal in animals:
        animal_info = f"ID: {animal['id']}\nTipo: {animal['tipo']}\nRaza: {animal['raza']}\nEdad: {animal['edad']}\nVacunas: {', '.join(animal['vacunas'])}\nFotos: {', '.join(animal['fotos'])}\n"
        tk.Label(window, text=animal_info).pack()
    tk.Button(window, text="Atrás", command=show_admin_options).pack()

def clear_window():
    for widget in window.winfo_children():
        widget.destroy()

window = tk.Tk()
window.title("Aplicación de Adopción")
elegir_tipo_usuario()
window.mainloop()
