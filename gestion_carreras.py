# gestion_carreras.py - VERSIÓN COMPLETA CORREGIDA
import tkinter as tk
from tkinter import messagebox
from gestion_docentes import DocenteFormulario
from gestion_modulos import ModuloFormulario
from vista_docente import VistaDocente

class CarreraFormulario:
    def __init__(self, root, db, carrera=None, callback_actualizar=None):
        self.root = root
        self.db = db
        self.carrera = carrera
        self.callback_actualizar = callback_actualizar
        
        self.mostrar_formulario()
    
    def mostrar_formulario(self):
        # Crear ventana de formulario
        self.form_window = tk.Toplevel(self.root)
        self.form_window.title("Añadir/Editar Carrera" if not self.carrera else "Editar Carrera")
        self.form_window.geometry("500x500")
        self.form_window.configure(bg='#f0f0f0')
        self.form_window.transient(self.root)
        self.form_window.grab_set()
        
        # Frame principal
        main_frame = tk.Frame(self.form_window, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="Datos de la Carrera", font=("Arial", 16, "bold"), 
                bg='#f0f0f0', fg='#2c3e50').pack(anchor='w', pady=(0, 20))
        
        # Campos del formulario
        tk.Label(main_frame, text="Nombre", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        self.nombre_entry = tk.Entry(main_frame, font=("Arial", 12), width=40)
        self.nombre_entry.pack(fill='x', pady=(0, 10))
        
        tk.Label(main_frame, text="Jornada", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        self.jornada_var = tk.StringVar(value="Diurna")
        jornada_frame = tk.Frame(main_frame, bg='#f0f0f0')
        jornada_frame.pack(fill='x', pady=(0, 10))
        tk.Radiobutton(jornada_frame, text="Diurna", variable=self.jornada_var, value="Diurna", 
                      bg='#f0f0f0', font=("Arial", 10)).pack(side='left')
        tk.Radiobutton(jornada_frame, text="Vespertina", variable=self.jornada_var, value="Vespertina", 
                      bg='#f0f0f0', font=("Arial", 10)).pack(side='left', padx=(20, 0))
        
        tk.Label(main_frame, text="Semestres", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        semestres_frame = tk.Frame(main_frame, bg='#f0f0f0')
        semestres_frame.pack(fill='x', pady=(0, 10))
        
        self.semestres_vars = {}
        for semestre in ["I", "II", "III", "IV"]:
            self.semestres_vars[semestre] = tk.BooleanVar()
            tk.Checkbutton(semestres_frame, text=f"Semestre {semestre}", 
                          variable=self.semestres_vars[semestre], bg='#f0f0f0', 
                          font=("Arial", 10)).pack(side='left', padx=(0, 10))
        
        tk.Label(main_frame, text="Salas Disponibles", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        salas_frame = tk.Frame(main_frame, bg='#f0f0f0')
        salas_frame.pack(fill='x', pady=(0, 10))
        
        # Obtener salas desde la base de datos
        salas = self.db.obtener_salas()
        self.salas_vars = {}
        for sala in salas:
            self.salas_vars[sala["id"]] = tk.BooleanVar()
            tk.Checkbutton(salas_frame, text=sala["nombre"], 
                          variable=self.salas_vars[sala["id"]], bg='#f0f0f0', 
                          font=("Arial", 10)).pack(anchor='w')
        
        tk.Label(main_frame, text="Alumnos Proyectados", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        self.alumnos_entry = tk.Entry(main_frame, font=("Arial", 12), width=30)
        self.alumnos_entry.pack(fill='x', pady=(0, 20))
        
        # Si estamos editando, llenar los campos
        if self.carrera:
            self.nombre_entry.insert(0, self.carrera["nombre"])
            self.jornada_var.set(self.carrera["jornada"])
            self.alumnos_entry.insert(0, str(self.carrera["alumnos_proyectados"]))
            
            # Cargar semestres de la carrera
            semestres_carrera = self.db.obtener_semestres_carrera(self.carrera["id"])
            for semestre in semestres_carrera:
                if semestre in self.semestres_vars:
                    self.semestres_vars[semestre].set(True)
            
            # Cargar salas de la carrera
            salas_carrera = self.db.obtener_salas_carrera(self.carrera["id"])
            for sala in salas_carrera:
                if sala["id"] in self.salas_vars:
                    self.salas_vars[sala["id"]].set(True)
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg='#f0f0f0')
        btn_frame.pack(fill='x', pady=(10, 0))
        
        guardar_btn = tk.Button(btn_frame, text="Guardar Cambios", font=("Arial", 12), 
                               command=self.guardar_carrera, bg='#3498db', fg='white')
        guardar_btn.pack(side='left', padx=(0, 10))
        
        cancelar_btn = tk.Button(btn_frame, text="Cancelar", font=("Arial", 12), 
                                command=self.form_window.destroy, bg='#95a5a6', fg='white')
        cancelar_btn.pack(side='left')
    
    def guardar_carrera(self):
        nombre = self.nombre_entry.get()
        jornada = self.jornada_var.get()
        alumnos = self.alumnos_entry.get()
        
        if not nombre or not alumnos:
            messagebox.showerror("Error", "Nombre y alumnos son obligatorios")
            return
        
        # Validar que alumnos sea un número
        try:
            alumnos = int(alumnos)
        except ValueError:
            messagebox.showerror("Error", "Alumnos debe ser un número")
            return
        
        # Obtener semestres seleccionados
        semestres_seleccionados = [sem for sem, var in self.semestres_vars.items() if var.get()]
        if not semestres_seleccionados:
            messagebox.showerror("Error", "Debe seleccionar al menos un semestre")
            return
        
        # Obtener salas seleccionadas
        salas_seleccionadas = [sala_id for sala_id, var in self.salas_vars.items() if var.get()]
        
        # Guardar o actualizar carrera en la base de datos
        carrera_data = (nombre, jornada, alumnos)
        if self.carrera:
            # Actualizar carrera existente
            resultado = self.db.guardar_carrera(carrera_data, semestres_seleccionados, salas_seleccionadas, self.carrera["id"])
        else:
            # Añadir nueva carrera
            resultado = self.db.guardar_carrera(carrera_data, semestres_seleccionados, salas_seleccionadas)
        
        if resultado:
            if self.callback_actualizar:
                self.callback_actualizar()
            self.form_window.destroy()
            messagebox.showinfo("Éxito", "Carrera guardada correctamente")
        else:
            messagebox.showerror("Error", "Error al guardar la carrera en la base de datos")

class VistaModulosCarrera:
    def __init__(self, root, db, carrera, callback_volver):
        self.root = root
        self.db = db
        self.carrera = carrera
        self.callback_volver = callback_volver
        self.semestre_actual = "Todos"
        
        self.mostrar_vista()
    
    def mostrar_vista(self):
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Crear frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True)
        
        # Barra superior
        top_bar = tk.Frame(main_frame, bg='#2c3e50', height=50)
        top_bar.pack(fill='x', side='top')
        top_bar.pack_propagate(False)
        
        tk.Label(top_bar, text="CEDUC", font=("Arial", 14, "bold"), 
                bg='#2c3e50', fg='white').pack(side='left', padx=20, pady=10)
        
        # Botón para volver al panel principal
        volver_btn = tk.Button(top_bar, text="Volver", font=("Arial", 10), 
                              command=self.callback_volver, bg='#3498db', fg='white')
        volver_btn.pack(side='right', padx=20, pady=10)
        
        # Contenido principal dividido en dos columnas
        content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Columna izquierda (25%)
        left_frame = tk.Frame(content_frame, bg='#f0f0f0', width=300)
        left_frame.pack(side='left', fill='y')
        left_frame.pack_propagate(False)
        
        # Nombre de la carrera y botón editar
        carrera_frame = tk.Frame(left_frame, bg='#f0f0f0')
        carrera_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(carrera_frame, text=self.carrera["nombre"], font=("Arial", 16, "bold"), 
                bg='#f0f0f0', fg='#2c3e50').pack(anchor='w')
        
        editar_btn = tk.Button(carrera_frame, text="Editar Carrera", font=("Arial", 10),
                              command=lambda: CarreraFormulario(self.root, self.db, self.carrera, self.actualizar_vista))
        editar_btn.pack(anchor='e', pady=(5, 0))
        
        # Selectores de jornada y semestre
        selectores_frame = tk.Frame(left_frame, bg='#f0f0f0')
        selectores_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(selectores_frame, text="Jornada:", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w')
        self.jornada_var = tk.StringVar(value=self.carrera["jornada"])
        tk.Radiobutton(selectores_frame, text="Diurna", variable=self.jornada_var, value="Diurna", 
                      bg='#f0f0f0', font=("Arial", 10)).pack(anchor='w')
        tk.Radiobutton(selectores_frame, text="Vespertina", variable=self.jornada_var, value="Vespertina", 
                      bg='#f0f0f0', font=("Arial", 10)).pack(anchor='w')
        
        # Selector de semestre para filtrar módulos
        tk.Label(selectores_frame, text="Filtrar por Semestre:", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 0))
        
        semestre_filter_frame = tk.Frame(selectores_frame, bg='#f0f0f0')
        semestre_filter_frame.pack(fill='x', pady=(5, 0))
        
        self.semestre_filter_var = tk.StringVar(value="Todos")
        
        # Opción "Todos"
        tk.Radiobutton(semestre_filter_frame, text="Todos los semestres", 
                      variable=self.semestre_filter_var, value="Todos", 
                      bg='#f0f0f0', font=("Arial", 10),
                      command=self.filtrar_modulos_por_semestre).pack(anchor='w')
        
        # Opciones específicas de semestres de la carrera
        semestres_carrera = self.db.obtener_semestres_carrera(self.carrera["id"])
        for semestre in semestres_carrera:
            tk.Radiobutton(semestre_filter_frame, text=f"Semestre {semestre}", 
                          variable=self.semestre_filter_var, value=semestre, 
                          bg='#f0f0f0', font=("Arial", 10),
                          command=self.filtrar_modulos_por_semestre).pack(anchor='w')
        
        # Lista de docentes
        tk.Label(left_frame, text="DOCENTES", font=("Arial", 14, "bold"), 
                bg='#f0f0f0', fg='#2c3e50').pack(anchor='w', pady=(20, 10))
        
        self.docentes_frame = tk.Frame(left_frame, bg='#f0f0f0')
        self.docentes_frame.pack(fill='both', expand=True)
        
        self.actualizar_lista_docentes()
        
        # Botón añadir docente
        add_docente_btn = tk.Button(left_frame, text="AÑADIR DOCENTE", font=("Arial", 10, "bold"), 
                                   command=lambda: DocenteFormulario(self.root, self.db, None, self.actualizar_lista_docentes), 
                                   bg='#27ae60', fg='white')
        add_docente_btn.pack(fill='x', pady=(10, 0))
        
        # Columna derecha (75%)
        right_frame = tk.Frame(content_frame, bg='#f0f0f0')
        right_frame.pack(side='left', fill='both', expand=True, padx=(20, 0))
        
        tk.Label(right_frame, text="MÓDULOS", font=("Arial", 14, "bold"), 
                bg='#f0f0f0', fg='#2c3e50').pack(anchor='w', pady=(0, 10))
        
        # Grid de módulos
        self.modulos_frame = tk.Frame(right_frame, bg='#f0f0f0')
        self.modulos_frame.pack(fill='both', expand=True)
        
        self.actualizar_grid_modulos()
        
        # Botón añadir módulo
        add_modulo_btn = tk.Button(right_frame, text="AÑADIR MÓDULO", font=("Arial", 10, "bold"), 
                                  command=lambda: ModuloFormulario(self.root, self.db, self.carrera, None, self.actualizar_grid_modulos), 
                                  bg='#27ae60', fg='white')
        add_modulo_btn.pack(fill='x', pady=(10, 0))
    
    def actualizar_vista(self):
        self.mostrar_vista()
    
    def filtrar_modulos_por_semestre(self):
        """Filtra los módulos mostrados según el semestre seleccionado"""
        self.semestre_actual = self.semestre_filter_var.get()
        self.actualizar_grid_modulos()
    
    def actualizar_lista_docentes(self):
        # Limpiar frame de docentes
        for widget in self.docentes_frame.winfo_children():
            widget.destroy()
        
        # Obtener docentes desde la base de datos
        docentes = self.db.obtener_docentes()
        
        # Mostrar cada docente
        for docente in docentes:
            docente_frame = tk.Frame(self.docentes_frame, bg='white', relief='raised', bd=1)
            docente_frame.pack(fill='x', pady=5)
            
            # Hacer la tarjeta clickeable
            docente_frame.bind("<Button-1>", lambda e, d=docente: VistaDocente(self.root, self.db, d, self.carrera, self.mostrar_vista))
            
            # Información del docente
            info_frame = tk.Frame(docente_frame, bg='white')
            info_frame.pack(fill='x', padx=10, pady=10)
            info_frame.bind("<Button-1>", lambda e, d=docente: VistaDocente(self.root, self.db, d, self.carrera, self.mostrar_vista))
            
            # Nombre y título
            nombre_label = tk.Label(info_frame, text=docente["nombre"], font=("Arial", 12, "bold"), 
                    bg='white', fg='#2c3e50')
            nombre_label.pack(anchor='w')
            nombre_label.bind("<Button-1>", lambda e, d=docente: VistaDocente(self.root, self.db, d, self.carrera, self.mostrar_vista))
            
            titulo_label = tk.Label(info_frame, text=docente["titulo"], font=("Arial", 10), 
                    bg='white', fg='#7f8c8d')
            titulo_label.pack(anchor='w')
            titulo_label.bind("<Button-1>", lambda e, d=docente: VistaDocente(self.root, self.db, d, self.carrera, self.mostrar_vista))
            
            contrato_label = tk.Label(info_frame, text=f"Contrato: {docente['contrato']}", font=("Arial", 10), 
                    bg='white', fg='#7f8c8d')
            contrato_label.pack(anchor='w')
            contrato_label.bind("<Button-1>", lambda e, d=docente: VistaDocente(self.root, self.db, d, self.carrera, self.mostrar_vista))
            
            # Barra de horas
            horas_frame = tk.Frame(docente_frame, bg='white')
            horas_frame.pack(fill='x', padx=10, pady=(0, 10))
            horas_frame.bind("<Button-1>", lambda e, d=docente: VistaDocente(self.root, self.db, d, self.carrera, self.mostrar_vista))
            
            # Barra de progreso
            total_horas = docente["horas_contratadas"]
            horas_asignadas = docente["horas_asignadas"]
            porcentaje = (horas_asignadas / total_horas) * 100 if total_horas > 0 else 0
            
            # Crear barra de progreso visual
            bar_frame = tk.Frame(horas_frame, bg='#ecf0f1', height=20, width=200)
            bar_frame.pack(side='left', fill='x', expand=True)
            bar_frame.pack_propagate(False)
            bar_frame.bind("<Button-1>", lambda e, d=docente: VistaDocente(self.root, self.db, d, self.carrera, self.mostrar_vista))
            
            # Parte asignada
            asignada_frame = tk.Frame(bar_frame, bg='#e74c3c', height=20)
            asignada_frame.place(relwidth=porcentaje/100, relheight=1)
            
            # Texto de horas
            horas_label = tk.Label(horas_frame, text=f"{horas_asignadas}/{total_horas} hrs", 
                    font=("Arial", 10), bg='white')
            horas_label.pack(side='right', padx=(10, 0))
            horas_label.bind("<Button-1>", lambda e, d=docente: VistaDocente(self.root, self.db, d, self.carrera, self.mostrar_vista))
            
            # Botón para editar docente
            edit_btn = tk.Button(docente_frame, text="Editar", font=("Arial", 8),
                                command=lambda d=docente: DocenteFormulario(self.root, self.db, d, self.actualizar_lista_docentes),
                                bg='#3498db', fg='white')
            edit_btn.pack(anchor='e', padx=10, pady=(0, 10))
    
    def actualizar_grid_modulos(self):
        # Limpiar frame de módulos
        for widget in self.modulos_frame.winfo_children():
            widget.destroy()
        
        # Obtener módulos de la carrera desde la base de datos
        modulos = self.db.obtener_modulos_carrera(self.carrera["id"])
        
        # Si no hay módulos, mostrar mensaje
        if not modulos:
            mensaje_frame = tk.Frame(self.modulos_frame, bg='#f0f0f0')
            mensaje_frame.pack(fill='both', expand=True)
            
            tk.Label(mensaje_frame, text="No hay módulos en esta carrera", font=("Arial", 12), 
                    bg='#f0f0f0', fg='#7f8c8d').pack(expand=True)
            return
        
        # Filtrar módulos por semestre
        modulos_filtrados = []
        for modulo in modulos:
            if self.semestre_actual == "Todos" or modulo.get("semestre", "") == self.semestre_actual:
                modulos_filtrados.append(modulo)
        
        # Crear grid de módulos (3 columnas, 5 filas) con los módulos filtrados
        row, col = 0, 0
        for modulo in modulos_filtrados:
            modulo_frame = tk.Frame(self.modulos_frame, bg='white', relief='raised', bd=1, width=200, height=120)
            modulo_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            modulo_frame.grid_propagate(False)
            
            # Nombre del módulo
            tk.Label(modulo_frame, text=modulo["nombre"], font=("Arial", 10, "bold"), 
                    bg='white', fg='#2c3e50', wraplength=180).pack(padx=10, pady=(10, 5))
            
            # Código y docente
            tk.Label(modulo_frame, text=f"Código: {modulo['codigo']}", font=("Arial", 9), 
                    bg='white', fg='#7f8c8d').pack(anchor='w', padx=10)
            tk.Label(modulo_frame, text=f"Docente: {modulo.get('docente_nombre', 'No asignado')}", font=("Arial", 9), 
                    bg='white', fg='#7f8c8d').pack(anchor='w', padx=10)
            
            # Mostrar semestre del módulo
            semestre_modulo = modulo.get("semestre", "No asignado")
            tk.Label(modulo_frame, text=f"Semestre: {semestre_modulo}", font=("Arial", 9), 
                    bg='white', fg='#7f8c8d').pack(anchor='w', padx=10)
            
            # Configurar el comando al hacer clic
            modulo_frame.bind("<Button-1>", lambda e, m=modulo: ModuloFormulario(self.root, self.db, self.carrera, m, self.actualizar_grid_modulos))
            for child in modulo_frame.winfo_children():
                child.bind("<Button-1>", lambda e, m=modulo: ModuloFormulario(self.root, self.db, self.carrera, m, self.actualizar_grid_modulos))
            
            # Actualizar fila y columna
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        # Mostrar mensaje si no hay módulos filtrados
        if not modulos_filtrados:
            mensaje_frame = tk.Frame(self.modulos_frame, bg='#f0f0f0')
            mensaje_frame.grid(row=0, column=0, columnspan=3, sticky='nsew')
            
            mensaje = "No hay módulos en este semestre" if self.semestre_actual != "Todos" else "No hay módulos en esta carrera"
            tk.Label(mensaje_frame, text=mensaje, font=("Arial", 12), 
                    bg='#f0f0f0', fg='#7f8c8d').pack(expand=True)
        
        # Configurar el grid para que se expanda
        for i in range(3):
            self.modulos_frame.columnconfigure(i, weight=1)
        for i in range(5):
            self.modulos_frame.rowconfigure(i, weight=1)