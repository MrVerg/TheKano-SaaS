# gestion_salas.py
import tkinter as tk
from tkinter import messagebox

class SalaFormulario:
    def __init__(self, root, db, sala=None, callback_actualizar=None):
        self.root = root
        self.db = db
        self.sala = sala
        self.callback_actualizar = callback_actualizar
        
        self.mostrar_formulario()
    
    def mostrar_formulario(self):
        # Crear ventana de formulario
        self.form_window = tk.Toplevel(self.root)
        self.form_window.title("Añadir/Editar Sala" if not self.sala else "Editar Sala")
        self.form_window.geometry("400x300")
        self.form_window.configure(bg='#f0f0f0')
        self.form_window.transient(self.root)
        self.form_window.grab_set()
        
        # Frame principal
        main_frame = tk.Frame(self.form_window, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="Datos de la Sala", font=("Arial", 16, "bold"), 
                bg='#f0f0f0', fg='#2c3e50').pack(anchor='w', pady=(0, 20))
        
        # Campos del formulario
        tk.Label(main_frame, text="Nombre", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        self.nombre_entry = tk.Entry(main_frame, font=("Arial", 12), width=30)
        self.nombre_entry.pack(fill='x', pady=(0, 10))
        
        tk.Label(main_frame, text="Capacidad", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        self.capacidad_entry = tk.Entry(main_frame, font=("Arial", 12), width=30)
        self.capacidad_entry.pack(fill='x', pady=(0, 10))
        
        tk.Label(main_frame, text="Horas Disponibles", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        self.horas_entry = tk.Entry(main_frame, font=("Arial", 12), width=30)
        self.horas_entry.pack(fill='x', pady=(0, 20))
        
        # Si estamos editando, llenar los campos
        if self.sala:
            self.nombre_entry.insert(0, self.sala["nombre"])
            self.capacidad_entry.insert(0, str(self.sala["capacidad"]))
            self.horas_entry.insert(0, str(self.sala["horas_disponibles"]))
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg='#f0f0f0')
        btn_frame.pack(fill='x', pady=(10, 0))
        
        guardar_btn = tk.Button(btn_frame, text="Guardar Cambios", font=("Arial", 12), 
                               command=self.guardar_sala, bg='#3498db', fg='white')
        guardar_btn.pack(side='left', padx=(0, 10))
        
        cancelar_btn = tk.Button(btn_frame, text="Cancelar", font=("Arial", 12), 
                                command=self.form_window.destroy, bg='#95a5a6', fg='white')
        cancelar_btn.pack(side='left')
    
    def guardar_sala(self):
        nombre = self.nombre_entry.get()
        capacidad = self.capacidad_entry.get()
        horas = self.horas_entry.get()
        
        if not nombre or not capacidad or not horas:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        # Validar que capacidad y horas sean números
        try:
            capacidad = int(capacidad)
            horas = int(horas)
        except ValueError:
            messagebox.showerror("Error", "Capacidad y horas deben ser números")
            return
        
        # Guardar en base de datos
        sala_data = (nombre, capacidad, horas)
        if self.sala:
            # Actualizar en BD
            resultado = self.db.guardar_sala(sala_data, self.sala["id"])
        else:
            # Insertar en BD
            resultado = self.db.guardar_sala(sala_data)
        
        if resultado:
            if self.callback_actualizar:
                self.callback_actualizar()
            self.form_window.destroy()
            messagebox.showinfo("Éxito", "Sala guardada correctamente")
        else:
            messagebox.showerror("Error", "Error al guardar en la base de datos")