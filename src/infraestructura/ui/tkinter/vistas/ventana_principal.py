import tkinter as tk
from tkinter import messagebox, ttk

class VentanaPrincipal:
    def __init__(self, ui_service):
        self.ui_service = ui_service
        self.ventana = tk.Tk()
        self.ventana.title("Ventana Login")
        self.ventana.geometry("400x250")
        self.crear_interfaz()
        
    def iniciar(self):
        self.ventana.mainloop()
    
    def crear_interfaz(self):
        marco = ttk.Frame(self.ventana, padding="20")
        marco.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(marco, text="¡Bienvenido!", font=('Arial', 14)).pack(pady=10)
        
        # inputs de login
        ttk.Label(marco, text="Usuario:").pack()
        self.entrada_usuario = ttk.Entry(marco, width=30)
        self.entrada_usuario.pack(pady=5)
        
        ttk.Label(marco, text="Contraseña:").pack()
        self.entrada_clave = ttk.Entry(marco, show="*", width=30)
        self.entrada_clave.pack(pady=5)
        
        # botonnes
        frame_botones = ttk.Frame(marco)
        frame_botones.pack(pady=20)
        ttk.Button(frame_botones, text="Ingresar", command=self.validar_usuario).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Registrarse", command=self.mostrar_registro).pack(side=tk.LEFT, padx=5)

    def mostrar_registro(self):
        ventana_registro = tk.Toplevel(self.ventana)
        ventana_registro.title("Registro de Usuario Nuevo")
        ventana_registro.geometry("300x200")
        
        marco = ttk.Frame(ventana_registro, padding="20")
        marco.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(marco, text="Nuevo Usuario:").pack()
        nuevo_usuario = ttk.Entry(marco, width=30)
        nuevo_usuario.pack(pady=5)
        
        ttk.Label(marco, text="Nueva Contraseña:").pack()
        nueva_clave = ttk.Entry(marco, show="*", width=30)
        nueva_clave.pack(pady=5)
        
        def registrar():
            try:
                self.ui_service.registrar_usuario(
                    nuevo_usuario.get(),
                    nueva_clave.get()
                )
                messagebox.showinfo("Éxito", "¡Usuario registrado exitosamente!")
                ventana_registro.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(marco, text="Registrar", command=registrar).pack(pady=20)

    def validar_usuario(self):
        try:
            if self.ui_service.validar_login(
                self.entrada_usuario.get(),
                self.entrada_clave.get()
            ):
                self.mostrar_datos_api()
            else:
                if self.ui_service.usuario_existe(self.entrada_usuario.get()):
                    messagebox.showerror("Error", "¡Contraseña incorrecta!")
                else:
                    if messagebox.askyesno("Usuario no existe","¡Este usuario no existe! ¿Deseas registrarte?"):
                        self.mostrar_registro()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def mostrar_datos_api(self):
        ventana_datos = tk.Toplevel(self.ventana)
        ventana_datos.title("Personajes de Rick y Morty")
        ventana_datos.geometry("500x400")
        
        tabla = ttk.Treeview(ventana_datos, columns=('ID', 'Nombre', 'Estado'), show='headings')
        tabla.heading('ID', text='ID')
        tabla.heading('Nombre', text='Nombre')
        tabla.heading('Estado', text='Estado')
        tabla.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        try:
            personajes = self.ui_service.obtener_personajes()
            for personaje in personajes:
                tabla.insert('', 'end', values=(
                    personaje['id'],
                    personaje['name'],
                    'Personaje Vigente' if personaje['status'] == 'Alive' else 'Personaje Descontinuado'
                ))
        except Exception as error:
            messagebox.showerror("Error", f"¡falló en la API!: {error}")