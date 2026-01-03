# gestion_modulos.py
import tkinter as tk
from tkinter import ttk, messagebox

class ModuloFormulario:
    def __init__(self, root, db, carrera, modulo=None, callback_actualizar=None):
        self.root = root
        self.db = db
        self.carrera = carrera
        self.modulo = modulo
        self.callback_actualizar = callback_actualizar
        self.horarios = []
        
        self.mostrar_formulario()
    
    def mostrar_formulario(self):
        # Crear ventana de formulario - Aumentar altura para incluir horarios
        self.form_window = tk.Toplevel(self.root)
        self.form_window.title("Añadir/Editar Módulo" if not self.modulo else "Editar Módulo")
        self.form_window.geometry("600x700")  # Aumentada la altura y ancho
        self.form_window.configure(bg='#f0f0f0')
        self.form_window.transient(self.root)
        self.form_window.grab_set()
        
        # Frame principal con scroll
        main_frame = tk.Frame(self.form_window, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Canvas y scrollbar
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
        
        tk.Label(scrollable_frame, text="Datos del Módulo", font=("Arial", 16, "bold"), 
                bg='#f0f0f0', fg='#2c3e50').pack(anchor='w', pady=(0, 20))
        
        # Campos del formulario
        tk.Label(scrollable_frame, text="Nombre", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        self.nombre_entry = tk.Entry(scrollable_frame, font=("Arial", 12), width=40)
        self.nombre_entry.pack(fill='x', pady=(0, 10))
        
        tk.Label(scrollable_frame, text="Código", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        self.codigo_entry = tk.Entry(scrollable_frame, font=("Arial", 12), width=40)
        self.codigo_entry.pack(fill='x', pady=(0, 10))
        
        # Selector de semestre
        tk.Label(scrollable_frame, text="Semestre", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        semestres_carrera = self.db.obtener_semestres_carrera(self.carrera["id"])
        self.semestre_var = tk.StringVar(value=semestres_carrera[0] if semestres_carrera else "")
        self.semestre_combo = ttk.Combobox(scrollable_frame, textvariable=self.semestre_var, font=("Arial", 12), width=38)
        self.semestre_combo['values'] = semestres_carrera
        self.semestre_combo.pack(fill='x', pady=(0, 10))
        
        tk.Label(scrollable_frame, text="Docente Asignado", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        self.docente_var = tk.StringVar()
        self.docente_combo = ttk.Combobox(scrollable_frame, textvariable=self.docente_var, font=("Arial", 12), width=38)
        
        # Obtener docentes desde BD
        docentes = self.db.obtener_docentes()
        self.docente_combo['values'] = [f"{docente['id']}: {docente['nombre']}" for docente in docentes]
        self.docente_combo.pack(fill='x', pady=(0, 10))
        
        tk.Label(scrollable_frame, text="Alumnos Proyectados", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        self.alumnos_entry = tk.Entry(scrollable_frame, font=("Arial", 12), width=30)
        self.alumnos_entry.pack(fill='x', pady=(0, 10))
        
        tk.Label(scrollable_frame, text="Horas Teóricas", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        self.horas_teoricas_entry = tk.Entry(scrollable_frame, font=("Arial", 12), width=30)
        self.horas_teoricas_entry.pack(fill='x', pady=(0, 10))
        
        tk.Label(scrollable_frame, text="Horas Prácticas", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        self.horas_practicas_entry = tk.Entry(scrollable_frame, font=("Arial", 12), width=30)
        self.horas_practicas_entry.pack(fill='x', pady=(0, 10))
        
        tk.Label(scrollable_frame, text="Sala Asignada", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w', pady=(10, 5))
        self.sala_var = tk.StringVar()
        self.sala_combo = ttk.Combobox(scrollable_frame, textvariable=self.sala_var, font=("Arial", 12), width=38)
        
        # Obtener salas asignadas a esta carrera desde BD
        salas_carrera = self.db.obtener_salas_carrera(self.carrera["id"])
        self.salas_disponibles = [f"{sala['id']}: {sala['nombre']}" for sala in salas_carrera]
        self.sala_combo['values'] = self.salas_disponibles
        
        # Si no hay salas asignadas a la carrera, mostrar mensaje
        if not self.salas_disponibles:
            self.sala_combo['values'] = ["No hay salas asignadas a esta carrera"]
            self.sala_combo.set("No hay salas asignadas a esta carrera")
            self.sala_combo.config(state="disabled")
        else:
            self.sala_combo.pack(fill='x', pady=(0, 20))
        
        # SECCIÓN DE HORARIOS
        tk.Label(scrollable_frame, text="Horarios del Módulo", font=("Arial", 14, "bold"), 
                bg='#f0f0f0', fg='#2c3e50').pack(anchor='w', pady=(20, 10))
        
        # Frame para agregar horarios
        horario_frame = tk.Frame(scrollable_frame, bg='#f0f0f0')
        horario_frame.pack(fill='x', pady=(0, 10))
        
        # Día
        tk.Label(horario_frame, text="Día:", font=("Arial", 10), bg='#f0f0f0').grid(row=0, column=0, padx=(0, 10))
        self.dia_var = tk.StringVar()
        dia_combo = ttk.Combobox(horario_frame, textvariable=self.dia_var, width=10, font=("Arial", 10))
        dia_combo['values'] = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES"]
        dia_combo.grid(row=0, column=1, padx=(0, 10))
        
        # Hora inicio
        tk.Label(horario_frame, text="Hora inicio:", font=("Arial", 10), bg='#f0f0f0').grid(row=0, column=2, padx=(0, 10))
        self.hora_inicio_var = tk.StringVar()
        hora_inicio_combo = ttk.Combobox(horario_frame, textvariable=self.hora_inicio_var, width=8, font=("Arial", 10))
        hora_inicio_combo['values'] = ["8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
        hora_inicio_combo.grid(row=0, column=3, padx=(0, 10))
        
        # Hora fin
        tk.Label(horario_frame, text="Hora fin:", font=("Arial", 10), bg='#f0f0f0').grid(row=0, column=4, padx=(0, 10))
        self.hora_fin_var = tk.StringVar()
        hora_fin_combo = ttk.Combobox(horario_frame, textvariable=self.hora_fin_var, width=8, font=("Arial", 10))
        hora_fin_combo['values'] = ["9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
        hora_fin_combo.grid(row=0, column=5, padx=(0, 10))
        
        # Botón agregar horario
        agregar_btn = tk.Button(horario_frame, text="Agregar Horario", font=("Arial", 10),
                               command=self.agregar_horario, bg='#3498db', fg='white')
        agregar_btn.grid(row=0, column=6, padx=(10, 0))
        
        # Lista de horarios
        self.horarios_frame = tk.Frame(scrollable_frame, bg='#f0f0f0')
        self.horarios_frame.pack(fill='x', pady=(10, 20))
        
        # Si estamos editando, llenar los campos y cargar horarios existentes
        if self.modulo:
            self.nombre_entry.insert(0, self.modulo["nombre"])
            self.codigo_entry.insert(0, self.modulo["codigo"])
            self.semestre_var.set(self.modulo.get("semestre", semestres_carrera[0] if semestres_carrera else ""))
            
            # Configurar docente
            if self.modulo.get("docente_id"):
                docente_str = f"{self.modulo['docente_id']}: {self.modulo.get('docente_nombre', '')}"
                self.docente_var.set(docente_str)
            
            self.alumnos_entry.insert(0, str(self.modulo["alumnos_proyectados"]))
            self.horas_teoricas_entry.insert(0, str(self.modulo["horas_teoricas"]))
            self.horas_practicas_entry.insert(0, str(self.modulo["horas_practicas"]))
            
            # Configurar sala - verificar si la sala actual está en las salas disponibles
            if self.modulo.get("sala_id"):
                sala_actual_str = f"{self.modulo['sala_id']}: {self.modulo.get('sala_nombre', '')}"
                
                # Verificar si la sala actual está en las salas disponibles de la carrera
                sala_encontrada = False
                for sala_str in self.salas_disponibles:
                    if sala_str.startswith(str(self.modulo['sala_id']) + ":"):
                        self.sala_var.set(sala_str)
                        sala_encontrada = True
                        break
                
                # Si la sala actual no está en las salas disponibles, mostrarla igual pero deshabilitar el combo
                if not sala_encontrada:
                    self.sala_combo['values'] = [sala_actual_str] + self.salas_disponibles
                    self.sala_combo.set(sala_actual_str)
                    # Mostrar advertencia
                    tk.Label(scrollable_frame, 
                            text="⚠️ La sala asignada no está disponible para esta carrera. Debe cambiar la sala.",
                            font=("Arial", 9), bg='#f0f0f0', fg='#e74c3c').pack(anchor='w', pady=(0, 10))
            
            # Cargar horarios existentes
            self.horarios = self.db.obtener_horarios_modulo(self.modulo["id"])
            self.actualizar_lista_horarios()
        
        # Botones
        btn_frame = tk.Frame(scrollable_frame, bg='#f0f0f0')
        btn_frame.pack(fill='x', pady=(10, 0))
        
        guardar_btn = tk.Button(btn_frame, text="Guardar Cambios", font=("Arial", 12), 
                               command=self.guardar_modulo, bg='#3498db', fg='white')
        guardar_btn.pack(side='left', padx=(0, 10))
        
        cancelar_btn = tk.Button(btn_frame, text="Cancelar", font=("Arial", 12), 
                                command=self.form_window.destroy, bg='#95a5a6', fg='white')
        cancelar_btn.pack(side='left')
    
    def agregar_horario(self):
        """Agrega un horario a la lista"""
        dia = self.dia_var.get()
        hora_inicio = self.hora_inicio_var.get()
        hora_fin = self.hora_fin_var.get()
        
        if not dia or not hora_inicio or not hora_fin:
            messagebox.showerror("Error", "Todos los campos del horario son obligatorios")
            return
        
        # Validar que hora_inicio sea menor que hora_fin
        if self.comparar_horas(hora_inicio, hora_fin) >= 0:
            messagebox.showerror("Error", "La hora de inicio debe ser menor que la hora de fin")
            return
        
        # Agregar horario a la lista
        nuevo_horario = {
            "dia": dia,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin
        }
        
        self.horarios.append(nuevo_horario)
        self.actualizar_lista_horarios()
        
        # Limpiar campos
        self.dia_var.set("")
        self.hora_inicio_var.set("")
        self.hora_fin_var.set("")
    
    def comparar_horas(self, hora1, hora2):
        """Compara dos horas en formato HH:MM"""
        h1, m1 = map(int, hora1.split(':'))
        h2, m2 = map(int, hora2.split(':'))
        
        if h1 != h2:
            return h1 - h2
        return m1 - m2
    
    def actualizar_lista_horarios(self):
        """Actualiza la lista visual de horarios"""
        # Limpiar frame de horarios
        for widget in self.horarios_frame.winfo_children():
            widget.destroy()
        
        if not self.horarios:
            tk.Label(self.horarios_frame, text="No hay horarios asignados", 
                    font=("Arial", 10), bg='#f0f0f0', fg='#7f8c8d').pack(anchor='w')
            return
        
        for i, horario in enumerate(self.horarios):
            horario_frame = tk.Frame(self.horarios_frame, bg='white', relief='raised', bd=1)
            horario_frame.pack(fill='x', pady=2)
            
            texto = f"{horario['dia']}: {horario['hora_inicio']} - {horario['hora_fin']}"
            tk.Label(horario_frame, text=texto, font=("Arial", 10), 
                    bg='white', fg='#2c3e50').pack(side='left', padx=10, pady=5)
            
            # Botón para eliminar horario
            eliminar_btn = tk.Button(horario_frame, text="Eliminar", font=("Arial", 8),
                                    command=lambda idx=i: self.eliminar_horario(idx), 
                                    bg='#e74c3c', fg='white')
            eliminar_btn.pack(side='right', padx=10, pady=5)
    
    def eliminar_horario(self, index):
        """Elimina un horario de la lista"""
        if 0 <= index < len(self.horarios):
            self.horarios.pop(index)
            self.actualizar_lista_horarios()
    
    def guardar_modulo(self):
        nombre = self.nombre_entry.get()
        codigo = self.codigo_entry.get()
        semestre = self.semestre_var.get()
        
        # Obtener ID del docente
        docente_str = self.docente_var.get()
        docente_id = None
        if docente_str and ":" in docente_str:
            docente_id = int(docente_str.split(":")[0])
        
        # Obtener ID de la sala - validar que esté en las salas disponibles
        sala_str = self.sala_var.get()
        sala_id = None
        
        if not self.salas_disponibles:
            messagebox.showerror("Error", "No hay salas asignadas a esta carrera. Debe asignar salas a la carrera primero.")
            return
        
        if sala_str and ":" in sala_str:
            sala_id_candidato = int(sala_str.split(":")[0])
            
            # Verificar que la sala esté en las salas disponibles de la carrera
            sala_valida = False
            for sala_disponible in self.salas_disponibles:
                if sala_disponible.startswith(str(sala_id_candidato) + ":"):
                    sala_id = sala_id_candidato
                    sala_valida = True
                    break
            
            if not sala_valida:
                messagebox.showerror("Error", "La sala seleccionada no está asignada a esta carrera. Por favor, seleccione una sala válida.")
                return
        
        alumnos = self.alumnos_entry.get()
        horas_teoricas = self.horas_teoricas_entry.get()
        horas_practicas = self.horas_practicas_entry.get()
        
        if not nombre or not codigo or not semestre or not docente_id or not alumnos or not horas_teoricas or not horas_practicas or not sala_id:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        # Validar que alumnos y horas sean números
        try:
            alumnos = int(alumnos)
            horas_teoricas = int(horas_teoricas)
            horas_practicas = int(horas_practicas)
        except ValueError:
            messagebox.showerror("Error", "Alumnos y horas deben ser números")
            return
        
        # Validar que el semestre sea válido para la carrera
        semestres_carrera = self.db.obtener_semestres_carrera(self.carrera["id"])
        if semestre not in semestres_carrera:
            messagebox.showerror("Error", f"El semestre {semestre} no es válido para esta carrera")
            return
        
        # Validar que haya al menos un horario
        if not self.horarios:
            messagebox.showerror("Error", "Debe agregar al menos un horario para el módulo")
            return
        
        # Preparar datos para BD
        modulo_data = (nombre, codigo, horas_teoricas, horas_practicas, alumnos, 
                      self.carrera["id"], semestre, docente_id, sala_id)
        
        # Guardar en base de datos
        if self.modulo:
            # Actualizar módulo existente
            resultado = self.db.guardar_modulo(modulo_data, self.horarios, self.modulo["id"])
        else:
            # Insertar nuevo módulo
            resultado = self.db.guardar_modulo(modulo_data, self.horarios)
        
        if resultado:
            if self.callback_actualizar:
                self.callback_actualizar()
            self.form_window.destroy()
            messagebox.showinfo("Éxito", "Módulo guardado correctamente")
        else:
            messagebox.showerror("Error", "Error al guardar en la base de datos")