import tkinter as tk
from tkinter import ttk, messagebox
import requests

# --- Configuración de la API ---
API_URL = 'http://127.0.0.1:8021'

# --- Definiciones de funciones ---

def clear_window():
    for widget in window.winfo_children():
        widget.destroy()

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

def admin_login(username, password):
    response = requests.post(f'{API_URL}/iniciar_sesion/', json={"usuario": username, "contrasena": password})
    if response.status_code == 200:
        data = response.json()
        if data['rol'] == 'admin':
            show_admin_options()
        else:
            messagebox.showerror("Error", "Acceso solo para administradores")
    else:
        messagebox.showerror("Error", "Credenciales inválidas")

def show_admin_options():
    clear_window()
    ttk.Label(window, text="Opciones del Administrador", font=("Arial", 16)).pack(pady=10)
    ttk.Button(window, text="Ver Datos de Animales", command=show_animal_data).pack(pady=5)
    ttk.Button(window, text="Agregar Nuevo Animal", command=show_add_animal).pack(pady=5)
    ttk.Button(window, text="Eliminar Animal", command=show_delete_animal).pack(pady=5)
    ttk.Button(window, text="Cerrar Sesión", command=elegir_tipo_usuario).pack(pady=10)

def show_client_options():
    clear_window()
    ttk.Label(window, text="Opciones del Cliente", font=("Arial", 16)).pack(pady=10)
    ttk.Button(window, text="Ver Animales", command=show_animal_data).pack(pady=5)
    ttk.Button(window, text="Cerrar Sesión", command=elegir_tipo_usuario).pack(pady=10)

def show_animal_data():
    response = requests.get(f'{API_URL}/animales/')
    if response.status_code == 200:
        animals = response.json()
        clear_window()
        ttk.Label(window, text="Animales en adopción", font=("Arial", 16)).pack(pady=10)
        for animal in animals:
            ttk.Label(window, text=f"{animal['tipo']} - {animal['raza']}, Edad: {animal['edad']} años").pack()
        ttk.Button(window, text="Volver", command=show_admin_options).pack(pady=10)
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
        if response.status_code // 100 == 2:
            messagebox.showinfo("Éxito", "Animal agregado exitosamente")
            show_admin_options()
        else:
            messagebox.showerror("Error", f"No se pudo agregar el animal. {response.text}")

    ttk.Button(frame, text="Agregar", command=add_animal).pack(pady=10)
    ttk.Button(frame, text="Volver", command=show_admin_options).pack()

def show_delete_animal():
    response = requests.get(f'{API_URL}/animales/')
    if response.status_code == 200:
        animals = response.json()
        clear_window()
        ttk.Label(window, text="Eliminar Animal", font=("Arial", 16)).pack(pady=10)
        
        # Crear un dropdown con los animales
        ttk.Label(window, text="Seleccione un animal para eliminar:").pack(anchor="w")
        
        animal_choices = []
        for animal in animals:
            # Manejar el caso donde no haya raza disponible
            raza = animal['raza'] if animal['raza'] else "Desconocida"
            animal_choices.append(f"{animal['tipo']} - {raza} (Edad: {animal['edad']})")
        
        animal_combobox = ttk.Combobox(window, values=animal_choices, width=40)
        animal_combobox.pack(pady=5)
        
        def delete_animal():
            selected_animal = animal_combobox.get()
            print(f"selected_animal: {selected_animal}")
            
            # Extraer tipo, raza y edad
            try:
                # Intentamos dividir el texto como tipo - raza (Edad: x)
                parts = selected_animal.split(" - ")
                if len(parts) == 2:
                    tipo = parts[0]
                    raza_y_edad = parts[1].strip()
                    # Encontrar la edad en el formato "(Edad: x)"
                    edad_str = raza_y_edad.split(" (Edad: ")
                    if len(edad_str) == 2:
                        raza = edad_str[0]
                        edad = int(edad_str[1].replace(")", ""))  # Extraer la edad y eliminar el paréntesis
                        
                        # Buscar el animal con estos datos
                        animal_data = {
                            "tipo": tipo,
                            "raza": raza,
                            "edad": edad
                        }
                        print(f"Enviando solicitud de eliminación con los siguientes datos: {animal_data}")
                        
                        response = requests.delete(f"{API_URL}/animales/eliminar_por_datos/", json=animal_data)
                        
                        # Mostrar más información de la respuesta para depuración
                        print(f"Respuesta de la API: {response.status_code} - {response.text}")
                        
                        if response.status_code == 200:
                            messagebox.showinfo("Éxito", "Animal eliminado exitosamente")
                            show_admin_options()
                        else:
                            messagebox.showerror("Error", f"No se pudo eliminar el animal. Respuesta del servidor: {response.status_code} - {response.text}")
                    else:
                        messagebox.showerror("Error", "No se pudo extraer la edad correctamente.")
                else:
                    messagebox.showerror("Error", "El formato del animal seleccionado es incorrecto.")
            except Exception as e:
                print(f"Error procesando la selección: {e}")
                messagebox.showerror("Error", f"Error procesando la eliminación: {e}")



def elegir_tipo_usuario():
    clear_window()
    frame = ttk.Frame(window, padding="20")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ttk.Label(frame, text="Seleccione el tipo de usuario", font=("Arial", 16)).pack(pady=10)
    ttk.Button(frame, text="Administrador", command=show_admin_login).pack(pady=5)
    ttk.Button(frame, text="Cliente", command=show_client_options).pack(pady=5)

# --- Configuración de la ventana ---
window = tk.Tk()
window.title("Aplicación de Adopción")
window.geometry("500x600")
window.resizable(False, False)

# Mostrar interfaz principal
elegir_tipo_usuario()
window.mainloop()
