# vista_docente.py - VERSIÓN CORREGIDA
import tkinter as tk
from tkinter import ttk
from gestion_docentes import DocenteFormulario
from gestion_modulos import ModuloFormulario

class ToolTip:
    """Clase para crear tooltips en widgets"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        if self.tooltip:
            return
        
        # Posición del tooltip
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        
        # Crear ventana de tooltip
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        # Label con el texto
        label = tk.Label(self.tooltip, text=self.text, justify='left',
                        background="#ffffe0", relief='solid', borderwidth=1,
                        font=("Arial", 10))
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class VistaDocente:
    def __init__(self, root, db, docente, carrera_actual=None, callback_volver=None):
        self.root = root
        self.db = db
        self.docente = docente
        self.carrera_actual = carrera_actual
        self.callback_volver = callback_volver
        
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
        
        tk.Label(top_bar, text="CEDUC - Vista del Docente", font=("Arial", 14, "bold"), 
                bg='#2c3e50', fg='white').pack(side='left', padx=20, pady=10)
        
        # Botón para volver
        if self.carrera_actual:
            volver_btn = tk.Button(top_bar, text="Volver a Carrera", font=("Arial", 10), 
                                  command=self.callback_volver, bg='#3498db', fg='white')
        else:
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
        
        # Información del docente
        info_frame = tk.Frame(left_frame, bg='white', relief='raised', bd=1)
        info_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(info_frame, text="INFORMACIÓN DEL DOCENTE", font=("Arial", 12, "bold"), 
                bg='white', fg='#2c3e50').pack(anchor='w', padx=10, pady=(10, 5))
        
        # Foto de perfil (placeholder)
        foto_frame = tk.Frame(info_frame, bg='white', width=80, height=80)
        foto_frame.pack(anchor='w', padx=10, pady=(0, 10))
        foto_frame.pack_propagate(False)
        
        # Simular foto de perfil con un círculo
        foto_canvas = tk.Canvas(foto_frame, width=80, height=80, bg='white', highlightthickness=0)
        foto_canvas.pack()
        foto_canvas.create_oval(5, 5, 75, 75, fill='#3498db', outline='#2980b9')
        foto_canvas.create_text(40, 40, text="Foto", fill='white', font=("Arial", 10, "bold"))
        
        tk.Label(info_frame, text=self.docente["nombre"], font=("Arial", 14, "bold"), 
                bg='white', fg='#2c3e50').pack(anchor='w', padx=10, pady=(0, 5))
        
        tk.Label(info_frame, text=self.docente["titulo"], font=("Arial", 11), 
                bg='white', fg='#7f8c8d').pack(anchor='w', padx=10, pady=(0, 5))
        
        tk.Label(info_frame, text=f"Contrato: {self.docente['contrato']}", font=("Arial", 10), 
                bg='white', fg='#7f8c8d').pack(anchor='w', padx=10, pady=(0, 5))
        
        tk.Label(info_frame, text=f"Email: {self.docente['email']}", font=("Arial", 10), 
                bg='white', fg='#7f8c8d').pack(anchor='w', padx=10, pady=(0, 5))
        
        tk.Label(info_frame, text=f"Evaluación: {self.docente.get('evaluacion', 'N/A')}", font=("Arial", 10), 
                bg='white', fg='#7f8c8d').pack(anchor='w', padx=10, pady=(0, 10))
        
        # Barra de horas
        horas_frame = tk.Frame(info_frame, bg='white')
        horas_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        total_horas = self.docente["horas_contratadas"]
        horas_asignadas = self.docente["horas_asignadas"]
        porcentaje = (horas_asignadas / total_horas) * 100 if total_horas > 0 else 0
        
        # Crear barra de progreso visual
        bar_frame = tk.Frame(horas_frame, bg='#ecf0f1', height=20, width=200)
        bar_frame.pack(side='left', fill='x', expand=True)
        bar_frame.pack_propagate(False)
        
        # Parte asignada
        asignada_frame = tk.Frame(bar_frame, bg='#e74c3c', height=20)
        asignada_frame.place(relwidth=porcentaje/100, relheight=1)
        
        # Texto de horas
        tk.Label(horas_frame, text=f"{horas_asignadas}/{total_horas} hrs", 
                font=("Arial", 10), bg='white').pack(side='right', padx=(10, 0))
        
        # Botón editar docente
        editar_btn = tk.Button(info_frame, text="Editar Docente", font=("Arial", 10),
                              command=lambda: DocenteFormulario(self.root, self.db, self.docente, self.actualizar_vista), 
                              bg='#3498db', fg='white')
        editar_btn.pack(anchor='e', padx=10, pady=(0, 10))
        
        # Módulos asignados al docente
        modulos_frame = tk.Frame(left_frame, bg='#f0f0f0')
        modulos_frame.pack(fill='both', expand=True)
        
        tk.Label(modulos_frame, text="MÓDULOS ASIGNADOS", font=("Arial", 12, "bold"), 
                bg='#f0f0f0', fg='#2c3e50').pack(anchor='w', pady=(0, 10))
        
        # Frame con scroll para módulos
        modulos_scroll_frame = tk.Frame(modulos_frame, bg='#f0f0f0')
        modulos_scroll_frame.pack(fill='both', expand=True)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(modulos_scroll_frame, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(modulos_scroll_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Lista de módulos del docente
        self.modulos_docente_frame = tk.Frame(scrollable_frame, bg='#f0f0f0')
        self.modulos_docente_frame.pack(fill='both', expand=True)
        
        # Obtener módulos del docente desde la base de datos
        self.modulos_docente = self.obtener_modulos_docente()
        self.actualizar_lista_modulos()
        
        # Botón añadir módulo
        add_modulo_btn = tk.Button(left_frame, text="AÑADIR MÓDULO", font=("Arial", 10, "bold"), 
                                  command=self.añadir_modulo, bg='#27ae60', fg='white')
        add_modulo_btn.pack(fill='x', pady=(10, 0))
        
        # Columna derecha (75%)
        right_frame = tk.Frame(content_frame, bg='#f0f0f0')
        right_frame.pack(side='left', fill='both', expand=True, padx=(20, 0))
        
        tk.Label(right_frame, text="HORARIO SEMANAL - DISPONIBILIDAD Y MÓDULOS", font=("Arial", 14, "bold"), 
                bg='#f0f0f0', fg='#2c3e50').pack(anchor='w', pady=(0, 10))
        
        # Frame para la grilla unificada
        horario_frame = tk.Frame(right_frame, bg='#f0f0f0')
        horario_frame.pack(fill='both', expand=True)
        
        # Crear grilla unificada
        self.crear_grilla_unificada(horario_frame)
    
    def obtener_modulos_docente(self):
        """Obtiene los módulos asignados al docente desde la base de datos"""
        # Obtener todas las carreras
        carreras = self.db.obtener_carreras()
        modulos_docente = []
        
        for carrera in carreras:
            # Obtener módulos de cada carrera
            modulos_carrera = self.db.obtener_modulos_carrera(carrera["id"])
            for modulo in modulos_carrera:
                # Verificar si el módulo está asignado a este docente
                if modulo.get("docente_id") == self.docente["id"]:
                    modulo_con_info = modulo.copy()
                    modulo_con_info["carrera"] = carrera["nombre"]
                    modulos_docente.append(modulo_con_info)
        
        return modulos_docente
    
    def añadir_modulo(self):
        """Abre el formulario para añadir un nuevo módulo"""
        # Si hay una carrera actual, usarla, sino pedir seleccionar una
        if self.carrera_actual:
            ModuloFormulario(self.root, self.db, self.carrera_actual, None, self.actualizar_vista)
        else:
            # En una implementación completa, aquí se pediría seleccionar una carrera
            from tkinter import messagebox
            messagebox.showinfo("Información", "Para añadir un módulo, diríjase a la vista de la carrera correspondiente.")
    
    def actualizar_vista(self):
        """Actualiza toda la vista"""
        self.mostrar_vista()
    
    def actualizar_lista_modulos(self):
        """Actualiza la lista de módulos del docente"""
        # Limpiar frame de módulos
        for widget in self.modulos_docente_frame.winfo_children():
            widget.destroy()
        
        if not self.modulos_docente:
            tk.Label(self.modulos_docente_frame, text="No hay módulos asignados", 
                    font=("Arial", 10), bg='#f0f0f0', fg='#7f8c8d').pack(anchor='w', pady=10)
            return
        
        for modulo in self.modulos_docente:
            modulo_frame = tk.Frame(self.modulos_docente_frame, bg='white', relief='raised', bd=1)
            modulo_frame.pack(fill='x', pady=5)
            
            # Nombre del módulo (más grande)
            tk.Label(modulo_frame, text=modulo["nombre"], font=("Arial", 11, "bold"), 
                    bg='white', fg='#2c3e50', wraplength=250, justify='left').pack(anchor='w', padx=10, pady=5)
            
            # Información adicional
            info_frame = tk.Frame(modulo_frame, bg='white')
            info_frame.pack(fill='x', padx=10, pady=(0, 10))
            
            tk.Label(info_frame, text=f"Carrera: {modulo['carrera']}", font=("Arial", 9), 
                    bg='white', fg='#7f8c8d', justify='left').pack(anchor='w')
            
            tk.Label(info_frame, text=f"Código: {modulo['codigo']} | Sala: {modulo.get('sala_nombre', 'No asignada')}", 
                    font=("Arial", 9), bg='white', fg='#7f8c8d', justify='left').pack(anchor='w')
            
            tk.Label(info_frame, text=f"Horas: T{modulo['horas_teoricas']} P{modulo['horas_practicas']} | Alumnos: {modulo['alumnos_proyectados']}", 
                    font=("Arial", 9), bg='white', fg='#7f8c8d', justify='left').pack(anchor='w')
            
            # Horarios específicos
            horarios = self.db.obtener_horarios_modulo(modulo["id"])
            if horarios:
                horarios_text = "Horarios: " + ", ".join([f"{h['dia']} {h['hora_inicio']}-{h['hora_fin']}" for h in horarios])
                tk.Label(info_frame, text=horarios_text, font=("Arial", 8), 
                        bg='white', fg='#7f8c8d', justify='left', wraplength=250).pack(anchor='w')
    
    def crear_grilla_unificada(self, parent):
        """Crea una grilla que combina disponibilidad y módulos asignados"""
        # Frame principal de la grilla
        grilla_frame = tk.Frame(parent, bg='white', relief='sunken', bd=1)
        grilla_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Configurar grid para la grilla
        for i in range(6):  # 5 días + 1 columna para horas
            grilla_frame.columnconfigure(i, weight=1)
        for i in range(10):  # 9 horas + 1 fila para encabezados
            grilla_frame.rowconfigure(i, weight=1)
        
        # Encabezados de días
        dias = ["Hora", "LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES"]
        for i, dia in enumerate(dias):
            label = tk.Label(grilla_frame, text=dia, font=("Arial", 10, "bold"), 
                           bg='#34495e', fg='white', relief='raised', bd=1)
            label.grid(row=0, column=i, sticky='nsew', padx=1, pady=1)
        
        # Horas y celdas combinadas
        horas = ["8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
        for i, hora in enumerate(horas):
            # Etiqueta de la hora
            label = tk.Label(grilla_frame, text=hora, font=("Arial", 9), 
                           bg='#34495e', fg='white', relief='raised', bd=1)
            label.grid(row=i+1, column=0, sticky='nsew', padx=1, pady=1)
            
            # Celdas para cada día
            for j in range(1, 6):  # Columnas 1-5 para los días
                celda = tk.Frame(grilla_frame, relief='raised', bd=1)
                celda.grid(row=i+1, column=j, sticky='nsew', padx=1, pady=1)
                
                # Verificar disponibilidad del docente
                dia_semana = dias[j]  # LUNES, MARTES, etc.
                disponible = self.verificar_disponibilidad(dia_semana, hora)
                
                # Verificar si hay módulos en este horario
                modulos_en_horario = self.obtener_modulos_por_horario(dia_semana, hora)
                print(f"Día: {dia_semana}, Hora: {hora}, Módulos: {modulos_en_horario}")
                
                # Determinar el color y contenido de la celda
                if modulos_en_horario:
                    # Hay módulos - color azul
                    color = '#3498db'
                    texto = self.obtener_texto_modulos(modulos_en_horario)
                    tooltip_text = self.obtener_tooltip_modulos(modulos_en_horario, dia_semana)
                elif disponible:
                    # Disponible y sin módulos - color verde
                    color = '#2ecc71'
                    texto = "Disponible"
                    tooltip_text = f"{dia_semana} {hora}\nDisponible"
                else:
                    # No disponible - color rojo
                    color = '#e74c3c'
                    texto = "No Disponible"
                    tooltip_text = f"{dia_semana} {hora}\nNo Disponible"
                
                # Configurar celda
                celda.configure(bg=color)
                
                # Texto en la celda
                label_celda = tk.Label(celda, text=texto, font=("Arial", 8), 
                                      bg=color, fg='white', wraplength=100, justify='center')
                label_celda.pack(expand=True, fill='both', padx=2, pady=2)
                
                # Agregar tooltip
                ToolTip(celda, tooltip_text)
                ToolTip(label_celda, tooltip_text)
    
    def verificar_disponibilidad(self, dia, hora):
        """Verifica la disponibilidad del docente en un día y hora específicos"""
        disponibilidad = self.db.obtener_disponibilidad_docente(self.docente["id"])
        if dia in disponibilidad and hora in disponibilidad[dia]:
            return disponibilidad[dia][hora]
        return True  # Por defecto, disponible
    
    def obtener_modulos_por_horario(self, dia, hora):
        """Obtiene los módulos que coinciden con el día y hora especificados"""
        modulos_en_horario = []
        for modulo in self.modulos_docente:
            horarios = self.db.obtener_horarios_modulo(modulo["id"])
            for horario in horarios:
                if horario["dia"] == dia and self.hora_en_rango(hora, horario["hora_inicio"], horario["hora_fin"]):
                    modulos_en_horario.append(modulo)
                    break  # Solo una vez por módulo
        return modulos_en_horario
    
    def hora_en_rango(self, hora_actual, hora_inicio, hora_fin):
        """Verifica si una hora está dentro de un rango"""
        def hora_a_minutos(hora_str):
            partes = hora_str.split(':')
            return int(partes[0]) * 60 + int(partes[1])
        
        actual_min = hora_a_minutos(hora_actual)
        inicio_min = hora_a_minutos(hora_inicio)
        fin_min = hora_a_minutos(hora_fin)
        
        return actual_min >= inicio_min and actual_min < fin_min
    
    def obtener_texto_modulos(self, modulos):
        """Obtiene el texto a mostrar en la celda para múltiples módulos"""
        textos = []
        for modulo in modulos:
            nombre = modulo["nombre"]
            if len(nombre) > 20:
                textos.append(nombre[:20] + "...")
            else:
                textos.append(nombre)
        return "\n".join(textos)
    
    def obtener_tooltip_modulos(self, modulos, dia):
        """Obtiene el texto del tooltip para múltiples módulos"""
        tooltip_text = ""
        for i, modulo in enumerate(modulos):
            tooltip_text += f"Módulo {i+1}: {modulo['nombre']}\n"
            tooltip_text += f"Carrera: {modulo['carrera']}\n"
            tooltip_text += f"Código: {modulo['codigo']}\n"
            tooltip_text += f"Sala: {modulo.get('sala_nombre', 'No asignada')}\n"
            
            # Horarios específicos de este módulo para este día
            horarios = self.db.obtener_horarios_modulo(modulo["id"])
            horarios_dia = [h for h in horarios if h['dia'] == dia]
            for horario in horarios_dia:
                tooltip_text += f"Horario: {horario['hora_inicio']} - {horario['hora_fin']}\n"
            
            tooltip_text += "---\n" if i < len(modulos) - 1 else ""
        
        return tooltip_text