# panel_principal.py - VERSIÓN COMPLETA CORREGIDA
import tkinter as tk
from gestion_salas import SalaFormulario
from gestion_carreras import CarreraFormulario
from gestion_carreras import VistaModulosCarrera

class PanelPrincipal:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        
        self.mostrar_panel_principal()
    
    def mostrar_panel_principal(self):
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
        
        tk.Label(top_bar, text="CEDUC - Sistema de Gestión Académica", font=("Arial", 14, "bold"), 
                bg='#2c3e50', fg='white').pack(side='left', padx=20, pady=10)
        
        # Contenido principal dividido en dos columnas
        content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Columna izquierda (25%) - Salas
        left_frame = tk.Frame(content_frame, bg='#f0f0f0', width=300)
        left_frame.pack(side='left', fill='y')
        left_frame.pack_propagate(False)
        
        tk.Label(left_frame, text="SALAS", font=("Arial", 16, "bold"), 
                bg='#f0f0f0', fg='#2c3e50').pack(anchor='w', pady=(0, 10))
        
        # Lista de salas
        self.salas_frame = tk.Frame(left_frame, bg='#f0f0f0')
        self.salas_frame.pack(fill='both', expand=True)
        
        self.actualizar_lista_salas()
        
        # Botón añadir sala
        add_sala_btn = tk.Button(left_frame, text="AÑADIR SALA", font=("Arial", 10, "bold"), 
                                command=self.mostrar_formulario_sala, bg='#27ae60', fg='white')
        add_sala_btn.pack(fill='x', pady=(10, 0))
        
        # Columna derecha (75%) - Carreras
        right_frame = tk.Frame(content_frame, bg='#f0f0f0')
        right_frame.pack(side='left', fill='both', expand=True, padx=(20, 0))
        
        tk.Label(right_frame, text="CARRERAS", font=("Arial", 16, "bold"), 
                bg='#f0f0f0', fg='#2c3e50').pack(anchor='w', pady=(0, 10))
        
        # Grid de carreras (3 columnas, 5 filas)
        self.carreras_frame = tk.Frame(right_frame, bg='#f0f0f0')
        self.carreras_frame.pack(fill='both', expand=True)
        
        self.actualizar_grid_carreras()
        
        # Botón añadir carrera
        add_carrera_btn = tk.Button(right_frame, text="AÑADIR CARRERA", font=("Arial", 10, "bold"), 
                                   command=self.mostrar_formulario_carrera, bg='#27ae60', fg='white')
        add_carrera_btn.pack(fill='x', pady=(10, 0))
    
    def actualizar_lista_salas(self):
        # Limpiar frame de salas
        for widget in self.salas_frame.winfo_children():
            widget.destroy()
        
        # Obtener salas desde la base de datos
        salas = self.db.obtener_salas()
        
        # Mostrar cada sala
        for sala in salas:
            sala_frame = tk.Frame(self.salas_frame, bg='white', relief='raised', bd=1)
            sala_frame.pack(fill='x', pady=5)
            
            # Nombre de la sala
            tk.Label(sala_frame, text=sala["nombre"], font=("Arial", 12, "bold"), 
                    bg='white', fg='#2c3e50').pack(anchor='w', padx=10, pady=(10, 5))
            
            # Barra de horas disponibles
            horas_frame = tk.Frame(sala_frame, bg='white')
            horas_frame.pack(fill='x', padx=10, pady=(0, 10))
            
            # Para simplificar, mostramos solo las horas disponibles
            # En una implementación real, calcularíamos las horas ocupadas
            total_horas = sala["horas_disponibles"]
            
            # Crear barra de progreso visual
            bar_frame = tk.Frame(horas_frame, bg='#ecf0f1', height=20, width=200)
            bar_frame.pack(side='left', fill='x', expand=True)
            bar_frame.pack_propagate(False)
            
            # Texto de horas (solo disponibles por ahora)
            tk.Label(horas_frame, text=f"{total_horas} hrs disponibles", 
                    font=("Arial", 10), bg='white').pack(side='right', padx=(10, 0))
            
            # Botón para editar sala
            edit_btn = tk.Button(sala_frame, text="Editar", font=("Arial", 8),
                                command=lambda s=sala: self.mostrar_formulario_sala(s),
                                bg='#3498db', fg='white')
            edit_btn.pack(anchor='e', padx=10, pady=(0, 10))
    
    def actualizar_grid_carreras(self):
        # Limpiar frame de carreras
        for widget in self.carreras_frame.winfo_children():
            widget.destroy()
        
        # Obtener carreras desde la base de datos
        carreras = self.db.obtener_carreras()
        
        # Crear grid de carreras (3 columnas, 5 filas)
        row, col = 0, 0
        for carrera in carreras:
            carrera_frame = tk.Frame(self.carreras_frame, bg='white', relief='raised', bd=1, width=200, height=100)
            carrera_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            carrera_frame.grid_propagate(False)
            
            # Nombre de la carrera
            tk.Label(carrera_frame, text=carrera["nombre"], font=("Arial", 10, "bold"), 
                    bg='white', fg='#2c3e50', wraplength=180).pack(expand=True, fill='both', padx=10, pady=10)
            
            # Configurar el comando al hacer clic
            carrera_frame.bind("<Button-1>", lambda e, c=carrera: self.mostrar_modulos_carrera(c))
            for child in carrera_frame.winfo_children():
                child.bind("<Button-1>", lambda e, c=carrera: self.mostrar_modulos_carrera(c))
            
            # Actualizar fila y columna
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        # Configurar el grid para que se expanda
        for i in range(3):
            self.carreras_frame.columnconfigure(i, weight=1)
        for i in range(5):
            self.carreras_frame.rowconfigure(i, weight=1)
    
    def mostrar_formulario_sala(self, sala=None):
        SalaFormulario(self.root, self.db, sala, self.actualizar_lista_salas)
    
    def mostrar_formulario_carrera(self, carrera=None):
        CarreraFormulario(self.root, self.db, carrera, self.actualizar_grid_carreras)
    
    def mostrar_modulos_carrera(self, carrera):
        VistaModulosCarrera(self.root, self.db, carrera, self.mostrar_panel_principal)