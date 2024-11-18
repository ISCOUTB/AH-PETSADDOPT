import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = 'http://127.0.0.1:8000'

# --- Definiciones de funciones ---

# Definir los usuarios predefinidos
usuarios_validos = {
    "admin": {"contrasena": "admin123", "rol": "admin"},
    "cliente": {"contrasena": "cliente123", "rol": "usuario"},
}

def admin_login(username, password):
    # Validar las credenciales antes de hacer la solicitud
    if username in usuarios_validos and usuarios_validos[username]["contrasena"] == password:
        # Si son correctas, mostrar opciones del administrador
        show_admin_options()
    else:
        messagebox.showerror("Error", "Credenciales inválidas")

def client_login(username, password):
    # Validar las credenciales antes de hacer la solicitud
    if username in usuarios_validos and usuarios_validos[username]["contrasena"] == password:
        # Si son correctas, mostrar opciones del cliente
        show_client_options()
    else:
        messagebox.showerror("Error", "Credenciales inválidas")

def show_admin_options():
    clear_window()
    ttk.Label(window, text="Opciones del Administrador", font=("Arial", 16)).pack(pady=10)
    ttk.Button(window, text="Ver Datos de Animales", command=show_animal_data).pack(pady=5)
    ttk.Button(window, text="Agregar Nuevo Animal", command=show_add_animal).pack(pady=5)
    ttk.Button(window, text="Cerrar Sesión", command=elegir_tipo_usuario).pack(pady=10)

def show_client_options():
    clear_window()
    ttk.Label(window, text="Opciones del Cliente", font=("Arial", 16)).pack(pady=10)
    ttk.Button(window, text="Registrar", command=show_client_register).pack(pady=5)  # Primero mostrar el registro
    ttk.Button(window, text="Iniciar Sesión", command=show_client_login).pack(pady=5)  # Luego mostrar iniciar sesión
    ttk.Button(window, text="Cerrar Sesión", command=elegir_tipo_usuario).pack(pady=10)

def show_animal_data():
    response = requests.get(f'{API_URL}/animales/')
    if response.status_code == 200:
        animals = response.json()
        clear_window()
        ttk.Label(window, text="Animales en adopción", font=("Arial", 16)).pack(pady=10)
        for animal in animals:
            ttk.Label(window, text=f"{animal['tipo']} - {animal['raza']}, Edad: {animal['edad']} años").pack()
        ttk.Button(window, text="Volver", command=elegir_tipo_usuario).pack(pady=10)
    else:
        messagebox.showerror("Error", "No se pudo obtener la lista de animales")

def show_add_animal():
    clear_window()
    frame = ttk.Frame(window, padding="20")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ttk.Label(frame, text="Agregar Nuevo Animal", font=("Arial", 16)).pack(pady=10)

    ttk.Label(frame, text="Especie:").pack(anchor="w")
    especie_entry = ttk.Entry(frame, width=30)
    especie_entry.pack(pady=5)

    ttk.Label(frame, text="Raza:").pack(anchor="w")
    raza_entry = ttk.Entry(frame, width=30)
    raza_entry.pack(pady=5)

    ttk.Label(frame, text="Edad:").pack(anchor="w")
    edad_entry = ttk.Entry(frame, width=30)
    edad_entry.pack(pady=5)

    def add_animal():
        animal_data = {
            "tipo": especie_entry.get(),
            "raza": raza_entry.get(),
            "edad": int(edad_entry.get()),
            "vacunas": [],
        }
        response = requests.post(f"{API_URL}/animales/", json=animal_data)
        if response.status_code == 201:
            messagebox.showinfo("Éxito", "Animal agregado exitosamente")
            elegir_tipo_usuario()
        else:
            messagebox.showerror("Error", "No se pudo agregar el animal")

    ttk.Button(frame, text="Agregar", command=add_animal).pack(pady=10)
    ttk.Button(frame, text="Volver", command=show_admin_options).pack()

def elegir_tipo_usuario():
    clear_window()
    frame = ttk.Frame(window, padding="20")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ttk.Label(frame, text="Seleccione el tipo de usuario", font=("Arial", 16)).pack(pady=10)
    ttk.Button(frame, text="Administrador", command=show_admin_login).pack(pady=5)
    ttk.Button(frame, text="Cliente", command=show_client_options).pack(pady=5)

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
    ttk.Button(frame, text="Volver", command=elegir_tipo_usuario).pack()

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
    ttk.Button(frame, text="Volver", command=elegir_tipo_usuario).pack()

def show_client_register():
    clear_window()
    frame = ttk.Frame(window, padding="20")
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Registrar como Cliente", font=("Arial", 16)).pack(pady=10)
    ttk.Label(frame, text="Usuario:").pack(anchor="w")
    client_username_entry = ttk.Entry(frame, width=30)
    client_username_entry.pack(pady=5)

    ttk.Label(frame, text="Contraseña:").pack(anchor="w")
    client_password_entry = ttk.Entry(frame, show="*", width=30)
    client_password_entry.pack(pady=5)

    def register_user():
        username = client_username_entry.get()
        password = client_password_entry.get()

        if username and password:
            response = requests.post(f"{API_URL}/registrar/", json={"usuario": username, "contrasena": password, "rol": "usuario"})
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Usuario registrado exitosamente")
                elegir_tipo_usuario()  # Regresar a la pantalla inicial
            else:
                messagebox.showerror("Error", "No se pudo registrar el usuario")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    ttk.Button(frame, text="Registrar", command=register_user).pack(pady=10)
    ttk.Button(frame, text="Volver", command=show_client_options).pack()

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

