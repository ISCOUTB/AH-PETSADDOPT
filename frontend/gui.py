import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = 'http://127.0.0.1:8000'

# --- Definiciones de funciones ---

def admin_login(username, password):
    try:
        response = requests.post(f'{API_URL}/iniciar_sesion/', json={"usuario": username, "contrasena": password})
        if response.status_code == 200 and response.json()["rol"] == "admin":
            show_admin_options()
        else:
            messagebox.showerror("Error", "Credenciales inválidas")
    except Exception as e:
        messagebox.showerror("Error", f"Error al conectar con el servidor: {e}")

def client_login(username, password):
    try:
        response = requests.post(f'{API_URL}/iniciar_sesion/', json={"usuario": username, "contrasena": password})
        if response.status_code == 200 and response.json()["rol"] == "usuario":
            show_client_options()
        else:
            messagebox.showerror("Error", "Credenciales inválidas")
    except Exception as e:
        messagebox.showerror("Error", f"Error al conectar con el servidor: {e}")

def show_admin_options():
    clear_window()
    ttk.Label(window, text="Opciones del Administrador", font=("Arial", 16)).pack(pady=10)
    ttk.Button(window, text="Ver Datos de Animales", command=show_animal_data).pack(pady=5)
    ttk.Button(window, text="Agregar Nuevo Animal", command=show_add_animal).pack(pady=5)
    ttk.Button(window, text="Ver Familias Registradas", command=show_families).pack(pady=5)
    ttk.Button(window, text="Cerrar Sesión", command=elegir_tipo_usuario).pack(pady=10)

def show_client_options():
    clear_window()
    ttk.Label(window, text="Opciones del Cliente", font=("Arial", 16)).pack(pady=10)
    ttk.Button(window, text="Ver Animales en Adopción", command=show_animal_data).pack(pady=5)
    ttk.Button(window, text="Solicitar un Animal", command=show_request_animal).pack(pady=5)
    ttk.Button(window, text="Cerrar Sesión", command=elegir_tipo_usuario).pack(pady=10)

def show_animal_data():
    response = requests.get(f'{API_URL}/animales/')
    if response.status_code == 200:
        animals = response.json()
        clear_window()
        ttk.Label(window, text="Animales en adopción", font=("Arial", 16)).pack(pady=10)
        for animal in animals:
            ttk.Label(window, text=f"{animal['tipo']} - {animal['raza']}").pack()
        ttk.Button(window, text="Volver", command=elegir_tipo_usuario).pack(pady=10)
    else:
        messagebox.showerror("Error", "No se pudo obtener la lista de animales")

def show_add_animal():
    pass  # Implementar para agregar un nuevo animal

def show_families():
    response = requests.get(f'{API_URL}/familias/')
    if response.status_code == 200:
        families = response.json()
        clear_window()
        ttk.Label(window, text="Familias Registradas", font=("Arial", 16)).pack(pady=10)
        for family in families:
            ttk.Label(window, text=f"Familia: {family['nombre_familia']}").pack()
        ttk.Button(window, text="Volver", command=show_admin_options).pack(pady=10)
    else:
        messagebox.showerror("Error", "No se pudo obtener la lista de familias")

def show_request_animal():
    pass  # Implementar para solicitar un animal

def show_client_registration():
    clear_window()
    frame = ttk.Frame(window, padding="20")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ttk.Label(frame, text="Registrar como Cliente", font=("Arial", 16)).pack(pady=10)
    ttk.Label(frame, text="Nombre:").pack(anchor="w")
    client_name_entry = ttk.Entry(frame, width=30)
    client_name_entry.pack(pady=5)

    ttk.Label(frame, text="Email:").pack(anchor="w")
    client_email_entry = ttk.Entry(frame, width=30)
    client_email_entry.pack(pady=5)

    ttk.Label(frame, text="Teléfono:").pack(anchor="w")
    client_phone_entry = ttk.Entry(frame, width=30)
    client_phone_entry.pack(pady=5)

    ttk.Label(frame, text="Composición Familiar:").pack(anchor="w")
    client_family_entry = ttk.Entry(frame, width=30)
    client_family_entry.pack(pady=5)

    ttk.Label(frame, text="Estilo de Vida:").pack(anchor="w")
    client_lifestyle_entry = ttk.Entry(frame, width=30)
    client_lifestyle_entry.pack(pady=5)

    ttk.Button(frame, text="Registrar", command=lambda: register_client(client_name_entry.get(), client_email_entry.get(), client_phone_entry.get(), client_family_entry.get(), client_lifestyle_entry.get())).pack(pady=10)
    ttk.Button(frame, text="Atrás", command=elegir_tipo_usuario).pack()

def register_client(name, email, phone, family, lifestyle):
    data = {
        "nombre": name,
        "email": email,
        "telefono": phone,
        "composicion_familiar": family,
        "estilo_de_vida": lifestyle
    }
    try:
        response = requests.post(f'{API_URL}/registrar/', json=data)
        if response.status_code == 201:
            messagebox.showinfo("Éxito", "Cliente registrado exitosamente")
            elegir_tipo_usuario()
        else:
            messagebox.showerror("Error", "No se pudo registrar el cliente")
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar cliente: {e}")

def elegir_tipo_usuario():
    clear_window()
    frame = ttk.Frame(window, padding="20")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ttk.Label(frame, text="Seleccione el tipo de usuario", font=("Arial", 16)).pack(pady=10)
    ttk.Button(frame, text="Administrador", command=show_admin_login).pack(pady=5)
    ttk.Button(frame, text="Cliente", command=show_client_login).pack(pady=5)

def show_admin_login():
    clear_window()
    frame = ttk.Frame(window, padding="20")
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Iniciar Sesión como Administrador", font=("Arial", 16)).pack(pady=10)
    ttk.Label(frame, text="Usuario:").pack(anchor="w")
    admin_username_entry = ttk.Entry(frame, width=30)
    admin_username_entry.pack(pady=5)

    ttk.Label(frame, text="Contraseña:").pack(anchor="w")
    admin_password_entry = ttk.Entry(frame, show="*", width=30)
    admin_password_entry.pack(pady=5)

    ttk.Button(frame, text="Login", command=lambda: admin_login(admin_username_entry.get(), admin_password_entry.get())).pack(pady=10)
    ttk.Button(frame, text="Atrás", command=elegir_tipo_usuario).pack()

def show_client_login():
    clear_window()
    frame = ttk.Frame(window, padding="20")
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Iniciar Sesión como Cliente", font=("Arial", 16)).pack(pady=10)
    ttk.Label(frame, text="Usuario:").pack(anchor="w")
    client_username_entry = ttk.Entry(frame, width=30)
    client_username_entry.pack(pady=5)

    ttk.Label(frame, text="Contraseña:").pack(anchor="w")
    client_password_entry = ttk.Entry(frame, show="*", width=30)
    client_password_entry.pack(pady=5)

    ttk.Button(frame, text="Login", command=lambda: client_login(client_username_entry.get(), client_password_entry.get())).pack(pady=10)
    ttk.Button(frame, text="Atrás", command=elegir_tipo_usuario).pack()

def clear_window():
    for widget in window.winfo_children():
        widget.destroy()

# --- Configuración de la ventana ---
window = tk.Tk()
window.title("Aplicación de Adopción")
window.geometry("500x600")
window.resizable(False, False)

# Mostrar interfaz principal
elegir_tipo_usuario()

window.mainloop()

