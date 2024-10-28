
import tkinter as tk
from tkinter import messagebox

API_URL = 'http://127.0.0.1:8000'

# Función para elegir el tipo de usuario
def elegir_tipo_usuario():
    clear_window()
    tk.Label(window, text="Seleccione el tipo de usuario").pack()
    tk.Button(window, text="Administrador", command=show_admin_login).pack()
    tk.Button(window, text="Cliente", command=show_client_registration).pack()

# Función para mostrar el inicio de sesión del administrador
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

# Función para iniciar sesión como administrador
def admin_login(username, password):
    if username == "admin" and password == "admin1":
        show_admin_options()
    else:
        messagebox.showerror("Error", "Credenciales inválidas")

# Función para mostrar las opciones del administrador
def show_admin_options():
    clear_window()
    tk.Label(window, text="Opciones del Administrador").pack()
    tk.Button(window, text="Registrar Nuevo Administrador", command=show_register_admin).pack()
    tk.Button(window, text="Ver Datos de Animales", command=show_animal_data).pack()
    tk.Button(window, text="Cerrar Sesion", command=elegir_tipo_usuario).pack()

# Función para mostrar el registro de un nuevo administrador
def show_register_admin():
    clear_window()
    tk.Label(window, text="Registrar Nuevo Administrador").pack()
    tk.Label(window, text="Contraseña de Admin").pack()
    admin_password_entry = tk.Entry(window, show="*")
    admin_password_entry.pack()
    tk.Label(window, text="Nuevo Usuario").pack()
    new_username_entry = tk.Entry(window)
    new_username_entry.pack()
    tk.Button(window, text="Registrar", command=lambda: register_admin(admin_password_entry.get(), new_username_entry.get())).pack()

# Función para registrar un nuevo administrador
def register_admin(admin_password, new_username):
    if admin_password == "admin1":
        credentials[new_username] = "admin1"
        messagebox.showinfo("Éxito", "Administrador registrado exitosamente")
        show_admin_options()
    else:
        messagebox.showerror("Error", "Contraseña de administrador incorrecta")

# Función para mostrar el registro del cliente
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
    tk.Button(window, text="Cerrar sesión", command=elegir_tipo_usuario).pack()

# Función para registrar un nuevo cliente
def register_user(name, address, phone, email, family_composition, lifestyle):
    user_data = {
        "name": name,
        "address": address,
        "phone": phone,
        "email": email,
        "family_composition": family_composition,
        "lifestyle": lifestyle
    }
    response = requests.post(f'{API_URL}/registrar/', json=user_data)
    if response.status_code == 200:
        messagebox.showinfo("Éxito", "Usuario registrado exitosamente")
        elegir_tipo_usuario()
    else:
        messagebox.showerror("Error", "Error en el registro")

# Función para mostrar los datos de los animales
def show_animal_data():
    clear_window()
    response = requests.get(f'{API_URL}/animales/')
    animals = response.json()
    for animal in animals:
        animal_info = f"ID: {animal['id']}\nTipo: {animal['tipo']}\nRaza: {animal['raza']}\nEdad: {animal['edad']}\nVacunas: {', '.join(animal['vacunas'])}\nFotos: {', '.join(animal['fotos'])}\n"
        tk.Label(window, text=animal_info).pack()
    tk.Button(window, text="Cerrar Sesionn", command=elegir_tipo_usuario).pack()

# Función para limpiar la ventana
def clear_window():
    for widget in window.winfo_children():
        widget.destroy()

# Crear la ventana principal
window = tk.Tk()
window.title("Aplicación de Adopción")

# Mostrar la opción de elegir tipo de usuario
elegir_tipo_usuario()

# Iniciar el bucle principal
window.mainloop()
