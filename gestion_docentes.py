# gestion_docentes.py
import tkinter as tk
from tkinter import ttk, messagebox

class DocenteFormulario:
    def __init__(self, root, db, docente=None, callback_actualizar=None):
        self.root = root
        self.db = db
        self.docente = docente
        self.callback_actualizar = callback_actualizar
        
        self.mostrar_formulario()
    
    def mostrar_formulario(self):
        # Crear ventana de formulario
        self.form_window = tk.Toplevel(self.root)
        self.form_window.title("Añadir/Editar Docente" if not self.docente else "Editar Docente")
        self.form_window.geometry("800x700")
        self.form_window.configure(bg='#f0f0f0')
        self.form_window.transient(self.root)
        self.form_window.grab_set()
        
        # Frame principal con scroll
        main_frame = tk.Frame(self.form_window, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Canvas y scrollbar para el formulario largo
        canvas = tk.Canvas(main_frame, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(scrollable_frame, text="Datos del Docente", font=("Arial", 16, "bold"), 
                bg='#f0f0f0', fg='#2c3e50').pack(anchor='w', pady=(0, 20))
        
        # Campos del formulario - PRIMERA PARTE
        # Nombre
        tk.Label(scrollable_frame, text="Nombre", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        self.nombre_entry = tk.Entry(scrollable_frame, font=("Arial", 12), width=40)
        self.nombre_entry.pack(fill='x', pady=(0, 10))
        
        # Título académico
        tk.Label(scrollable_frame, text="Título Académico", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        self.titulo_entry = tk.Entry(scrollable_frame, font=("Arial", 12), width=40)
        self.titulo_entry.pack(fill='x', pady=(0, 10))
        
        # Tipo de contrato (selector desplegable)
        tk.Label(scrollable_frame, text="Tipo de Contrato", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        self.contrato_var = tk.StringVar(value="Planta")
        self.contrato_combo = ttk.Combobox(scrollable_frame, textvariable=self.contrato_var, font=("Arial", 12), width=38)
        self.contrato_combo['values'] = ["Planta", "Parcial", "Honorarios"]
        self.contrato_combo.pack(fill='x', pady=(0, 10))
        
        # Horas contratadas
        tk.Label(scrollable_frame, text="Horas Contratadas", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        self.horas_entry = tk.Entry(scrollable_frame, font=("Arial", 12), width=30)
        self.horas_entry.pack(fill='x', pady=(0, 20))
        
        # DISPONIBILIDAD HORARIA - SEGUNDA PARTE
        tk.Label(scrollable_frame, text="Disponibilidad Horaria", font=("Arial", 14, "bold"), 
                bg='#f0f0f0', fg='#2c3e50').pack(anchor='w', pady=(20, 10))
        
        # Frame para la grilla de disponibilidad
        disponibilidad_frame = tk.Frame(scrollable_frame, bg='white', relief='sunken', bd=1)
        disponibilidad_frame.pack(fill='x', pady=(0, 20))
        
        # Configurar grid para la grilla
        for i in range(6):  # 5 días + 1 columna para horas
            disponibilidad_frame.columnconfigure(i, weight=1)
        for i in range(10):  # 9 horas + 1 fila para encabezados
            disponibilidad_frame.rowconfigure(i, weight=1)
        
        # Variables para almacenar el estado de los checkboxes
        self.disponibilidad_vars = {}
        
        # Encabezados de días
        dias = ["Hora", "LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES"]
        for i, dia in enumerate(dias):
            label = tk.Label(disponibilidad_frame, text=dia, font=("Arial", 10, "bold"), 
                           bg='#34495e', fg='white', relief='raised', bd=1)
            label.grid(row=0, column=i, sticky='nsew', padx=1, pady=1)
        
        # Horas y checkboxes
        horas = ["8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
        for i, hora in enumerate(horas):
            # Etiqueta de la hora
            label = tk.Label(disponibilidad_frame, text=hora, font=("Arial", 9), 
                           bg='#34495e', fg='white', relief='raised', bd=1)
            label.grid(row=i+1, column=0, sticky='nsew', padx=1, pady=1)
            
            # Checkboxes para cada día
            for j in range(1, 6):  # Columnas 1-5 para los días
                var = tk.BooleanVar()
                # Por defecto, marcamos como disponible
                var.set(True)
                
                chk = tk.Checkbutton(disponibilidad_frame, variable=var, 
                                   bg='white', relief='raised', bd=1)
                chk.grid(row=i+1, column=j, sticky='nsew', padx=1, pady=1)
                
                # Guardar la variable en el diccionario
                dia_nombre = dias[j]  # LUNES, MARTES, etc.
                if dia_nombre not in self.disponibilidad_vars:
                    self.disponibilidad_vars[dia_nombre] = {}
                self.disponibilidad_vars[dia_nombre][hora] = var
        
        # Si estamos editando, llenar los campos y la disponibilidad
        if self.docente:
            self.nombre_entry.insert(0, self.docente["nombre"])
            self.titulo_entry.insert(0, self.docente["titulo"])
            self.contrato_var.set(self.docente["contrato"])
            self.horas_entry.insert(0, str(self.docente["horas_contratadas"]))
            
            # Cargar disponibilidad desde BD si existe
            disponibilidad_bd = self.db.obtener_disponibilidad_docente(self.docente["id"])
            if disponibilidad_bd:
                for disp in disponibilidad_bd:
                    dia = disp["dia"]
                    hora = disp["hora"]
                    disponible = disp["disponible"]
                    if dia in self.disponibilidad_vars and hora in self.disponibilidad_vars[dia]:
                        self.disponibilidad_vars[dia][hora].set(disponible)
        
        # Botones
        btn_frame = tk.Frame(scrollable_frame, bg='#f0f0f0')
        btn_frame.pack(fill='x', pady=(10, 0))
        
        guardar_btn = tk.Button(btn_frame, text="Guardar Cambios", font=("Arial", 12), 
                               command=self.guardar_docente, bg='#3498db', fg='white')
        guardar_btn.pack(side='left', padx=(0, 10))
        
        cancelar_btn = tk.Button(btn_frame, text="Cancelar", font=("Arial", 12), 
                                command=self.form_window.destroy, bg='#95a5a6', fg='white')
        cancelar_btn.pack(side='left')
    
    def guardar_docente(self):
        nombre = self.nombre_entry.get()
        titulo = self.titulo_entry.get()
        contrato = self.contrato_var.get()
        horas = self.horas_entry.get()
        
        if not nombre or not titulo or not contrato or not horas:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        # Validar que horas sea un número
        try:
            horas = int(horas)
        except ValueError:
            messagebox.showerror("Error", "Horas debe ser un número")
            return
        
        # Recoger la disponibilidad horaria
        disponibilidad_guardar = {}
        for dia, horas_dia in self.disponibilidad_vars.items():
            disponibilidad_guardar[dia] = {}
            for hora, var in horas_dia.items():
                disponibilidad_guardar[dia][hora] = var.get()
        
        # Preparar datos del docente
        docente_data = (nombre, titulo, contrato, horas, f"{nombre.lower().replace(' ', '.')}@ceduc.cl", 0.0)
        
        # Guardar en base de datos
        if self.docente:
            # Actualizar docente existente
            resultado = self.db.guardar_docente(docente_data, self.docente["id"])
            docente_id = self.docente["id"]
        else:
            # Insertar nuevo docente
            resultado = self.db.guardar_docente(docente_data)
            docente_id = resultado
        
        if resultado:
            # Guardar disponibilidad
            self.db.guardar_disponibilidad_docente(docente_id, disponibilidad_guardar)
            
            if self.callback_actualizar:
                self.callback_actualizar()
            
            self.form_window.destroy()
            messagebox.showinfo("Éxito", "Docente guardado correctamente")
        else:
            messagebox.showerror("Error", "Error al guardar en la base de datos")