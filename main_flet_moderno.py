#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Gestión Académica - Versión Flet Moderna
CEDUC - Centro Educacional
Autor: MiniMax Agent

Esta es la versión modernizada con Flet del sistema de gestión académica.
Incluye una interfaz moderna con Material Design, componentes visuales mejorados,
y una experiencia de usuario optimizada.
"""

import flet as ft
import logging
import os
import threading
from database import SistemaDAO
from datetime import datetime
from typing import List, Dict, Any, Optional
from reportes import ReportGenerator
from chatbot import AIChatbot
from gestion_datos import GestionDatos

# Configurar logging para ver el flujo
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SistemaGestionFlet:
    """Sistema de Gestión Académica con Flet - Interfaz Moderna"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        
        # Splash screen variables
        self.splash_progress_bar = None
        self.splash_status_text = None
        self.splash_container = None
        
        self.dao = SistemaDAO()
        self.report_generator = ReportGenerator()
        self.chatbot = AIChatbot(self.dao, self.report_generator)
        self.usuario_actual = None
        self.ventana_activa = "splash"
        self.email_field = None
        self.password_field = None
        self.salas_list_view = None
        self.carreras_list_view = None
        self.docente_detalle_actual = None  # Track which teacher's detail view is open
        
        # Chat UI variables
        self.chat_visible = False
        self.chat_messages = []
        self.chat_panel = None
        self.chat_list_view = None
        
        # Configurar tema de colores
        self.colores = {
            'primary': '#2C3E50',      # Azul oscuro profesional
            'secondary': '#3498DB',    # Azul brillante
            'success': '#27AE60',      # Verde
            'warning': '#F39C12',      # Naranja
            'error': '#E74C3C',        # Rojo
            'surface': '#FFFFFF',      # Blanco
            'background': '#F8F9FA',   # Gris claro
            'text_primary': '#2C3E50', # Texto principal
            'text_secondary': '#7F8C8D' # Texto secundario
        }
        
        # Configurar página
        self.configurar_pagina()
    
    def configurar_pagina(self):
        """Configura las propiedades de la página"""
        self.page.title = "Sistema de Gestión Académica - CEDUC"
        # Configurar tema oscuro
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        # Maximize window (fills screen excluding taskbar)
        self.page.window_maximized = True
        self.page.window_min_width = 800
        self.page.window_min_height = 600
        
        self.page.padding = 20
        self.page.bgcolor = self.colores['background']
        
        # Configurar fuentes
        # Configurar fuentes (Uso de Roboto por defecto de Flet)
        # self.page.fonts = {
        #     "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
        # }
        # self.page.theme_mode = ft.ThemeMode.LIGHT
        
        # Define standard time blocks for the application (35-minute intervals)
        self.bloques_horarios = [
            "08:30", "09:05", "09:40", "10:15", "10:50", "11:25", "12:00", "12:35",
            "13:10", "13:45", "14:20", "14:55", "15:30", "16:05", "16:40", "17:15",
            "17:50", "18:25", "19:00", "19:35", "20:10", "20:45", "21:20", "21:55"
        ]
        
        # Limpiar cualquier control previo que pueda causar errores
        self.page.controls.clear()
        self.page.overlay.clear()
        self.page.dialog = None
        self.page.snack_bar = None
        
        # Update page to apply settings
        self.page.update()
        
        # Show splash screen and initialize synchronously
        self.mostrar_splash_screen()
        self.inicializar_aplicacion()
    
    def mostrar_splash_screen(self):
        """Muestra la pantalla de carga inicial"""
        self.ventana_activa = "splash"
        
        # Progress bar
        self.splash_progress_bar = ft.ProgressBar(
            width=400,
            value=0,
            color=self.colores['secondary'],
            bgcolor='rgba(255,255,255,0.3)'
        )
        
        # Status text
        self.splash_status_text = ft.Text(
            value="Iniciando aplicación...",
            size=14,
            color='white',
            text_align=ft.TextAlign.CENTER
        )
        
        # Splash container
        self.splash_container = ft.Container(
            content=ft.Stack([
                ft.Container(
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment(-1, -1),
                        end=ft.Alignment(1, 1),
                        colors=['#667eea', '#764ba2']
                    ),
                    expand=True
                ),
                ft.Container(
                    content=ft.Column([
                        # Logo and title
                        ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    value="🏫",
                                    size=80,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Text(
                                    value="Sistema de Gestión Académica",
                                    size=32,
                                    weight=ft.FontWeight.BOLD,
                                    color='white',
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Text(
                                    value="CEDUC - Centro Educacional",
                                    size=16,
                                    color='rgba(255,255,255,0.8)',
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10),
                            margin=ft.margin.only(bottom=50)
                        ),
                        
                        # Progress section
                        ft.Container(
                            content=ft.Column([
                                self.splash_progress_bar,
                                ft.Container(height=20),
                                self.splash_status_text
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10),
                            width=400
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER),
                    alignment=ft.Alignment(0, 0),
                    expand=True
                )
            ]),
            expand=True
        )
        
        self.page.add(self.splash_container)
        self.page.update()
    
    
    def actualizar_progreso(self, mensaje: str, progreso: float):
        """Actualiza el progreso en la pantalla de carga"""
        if self.splash_status_text and self.splash_progress_bar:
            self.splash_status_text.value = mensaje
            self.splash_progress_bar.value = progreso
            self.page.update()

    def cerrar_dialogo(self, dialogo):
        """Cierra un diálogo abierto"""
        dialogo.open = False
        self.page.update()
    
    def abrir_dialogo(self, dialogo):
        """Abre un diálogo usando el método apropiado según la versión de Flet"""
        try:
            # Intentar usar el método moderno de Flet
            self.page.open(dialogo)
            logging.info("Diálogo abierto usando page.open()")
        except AttributeError:
            # Fallback al método legacy
            logging.warning("page.open() no disponible, usando método legacy")
            self.page.dialog = dialogo
            dialogo.open = True
            self.page.update()
    
    def mostrar_mensaje(self, mensaje, tipo='info'):
        """Muestra un mensaje al usuario usando SnackBar"""
        # Definir colores según el tipo de mensaje
        colores_tipo = {
            'success': '#27AE60',  # Verde
            'error': '#E74C3C',    # Rojo
            'warning': '#F39C12',  # Naranja
            'info': '#3498DB'      # Azul
        }
        
        # Definir iconos según el tipo
        iconos_tipo = {
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️'
        }
        
        color = colores_tipo.get(tipo, colores_tipo['info'])
        icono = iconos_tipo.get(tipo, iconos_tipo['info'])
        
        # Crear y mostrar el SnackBar
        snack = ft.SnackBar(
            content=ft.Text(f"{icono} {mensaje}", color='white', weight=ft.FontWeight.BOLD),
            bgcolor=color,
            duration=3000,  # 3 segundos
            action="OK",
            action_color='white'
        )
        
        self.page.snack_bar = snack
        snack.open = True
        self.page.update()
        logging.info(f"Mensaje mostrado ({tipo}): {mensaje}")
    
    def inicializar_aplicacion(self):
        """Inicializa la aplicación con feedback de progreso"""
        try:
            logging.info("=== Iniciando proceso de carga ===")
            
            # Step 1: Starting
            logging.info("Paso 1: Iniciando aplicación")
            self.actualizar_progreso("Iniciando aplicación...", 0.1)
            
            # Step 2: Database connection
            logging.info("Paso 2: Conectando a base de datos")
            self.actualizar_progreso("Conectando a base de datos...", 0.3)
            
            # Step 3: Initialize database
            logging.info("Paso 3: Inicializando tablas")
            self.actualizar_progreso("Inicializando tablas...", 0.5)
            
            # Quick connection test first
            try:
                logging.info("Probando conexión rápida a MySQL...")
                import pymysql
                test_conn = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='',
                    connect_timeout=2  # Very short timeout for test
                )
                test_conn.close()
                logging.info("Conexión rápida exitosa")
            except Exception as test_error:
                logging.error(f"Prueba de conexión falló: {test_error}")
                raise Exception(f"No se puede conectar a MySQL.\n\nPor favor:\n1. Abre XAMPP\n2. Inicia MySQL\n3. Reinicia esta aplicación")
            
            try:
                logging.info("Llamando a dao.inicializar_base_de_datos()...")
                self.dao.inicializar_base_de_datos()
                logging.info("dao.inicializar_base_de_datos() completado")
            except Exception as db_error:
                logging.error(f"Error en inicialización de BD: {db_error}", exc_info=True)
                raise Exception(f"No se pudo conectar a la base de datos.\\n\\nAsegúrate de que XAMPP esté corriendo y MySQL esté activo.\\n\\nError: {str(db_error)}")
            
            logging.info("Base de datos inicializada correctamente")
            
            # Step 4: Loading components
            logging.info("Paso 4: Cargando componentes")
            self.actualizar_progreso("Cargando componentes...", 0.7)
            
            # Step 5: Preparing interface
            logging.info("Paso 5: Preparando interfaz")
            self.actualizar_progreso("Preparando interfaz...", 0.9)
            
            # Step 6: Complete
            logging.info("Paso 6: Completado")
            self.actualizar_progreso("¡Listo!", 1.0)
            
            # Transition to login - remove splash screen first
            logging.info("Limpiando splash screen")
            self.page.controls.clear()
            self.page.update()
            
            logging.info("Mostrando pantalla de login")
            self.mostrar_login()
            logging.info("=== Proceso de carga completado ===")
            
        except Exception as e:
            logging.error(f"Error durante inicialización: {e}", exc_info=True)
            if self.splash_status_text:
                # Show error message on splash screen
                error_lines = str(e).split('\n')
                self.splash_status_text.value = error_lines[0] if error_lines else str(e)
                self.splash_status_text.color = self.colores['error']
                self.splash_progress_bar.color = self.colores['error']
                self.page.update()
            
            # Still try to show login even if there's an error
            logging.info("Intentando mostrar login después del error")
            self.page.controls.clear()
            self.page.update()
            self.mostrar_login()
    
    
    
    def mostrar_login(self, e=None):
        """Muestra la ventana de login con diseño moderno"""
        self.ventana_activa = "login"
        
        # Limpiar página
        self.page.controls.clear()
        
        # Crear fondo con gradiente
        fondo = ft.Container(
            content=ft.Stack([
                ft.Container(
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment(-1, -1),
                        end=ft.Alignment(1, 1),
                        colors=['#667eea', '#764ba2']
                    ),
                    expand=True
                ),
                ft.Container(
                    content=self.crear_formulario_login(),
                    alignment=ft.Alignment(0, 0),
                    expand=True
                )
            ]),
            expand=True
        )
        
        self.page.add(fondo)
        self.page.update()
    
    def crear_formulario_login(self):
        """Crea el formulario de login con diseño moderno"""
        self.email_field = ft.TextField(
            label="📧 Correo Electrónico",
            hint_text="admin@ceduc.cl",
            value="admin@ceduc.cl",
            width=300,
            filled=True,
            bgcolor='#F5F5F5',
            color='#333333',
            hint_style=ft.TextStyle(color='#999999'),
            label_style=ft.TextStyle(color='#666666'),
            border_color=self.colores['primary'],
            focused_border_color=self.colores['primary'],
            on_submit=self.validar_login
        )

        self.password_field = ft.TextField(
            label="🔒 Contraseña",
            hint_text="********",
            value="123456",
            width=300,
            password=True,
            can_reveal_password=True,
            filled=True,
            bgcolor='#F5F5F5',
            color='#333333',
            hint_style=ft.TextStyle(color='#999999'),
            label_style=ft.TextStyle(color='#666666'),
            border_color=self.colores['primary'],
            focused_border_color=self.colores['primary'],
            on_submit=self.validar_login
        )

        return ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        # Logo y título
                        ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    value="📚 Sistema de Gestión Académica",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=self.colores['primary'],  # Azul oscuro en vez de blanco
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Text(
                                    value="CEDUC - Centro de Educación",
                                    size=14,
                                    color='#666666',  # Gris oscuro en vez de blanco
                                    text_align=ft.TextAlign.CENTER
                                )
                            ]),
                            alignment=ft.Alignment(0, 0),
                            margin=ft.margin.only(bottom=30)
                        ),
                        
                        self.email_field,
                        self.password_field,
                        
                        # Botón de login
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Text(
                                    value="🚀 Iniciar Sesión",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color='white'
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER),
                            style=ft.ButtonStyle(
                                color='white',
                                bgcolor='#2C3E50',
                                shape=ft.RoundedRectangleBorder(radius=12),
                                padding=ft.padding.symmetric(vertical=15, horizontal=30)
                            ),
                            on_click=self.validar_login,
                            width=300,
                            elevation=3
                        ),
                        
                        # Información adicional
                        ft.Container(
                            content=ft.Text(
                                value="💡 Credenciales de prueba:\nadmin@ceduc.cl / 123456",
                                size=12,
                                color='rgba(255,255,255,0.8)',
                                text_align=ft.TextAlign.CENTER
                            ),
                            margin=ft.margin.only(top=20)
                        )
                    ], 
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=40,
                    alignment=ft.Alignment(0, 0)
                ),
                elevation=10,
                shape=ft.RoundedRectangleBorder(radius=16)
            ),
            width=400,
            height=550,
            border_radius=16,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color='rgba(0,0,0,0.2)'
            )
        )
    
    def validar_login(self, e):
        """Valida las credenciales de login"""
        logging.info("Intento de login iniciado.")
        email = self.email_field.value
        password = self.password_field.value
        
        logging.info(f"Validando: email='{email}'")

        # Validación básica
        if not email or not password:
            logging.warning("Login fallido: campos incompletos.")
            self.mostrar_mensaje("❌ Por favor complete todos los campos", 'error')
            return
        
        usuario = self.dao.verificar_usuario(email, password)
        logging.info(f"Resultado de DAO: {'Usuario encontrado' if usuario else 'Usuario no encontrado'}")
        
        if usuario:
            # Usar .get para acceso seguro y tener un fallback
            nombre_display = usuario.get('nombre', usuario['email'])
            logging.info(f"Login exitoso para {nombre_display}. Mostrando dashboard.")
            self.usuario_actual = usuario
            self.mostrar_dashboard()
        else:
            logging.warning(f"Login fallido para email '{email}'. Credenciales incorrectas.")
            self.mostrar_mensaje("❌ Credenciales incorrectas", 'error')
    
    def actualizar_notificaciones(self):
        """Actualiza el estado del centro de notificaciones"""
        if not hasattr(self, 'btn_notificaciones') or not hasattr(self, 'badge_notificaciones'):
            return
        
        # Verificar que los controles estén en la página (puede lanzar RuntimeError)
        try:
            _ = self.btn_notificaciones.page
            if _ is None:
                return
        except (RuntimeError, AttributeError):
            return

        try:
            modulos = self.dao.obtener_modulos()
            sin_docente = [m for m in modulos if not m.get('docente_id')]
            
            # Detectar conflictos de horario
            conflictos = []
            logging.info(f"=== Iniciando detección de conflictos para {len(modulos)} módulos ===")
            
            for m in modulos:
                # Skip modules without teacher or room
                if not m.get('docente_id') or not m.get('sala_id'):
                    continue
                
                try:
                    horarios = self.dao.obtener_horarios_modulo(m['id'])
                    if not horarios:
                        continue
                    
                    # Check for conflicts
                    conflicto_info = {'modulo': m, 'conflictos': []}
                    
                    # Conflict with teacher
                    try:
                        tiene_conflicto, mensaje, _ = self.dao.validar_conflicto_horario_docente(
                            m['docente_id'], horarios, m['id']
                        )
                        if tiene_conflicto:
                            conflicto_info['conflictos'].append(('docente', mensaje))
                            logging.info(f"Conflicto docente detectado en módulo {m['nombre']}: {mensaje}")
                    except Exception as e:
                        logging.error(f"Error validando conflicto docente para módulo {m['id']}: {e}")
                    
                    # Conflict with room
                    try:
                        tiene_conflicto, mensaje, _ = self.dao.validar_conflicto_sala(
                            m['sala_id'], horarios, m['id']
                        )
                        if tiene_conflicto:
                            conflicto_info['conflictos'].append(('sala', mensaje))
                            logging.info(f"Conflicto sala detectado en módulo {m['nombre']}: {mensaje}")
                    except Exception as e:
                        logging.error(f"Error validando conflicto sala para módulo {m['id']}: {e}")
                    
                    # Conflict with semester (par/impar)
                    if m.get('carrera_id') and m.get('semestre'):
                        try:
                            tiene_conflicto, mensaje, _ = self.dao.validar_conflicto_semestre_par_impar(
                                m['carrera_id'], m['semestre'], horarios, m['id']
                            )
                            if tiene_conflicto:
                                conflicto_info['conflictos'].append(('semestre', mensaje))
                                logging.info(f"Conflicto semestre detectado en módulo {m['nombre']}: {mensaje}")
                        except Exception as e:
                            logging.error(f"Error validando conflicto semestre para módulo {m['id']}: {e}")
                    
                    if conflicto_info['conflictos']:
                        conflictos.append(conflicto_info)
                        
                except Exception as e:
                    logging.error(f"Error procesando módulo {m.get('id', 'unknown')}: {e}")
                    
            logging.info(f"=== Detección completada: {len(conflictos)} módulos con conflictos ===")
                    
        except Exception as e:
            logging.error(f"Error al obtener notificaciones: {e}")
            import traceback
            logging.error(traceback.format_exc())
            sin_docente = []
            conflictos = []
        
        total_notificaciones = len(sin_docente) + len(conflictos)
        items = []
        
        if total_notificaciones == 0:
            items.append(ft.PopupMenuItem(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color="green"),
                    ft.Text("No hay notificaciones pendientes")
                ])
            ))
            self.btn_notificaciones.icon = ft.Icons.NOTIFICATIONS_NONE
            self.btn_notificaciones.tooltip = "Sin notificaciones"
            self.badge_notificaciones.visible = False
        else:
            # Módulos sin docente
            if sin_docente:
                items.append(ft.PopupMenuItem(
                    content=ft.Text(f"Módulos sin docente ({len(sin_docente)})", weight=ft.FontWeight.BOLD)
                ))
                for m in sin_docente:
                    items.append(
                        ft.PopupMenuItem(
                            content=ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.WARNING, color="#E74C3C", size=20),
                                    ft.Column([
                                        ft.Text(m['nombre'], weight=ft.FontWeight.BOLD, size=12),
                                        ft.Text(f"Cód: {m.get('codigo', 'N/A')}", size=10, color="grey")
                                    ], spacing=0)
                                ]),
                                padding=10,
                                border_radius=8,
                                border=ft.border.all(1, "#EEEEEE"),
                                bgcolor="#FAFAFA"
                            ),
                            on_click=lambda e, mod=m: self.editar_modulo(mod)
                        )
                    )
            
            # Conflictos de horario
            if conflictos:
                if sin_docente:  # Add separator if there are modules without teacher
                    items.append(ft.PopupMenuItem(content=ft.Divider()))
                
                items.append(ft.PopupMenuItem(
                    content=ft.Text(f"Conflictos de horario ({len(conflictos)})", weight=ft.FontWeight.BOLD)
                ))
                for conf_info in conflictos:
                    m = conf_info['modulo']
                    # Get first conflict message for display
                    tipo, mensaje = conf_info['conflictos'][0]
                    icono_color = "#E74C3C"  # Red for conflicts
                    
                    items.append(
                        ft.PopupMenuItem(
                            content=ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.ERROR, color=icono_color, size=20),
                                    ft.Column([
                                        ft.Text(m['nombre'], weight=ft.FontWeight.BOLD, size=12),
                                        ft.Text(f"Cód: {m.get('codigo', 'N/A')}", size=10, color="grey"),
                                        ft.Text(f"⚠️ {len(conf_info['conflictos'])} conflicto(s)", size=10, color="#E74C3C")
                                    ], spacing=0)
                                ]),
                                padding=10,
                                border_radius=8,
                                border=ft.border.all(1, "#FFDDDD"),
                                bgcolor="#FFF5F5"
                            ),
                            on_click=lambda e, mod=m: self.editar_modulo(mod)
                        )
                    )
            
            self.btn_notificaciones.icon = ft.Icons.NOTIFICATIONS_ACTIVE
            self.btn_notificaciones.tooltip = f"{total_notificaciones} notificación(es)"
            
            # Update Badge
            self.badge_notificaciones.content = ft.Text(str(total_notificaciones), color="white", size=10, weight=ft.FontWeight.BOLD)
            self.badge_notificaciones.visible = True

        self.btn_notificaciones.items = items
        
        # Update controls if they are in the page
        if self.btn_notificaciones.page:
            self.btn_notificaciones.update()
        if self.badge_notificaciones.page:
            self.badge_notificaciones.update()

    def _crear_componente_notificaciones(self):
        """Crea el componente de notificaciones con badge"""
        self.btn_notificaciones = ft.PopupMenuButton(
            icon=ft.Icons.NOTIFICATIONS_NONE,
            icon_color="white",
            bgcolor='white',
            items=[]
        )
        
        self.badge_notificaciones = ft.Container(
            content=ft.Text("0", color="white", size=10),
            bgcolor="red",
            border_radius=10,
            width=16,
            height=16,
            alignment=ft.Alignment(0, 0),
            visible=False,
            right=0,
            top=0
        )
        
        self.actualizar_notificaciones()
        
        return ft.Stack([
            self.btn_notificaciones,
            self.badge_notificaciones
        ], width=40, height=40)

    def mostrar_dashboard(self, e=None):
        """Muestra el dashboard principal con diseño moderno (Split View)"""
        self.ventana_activa = "dashboard"
        self.carrera_seleccionada = None # Resetear selección
        
        # Limpiar página
        self.page.controls.clear()
        if hasattr(self.page, 'overlay'):
            self.page.overlay.clear()
        
        # Initialize Chat UI (restore button and panel)
        self.crear_chat_ui()
        
        # Header con gradiente
        header = ft.Container(
            content=ft.Row([
                # Logo y título
                ft.Row([
                    ft.Text(
                        value="🏫 CEDUC",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color='white'
                    ),
                    ft.Text(
                        value="Sistema de Gestión Académica",
                        size=16,
                        color='rgba(255,255,255,0.8)'
                    )
                ], alignment=ft.MainAxisAlignment.START),
                
                # Información del usuario y botón de logout
                ft.Row([
                    # Botón de Gestión de Datos
                    ft.IconButton(
                        icon=ft.Icons.STORAGE,
                        tooltip="Gestión de Datos (Importar/Exportar)",
                        icon_color='white',
                        on_click=self.mostrar_gestion_datos,
                        bgcolor='rgba(255,255,255,0.2)'
                    ),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PERSON, color='white', size=20),
                            ft.Text(
                                value=f"👋 {self.usuario_actual.get('nombre', self.usuario_actual['email'])}",
                                color='white',
                                size=14
                            )
                        ]),
                        bgcolor='rgba(255,255,255,0.2)',
                    padding=ft.padding.symmetric(horizontal=15, vertical=8),
                    border_radius=20
                ),
                self._crear_componente_notificaciones(),
                ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                        tooltip="Cerrar Sesión",
                        icon_color='white',
                        on_click=self.mostrar_login,
                        bgcolor='rgba(255,255,255,0.2)'
                    )
                ], alignment=ft.MainAxisAlignment.END)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor='#2C3E50',
            padding=ft.padding.symmetric(horizontal=30, vertical=20),
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, -1),
                colors=['#2C3E50', '#3498DB']
            )
        )
        
        # Contenido principal dividido (Salas | Carreras | Docentes)
        panel_salas = self.crear_panel_salas()
        panel_carreras = self.crear_panel_carreras()
        panel_docentes = self.crear_panel_docentes()

        contenido_principal = ft.Row([
            # Columna Izquierda: Docentes
            ft.Container(
                content=panel_docentes,
                width=300,
                bgcolor='white',
                padding=20,
                border_radius=16,
                shadow=ft.BoxShadow(blur_radius=10, color='rgba(0,0,0,0.1)')
            ),
            # Columna Central: Carreras
            ft.Container(
                content=panel_carreras,
                expand=True, 
                bgcolor='white',
                padding=20,
                border_radius=16,
                shadow=ft.BoxShadow(blur_radius=10, color='rgba(0,0,0,0.1)')
            ),
            # Columna Derecha: Salas
            ft.Container(
                content=panel_salas,
                width=300, 
                bgcolor='white',
                padding=20,
                border_radius=16,
                shadow=ft.BoxShadow(blur_radius=10, color='rgba(0,0,0,0.1)')
            )
        ], expand=True, spacing=20)
        
        # Estructura principal
        self.page.add(
            ft.Column([
                header,
                ft.Container(content=contenido_principal, padding=20, expand=True)
            ], expand=True, spacing=0)
        )
        
        self.page.update()
    
    def mostrar_gestion_datos(self, e=None):
        """Muestra la interfaz de gestión de datos (importar/exportar)"""
        self.ventana_activa = "gestion_datos"
        
        # Limpiar página
        self.page.controls.clear()
        
        # Header con botón de volver
        header = ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color='white',
                        on_click=self.mostrar_dashboard,
                        tooltip="Volver al Dashboard"
                    ),
                    ft.Text(
                        "📊 Gestión de Datos",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color='white'
                    )
                ]),
                ft.Row([
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PERSON, color='white', size=20),
                            ft.Text(
                                value=f"👋 {self.usuario_actual.get('nombre', self.usuario_actual['email'])}",
                                color='white',
                                size=14
                            )
                        ]),
                        bgcolor='rgba(255,255,255,0.2)',
                        padding=ft.padding.symmetric(horizontal=15, vertical=8),
                        border_radius=20
                    ),
                    ft.IconButton(
                        icon=ft.Icons.HOME,
                        icon_color='white',
                        on_click=self.mostrar_dashboard,
                        tooltip="Ir al Dashboard"
                    )
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor='#2C3E50',
            padding=ft.padding.symmetric(horizontal=30, vertical=20),
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, -1),
                colors=['#2C3E50', '#3498DB']
            )
        )
        
        # Crear instancia de GestionDatos y obtener vista
        gestion = GestionDatos(self.page, self.dao)
        vista_gestion = gestion.crear_vista()
        
        # Estructura principal
        self.page.add(
            ft.Column([
                header,
                vista_gestion
            ], expand=True, spacing=0)
        )
        
        self.page.update()
    
    def _actualizar_vista_salas(self):
        """Recarga y muestra las salas desde la base de datos."""
        if not hasattr(self, 'salas_list_view'):
            return

        salas_data = self.dao.obtener_salas()
        self.salas_list_view.controls.clear()
        
        if not salas_data:
            self.salas_list_view.controls.append(ft.Text("No hay salas.", text_align=ft.TextAlign.CENTER, color=self.colores['text_secondary']))
        else:
            for sala in salas_data:
                # Diseño tipo "Sidebar Item" o Tarjeta compacta vertical
                card = ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(sala["nombre"], weight=ft.FontWeight.BOLD, size=16),
                            ft.Text(f"{sala.get('tipo', 'Sala')} | Cap: {sala.get('capacidad', 0)}", size=12, color='grey')
                        ], expand=True),
                        ft.PopupMenuButton(
                            items=[
                                ft.PopupMenuItem(content=ft.Text("Editar"), icon=ft.Icons.EDIT, on_click=lambda e, s=sala: self.editar_sala(s)),
                                ft.PopupMenuItem(content=ft.Text("Eliminar"), icon=ft.Icons.DELETE, on_click=lambda e, s=sala: self.eliminar_sala(s)),
                            ]
                        )
                    ]),
                    padding=15,
                    border=ft.border.all(1, '#EEEEEE'),
                    border_radius=10,
                    bgcolor='#F9F9F9',
                    on_click=lambda e, s=sala: self.mostrar_horario_sala(s) # Mostrar horario al hacer click
                )
                self.salas_list_view.controls.append(card)
        
        self.page.update()

    def cerrar_dialogo(self, dialog=None):
        """Cierra el diálogo actual"""
        try:
            if dialog:
                self.page.close(dialog)
                self.page.update()  # CRITICAL: Update page to reflect closed state
            else:
                if self.page.dialog:
                    self.page.dialog.open = False
                self.page.update()
        except Exception as e:
            logging.error(f"Error al cerrar diálogo: {e}")

    def mostrar_horario_sala(self, sala):
        """Muestra un modal con la grilla de disponibilidad de la sala"""
        logging.info(f"Abriendo horario para sala: {sala['nombre']}")
        try:
            horarios_ocupados = self.dao.obtener_horarios_ocupados_sala(sala['id'])
            if horarios_ocupados is None:
                horarios_ocupados = []
            
            # Definir bloques horarios estándar
            bloques = [
                ("08:30", "10:00"), ("10:15", "11:45"),
                ("12:00", "13:30"), ("13:45", "15:15"),
                ("15:30", "17:00"), ("17:15", "18:45"),
                ("19:00", "20:30"), ("20:45", "22:15")
            ]
            dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
            
            # Helper para verificar ocupación
            def obtener_ocupacion(dia, inicio, fin):
                """Verifica si un bloque está ocupado"""
                def hora_a_minutos(h):
                    """Convierte hora string o timedelta a minutos"""
                    if isinstance(h, str):
                        partes = h.split(':')
                        return int(partes[0]) * 60 + int(partes[1])
                    else:  # timedelta
                        return int(h.total_seconds() // 60)
                
                inicio_min = hora_a_minutos(inicio)
                fin_min = hora_a_minutos(fin)
                
                for h in horarios_ocupados:
                    if h['dia'].upper() == dia.upper():
                        h_inicio_min = hora_a_minutos(h['hora_inicio'])
                        h_fin_min = hora_a_minutos(h['hora_fin'])
                        
                        # Verificar si hay solapamiento
                        if (inicio_min < h_fin_min) and (fin_min > h_inicio_min):
                            return h.get('modulo_nombre', 'Ocupado')
                return None

            # Crear cabecera de días
            headers = [ft.Container(width=80)] # Espacio para horas
            for dia in dias:
                headers.append(ft.Container(
                    content=ft.Text(dia, weight=ft.FontWeight.BOLD, size=12, text_align=ft.TextAlign.CENTER),
                    width=100,
                    alignment=ft.Alignment(0, 0)
                ))
            
            grid_rows = [ft.Row(headers)]
            
            # Crear filas de bloques
            for inicio, fin in bloques:
                row_controls = [
                    ft.Container(
                        content=ft.Text(f"{inicio}\n{fin}", size=10, weight=ft.FontWeight.BOLD),
                        width=80,
                        alignment=ft.Alignment(1, 0),
                        padding=5
                    )
                ]
                
                for dia in dias:
                    modulo_ocupante = obtener_ocupacion(dia, inicio, fin)
                    ocupado = modulo_ocupante is not None
                    
                    btn = ft.Container(
                        content=ft.Column([
                            ft.Text(modulo_ocupante if ocupado else "Disponible", 
                                   size=10, 
                                   color="white" if ocupado else "black",
                                   text_align=ft.TextAlign.CENTER,
                                   overflow=ft.TextOverflow.ELLIPSIS)
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        width=100,
                        height=50,
                        bgcolor=self.colores['error'] if ocupado else "#E0E0E0",
                        border_radius=5,
                        padding=2,
                        alignment=ft.Alignment(0, 0),
                        tooltip=f"{dia} {inicio}-{fin}: {modulo_ocupante}" if ocupado else "Disponible"
                    )
                    row_controls.append(btn)
                
                grid_rows.append(ft.Row(row_controls))
                
            content = ft.Column(
                [
                    ft.Text(f"Horario Sala: {sala['nombre']}", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Capacidad: {sala.get('capacidad', 0)} personas", size=14, color='grey'),
                    ft.Divider(),
                    ft.Column(grid_rows, scroll=ft.ScrollMode.AUTO, height=400)
                ],
                width=650,
                height=500,
                tight=True
            )
            
            # Crear el diálogo
            dialog = ft.AlertDialog(
                content=content,
                modal=True,
                actions_alignment=ft.MainAxisAlignment.END
            )
            
            # Asignar acción de cerrar pasando el diálogo
            dialog.actions = [
                ft.TextButton("Cerrar", on_click=lambda e: self.cerrar_dialogo(dialog))
            ]
            
            # Intentar usar page.open (Flet moderno) o fallback a page.dialog
            try:
                self.page.open(dialog)
                logging.info("Diálogo abierto usando page.open")
            except AttributeError:
                logging.warning("page.open no disponible, usando page.dialog")
                self.page.dialog = dialog
                dialog.open = True
                self.page.update()
            
        except Exception as e:
            logging.error(f"Error al mostrar horario sala: {e}")
            self.mostrar_mensaje(f"Error al cargar horario: {e}", "error")

    def crear_panel_salas(self):
        """Crea el panel lateral de gestión de salas"""
        self.salas_list_view = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)
        
        btn_agregar = ft.ElevatedButton(
            "Añadir Sala",
            icon=ft.Icons.ADD,
            style=ft.ButtonStyle(
                bgcolor='#27AE60',
                color='white',
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=20
            ),
            width=260,
            on_click=self.agregar_sala
        )
        
        # Cargar los datos iniciales
        self._actualizar_vista_salas()

        return ft.Column([
            ft.Text("🏢 GESTIÓN DE SALAS", weight=ft.FontWeight.BOLD, size=18, color=self.colores['primary']),
            ft.Divider(),
            self.salas_list_view,
            ft.Container(content=btn_agregar, alignment=ft.Alignment(0, 0), margin=ft.margin.only(top=10))
        ], expand=True)
    
    def _actualizar_vista_carreras(self):
        """Recarga y muestra las carreras desde la base de datos."""
        if not hasattr(self, 'carreras_list_view') or self.carreras_list_view is None:
            return

        carreras_data = self.dao.obtener_carreras()
        self.carreras_list_view.controls.clear()
        
        if not carreras_data:
            self.carreras_list_view.controls.append(ft.Text("No hay carreras registradas.", text_align=ft.TextAlign.CENTER, size=16, color=self.colores['text_secondary']))
        else:
            for carrera in carreras_data:
                # Tarjeta de Carrera (Clickeable para ir a la vista de asignación)
                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.SCHOOL, color='#3498DB', size=30),
                                ft.Container(
                                    content=ft.Text(value=carrera["nombre"], size=16, weight=ft.FontWeight.BOLD, color=self.colores['text_primary'], text_align=ft.TextAlign.CENTER),
                                    expand=True
                                )
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Divider(),
                            ft.Text(f"🎓 {carrera.get('jornada', 'N/A')}", size=12, text_align=ft.TextAlign.CENTER),
                            ft.Text(f"👥 {carrera.get('alumnos_proyectados', 0)} Alumnos", size=12, text_align=ft.TextAlign.CENTER),
                            ft.Container(height=10),
                            ft.Row([
                                ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar Carrera", on_click=lambda e, c=carrera: self.editar_carrera(c)),
                                ft.IconButton(icon=ft.Icons.DELETE, tooltip="Eliminar Carrera", icon_color='#E74C3C', on_click=lambda e, c=carrera: self.eliminar_carrera(c)),
                            ], alignment=ft.MainAxisAlignment.CENTER)
                        ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                        padding=20,
                        on_click=lambda e, c=carrera: self.mostrar_vista_asignacion(c) # Navegación
                    ),
                    elevation=4,
                    shape=ft.RoundedRectangleBorder(radius=12)
                )
                self.carreras_list_view.controls.append(card)
        
        self.page.update()

    def crear_panel_carreras(self):
        """Crea el panel principal de carreras"""
        self.carreras_list_view = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=300,
            child_aspect_ratio=1.0,
            spacing=20,
            run_spacing=20,
            padding=10
        )
        
        btn_agregar = ft.ElevatedButton(
            "Añadir Carrera",
            icon=ft.Icons.ADD,
            on_click=self.agregar_carrera,
            style=ft.ButtonStyle(bgcolor='#27AE60', color='white', padding=20)
        )
        
        self._actualizar_vista_carreras()

        return ft.Column([
            ft.Row([
                ft.Text("🎓 CARRERAS", size=24, weight=ft.FontWeight.BOLD, color=self.colores['primary']),
                btn_agregar
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            
            # Buscador Global de Módulos
            ft.Container(
                content=ft.TextField(
                    hint_text="🔍 Buscar módulo en todas las carreras...",
                    on_change=self._buscar_modulos_global,
                    border_radius=8,
                    filled=True,
                    bgcolor="#F5F5F5",
                    prefix_icon=ft.Icons.SEARCH,
                    height=45,
                    text_size=14
                ),
                margin=ft.margin.only(bottom=10)
            ),
            
            self.carreras_list_view,
        ], expand=True)

    def _buscar_modulos_global(self, e):
        """Busca módulos globalmente y actualiza la vista de carreras con los resultados"""
        texto_busqueda = e.control.value.lower()
        
        if not texto_busqueda:
            # Si no hay búsqueda, restaurar la vista de carreras
            self.carreras_list_view.controls.clear()
            self.carreras_list_view.padding = 10
            self.carreras_list_view.spacing = 20
            self.carreras_list_view.run_spacing = 20
            # Restaurar GridView properties si se cambiaron a ListView
            # Nota: Flet no permite cambiar tipo de control fácilmente, así que limpiamos y rellenamos
            # Pero como self.carreras_list_view es un GridView, si queremos mostrar lista, 
            # tal vez sea mejor tener dos contenedores y alternar visibilidad.
            # Sin embargo, para simplificar, usaremos el mismo GridView pero con items de ancho completo si es posible,
            # o mejor, reconstruimos el contenido.
            
            # Mejor estrategia: Recargar la vista normal de carreras
            self._actualizar_vista_carreras()
            return

        # Realizar búsqueda
        all_modulos = self.dao.obtener_modulos()
        resultados = [
            m for m in all_modulos 
            if texto_busqueda in m['nombre'].lower() or 
               texto_busqueda in m.get('codigo', '').lower()
        ]
        
        self.carreras_list_view.controls.clear()
        
        if not resultados:
            self.carreras_list_view.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.SEARCH_OFF, size=50, color="grey"),
                        ft.Text("No se encontraron módulos", color="grey")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.Alignment(0, 0),
                    padding=20
                )
            )
        else:
            # Mostrar resultados como lista de tarjetas
            for mod in resultados:
                # Obtener nombre de carrera
                carrera_nombre = "Carrera Desconocida"
                if mod.get('carrera_id'):
                    carreras = self.dao.obtener_carreras()
                    carrera = next((c for c in carreras if c['id'] == mod['carrera_id']), None)
                    if carrera: carrera_nombre = carrera['nombre']

                card = ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(mod['nombre'], weight=ft.FontWeight.BOLD, size=16, color=self.colores['primary']),
                            ft.Text(f"Código: {mod.get('codigo', 'N/A')} | {carrera_nombre}", size=12, color="grey"),
                            ft.Text(f"Docente: {mod.get('docente_nombre', 'Sin asignar')} | Sala: {mod.get('sala_nombre', 'Sin sala')}", size=12, color="grey")
                        ], expand=True),
                        ft.ElevatedButton(
                            "Editar", 
                            icon=ft.Icons.EDIT, 
                            on_click=lambda e, m=mod: self.ir_a_modulo(m),
                            bgcolor=self.colores['secondary'],
                            color='white'
                        )
                    ]),
                    padding=15,
                    bgcolor="white",
                    border=ft.border.all(1, "#EEEEEE"),
                    border_radius=8,
                    shadow=ft.BoxShadow(blur_radius=5, color="#0D000000")
                )
                self.carreras_list_view.controls.append(card)
        
        self.carreras_list_view.update()
    
    def agregar_carrera(self, e):
        self.mostrar_dialogo_carrera("Agregar Nueva Carrera")

    def editar_carrera(self, carrera):
        logging.info(f"=== EDITAR_CARRERA LLAMADO: {carrera.get('nombre')} ===")
        self.mostrar_dialogo_carrera("Editar Carrera", carrera)

    def eliminar_carrera(self, carrera):
        logging.info(f"=== ELIMINAR_CARRERA LLAMADO: {carrera.get('nombre')} ===")
        def confirmar_eliminacion(e):
            if e.control.text == "Confirmar":
                try:
                    self.dao.eliminar_carrera(carrera['id'])
                    self.mostrar_mensaje(f"✅ Carrera '{carrera['nombre']}' eliminada.", 'success')
                    self._actualizar_vista_carreras()
                except Exception as ex:
                    self.mostrar_mensaje(f"❌ Error al eliminar carrera: {ex}", 'error')
            self.cerrar_dialogo(dialogo_confirmacion)
        
        dialogo_confirmacion = ft.AlertDialog(
            title=ft.Text("🗑️ Confirmar Eliminación"),
            content=ft.Text(f"¿Está seguro que desea eliminar la carrera '{carrera['nombre']}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dialogo_confirmacion)),
                ft.ElevatedButton("Confirmar", on_click=confirmar_eliminacion, bgcolor='#E74C3C', color='white')
            ],
        )
        self.abrir_dialogo(dialogo_confirmacion)

    def mostrar_dialogo_carrera(self, titulo, carrera=None):
        # Campos del formulario
        nombre_field = ft.TextField(label="Nombre de la Carrera", value=carrera['nombre'] if carrera else "")
        jornada_dd = ft.Dropdown(
            label="Jornada",
            value=carrera['jornada'] if carrera else None,
            options=[ft.dropdown.Option("Diurna"), ft.dropdown.Option("Vespertina")]
        )
        alumnos_field = ft.TextField(label="Alumnos Proyectados", value=str(carrera.get('alumnos_proyectados', '')) if carrera else "", keyboard_type=ft.KeyboardType.NUMBER)
        
        # Semestres (Duración)
        semestres_actuales = self.dao.obtener_semestres_carrera(carrera['id']) if carrera else []
        duracion_valor = str(len(semestres_actuales)) if semestres_actuales else "8" # Default 8 semesters
        duracion_field = ft.TextField(label="Duración (Semestres)", value=duracion_valor, keyboard_type=ft.KeyboardType.NUMBER, suffix_text="semestres")
        
        # Salas - Create button grid instead of checkboxes
        salas_disponibles = self.dao.obtener_salas()
        salas_actuales_ids = [s['id'] for s in self.dao.obtener_salas_carrera(carrera['id'])] if carrera else []
        
        # Dictionary to store button references: {sala_id: button_container}
        salas_buttons = {}
        
        def crear_boton_sala(sala):
            """Crea un botón toggleable para una sala"""
            is_selected = sala['id'] in salas_actuales_ids
            
            def toggle_sala(e):
                # Toggle selection state
                current_state = e.control.data['selected']
                new_state = not current_state
                e.control.data['selected'] = new_state
                
                # Update visual appearance
                if new_state:
                    e.control.bgcolor = "#27AE60"
                    e.control.content.color = "white"
                else:
                    e.control.bgcolor = "#ECF0F1"
                    e.control.content.color = "#2C3E50"
                
                e.control.update()
            
            button = ft.Container(
                content=ft.Text(
                    sala['nombre'],
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color="white" if is_selected else "#2C3E50"
                ),
                bgcolor="#27AE60" if is_selected else "#ECF0F1",
                padding=10,
                border_radius=8,
                alignment=ft.Alignment(0, 0),
                data={'sala_id': sala['id'], 'selected': is_selected},
                on_click=toggle_sala,
                ink=True,
                tooltip=f"Sala: {sala['nombre']}\nCapacidad: {sala.get('capacidad', 'N/A')}\nTipo: {sala.get('tipo', 'N/A')}"
            )
            
            salas_buttons[sala['id']] = button
            return button
        
        # Create 4-column grid of room buttons with equal widths
        salas_grid_rows = []
        for i in range(0, len(salas_disponibles), 4):
            row_salas = salas_disponibles[i:i+4]
            # Create buttons with expand to make them equal width
            buttons = []
            for sala in row_salas:
                btn = crear_boton_sala(sala)
                btn.expand = True  # Make all buttons equal width
                buttons.append(btn)
            
            row = ft.Row(
                buttons,
                spacing=10,
                alignment=ft.MainAxisAlignment.START
            )
            salas_grid_rows.append(row)
        
        salas_grid = ft.Column(
            salas_grid_rows,
            scroll=ft.ScrollMode.AUTO,
            spacing=10
        )
        
        def guardar_carrera_handler(e):
            try:
                logging.info("=== GUARDAR_CARRERA_HANDLER INICIADO ===")
                
                # Recolección de datos
                nombre = nombre_field.value
                jornada = jornada_dd.value
                alumnos_proyectados = int(alumnos_field.value) if alumnos_field.value else 0
                
                logging.info(f"Datos recolectados: nombre={nombre}, jornada={jornada}, alumnos={alumnos_proyectados}")
                
                # Generar lista de semestres basada en la duración
                try:
                    duracion = int(duracion_field.value)
                    if duracion < 1: raise ValueError("La duración debe ser al menos 1 semestre")
                    semestres_seleccionados = list(range(1, duracion + 1))
                    logging.info(f"Semestres generados: {semestres_seleccionados}")
                except ValueError as ve:
                    logging.error(f"Error en duración: {ve}")
                    self.mostrar_mensaje("La duración debe ser un número válido mayor a 0.", 'error')
                    return

                # Get selected rooms from button states
                salas_seleccionadas_ids = [btn.data['sala_id'] for btn in salas_buttons.values() if btn.data['selected']]
                logging.info(f"Salas seleccionadas: {salas_seleccionadas_ids}")

                if not nombre or not jornada:
                    logging.warning("Validación fallida: campos obligatorios vacíos")
                    self.mostrar_mensaje("Nombre y Jornada son obligatorios.", 'error')
                    return

                carrera_data = (nombre, jornada, alumnos_proyectados)
                carrera_id = carrera['id'] if carrera else None
                
                logging.info(f"Llamando a guardar_carrera con carrera_id={carrera_id}")
                resultado = self.dao.guardar_carrera(carrera_data, semestres_seleccionados, salas_seleccionadas_ids, carrera_id)
                
                if resultado is None:
                    logging.error("guardar_carrera retornó None - operación falló")
                    self.mostrar_mensaje(f"❌ Error al guardar carrera. Revisa los logs para más detalles.", 'error')
                    return
                
                logging.info(f"Carrera guardada exitosamente con ID: {resultado}")
                self.mostrar_mensaje(f"✅ Carrera '{nombre}' guardada exitosamente.", 'success')
                self.cerrar_dialogo(dialogo)
                self._actualizar_vista_carreras()

            except Exception as ex:
                logging.error(f"Error en guardar_carrera_handler: {ex}")
                import traceback
                logging.error(traceback.format_exc())
                self.mostrar_mensaje(f"❌ Error al guardar carrera: {ex}", 'error')

        # Left Column: Form Fields
        left_column = ft.Column([
            ft.Text("Información General", weight="bold", color=self.colores['primary']),
            nombre_field,
            jornada_dd,
            alumnos_field,
            duracion_field,
        ], scroll=ft.ScrollMode.AUTO, expand=True, alignment=ft.MainAxisAlignment.START, spacing=15)
        
        # Right Column: Room Selection Grid
        right_column = ft.Column([
            ft.Text("Salas Asignables", weight="bold", color=self.colores['primary']),
            ft.Text("Seleccione las salas disponibles para esta carrera", size=12, color="grey"),
            ft.Container(
                content=salas_grid,
                height=400,
                border=ft.border.all(1, "#BDC3C7"),
                border_radius=8,
                padding=10,
                bgcolor="white"
            )
        ], expand=True, spacing=10)

        dialogo = ft.AlertDialog(
            title=ft.Text(titulo, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=left_column,
                        expand=2,  # 40% width
                        padding=ft.padding.only(right=20),
                        alignment=ft.Alignment(-1, -1)
                    ),
                    ft.VerticalDivider(width=1),
                    ft.Container(
                        content=right_column,
                        expand=3,  # 60% width
                        padding=10,
                        alignment=ft.Alignment(-1, -1)
                    )
                ], expand=True),
                width=1000,
                height=550
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dialogo)),
                ft.ElevatedButton("💾 Guardar", bgcolor='#27AE60', color='white', on_click=guardar_carrera_handler),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.abrir_dialogo(dialogo)

    def mostrar_vista_asignacion(self, carrera):
        """Muestra la vista de asignación de módulos y docentes para una carrera"""
        self.carrera_actual = carrera # Guardar referencia para volver
        self.ventana_activa = "asignacion"
        self.carrera_seleccionada = carrera
        
        # Limpiar página
        self.page.controls.clear()
        
        def exportar_pdf_carrera(e):
            try:
                # Fetch all modules for this career with teacher and room names
                modulos = self.dao.obtener_modulos_carrera(carrera['id'])
                
                # Enrich module data with teacher and room names
                for m in modulos:
                    if m.get('docente_id'):
                        docentes = self.dao.obtener_docentes()
                        docente = next((d for d in docentes if d['id'] == m['docente_id']), None)
                        m['docente_nombre'] = docente['nombre'] if docente else 'Sin asignar'
                    else:
                        m['docente_nombre'] = 'Sin asignar'
                    
                    if m.get('sala_id'):
                        salas = self.dao.obtener_salas()
                        sala = next((s for s in salas if s['id'] == m['sala_id']), None)
                        m['sala_nombre'] = sala['nombre'] if sala else 'Sin asignar'
                    else:
                        m['sala_nombre'] = 'Sin asignar'
                
                filepath = self.report_generator.generar_reporte_carrera(carrera, modulos)
                
                # Show success message
                self.mostrar_mensaje(f"✅ Reporte generado: {filepath}", 'success')
                
                # Open file automatically
                import os
                os.startfile(filepath)
                
            except Exception as ex:
                self.mostrar_mensaje(f"❌ Error al generar reporte: {ex}", 'error')
                logging.error(f"Error generating career PDF: {ex}")
        
        # Header simplificado con botón de volver
        header = ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color='white', on_click=self.mostrar_dashboard),
                    ft.Text(f"Gestión: {carrera['nombre']}", size=20, weight=ft.FontWeight.BOLD, color='white')
                ]),
                ft.Row([
                ft.Text(f"Jornada: {carrera.get('jornada', 'N/A')}", color='white'),
                ft.Container(width=20),
                self._crear_componente_notificaciones(),
                ft.IconButton(
                    icon=ft.Icons.PICTURE_AS_PDF, 
                        tooltip="Exportar Reporte PDF",
                        icon_color="red",
                        on_click=exportar_pdf_carrera
                    ),
                    ft.IconButton(icon=ft.Icons.HOME, icon_color='white', on_click=self.mostrar_dashboard)
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor='#2C3E50',
            padding=20
        )

        # Paneles
        panel_docentes = self.crear_panel_docentes()
        panel_modulos = self.crear_panel_modulos(carrera)

        contenido_principal = ft.Row([
            # Columna Izquierda: Docentes
            ft.Container(
                content=panel_docentes,
                width=300,
                bgcolor='white',
                padding=20,
                border_radius=16,
                shadow=ft.BoxShadow(blur_radius=10, color='rgba(0,0,0,0.1)')
            ),
            # Columna Derecha: Módulos
            ft.Container(
                content=panel_modulos,
                expand=True,
                bgcolor='white',
                padding=20,
                border_radius=16,
                shadow=ft.BoxShadow(blur_radius=10, color='rgba(0,0,0,0.1)')
            )
        ], expand=True, spacing=20)

        self.page.add(
            ft.Column([
                header,
                ft.Container(content=contenido_principal, padding=20, expand=True)
            ], expand=True, spacing=0)
        )
        self.page.update()

    def _actualizar_vista_docentes(self, filtro=""):
        """Recarga y muestra los docentes desde la base de datos."""
        if not hasattr(self, 'docentes_list_view') or self.docentes_list_view is None:
            return

        docentes_data = self.dao.obtener_docentes()
        self.docentes_list_view.controls.clear()
        
        # Filtrar docentes por nombre
        if filtro:
            filtro_lower = filtro.lower()
            docentes_data = [d for d in docentes_data if filtro_lower in d['nombre'].lower()]
        
        if not docentes_data:
            mensaje = "No se encontraron docentes." if filtro else "No hay docentes."
            self.docentes_list_view.controls.append(ft.Text(mensaje, text_align=ft.TextAlign.CENTER, color=self.colores['text_secondary']))
        else:
            for docente in docentes_data:
                # Calcular horas asignadas y porcentaje
                horas_contratadas = docente.get('horas_contratadas', 0)
                horas_asignadas = self.dao.obtener_horas_asignadas_docente(docente['id'])
                porcentaje = (horas_asignadas / horas_contratadas * 100) if horas_contratadas > 0 else 0
                
                # Determinar color de la barra según porcentaje
                if porcentaje >= 90:
                    color_barra = 'red'  # Rojo
                elif porcentaje >= 70:
                    color_barra = 'orange'  # Amarillo/Naranja
                else:
                    color_barra = 'green'  # Verde
                
                logging.info(f"Docente {docente['nombre']}: {horas_asignadas}h/{horas_contratadas}h = {porcentaje:.1f}% -> Color: {color_barra}")
                
                # Tarjeta compacta de docente (Sidebar item)
                card = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.CircleAvatar(
                                content=ft.Text(docente['nombre'][0] if docente['nombre'] else "?"),
                                bgcolor=self.colores['secondary'],
                                radius=20
                            ),
                            ft.Column([
                                ft.Text(docente["nombre"], weight=ft.FontWeight.BOLD, size=14),
                                ft.Text(docente.get('titulo', 'Docente'), size=12, color='grey')
                            ], expand=True),
                            ft.PopupMenuButton(
                                items=[
                                    ft.PopupMenuItem(content=ft.Text("Editar"), icon=ft.Icons.EDIT, on_click=lambda e, d=docente: self.editar_docente(d)),
                                    ft.PopupMenuItem(content=ft.Text("Eliminar"), icon=ft.Icons.DELETE, on_click=lambda e, d=docente: self.eliminar_docente(d)),
                                ]
                            )
                        ], spacing=10),
                        # Barra de progreso de horas
                        ft.Column([
                            ft.Text(f"{int(horas_asignadas)}h / {int(horas_contratadas)}h ({int(porcentaje)}%)", 
                                   size=10, color='grey'),
                            ft.ProgressBar(
                                value=min(horas_asignadas / horas_contratadas, 1.0) if horas_contratadas > 0 else 0,
                                color=color_barra,
                                bgcolor='#E0E0E0',
                                height=8,
                                bar_height=8
                            )
                        ], spacing=2)
                    ], spacing=5),
                    padding=10,
                    border=ft.border.all(1, '#EEEEEE'),
                    border_radius=10,
                    bgcolor='#F9F9F9',
                    on_click=lambda e, d=docente: self.mostrar_vista_detalle_docente(d), # Click en tarjeta abre detalle
                    ink=True
                )
                self.docentes_list_view.controls.append(card)
        
        self.page.update()

    def crear_panel_docentes(self):
        """Crea el panel lateral de docentes"""
        self.docentes_list_view = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)
        
        # Campo de búsqueda
        def on_search_change(e):
            self._actualizar_vista_docentes(filtro=search_field.value)
        
        search_field = ft.TextField(
            hint_text="🔍 Buscar docente...",
            on_change=on_search_change,
            border_radius=8,
            filled=True,
            bgcolor="#F5F5F5",
            border_color="#E0E0E0",
            focused_border_color=self.colores['primary'],
            text_size=14,
            height=45
        )
        
        btn_agregar = ft.ElevatedButton(
            "Añadir Docente",
            icon=ft.Icons.ADD,
            style=ft.ButtonStyle(
                bgcolor='#27AE60',
                color='white',
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=20
            ),
            width=260,
            on_click=self.agregar_docente
        )
        
        self._actualizar_vista_docentes()

        return ft.Column([
            ft.Text("👨‍🏫 DOCENTES", weight=ft.FontWeight.BOLD, size=18, color=self.colores['primary']),
            ft.Divider(),
            search_field,
            ft.Container(height=10),
            self.docentes_list_view,
            ft.Container(content=btn_agregar, alignment=ft.Alignment(0, 0), margin=ft.margin.only(top=10))
        ], expand=True)
    
    def agregar_docente(self, e):
        self.mostrar_dialogo_docente("Agregar Nuevo Docente")

    def editar_docente(self, docente):
        self.mostrar_dialogo_docente("Editar Docente", docente)

    def eliminar_docente(self, docente):
        """Elimina un docente"""
        def confirmar_eliminacion(e):
            if e.control.text == "Confirmar":
                try:
                    self.dao.eliminar_docente(docente['id'])
                    self.mostrar_mensaje(f"✅ Docente '{docente['nombre']}' eliminado.", 'success')
                    self._actualizar_vista_docentes()
                    self._actualizar_vista_modulos()
                    self.actualizar_notificaciones()
                except Exception as ex:
                    self.mostrar_mensaje(f"❌ Error al eliminar docente: {ex}", 'error')
            self.cerrar_dialogo(dialogo_confirmacion)
        
        dialogo_confirmacion = ft.AlertDialog(
            title=ft.Text("🗑️ Confirmar Eliminación"),
            content=ft.Text(f"¿Está seguro que desea eliminar al docente '{docente['nombre']}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dialogo_confirmacion)),
                ft.ElevatedButton("Confirmar", on_click=confirmar_eliminacion, bgcolor='#E74C3C', color='white')
            ],
        )
        self.abrir_dialogo(dialogo_confirmacion)

    def _refresh_detalle_callback(self):
        """Callback para refrescar la vista de detalle reconstruyendo completamente"""
        logging.info("Callback _refresh_detalle_callback iniciado")
        
        def delayed_refresh():
            try:
                logging.info("Ejecutando refresh tras delay...")
                if hasattr(self, 'docente_detalle_actual') and self.docente_detalle_actual:
                    docente_id = self.docente_detalle_actual['id']
                    logging.info(f"Recargando datos para docente ID: {docente_id}")
                    docente_actualizado = self.dao.obtener_docente_por_id(docente_id)
                    
                    if docente_actualizado:
                        logging.info("Datos recargados. Reconstruyendo vista completa...")
                        self.mostrar_vista_detalle_docente(docente_actualizado)
                        logging.info("Vista reconstruida exitosamente")
                    else:
                        logging.warning("No se pudo recargar el docente")
            except Exception as e:
                logging.error(f"Error en refresh callback: {e}")
                import traceback
                logging.error(traceback.format_exc())
        
        # Wait 500ms for dialog to close completely before refreshing
        import threading
        timer = threading.Timer(0.5, delayed_refresh)
        timer.daemon = True
        timer.start()
        logging.info("Timer de refresh iniciado (500ms)")

    def ir_a_modulo(self, modulo, docente_origen=None):
        """Navega a la vista de módulos de la carrera y abre el diálogo de edición"""
        try:
            if not modulo:
                return
                
            carrera_id = modulo.get('carrera_id')
            if not carrera_id:
                self.mostrar_mensaje("❌ Error: El módulo no tiene carrera asignada", 'error')
                return

            # Buscar la carrera
            carreras = self.dao.obtener_carreras()
            carrera = next((c for c in carreras if c['id'] == carrera_id), None)
            
            if not carrera:
                self.mostrar_mensaje("❌ Error: No se encontró la carrera del módulo", 'error')
                return

            # Navegar a la vista de asignación
            self.mostrar_mensaje(f"🔄 Redirigiendo a {carrera['nombre']}...", 'info')
            self.mostrar_vista_asignacion(carrera)
            
            # Definir callback de retorno si venimos de un docente
            def on_save_callback():
                if docente_origen:
                    # Pequeña pausa para asegurar que la base de datos se actualizó
                    import time
                    time.sleep(0.1)
                    self.mostrar_mensaje(f"🔄 Volviendo a vista de docente...", 'info')
                    # Recargar datos del docente para asegurar frescura
                    docente_actualizado = self.dao.obtener_docente_por_id(docente_origen['id'])
                    if docente_actualizado:
                        self.mostrar_vista_detalle_docente(docente_actualizado)
                    else:
                        self.mostrar_vista_detalle_docente(docente_origen)

            # Abrir el diálogo después de un pequeño delay para asegurar que la vista cargó
            import time
            time.sleep(0.2)
            self.mostrar_dialogo_modulo("Editar Módulo", modulo, on_save=on_save_callback, on_cancel=on_save_callback)
            
        except Exception as e:
            logging.error(f"Error en ir_a_modulo: {e}")
            self.mostrar_mensaje(f"❌ Error al navegar: {e}", 'error')

    def mostrar_vista_detalle_docente(self, docente):
        """Muestra la vista detallada de un docente con su disponibilidad y módulos"""
        logging.info(f"Mostrando detalle docente: {docente.get('nombre')} (ID: {docente.get('id')})")
        self.docente_detalle_actual = docente
        self.page.clean()
        
        # --- 1. Header (Perfil y Progreso) ---
        horas_contratadas = docente.get('horas_contratadas', 0)
        modulos = self.dao.obtener_modulos_docente(docente['id'])
        horas_asignadas = sum([m['horas_teoricas'] + m['horas_practicas'] for m in modulos]) if modulos else 0
        
        progreso = min(horas_asignadas / horas_contratadas, 1.0) if horas_contratadas > 0 else 0
        porcentaje = (horas_asignadas / horas_contratadas * 100) if horas_contratadas > 0 else 0
        
        if porcentaje >= 90: color_barra = 'red'
        elif porcentaje >= 70: color_barra = 'orange'
        else: color_barra = 'green'

        def exportar_pdf(e):
            try:
                modulos_full = self.dao.obtener_modulos_docente(docente['id'])
                for m in modulos_full:
                    m['horarios'] = self.dao.obtener_horarios_modulo(m['id'])
                filepath = self.report_generator.generar_reporte_docente(docente, modulos_full)
                self.mostrar_mensaje(f"✅ Reporte generado: {filepath}", 'success')
                import os
                os.startfile(filepath)
            except Exception as ex:
                self.mostrar_mensaje(f"❌ Error al generar reporte: {ex}", 'error')

        header_content = ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.CircleAvatar(
                        content=ft.Text(docente['nombre'][0], size=30, weight=ft.FontWeight.BOLD),
                        radius=40,
                        bgcolor=self.colores['secondary']
                    ),
                    ft.Column([
                        ft.Row([
                            ft.Text(docente['nombre'], size=24, weight=ft.FontWeight.BOLD, color=self.colores['text_primary']),
                            ft.IconButton(icon=ft.Icons.EDIT, icon_size=20, tooltip="Editar Perfil", on_click=lambda e: self.editar_docente(docente))
                        ], spacing=10, alignment=ft.MainAxisAlignment.START),
                        ft.Text(docente.get('titulo', 'Sin Título'), size=16, color=self.colores['text_secondary']),
                        ft.Text(f"Contrato: {docente.get('contrato', 'N/A')}", size=14, color=self.colores['text_secondary']),
                        ft.Container(height=5),
                        ft.Row([
                            ft.Text(f"{int(horas_asignadas)}/{int(horas_contratadas)} hrs ({int(porcentaje)}%)", size=12, weight=ft.FontWeight.BOLD),
                            ft.ProgressBar(value=progreso, width=150, color=color_barra, bgcolor='#E0E0E0', height=8),
                            ft.Text("Asignadas", size=12, color='grey')
                        ], alignment=ft.MainAxisAlignment.START)
                    ], spacing=2),
                ]),
                ft.Row([
                    ft.IconButton(icon=ft.Icons.PICTURE_AS_PDF, tooltip="Exportar Reporte PDF", icon_color="red", icon_size=30, on_click=exportar_pdf),
                    ft.IconButton(icon=ft.Icons.HOME, icon_color=self.colores['primary'], icon_size=30, on_click=self.mostrar_dashboard, tooltip="Volver al Dashboard")
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=20),
            padding=20,
            bgcolor='white',
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=10, color="#1A000000")
        )

        # --- 2. Sidebar (Módulos) ---
        lista_modulos = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=10, expand=True)
        if not modulos:
            lista_modulos.controls.append(ft.Text("Sin módulos asignados", color='grey'))
        else:
            for mod in modulos:
                horarios = self.dao.obtener_horarios_modulo(mod['id'])
                horarios_texto = "Sin horario"
                if horarios:
                    horarios_list = []
                    for h in horarios:
                        h_inicio = str(h['hora_inicio'])
                        h_fin = str(h['hora_fin'])
                        if "days" in h_inicio: h_inicio = h_inicio.split(", ")[1]
                        if "days" in h_fin: h_fin = h_fin.split(", ")[1]
                        horarios_list.append(f"{h['dia']} {h_inicio[:5]}-{h_fin[:5]}")
                    horarios_texto = "\n".join(horarios_list)

                total_horas = mod.get('horas_teoricas', 0) + mod.get('horas_practicas', 0)
                
                card_modulo = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(mod['nombre'], weight=ft.FontWeight.BOLD, size=14, expand=True),
                            ft.Text(f"{total_horas}h", size=18, weight=ft.FontWeight.BOLD, color=self.colores['primary'])
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Text(f"Código: {mod['codigo']}", size=12, color='grey'),
                        ft.Text(mod.get('carrera_nombre', ''), size=10, color=self.colores['primary']),
                        ft.Divider(),
                        ft.Text(horarios_texto, size=11, color=self.colores['text_secondary'])
                    ]),
                    padding=15,
                    border=ft.border.all(1, self.colores['primary']),
                    border_radius=8,
                    bgcolor='white',
                    ink=True,
                    on_click=lambda e, m=mod: self.ir_a_modulo(m, docente_origen=docente),
                    tooltip="Ir a editar módulo"
                )
                lista_modulos.controls.append(card_modulo)

        sidebar_content = ft.Container(
            content=ft.Column([
                ft.Text("MÓDULOS ASIGNADOS", weight=ft.FontWeight.BOLD, size=16),
                ft.Divider(),
                lista_modulos
            ], expand=True),
            width=300,
            padding=20,
            bgcolor='white',
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=5, color="#0D000000")
        )

        # --- 3. Grid Horaria ---
        dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
        bloques = [
            ("08:30", "09:05"), ("09:05", "09:40"), ("09:40", "10:15"), ("10:15", "10:50"),
            ("10:50", "11:25"), ("11:25", "12:00"), ("12:00", "12:35"), ("12:35", "13:10"),
            ("13:10", "13:45"), ("13:45", "14:20"), ("14:20", "14:55"), ("14:55", "15:30"),
            ("15:30", "16:05"), ("16:05", "16:40"), ("16:40", "17:15"), ("17:15", "17:50"),
            ("17:50", "18:25"), ("18:25", "19:00"), ("19:00", "19:35"), ("19:35", "20:10"),
            ("20:10", "20:45"), ("20:45", "21:20"), ("21:20", "21:55")
        ]
        
        def hora_en_rango(hora_actual, hora_inicio, hora_fin):
            try:
                def h_to_m(h):
                    parts = str(h).split(':')
                    return int(parts[0]) * 60 + int(parts[1])
                return h_to_m(hora_actual) >= h_to_m(hora_inicio) and h_to_m(hora_actual) < h_to_m(hora_fin)
            except: return False

        modulos_con_horarios = []
        for mod in modulos:
            horarios = self.dao.obtener_horarios_modulo(mod['id'])
            if horarios:
                for h in horarios:
                    modulos_con_horarios.append({
                        'modulo': mod,
                        'dia': h['dia'],
                        'hora_inicio': h['hora_inicio'],
                        'hora_fin': h['hora_fin']
                    })
        
        disponibilidad = self.dao.obtener_disponibilidad_docente(docente['id'])
        
        headers = [ft.Container(content=ft.Text("Hora", weight=ft.FontWeight.BOLD, color='white', size=12), bgcolor='#2C3E50', padding=10, width=80, alignment=ft.Alignment(0, 0), border_radius=4)]
        for dia in dias:
            headers.append(ft.Container(content=ft.Text(dia, weight=ft.FontWeight.BOLD, color='white', size=12), bgcolor='#2C3E50', padding=10, expand=True, alignment=ft.Alignment(0, 0), border_radius=4))

        grid_rows = []
        for inicio, fin in bloques:
            row_cells = [ft.Container(content=ft.Text(inicio, size=10, weight=ft.FontWeight.BOLD), width=80, alignment=ft.Alignment(0, 0), bgcolor='#F8F9FA', border_radius=4, padding=5)]
            for dia in dias:
                modulos_en_bloque = [mh['modulo'] for mh in modulos_con_horarios if mh['dia'].upper() == dia and hora_en_rango(inicio, mh['hora_inicio'], mh['hora_fin'])]
                is_disponible = disponibilidad.get(dia, {}).get(inicio, True)
                
                if modulos_en_bloque:
                    mod = modulos_en_bloque[0]
                    cell_content = ft.Column([
                        ft.Text(mod.get('codigo', 'N/A'), size=10, weight=ft.FontWeight.BOLD, color="#1565C0"),
                        ft.Text(mod['nombre'], size=11, weight=ft.FontWeight.BOLD, overflow=ft.TextOverflow.ELLIPSIS, max_lines=1),
                        ft.Text(f"🏢 {mod.get('sala_nombre', 'Sin sala')}", size=9, color="#666666", italic=True)
                    ], spacing=1, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    bg, border = "#BBDEFB", "#2196F3"
                    tooltip = f"{mod['nombre']}\n{mod.get('codigo')}\nSala: {mod.get('sala_nombre')}\n(Ir a editar módulo)"
                    on_click = lambda e, m=mod: self.ir_a_modulo(m, docente_origen=docente)
                    ink = True
                elif is_disponible:
                    cell_content = ft.Text("Disponible", size=9)
                    bg, border = "#C8E6C9", "#4CAF50"
                    tooltip, on_click, ink = "Disponible", None, False
                else:
                    cell_content = ft.Text("No Disp.", size=9)
                    bg, border = "#FFCDD2", "#F44336"
                    tooltip, on_click, ink = "No Disponible", None, False
                
                row_cells.append(ft.Container(content=cell_content, bgcolor=bg, border=ft.border.all(1, border), border_radius=4, padding=5, height=60, expand=True, tooltip=tooltip, on_click=on_click, ink=ink))
            grid_rows.append(ft.Row(row_cells, spacing=5))

        grid_content = ft.Container(
            content=ft.Column([
                ft.Row(headers, spacing=5),
                ft.Column(grid_rows, spacing=5, scroll=ft.ScrollMode.AUTO, expand=True)
            ], expand=True),
            padding=20,
            bgcolor='white',
            border_radius=15,
            expand=True,
            shadow=ft.BoxShadow(blur_radius=5, color="#0D000000")
        )

        # --- Layout Principal ---
        def volver_atras(e):
            if hasattr(self, 'carrera_actual') and self.carrera_actual:
                self.mostrar_vista_asignacion(self.carrera_actual)
            else:
                self.mostrar_dashboard()
        
        layout = ft.Column([
            ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=volver_atras),
                ft.Text("Volver", size=16, weight=ft.FontWeight.BOLD)
            ]),
            header_content,
            ft.Container(height=10),
            ft.Row([sidebar_content, grid_content], expand=True, spacing=20)
        ], expand=True, spacing=10)

        self.page.add(layout)
        self.page.update()
        logging.info("Vista detalle docente renderizada completamente.")



    def crear_panel_docentes(self):
        """Crea el panel lateral de docentes"""
        self.docentes_list_view = ft.ListView(expand=True, spacing=10, padding=10)
        
        # Campo de búsqueda
        def on_search_change(e):
            self._actualizar_vista_docentes(filtro=search_field.value)
        
        search_field = ft.TextField(
            hint_text="🔍 Buscar docente...",
            on_change=on_search_change,
            border_radius=8,
            filled=True,
            bgcolor="#F5F5F5",
            border_color="#E0E0E0",
            focused_border_color=self.colores['primary'],
            text_size=14,
            height=45
        )
        
        self._actualizar_vista_docentes()

        btn_agregar = ft.ElevatedButton(
            "Añadir Docente",
            icon=ft.Icons.ADD,
            on_click=self.agregar_docente,
            bgcolor=self.colores['primary'],
            color='white',
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )

        return ft.Container(
            content=ft.Column([
                ft.Text("Gestión de Docentes", size=20, weight=ft.FontWeight.BOLD, color=self.colores['text_primary']),
                ft.Divider(),
                search_field,
                ft.Container(height=10),
                btn_agregar,
                ft.Container(height=10),
                self.docentes_list_view
            ]),
            padding=20,
            bgcolor='white',
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=5, color="#0D000000")
        )

    def agregar_docente(self, e):
        logging.info("=== AGREGAR_DOCENTE LLAMADO ===")
        try:
            self.mostrar_dialogo_docente("Agregar Nuevo Docente")
        except Exception as ex:
            logging.error(f"Error en agregar_docente: {ex}")
            import traceback
            logging.error(traceback.format_exc())
            self.mostrar_mensaje(f"Error al abrir diálogo: {ex}", 'error')

    def editar_docente(self, docente):
        self.mostrar_dialogo_docente("Editar Docente", docente)

    def mostrar_dialogo_docente(self, titulo, docente=None):
        logging.info(f"=== MOSTRAR_DIALOGO_DOCENTE LLAMADO: {titulo} ===")
        nombre_field = ft.TextField(label="Nombre Completo", value=docente['nombre'] if docente else "", icon=ft.Icons.PERSON)
        titulo_field = ft.TextField(label="Título Académico", value=docente['titulo'] if docente else "", icon=ft.Icons.SCHOOL)
        email_field = ft.TextField(label="Email", value=docente['email'] if docente else "", icon=ft.Icons.EMAIL)
        contrato_dd = ft.Dropdown(
            label="Tipo de Contrato",
            value=docente['contrato'] if docente else None,
            options=[ft.dropdown.Option("Planta"), ft.dropdown.Option("Honorarios"), ft.dropdown.Option("Reemplazo")],
            prefix_icon=ft.Icons.WORK
        )
        horas_field = ft.TextField(label="Horas Contratadas", value=str(docente.get('horas_contratadas', '')) if docente else "", keyboard_type=ft.KeyboardType.NUMBER, icon=ft.Icons.ACCESS_TIME, expand=True)
        evaluacion_field = ft.TextField(label="Evaluación (0.0 - 5.0)", value=str(docente.get('evaluacion', '')) if docente else "", keyboard_type=ft.KeyboardType.NUMBER, icon=ft.Icons.STAR, expand=True)

        # Availability Grid
        dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
        # Use class attribute for time blocks
        bloques_horarios = self.bloques_horarios
        
        # Dictionary to store checkbox references: {(dia, hora): checkbox}
        disponibilidad_checkboxes = {}
        last_clicked_cell = {'dia': None, 'hora': None}  # Track last clicked cell for shift+click
        
        # Load existing availability if editing
        disponibilidad_existente = {}
        horarios_ocupados = []
        
        if docente:
            disp_data = self.dao.obtener_disponibilidad_docente(docente['id'])
            disponibilidad_existente = disp_data  # {dia: {hora: bool}}
            # --- Grilla Horaria ---
            horarios_ocupados = self.dao.obtener_horarios_ocupados_docente(docente['id'])
        else:
            # For new teachers, initialize empty availability
            horarios_ocupados = []
        logging.info(f"Grilla Docente: {len(horarios_ocupados)} bloques ocupados cargados desde BD")
        
        dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
        # Helper to check if a slot is occupied
        def is_slot_occupied(dia, hora_bloque):
            def h_to_m(h_str):
                parts = str(h_str).split(':')
                return int(parts[0]) * 60 + int(parts[1])
            
            bloque_min = h_to_m(hora_bloque)
            # Assume block duration is 45 mins
            bloque_fin_min = bloque_min + 45
            
            for ocupado in horarios_ocupados:
                if ocupado['dia'].upper() == dia.upper():
                    inicio = h_to_m(ocupado['hora_inicio'])
                    fin = h_to_m(ocupado['hora_fin'])
                    
                    # Check overlap: (StartA <= EndB) and (EndA >= StartB)
                    if (bloque_min < fin) and (bloque_fin_min > inicio):
                        return True, ocupado['modulo_nombre']
            return False, None

        # Function to toggle entire column (day)
        def toggle_column(dia):
            def handler(e):
                # Check if all cells in this column are selected
                cells_in_column = [(d, h) for (d, h) in disponibilidad_checkboxes.keys() if d == dia]
                
                # Filter out locked cells from toggle logic
                toggleable_cells = [key for key in cells_in_column if not disponibilidad_checkboxes[key].data.get('locked', False)]
                
                if not toggleable_cells:
                    return

                all_selected = all(disponibilidad_checkboxes[key].data['available'] for key in toggleable_cells)
                
                # If all selected, deselect all. Otherwise, select all
                new_state = not all_selected
                
                for key in toggleable_cells:
                    cell = disponibilidad_checkboxes[key]
                    cell.data['available'] = new_state
                    cell.bgcolor = '#27AE60' if new_state else '#95A5A6'
                    cell.tooltip = f"{'Disponible' if new_state else 'No disponible'} - Click para cambiar"
                    cell.update()
            return handler
        
        # Create grid headers with expand for equal width
        grid_headers = [ft.Container(content=ft.Text("Hora", size=11, weight=ft.FontWeight.BOLD, color='white'), 
                                    bgcolor='#2C3E50', padding=8, alignment=ft.Alignment(0, 0), 
                                    border_radius=4, width=80)]
        for dia in dias:
            header = ft.Container(
                content=ft.Text(dia, size=11, weight=ft.FontWeight.BOLD, color='white', text_align=ft.TextAlign.CENTER),
                bgcolor='#2C3E50',
                padding=8,
                alignment=ft.Alignment(0, 0),
                border_radius=4,
                expand=True,
                ink=True,
                tooltip=f"Click para seleccionar/deseleccionar todo {dia}",
                on_click=toggle_column(dia)
            )
            grid_headers.append(header)
        
        # Create grid rows
        grid_rows = [ft.Row(grid_headers, spacing=5)]
        
        for hora in bloques_horarios:
            row_cells = [
                ft.Container(
                    content=ft.Text(hora, size=11, weight=ft.FontWeight.BOLD),
                    width=80,
                    alignment=ft.Alignment(0, 0),
                    bgcolor='#F8F9FA',
                    border_radius=4,
                    padding=5
                )
            ]
            
            for dia in dias:
                # Check if this slot is marked as available
                is_available = disponibilidad_existente.get(dia, {}).get(hora, True)  # Default to available
                
                # Check if occupied by module
                occupied, module_name = is_slot_occupied(dia, hora)
                is_locked = False
                
                if occupied:
                    is_available = True # Must be available if occupied
                    is_locked = True
                
                # Create a clickable container instead of checkbox
                def create_availability_cell(d, h, available, locked, mod_name):
                    # Determine color
                    if locked:
                        color = '#F1C40F' # Yellow for locked/occupied
                        tooltip_text = f"Ocupado por {mod_name} (No modificable)"
                    else:
                        color = '#27AE60' if available else '#95A5A6'
                        tooltip_text = f"{'Disponible' if available else 'No disponible'} - Click para cambiar | Shift+Click para rango"

                    # Store state in container's data
                    cell_container = ft.Container(
                        data={'dia': d, 'hora': h, 'available': available, 'locked': locked},
                        bgcolor=color,
                        border_radius=6,
                        padding=10,
                        alignment=ft.Alignment(0, 0),
                        expand=True,
                        ink=not locked,
                        tooltip=tooltip_text
                    )
                    
                    def toggle_availability(e):
                        if cell_container.data['locked']:
                            return # Do nothing if locked
                            
                        # Check if shift key is pressed for range selection
                        if hasattr(e, 'shift') and e.shift and last_clicked_cell['dia'] == d and last_clicked_cell['hora'] is not None:
                            # Range selection within the same column
                            current_hora_idx = bloques_horarios.index(h)
                            last_hora_idx = bloques_horarios.index(last_clicked_cell['hora'])
                            
                            # Determine range
                            start_idx = min(current_hora_idx, last_hora_idx)
                            end_idx = max(current_hora_idx, last_hora_idx)
                            
                            # Get the state of the current cell to apply to range
                            target_state = cell_container.data['available']
                            
                            # Apply to all cells in range
                            for idx in range(start_idx, end_idx + 1):
                                hora_in_range = bloques_horarios[idx]
                                key = (d, hora_in_range)
                                if key in disponibilidad_checkboxes:
                                    range_cell = disponibilidad_checkboxes[key]
                                    if not range_cell.data['locked']: # Skip locked cells
                                        range_cell.data['available'] = target_state
                                        range_cell.bgcolor = '#27AE60' if target_state else '#95A5A6'
                                        range_cell.tooltip = f"{'Disponible' if target_state else 'No disponible'} - Click para cambiar | Shift+Click para rango"
                                        range_cell.update()
                        else:
                            # Normal toggle
                            cell_container.data['available'] = not cell_container.data['available']
                            cell_container.bgcolor = '#27AE60' if cell_container.data['available'] else '#95A5A6'
                            cell_container.tooltip = f"{'Disponible' if cell_container.data['available'] else 'No disponible'} - Click para cambiar | Shift+Click para rango"
                            cell_container.update()
                        
                        # Update last clicked cell
                        last_clicked_cell['dia'] = d
                        last_clicked_cell['hora'] = h
                    
                    cell_container.on_click = toggle_availability
                    return cell_container
                
                cell = create_availability_cell(dia, hora, is_available, is_locked, module_name)
                disponibilidad_checkboxes[(dia, hora)] = cell  # Store container instead of checkbox
                
                row_cells.append(cell)
            
            grid_rows.append(ft.Row(row_cells, spacing=5))
        
        availability_grid = ft.Container(
            content=ft.Column(grid_rows, spacing=5, scroll=ft.ScrollMode.AUTO),
            bgcolor='white',
            border=ft.border.all(1, '#BDC3C7'),
            border_radius=8,
            padding=10,
            height=450  # Max height to fit in dialog and enable scrolling
        )

        def guardar_docente_handler(e):
            logging.info("Iniciando guardar_docente_handler")
            try:
                nombre = nombre_field.value
                logging.info(f"Nombre: {nombre}")
                if not nombre:
                    self.mostrar_mensaje("El nombre es obligatorio.", 'error')
                    return

                logging.info(f"Horas raw: {horas_field.value}")
                horas_val = int(horas_field.value) if horas_field.value and horas_field.value.strip() else 0
                logging.info(f"Horas parsed: {horas_val}")

                logging.info(f"Evaluacion raw: {evaluacion_field.value}")
                eval_val = float(evaluacion_field.value) if evaluacion_field.value else 0.0
                logging.info(f"Evaluacion parsed: {eval_val}")

                docente_data = (
                    nombre,
                    titulo_field.value,
                    contrato_dd.value,
                    horas_val,
                    email_field.value,
                    eval_val
                )
                docente_id = docente['id'] if docente else None
                
                logging.info(f"Llamando a dao.guardar_docente con id: {docente_id}")
                # Save docente
                saved_id = self.dao.guardar_docente(docente_data, docente_id)
                logging.info(f"Docente guardado, ID: {saved_id}")
                
                # If new docente, use the returned ID
                if not docente_id:
                    docente_id = saved_id
                
                # Save availability
                if docente_id:
                    logging.info("Guardando disponibilidad...")
                    # Convert container states to dictionary format
                    disponibilidad_dict = {}
                    for (dia, hora), cell in disponibilidad_checkboxes.items():
                        if dia not in disponibilidad_dict:
                            disponibilidad_dict[dia] = {}
                        # Get the state from the container's data
                        disponibilidad_dict[dia][hora] = cell.data['available']
                    
                    self.dao.guardar_disponibilidad_docente(docente_id, disponibilidad_dict)
                    logging.info("Disponibilidad guardada.")
                
                self.mostrar_mensaje(f"✅ Docente '{nombre}' guardado exitosamente.", 'success')
                self.cerrar_dialogo(dialogo_docente)
                self._actualizar_vista_docentes()
                
                # Refresh detail view if we were editing (to show updated availability)
                if docente:
                    # Fetch updated docente data
                    docentes = self.dao.obtener_docentes()
                    docente_actualizado = next((d for d in docentes if d['id'] == docente_id), None)
                    if docente_actualizado:
                        self.mostrar_vista_detalle_docente(docente_actualizado)

            except Exception as ex:
                logging.error(f"Excepcion en guardar_docente_handler: {ex}")
                import traceback
                logging.error(traceback.format_exc())
                self.mostrar_mensaje(f"❌ Error al guardar docente: {ex}", 'error')

        # --- LAYOUT REFACTORING ---
    
        # Left Column: Form Fields
        left_column = ft.Column([
            ft.Text("Información Personal", weight="bold", color=self.colores['primary']),
            nombre_field,
            titulo_field,
            email_field,
            ft.Divider(),
            ft.Text("Información Contractual", weight="bold", color=self.colores['primary']),
            contrato_dd,
            ft.Row([horas_field, evaluacion_field], spacing=10),
        ], scroll=ft.ScrollMode.AUTO, expand=True, alignment=ft.MainAxisAlignment.START, spacing=15)
        
        # Right Column: Availability Grid
        grid_container = ft.Column([
            ft.Text("Disponibilidad Horaria", weight="bold", color=self.colores['primary']),
            ft.Text("Verde: Disponible | Gris: No Disponible | Amarillo: Ocupado (No editable)", size=12, color="grey"),
            availability_grid
        ], expand=True, spacing=10)

        dialogo_docente = ft.AlertDialog(
            title=ft.Text(titulo, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=left_column, 
                        expand=2, # 40% width
                        padding=ft.padding.only(right=20),
                        alignment=ft.Alignment(-1, -1)
                    ),
                    ft.VerticalDivider(width=1),
                    ft.Container(
                        content=grid_container, 
                        expand=3, # 60% width
                        padding=10,
                        alignment=ft.Alignment(-1, -1)
                    )
                ], expand=True),
                width=1100,
                height=600
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dialogo_docente)),
                ft.ElevatedButton("💾 Guardar", bgcolor='#27AE60', color='white', on_click=guardar_docente_handler)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        logging.info("=== Abriendo diálogo de docente ===")
        self.abrir_dialogo(dialogo_docente)
        logging.info("=== Diálogo de docente abierto ===")
    
    
    def _crear_tarjeta_modulo(self, modulo, mostrar_editar=True, on_save=None):
        """Crea una tarjeta de módulo unificada con información de horarios"""
        # Obtener horarios del módulo
        horarios = self.dao.obtener_horarios_modulo(modulo['id'])
        
        # Formatear horarios para mostrar
        horarios_texto = []
        if horarios:
            for h in horarios:
                hora_inicio = h['hora_inicio']
                hora_fin = h['hora_fin']
                
                # Convert timedelta to string if needed
                if hasattr(hora_inicio, 'total_seconds'):
                    total_seconds = int(hora_inicio.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    hora_inicio = f"{hours:02d}:{minutes:02d}"
                
                if hasattr(hora_fin, 'total_seconds'):
                    total_seconds = int(hora_fin.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    hora_fin = f"{hours:02d}:{minutes:02d}"
                
                horarios_texto.append(f"{h['dia']}: {hora_inicio}-{hora_fin}")
        
        horarios_display = "\n".join(horarios_texto) if horarios_texto else "Sin horarios asignados"
        
        # Check if teacher is assigned
        docente_id = modulo.get('docente_id')
        has_docente = docente_id is not None and docente_id > 0
        
        # Check for schedule conflicts
        has_conflicts = False
        if has_docente and modulo.get('sala_id') and horarios:
            try:
                # Check teacher conflict
                tiene_conflicto, _, _ = self.dao.validar_conflicto_horario_docente(
                    docente_id, horarios, modulo['id']
                )
                if tiene_conflicto:
                    has_conflicts = True
                
                # Check room conflict
                if not has_conflicts:
                    tiene_conflicto, _, _ = self.dao.validar_conflicto_sala(
                        modulo['sala_id'], horarios, modulo['id']
                    )
                    if tiene_conflicto:
                        has_conflicts = True
                
                # Check semester conflict
                if not has_conflicts and modulo.get('carrera_id') and modulo.get('semestre'):
                    tiene_conflicto, _, _ = self.dao.validar_conflicto_semestre_par_impar(
                        modulo['carrera_id'], modulo['semestre'], horarios, modulo['id']
                    )
                    if tiene_conflicto:
                        has_conflicts = True
            except Exception as e:
                logging.error(f"Error checking conflicts for module {modulo['id']}: {e}")
        
        header_content = [
            ft.Icon(ft.Icons.BOOK, color='#3498DB', size=24),
            ft.Text(value=modulo["nombre"], size=16, weight=ft.FontWeight.BOLD, 
                   color=self.colores['text_primary'], expand=True)
        ]
        
        if not has_docente:
            header_content.append(ft.Icon(ft.Icons.WARNING, color="red", tooltip="⚠️ Sin docente asignado"))
        elif has_conflicts:
            header_content.append(ft.Icon(ft.Icons.ERROR, color="#E74C3C", tooltip="⚠️ Conflicto de horario"))

        # Contenido con scroll (información del módulo)
        info_content = ft.Column([
            ft.Row(header_content, alignment=ft.MainAxisAlignment.START),
            ft.Divider(),
            ft.Text(f"🔢 Código: {modulo.get('codigo', 'N/A')}", size=12),
            ft.Text(f"👨‍🏫 {modulo.get('docente_nombre', 'Sin asignar')}", size=12, weight=ft.FontWeight.BOLD, color="red" if not has_docente else self.colores['text_primary']),
            ft.Text(f"🏢 {modulo.get('sala_nombre', 'Sin sala')}", size=12),
            ft.Text(f"📚 {modulo.get('horas_teoricas', 0)}h T + {modulo.get('horas_practicas', 0)}h P", size=12),
            ft.Container(height=5),
            ft.Container(
                content=ft.Column([
                    ft.Text("📅 Horarios:", size=11, weight=ft.FontWeight.BOLD, color=self.colores['primary']),
                    ft.Text(horarios_display, size=10, color='grey')
                ], spacing=2),
                bgcolor='#F5F5F5',
                padding=8,
                border_radius=5
            ),
        ], spacing=5, scroll=ft.ScrollMode.AUTO)
        
        # Estructura de la tarjeta: contenido con scroll + botón fijo abajo
        if mostrar_editar:
            card_structure = ft.Column([
                ft.Container(
                    content=info_content,
                    expand=True  # Ocupa el espacio disponible
                ),
                ft.Divider(height=1),
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton("Editar", icon=ft.Icons.EDIT, 
                                        on_click=lambda e, m=modulo: self.editar_modulo(m, on_save=on_save), 
                                        style=ft.ButtonStyle(padding=5, bgcolor='#3498DB', color='white')),
                        ft.ElevatedButton("Eliminar", icon=ft.Icons.DELETE, 
                                        on_click=lambda e, m=modulo: self.eliminar_modulo(m), 
                                        style=ft.ButtonStyle(padding=5, bgcolor='#E74C3C', color='white')),
                    ], alignment=ft.MainAxisAlignment.END, spacing=5),
                    padding=ft.padding.only(top=5)
                )
            ], spacing=0)
        else:
            # Sin botón de editar, solo el contenido
            card_structure = info_content
        
        return ft.Card(
            content=ft.Container(
                content=card_structure,
                padding=15,
                height=350  # Altura fija para mantener consistencia
            ),
            elevation=2,
            shape=ft.RoundedRectangleBorder(radius=12)
        )
    
    def _actualizar_vista_modulos(self, carrera_id=None, semestre_filtro=None, filtro_texto=""):
        """Recarga y muestra los módulos, filtrando por semestre y texto."""
        if not hasattr(self, 'modulos_list_view') or self.modulos_list_view is None:
            return
            
        # Si estamos en la vista de asignación, filtramos por la carrera seleccionada
        if self.carrera_seleccionada:
            carrera_id = self.carrera_seleccionada['id']
            modulos = self.dao.obtener_modulos_carrera(carrera_id)
        else:
            # Fallback si no hay carrera seleccionada (no debería pasar en esta vista)
            modulos = []

        # Filtrar por texto
        if filtro_texto:
            modulos = [m for m in modulos if filtro_texto.lower() in m['nombre'].lower()]

        # Filtrar por semestre si se especifica
        if semestre_filtro and semestre_filtro != "Todos":
            try:
                semestre_num = int(semestre_filtro.split(" ")[1]) # "Semestre 1" -> 1
                modulos = [m for m in modulos if m.get('semestre') == semestre_num]
            except:
                pass # Si falla el parseo, mostrar todos

        self.modulos_list_view.controls.clear()
        
        if not modulos:
             mensaje = "No se encontraron módulos." if filtro_texto else "No hay módulos registrados para este semestre."
             self.modulos_list_view.controls.append(ft.Text(mensaje, text_align=ft.TextAlign.CENTER))
        else:
            cards_container = ft.Row(
                wrap=True,
                spacing=20,
                run_spacing=20,
                alignment=ft.MainAxisAlignment.START
            )
            
            # Define callback to refresh with current filters
            # Use default arguments to capture current values in closure
            def refresh_callback(cid=carrera_id, sf=semestre_filtro, ft=filtro_texto):
                self._actualizar_vista_modulos(cid, sf, ft)

            for modulo in modulos:
                card = self._crear_tarjeta_modulo(modulo, mostrar_editar=True, on_save=refresh_callback)
                # Wrap card in container with fixed width to simulate grid
                cards_container.controls.append(ft.Container(content=card, width=300))
            
            self.modulos_list_view.controls.append(cards_container)
        
        self.page.update()

    def crear_panel_modulos(self, carrera):
        """Crea el panel principal de módulos con pestañas por semestre"""
        self.modulos_list_view = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=20
        )
        
        # Campo de búsqueda
        search_field = ft.TextField(
            hint_text="🔍 Buscar módulo...",
            border_radius=8,
            filled=True,
            bgcolor="#F5F5F5",
            border_color="#E0E0E0",
            focused_border_color=self.colores['primary'],
            text_size=14,
            height=45,
            expand=True
        )

        btn_agregar = ft.ElevatedButton(
            "Añadir Módulo",
            icon=ft.Icons.ADD,
            on_click=lambda e: self.agregar_modulo(e, carrera),
            style=ft.ButtonStyle(bgcolor='#27AE60', color='white', padding=20)
        )
        
        # Obtener semestres de la carrera para crear las pestañas
        # Obtener semestres de la carrera para crear las pestañas
        semestres = self.dao.obtener_semestres_carrera(carrera['id'])
        tab_labels = ["Todos"]
        tabs = [ft.Tab(text="Todos")]
        if semestres:
            semestres.sort()
            for s in semestres:
                label = f"Semestre {s}"
                tab_labels.append(label)
                tabs.append(ft.Tab(text=label))
        
        # Handler para cambio de pestaña
        def on_tab_change(e):
            # En la versión 0.28.3, e.control.tabs[index].text es válido
            semestre_seleccionado = tabs[tabs_control.selected_index].text
            self._actualizar_vista_modulos(carrera['id'], semestre_seleccionado, search_field.value)

        # Handler para búsqueda
        def on_search_change(e):
            semestre_seleccionado = tabs[tabs_control.selected_index].text
            self._actualizar_vista_modulos(carrera['id'], semestre_seleccionado, search_field.value)
            
        search_field.on_change = on_search_change

        tabs_control = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=tabs,
            on_change=on_tab_change,
            scrollable=True
        )
        
        # Cargar vista inicial (Todos)
        self._actualizar_vista_modulos(carrera['id'], "Todos")

        return ft.Column([
            ft.Row([
                ft.Text(f"📖 {carrera['nombre']}", size=24, weight=ft.FontWeight.BOLD, color=self.colores['primary']),
                btn_agregar
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([search_field], alignment=ft.MainAxisAlignment.CENTER),
            tabs_control,
            ft.Divider(),
            self.modulos_list_view,
        ], expand=True)

    def agregar_modulo(self, e, carrera=None):
        self.mostrar_dialogo_modulo("Agregar Nuevo Módulo", carrera_preseleccionada=carrera)

    def editar_modulo(self, modulo, on_save=None):
        logging.info(f"=== EDITAR_MODULO LLAMADO: {modulo.get('nombre')} ===")
        self.mostrar_dialogo_modulo("Editar Módulo", modulo, on_save)

    def eliminar_modulo(self, modulo):
        """Elimina un módulo con confirmación"""
        logging.info(f"=== ELIMINAR_MODULO LLAMADO: {modulo.get('nombre')} ===")
        def confirmar_eliminacion(e):
            if e.control.text == "Confirmar":
                try:
                    self.dao.eliminar_modulo(modulo['id'])
                    self.mostrar_mensaje(f"✅ Módulo '{modulo['nombre']}' eliminado correctamente.", 'success')
                    self._actualizar_vista_modulos()
                except Exception as ex:
                    self.mostrar_mensaje(f"❌ Error al eliminar módulo: {ex}", 'error')
            self.cerrar_dialogo(dialogo_confirmacion)
        
        dialogo_confirmacion = ft.AlertDialog(
            title=ft.Text("🗑️ Confirmar Eliminación", weight=ft.FontWeight.BOLD),
            content=ft.Text(f"¿Está seguro que desea eliminar el módulo '{modulo['nombre']}'?\n\n⚠️ Esta acción eliminará también todos los horarios asociados y no se puede deshacer."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dialogo_confirmacion)),
                ft.ElevatedButton("Confirmar", on_click=confirmar_eliminacion, bgcolor='#E74C3C', color='white')
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.abrir_dialogo(dialogo_confirmacion)

    def mostrar_dialogo_modulo(self, titulo, modulo=None, on_save=None, on_cancel=None, carrera_preseleccionada=None):
        logging.info(f"Abriendo diálogo módulo: {titulo}")
        try:
            nombre_field = ft.TextField(label="Nombre del Módulo", value=modulo['nombre'] if modulo else "")
            codigo_field = ft.TextField(label="Código", value=modulo['codigo'] if modulo else "")
            horas_t_field = ft.TextField(label="Horas Teóricas", value=str(modulo.get('horas_teoricas', 0)) if modulo else "0", keyboard_type=ft.KeyboardType.NUMBER)
            horas_p_field = ft.TextField(label="Horas Prácticas", value=str(modulo.get('horas_practicas', 0)) if modulo else "0", keyboard_type=ft.KeyboardType.NUMBER)
            alumnos_field = ft.TextField(label="Alumnos Proyectados", value=str(modulo.get('alumnos_proyectados', 0)) if modulo else "0", keyboard_type=ft.KeyboardType.NUMBER)
            semestre_field = ft.TextField(label="Semestre", value=str(modulo.get('semestre', 1)) if modulo else "1", keyboard_type=ft.KeyboardType.NUMBER)

            # Error Container for Validation
            error_validacion = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ERROR_OUTLINE, color="white"),
                    ft.Text("", color="white", weight="bold")
                ]),
                bgcolor="#E74C3C",
                padding=10,
                border_radius=5,
                visible=False
            )

            # Dropdowns para relaciones
            logging.info("DEBUG: Cargando carreras...")
            carreras = self.dao.obtener_carreras()
            logging.info(f"DEBUG: {len(carreras)} carreras cargadas")
            
            # Determinar valor inicial de carrera
            carrera_inicial = None
            if modulo and modulo.get('carrera_id'):
                carrera_inicial = str(modulo['carrera_id'])
            elif carrera_preseleccionada:
                carrera_inicial = str(carrera_preseleccionada['id'])

            carrera_dd = ft.Dropdown(
                label="Carrera",
                value=carrera_inicial,
                options=[ft.dropdown.Option(key=str(c['id']), text=c['nombre']) for c in carreras],
                disabled=True # Carrera no editable
            )

            logging.info("DEBUG: Cargando docentes...")
            docentes = self.dao.obtener_docentes()
            logging.info(f"DEBUG: {len(docentes)} docentes cargados")
            
            docente_dd = ft.Dropdown(
                label="Docente",
                value=str(modulo['docente_id']) if modulo and modulo.get('docente_id') else None,
                options=[ft.dropdown.Option(key=str(d['id']), text=d['nombre']) for d in docentes]
            )

            # Sala Preferente
            sala_dd = ft.Dropdown(
                label="Sala Preferente",
                value=str(modulo['sala_id']) if modulo and modulo.get('sala_id') else None,
                options=[],
                disabled=True
            )

            def actualizar_salas_por_carrera(e=None):
                carrera_id = carrera_dd.value
                if not carrera_id:
                    sala_dd.options = []
                    sala_dd.value = None
                    sala_dd.disabled = True
                    if sala_dd.page:
                        sala_dd.update()
                    return

                salas_carrera = self.dao.obtener_salas_carrera(carrera_id)
                sala_dd.options = [ft.dropdown.Option(key=str(s['id']), text=s['nombre']) for s in salas_carrera]
                sala_dd.disabled = False
                if sala_dd.value:
                    salas_ids = [str(s['id']) for s in salas_carrera]
                    if sala_dd.value not in salas_ids:
                        sala_dd.value = None
                if sala_dd.page:
                    sala_dd.update()

            carrera_dd.on_change = actualizar_salas_por_carrera

            # Inicializar las salas si hay una carrera seleccionada (modo edición)
            if carrera_dd.value:
                actualizar_salas_por_carrera()

            # --- INTERACTIVE GRID LOGIC ---
            grid_container = ft.Column(scroll=ft.ScrollMode.AUTO, height=400)
            grid_cells = {} # {(dia, hora): cell_control}
            
            def actualizar_grilla_docente(e=None):
                docente_id = docente_dd.value
                sala_id = sala_dd.value
                grid_cells.clear()
                
                if not docente_id:
                    grid_container.controls = [ft.Text("Seleccione un docente para ver su disponibilidad", italic=True, color='grey')]
                    if grid_container.page:
                        grid_container.update()
                    return

                # Obtener semestre del módulo para filtrar conflictos
                semestre_modulo = None
                
                # Priorizar el valor actual del campo (lo que el usuario está viendo/editando)
                if semestre_field.value:
                    try:
                        semestre_modulo = int(semestre_field.value)
                    except:
                        # Si el campo tiene texto inválido, intentar usar el del módulo original si existe
                        if modulo:
                            semestre_modulo = modulo.get('semestre')
                elif modulo:
                    # Si el campo está vacío pero estamos editando (raro, pero posible)
                    semestre_modulo = modulo.get('semestre')

                # Fetch data con filtro de semestre
                disponibilidad = self.dao.obtener_disponibilidad_docente(docente_id)
                ocupados_docente = self.dao.obtener_horarios_ocupados_docente(docente_id, semestre_modulo) or []
                ocupados_sala = []
                if sala_id:
                    ocupados_sala = self.dao.obtener_horarios_ocupados_sala(sala_id, semestre_modulo) or []
                
                # If editing, get current module schedules
                mod_horarios = []
                if modulo and str(modulo.get('docente_id')) == str(docente_id):
                    mod_horarios = self.dao.obtener_horarios_modulo(modulo['id']) or []
                    logging.info(f"Módulo {modulo.get('nombre')}: {len(mod_horarios)} horarios encontrados")
                    for h in mod_horarios:
                        logging.info(f"  - Horario: {h.get('dia')} {h.get('hora_inicio')}-{h.get('hora_fin')}")
                
                # DEBUG: Log room occupation data
                logging.info(f"DEBUG actualizar_grilla: sala_id={sala_id}, ocupados_sala count={len(ocupados_sala) if ocupados_sala else 0}")
                if sala_id and ocupados_sala:
                    logging.info(f"DEBUG: Sala {sala_id} tiene {len(ocupados_sala)} horarios ocupados")
                    for oc in ocupados_sala[:3]:  # Show first 3
                        logging.info(f"  - {oc.get('dia')} {oc.get('hora_inicio')}-{oc.get('hora_fin')} por módulo ID {oc.get('modulo_id')} ({oc.get('modulo_nombre')})")
                    if modulo:
                        logging.info(f"DEBUG: Módulo actual ID: {modulo.get('id')}")
                else:
                    logging.info(f"DEBUG: NO room occupation data - sala_id={sala_id}, ocupados_sala={len(ocupados_sala) if ocupados_sala else 'None'}")


                # Helper to check if slot is occupied by OTHER module
                def get_slot_status(dia, hora_bloque):
                    from datetime import timedelta
                    def h_to_m(h_str):
                        """Convierte hora string o timedelta a minutos"""
                        if isinstance(h_str, timedelta):
                            return int(h_str.total_seconds() / 60)
                        h, m = map(int, h_str.split(':'))
                        return h * 60 + m
                    
                    bloque_min = h_to_m(hora_bloque)
                    bloque_fin_min = bloque_min + 45
                    
                    # 1. Check if this block belongs to THIS module
                    is_this_module = False
                    for h in mod_horarios:
                        if h['dia'].upper() == dia.upper():
                            h_inicio_min = h_to_m(h['hora_inicio'])
                            h_fin_min = h_to_m(h['hora_fin'])
                            if (bloque_min < h_fin_min) and (bloque_fin_min > h_inicio_min):
                                is_this_module = True
                                break
                    
                    # 2. Check if occupied by ANY OTHER module (Teacher)
                    occupied_by_teacher = None
                    for oc in ocupados_docente:
                        if oc['dia'].upper() == dia.upper():
                            inicio = h_to_m(oc['hora_inicio'])
                            fin = h_to_m(oc['hora_fin'])
                            if (bloque_min < fin) and (bloque_fin_min > inicio):
                                # Skip if this is the current module
                                if modulo and str(oc.get('modulo_id')) == str(modulo.get('id')):
                                    continue
                                occupied_by_teacher = oc
                                break
                    
                    # 3. Check if occupied by ANY OTHER module (Room)
                    occupied_by_room = None
                    if sala_id:
                        for oc in ocupados_sala:
                            if oc['dia'].upper() == dia.upper():
                                inicio = h_to_m(oc['hora_inicio'])
                                fin = h_to_m(oc['hora_fin'])
                                if (bloque_min < fin) and (bloque_fin_min > inicio):
                                    # Skip if this is the current module
                                    if modulo and str(oc.get('modulo_id')) == str(modulo.get('id')):
                                        continue
                                    occupied_by_room = oc
                                    break

                    # 4. Determine Status
                    # If occupied by others, it's a conflict or locked
                    if occupied_by_teacher:
                        info = f"Docente ocupado en {occupied_by_teacher['modulo_nombre']}"
                        if is_this_module:
                            return "CONFLICT", info # It's mine but conflicts!
                        return "LOCKED", info
                    
                    if occupied_by_room:
                        info = f"Sala ocupada por {occupied_by_room['modulo_nombre']}"
                        if is_this_module:
                            return "CONFLICT", info # It's mine but conflicts!
                        return "LOCKED", info

                    # If no conflict, check if it's mine
                    if is_this_module:
                        return "SELECTED", None

                    # Check availability preference
                    is_teacher_available = disponibilidad.get(dia, {}).get(hora_bloque, True)
                    if is_teacher_available:
                        return "AVAILABLE", None
                    else:
                        return "UNAVAILABLE", None

                # Build Grid
                dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
                
                # Headers
                headers = [ft.Container(width=80, content=ft.Text("Hora", weight="bold", color="white"), bgcolor="#2C3E50", padding=5, alignment=ft.Alignment(0, 0))]
                for d in dias:
                    headers.append(ft.Container(expand=True, content=ft.Text(d, weight="bold", color="white"), bgcolor="#2C3E50", padding=5, alignment=ft.Alignment(0, 0)))
                
                rows = [ft.Row(headers)]
                
                for hora in self.bloques_horarios:
                    row_cells = [ft.Container(width=80, content=ft.Text(hora, weight="bold"), bgcolor="#ECF0F1", padding=5, alignment=ft.Alignment(0, 0))]
                    
                    for dia in dias:
                        status, info = get_slot_status(dia, hora)
                        
                        color = "#95A5A6" # Default Gray (Unavailable/Locked)
                        tooltip = "No disponible"
                        clickable = False
                        data_status = "unavailable"

                        if status == "LOCKED":
                            color = "#E74C3C" # Red for locked/conflict
                            tooltip = f"{info} (No modificable)"
                            clickable = False
                            data_status = "locked"
                        elif status == "CONFLICT":
                            color = "#C0392B" # Dark Red for self-conflict
                            tooltip = f"{info} (CONFLICTO - Click para quitar)"
                            clickable = True # Allow deselecting to fix conflict
                            data_status = "conflict" # Separate status for conflicts
                        elif status == "SELECTED":
                            color = "#F1C40F" # Yellow for selected
                            tooltip = "Asignado a este módulo (Click para quitar)"
                            clickable = True
                            data_status = "selected"
                        elif status == "AVAILABLE":
                            color = "#27AE60" # Green for available
                            tooltip = "Disponible (Click para asignar)"
                            clickable = True
                            data_status = "available"
                        elif status == "UNAVAILABLE":
                            color = "#95A5A6" # Gray
                            tooltip = "Docente no disponible"
                            clickable = False
                            data_status = "unavailable"
                        
                        cell = ft.Container(
                            expand=True,
                            bgcolor=color,
                            border_radius=4,
                            padding=10,
                            data={'status': data_status, 'dia': dia, 'hora': hora},
                            tooltip=tooltip,
                            ink=clickable,
                            on_click=lambda e, c=None: toggle_cell(e) if c else None # Placeholder
                        )
                        
                        # Closure hack for event handler
                        def create_handler(c):
                            def handler(e):
                                if c.data['status'] == "locked" or c.data['status'] == "unavailable":
                                    return
                                
                                # Handle conflict blocks: deselect them and return to locked
                                if c.data['status'] == "conflict":
                                    # Return to locked state because the slot is occupied by another module
                                    c.data['status'] = "locked"
                                    c.bgcolor = "#E74C3C"  # Red for locked
                                    c.tooltip = "Ocupado por otro módulo (No modificable)"
                                    c.update()
                                    actualizar_progreso_docente()
                                    return
                                
                                if c.data['status'] == "available":
                                    # Validate if teacher has enough hours
                                    if docente_dd.value:
                                        docente_id = int(docente_dd.value)
                                        docente = next((d for d in docentes if d['id'] == docente_id), None)
                                        if docente:
                                            horas_contrato = docente.get('horas_contratadas', 0)
                                            
                                            # Calculate currently assigned hours (from DB) - ACADEMIC
                                            modulos_docente = self.dao.obtener_modulos_docente(docente_id)
                                            horas_asignadas_db_academicas = sum([m['horas_teoricas'] + m['horas_practicas'] for m in modulos_docente if m['id'] != (modulo['id'] if modulo else -1)])
                                            
                                            # Calculate hours selected in current grid - ACADEMIC
                                            bloques_seleccionados = 0
                                            for cell in grid_cells.values(): 
                                                if cell.data.get('status') == 'selected': 
                                                    bloques_seleccionados += 1
                                            
                                            # Check if adding 1 more block exceeds contract hours (Chronological)
                                            total_academicas_futuras = horas_asignadas_db_academicas + bloques_seleccionados + 1
                                            total_cronologicas_futuras = total_academicas_futuras * 0.75
                                            
                                            if total_cronologicas_futuras > horas_contrato:
                                                self.mostrar_mensaje(f"⚠️ Límite de horas excedido ({horas_contrato}h cronológicas). No se puede asignar más.", 'warning')
                                                return

                                    c.data['status'] = "selected"
                                    c.bgcolor = "#F1C40F"
                                    c.tooltip = "Asignado a este módulo"
                                else: # selected
                                    c.data['status'] = "available"
                                    c.bgcolor = "#27AE60"
                                    c.tooltip = "Disponible"
                                c.update()
                                actualizar_progreso_docente() # Call after cell update
                            return handler
                        
                        cell.on_click = create_handler(cell)
                        grid_cells[(dia, hora)] = cell
                        row_cells.append(cell)
                    
                    rows.append(ft.Row(row_cells, spacing=2))
                
                grid_container.controls = rows
                if grid_container.page:
                    grid_container.update()

            # Progress Bar for Teacher Hours
            progreso_horas = ft.ProgressBar(width=400, color="green", bgcolor="#E0E0E0", value=0)
            texto_progreso = ft.Text("0/0 hrs (0%)", size=12, color="grey")
            container_progreso = ft.Column([
                ft.Text("Carga Horaria Docente:", size=12, weight="bold"),
                progreso_horas,
                texto_progreso
            ], spacing=2)

            def actualizar_progreso_docente():
                if not docente_dd.value:
                    container_progreso.visible = False
                    if container_progreso.page:
                        container_progreso.update()
                    return
                
                docente_id = int(docente_dd.value)
                docente = next((d for d in docentes if d['id'] == docente_id), None)
                if not docente: return

                horas_contrato = docente.get('horas_contratadas', 0)
                if horas_contrato == 0:
                    progreso_horas.value = 0
                    texto_progreso.value = "0/0 hrs (0%)"
                    container_progreso.visible = True
                    if container_progreso.page:
                        container_progreso.update()
                    return

                # Calculate currently assigned hours (from DB) - These are ACADEMIC hours (45 min)
                modulos_docente = self.dao.obtener_modulos_docente(docente_id)
                horas_asignadas_db_academicas = sum([m['horas_teoricas'] + m['horas_practicas'] for m in modulos_docente if m['id'] != (modulo['id'] if modulo else -1)])
                
                # Calculate hours selected in current grid - These are ACADEMIC hours (45 min)
                bloques_seleccionados = 0
                for cell in grid_cells.values(): 
                    if cell.data.get('status') == 'selected': 
                        bloques_seleccionados += 1
                
                total_horas_academicas = horas_asignadas_db_academicas + bloques_seleccionados
                
                # Convert to Chronological Hours (1 Academic Hour = 0.75 Chronological Hours)
                total_horas_cronologicas = total_horas_academicas * 0.75
                
                porcentaje = min(total_horas_cronologicas / horas_contrato, 1.0)
                
                progreso_horas.value = porcentaje
                progreso_horas.color = "red" if porcentaje >= 1.0 else "orange" if porcentaje > 0.8 else "green"
                texto_progreso.value = f"{total_horas_cronologicas:.1f}/{int(horas_contrato)} hrs cronológicas ({int(porcentaje*100)}%)"
                
                container_progreso.visible = True
                if container_progreso.page:
                    container_progreso.update()

            def on_docente_change(e):
                actualizar_grilla_docente()
                actualizar_progreso_docente()

            docente_dd.on_change = on_docente_change
            sala_dd.on_change = actualizar_grilla_docente
            semestre_field.on_change = actualizar_grilla_docente  # Actualizar grilla cuando cambia semestre

            # Initial load if editing
            if modulo:
                actualizar_grilla_docente()
                actualizar_progreso_docente()

            def guardar_modulo(e):
                logging.info("=== GUARDAR MÓDULO INICIADO ===")
                nombre = nombre_field.value
                codigo = codigo_field.value
                logging.info(f"Nombre: {nombre}, Código: {codigo}, Carrera: {carrera_dd.value}, Docente: {docente_dd.value}")
                
                if not all([nombre, codigo, carrera_dd.value, docente_dd.value]):
                    self.mostrar_mensaje("❌ Complete los campos obligatorios", 'error')
                    logging.warning("Campos obligatorios incompletos")
                    return

                # Process Grid to get Schedules
                horarios_seleccionados = [] # List of tuples (dia, start_idx, end_idx)
                
                dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
                final_schedules = []
                
                for dia in dias:
                    # Find selected indices for this day
                    selected_indices = []
                    for idx, hora in enumerate(self.bloques_horarios):
                        cell = grid_cells.get((dia, hora))
                        if cell and cell.data['status'] == 'selected':
                            selected_indices.append(idx)
                    
                    if not selected_indices:
                        continue
                        
                    # Merge contiguous blocks
                    selected_indices.sort()
                    if not selected_indices:
                        continue
                        
                    start = selected_indices[0]
                    prev = start
                    
                    for i in range(1, len(selected_indices)):
                        curr = selected_indices[i]
                        if curr > prev + 1:
                            # Break in continuity
                            # Add block: start time of 'start' to end time of 'prev'
                            h_start = self.bloques_horarios[start]
                            # Calculate end time of 'prev' block (start + 45m)
                            def add_45m(h_str):
                                parts = h_str.split(':')
                                m = int(parts[0])*60 + int(parts[1]) + 45
                                return f"{m//60:02d}:{m%60:02d}"
                            
                            h_end = add_45m(self.bloques_horarios[prev])
                            final_schedules.append({'dia': dia, 'hora_inicio': h_start, 'hora_fin': h_end})
                            
                            start = curr
                        prev = curr
                    
                    # Add last block
                    h_start = self.bloques_horarios[start]
                    def add_45m(h_str):
                        parts = h_str.split(':')
                        m = int(parts[0])*60 + int(parts[1]) + 45
                        return f"{m//60:02d}:{m%60:02d}"
                    h_end = add_45m(self.bloques_horarios[prev])
                    final_schedules.append({'dia': dia, 'hora_inicio': h_start, 'hora_fin': h_end})

                # Validate that selected blocks match exactly the module hours (Theoretical + Practical)
                try:
                    horas_teoricas = int(horas_t_field.value)
                    horas_practicas = int(horas_p_field.value)
                    total_horas_modulo = horas_teoricas + horas_practicas
                    
                    # Count total selected blocks
                    total_bloques_seleccionados = 0
                    for cell in grid_cells.values():
                        if cell.data.get('status') == 'selected':
                            total_bloques_seleccionados += 1
                    
                    logging.info(f"Validación: Bloques seleccionados={total_bloques_seleccionados}, Horas requeridas={total_horas_modulo}")
                    
                    if total_bloques_seleccionados != total_horas_modulo:
                        self.mostrar_mensaje(f"❌ Error de validación: Se han seleccionado {total_bloques_seleccionados} bloques, pero el módulo requiere exactamente {total_horas_modulo} horas (bloques).", 'error')
                        error_validacion.content.controls[1].value = f"Seleccionados: {total_bloques_seleccionados} | Requeridos: {total_horas_modulo}"
                        error_validacion.visible = True
                        error_validacion.update()
                        logging.warning(f"Validación fallida: bloques no coinciden")
                        return
                    else:
                        error_validacion.visible = False
                        error_validacion.update()

                except ValueError:
                    self.mostrar_mensaje("❌ Error: Las horas teóricas y prácticas deben ser números enteros.", 'error')
                    return

                try:
                    modulo_data = (
                        nombre, codigo,
                        int(horas_t_field.value),
                        int(horas_p_field.value),
                        int(alumnos_field.value),
                        int(carrera_dd.value),
                        int(semestre_field.value),
                        int(docente_dd.value),
                        int(sala_dd.value) if sala_dd.value else None
                    )
                    
                    modulo_id = modulo['id'] if modulo else None
                    docente_id = int(docente_dd.value) if docente_dd.value else None
                    
                    # Validar horas del docente
                    if docente_id:
                        docentes = self.dao.obtener_docentes()
                        docente_actual = next((d for d in docentes if d['id'] == docente_id), None)
                        
                        if docente_actual:
                            horas_contratadas = docente_actual['horas_contratadas']
                            horas_asignadas = self.dao.obtener_horas_asignadas_docente(docente_id)
                            
                            # Si estamos editando, restar las horas del módulo actual (ACADEMIC)
                            if modulo_id:
                                horas_actuales_modulo = modulo.get('horas_teoricas', 0) + modulo.get('horas_practicas', 0)
                                # Note: horas_asignadas from DAO might be mixed or just sum of modules. 
                                # Let's recalculate from scratch to be safe and consistent with other checks
                                modulos_docente = self.dao.obtener_modulos_docente(docente_id)
                                horas_asignadas_academicas = sum([m['horas_teoricas'] + m['horas_practicas'] for m in modulos_docente if m['id'] != modulo_id])
                            else:
                                modulos_docente = self.dao.obtener_modulos_docente(docente_id)
                                horas_asignadas_academicas = sum([m['horas_teoricas'] + m['horas_practicas'] for m in modulos_docente])
                            
                            # Calcular horas del nuevo módulo (ACADEMIC)
                            horas_nuevo_modulo_academicas = int(horas_t_field.value) + int(horas_p_field.value)
                            
                            total_academicas = horas_asignadas_academicas + horas_nuevo_modulo_academicas
                            total_cronologicas = total_academicas * 0.75
                            
                            if total_cronologicas > horas_contratadas:
                                horas_disponibles_chrono = horas_contratadas - (horas_asignadas_academicas * 0.75)
                                self.mostrar_mensaje(f"❌ Conflicto de horas: El docente solo tiene {horas_disponibles_chrono:.1f}h cronológicas disponibles.", 'error')
                                return

                    # Validar conflicto de semestre (Par vs Impar)
                    logging.info("Validando conflictos de semestre (Par vs Impar)...")
                    if carrera_dd.value and semestre_field.value and final_schedules:
                        tiene_conflicto_semestre, msg_conflicto_semestre, mod_conflicto_semestre = self.dao.validar_conflicto_semestre_par_impar(
                            int(carrera_dd.value),
                            int(semestre_field.value),
                            final_schedules,
                            modulo_id
                        )
                        
                        if tiene_conflicto_semestre:
                            self.mostrar_mensaje(f"❌ {msg_conflicto_semestre}", 'error')
                            logging.warning(f"Conflicto de semestre: {msg_conflicto_semestre}")
                            return

                    # Validar conflicto de horario del docente
                    logging.info("Validando conflictos de horario del docente...")
                    if docente_id and final_schedules:
                        tiene_conflicto, mensaje, mod_conflicto = self.dao.validar_conflicto_horario_docente(
                            docente_id, final_schedules, modulo_id
                        )
                        if tiene_conflicto:
                            self.mostrar_mensaje(f"❌ {mensaje}", 'error')
                            logging.warning(f"Conflicto de horario docente: {mensaje}")
                            return
                    
                    # Validar conflicto de sala
                    logging.info("Validando conflictos de sala...")
                    if sala_dd.value and final_schedules:
                        tiene_conflicto, mensaje, mod_conflicto = self.dao.validar_conflicto_sala(
                            int(sala_dd.value), final_schedules, modulo_id
                        )
                        if tiene_conflicto:
                            self.mostrar_mensaje(f"❌ {mensaje}", 'error')
                            logging.warning(f"Conflicto de sala: {mensaje}")
                            return

                    logging.info("Guardando módulo en base de datos...")
                    logging.info("Guardando módulo en base de datos...")
                    resultado = self.dao.guardar_modulo(modulo_data, final_schedules, modulo_id)
                    
                    if not resultado:
                        self.mostrar_mensaje("❌ Error al guardar datos en la base de datos.", 'error')
                        return

                    self.mostrar_mensaje(f"✅ Módulo '{nombre}' guardado correctamente.", 'success')
                    self.cerrar_dialogo(dialogo_modulo)
                    
                    # Update notifications
                    self.actualizar_notificaciones()

                    # Execute callback if provided, otherwise go to dashboard
                    if on_save:
                        on_save()
                    else:
                        # Navigate back to dashboard (user can then click on Modules tab)
                        import time
                        time.sleep(0.1)
                        self.mostrar_dashboard()
                    
                except Exception as ex:
                    self.mostrar_mensaje(f"❌ Error al guardar módulo: {ex}", 'error')

            # Layout: 2 Columns
            # Left Column: Form Fields
            # Update fields to expand within rows
            horas_t_field.expand = True
            horas_p_field.expand = True
            alumnos_field.expand = True
            semestre_field.expand = True

            left_column = ft.Column([
                ft.Text("Información General", weight="bold", color=self.colores['primary']),
                nombre_field,
                codigo_field,
                carrera_dd,
                ft.Row([horas_t_field, horas_p_field], spacing=10),
                ft.Row([alumnos_field, semestre_field], spacing=10),
            ], scroll=ft.ScrollMode.AUTO, expand=True, alignment=ft.MainAxisAlignment.START, spacing=15)



            # Update progress when teacher changes or grid is clicked
            # We need to hook into the grid click event. 
            # The existing 'toggle_slot' function needs to call 'actualizar_progreso_docente'
            
            # ... (Layout code) ...

            # Right Column: Schedule Grid
            right_column = ft.Column([
                ft.Text("Docente y Sala", weight="bold", color=self.colores['primary']),
                ft.Row([docente_dd, sala_dd], spacing=20),
                container_progreso, # Add progress bar here
                ft.Divider(),
                ft.Text("Horario (Seleccione los bloques)", weight="bold", color=self.colores['primary']),
                ft.Text("Verde: Disponible | Amarillo: Seleccionado | Rojo: Conflicto | Gris: No Disp.", size=12, color="grey"),
                grid_container
            ], expand=True, spacing=10)

            dialogo_modulo = ft.AlertDialog(
                title=ft.Text(titulo, weight=ft.FontWeight.BOLD),
                content=ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=left_column, 
                            expand=2, # 40% width
                            padding=ft.padding.only(right=20),
                            alignment=ft.Alignment(-1, -1)
                        ),
                        ft.VerticalDivider(width=1),
                        ft.Container(
                            content=right_column, 
                            expand=3, # 60% width
                            padding=10,
                            alignment=ft.Alignment(-1, -1)
                        )
                    ], expand=True),
                    width=1100, # Increased width for 2 columns
                    height=700
                ),
                actions=[
                    ft.Row([
                        error_validacion, 
                        ft.Row([
                            ft.TextButton("Cancelar", on_click=lambda e: (on_cancel() if on_cancel else None, self.cerrar_dialogo(dialogo_modulo))),
                            ft.ElevatedButton("💾 Guardar", bgcolor='#27AE60', color='white', on_click=guardar_modulo)
                        ])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True)
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )

            logging.info("DEBUG: Intentando abrir diálogo...")
            self.abrir_dialogo(dialogo_modulo)
            logging.info("Diálogo de módulo abierto correctamente.")
            
        except Exception as e:
            logging.error(f"Error al abrir diálogo de módulo: {e}")
            self.mostrar_mensaje(f"Error interno al abrir formulario: {e}", 'error')
    
    def _actualizar_vista_horarios(self):
        """Recarga y muestra los horarios."""
        if not hasattr(self, 'horarios_list_view') or self.horarios_list_view is None:
            return

        # Esta vista es compleja. Por ahora mostraremos una lista de módulos con sus horarios asignados.
        # Idealmente sería una grilla semanal.
        
        carreras = self.dao.obtener_carreras()
        self.horarios_list_view.controls.clear()
        
        if not carreras:
             self.horarios_list_view.controls.append(ft.Text("No hay datos para mostrar horarios.", text_align=ft.TextAlign.CENTER))
             return

        for carrera in carreras:
            modulos = self.dao.obtener_modulos_carrera(carrera['id'])
            if modulos:
                expansion_tile = ft.ExpansionTile(
                    title=ft.Text(f"📅 Horarios - {carrera['nombre']}", weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(f"{carrera['jornada']} - {len(modulos)} módulos"),
                    controls=[]
                )
                
                for modulo in modulos:
                    horarios = self.dao.obtener_horarios_modulo(modulo['id'])
                    horarios_str = "Sin horario asignado"
                    if horarios:
                        horarios_str = "\n".join([f"• {h['dia']}: {h['hora_inicio']} - {h['hora_fin']}" for h in horarios])
                    
                    tile_content = ft.Container(
                        content=ft.Column([
                            ft.Text(f"📘 {modulo['nombre']}", weight=ft.FontWeight.BOLD),
                            ft.Text(f"👨‍🏫 {modulo.get('docente_nombre', 'Sin docente')} | 🏢 {modulo.get('sala_nombre', 'Sin sala')}"),
                            ft.Text(horarios_str, size=12, color=self.colores['text_secondary']),
                            ft.Divider()
                        ]),
                        padding=ft.padding.only(left=20, right=20, bottom=10)
                    )
                    expansion_tile.controls.append(tile_content)
                
                self.horarios_list_view.controls.append(expansion_tile)
        
        self.page.update()

    def crear_tab_horarios(self):
        """Crea la tab de gestión de horarios"""
        self.horarios_list_view = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        
        self._actualizar_vista_horarios()

        return ft.Tab(
            text="⏰ Gestión de Horarios",
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Text("⏰ Vista General de Horarios", size=24, weight=ft.FontWeight.BOLD, color=self.colores['primary']),
                            ft.IconButton(icon=ft.Icons.REFRESH, on_click=lambda e: self._actualizar_vista_horarios())
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        margin=ft.margin.only(bottom=20)
                    ),
                    self.horarios_list_view,
                ], spacing=20, expand=True),
                padding=20
            )
        )
    
    def agregar_sala(self, e):
        """Agrega una nueva sala"""
        self.mostrar_dialogo_sala("Agregar Nueva Sala")
    
    def editar_sala(self, sala):
        """Edita una sala existente"""
        self.mostrar_dialogo_sala("Editar Sala", sala)
    
    def eliminar_sala(self, sala):
        """Elimina una sala"""
        def confirmar_eliminacion(e):
            if e.control.text == "Confirmar":
                try:
                    self.dao.eliminar_sala(sala['id'])
                    self.mostrar_mensaje(f"✅ Sala '{sala['nombre']}' eliminada correctamente", 'success')
                    self._actualizar_vista_salas()
                except Exception as ex:
                    self.mostrar_mensaje(f"❌ Error al eliminar sala: {ex}", 'error')
            
            dialogo_confirmacion.open = False
            self.page.update()
        
        dialogo_confirmacion = ft.AlertDialog(
            title=ft.Text("🗑️ Confirmar Eliminación", weight=ft.FontWeight.BOLD),
            content=ft.Text(f"¿Está seguro que desea eliminar la sala '{sala['nombre']}'?\n\n⚠️ Esta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dialogo_confirmacion)),
                ft.ElevatedButton("Confirmar", bgcolor='#E74C3C', color='white', on_click=confirmar_eliminacion)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.dialog = dialogo_confirmacion
        dialogo_confirmacion.open = True
        self.page.update()
    
    def abrir_dialogo(self, dialogo):
        """Abre un diálogo de manera compatible con diferentes versiones de Flet"""
        try:
            # CRITICAL: Close any existing dialogs first to prevent stacking
            if hasattr(self.page, 'overlay') and self.page.overlay:
                # Close all AlertDialog instances in overlay
                for control in list(self.page.overlay):
                    if isinstance(control, ft.AlertDialog):
                        try:
                            self.page.close(control)
                        except:
                            pass
                self.page.update()
            
            # Intento moderno (Flet 0.21+)
            self.page.open(dialogo)
            self.page.update()
        except AttributeError:
            # Fallback para versiones antiguas
            self.page.dialog = dialogo
            dialogo.open = True
            self.page.update()
        except Exception as e:
            logging.error(f"Error al abrir diálogo: {e}")
            self.mostrar_mensaje(f"Error al abrir ventana: {e}", 'error')

    def cerrar_dialogo(self, dialogo):
        """Cierra un diálogo"""
        try:
            # Intento moderno
            self.page.close(dialogo)
            self.page.update()
        except AttributeError:
            # Fallback
            dialogo.open = False
            self.page.update()
        except Exception as e:
            logging.error(f"Error al cerrar diálogo: {e}")
    
    def mostrar_mensaje(self, mensaje, tipo='info'):
        """Muestra un mensaje al usuario"""
        colores_mensaje = {
            'success': '#27AE60',
            'error': '#E74C3C',
            'warning': '#F39C12',
            'info': '#3498DB'
        }
        
        banner = ft.SnackBar(
            content=ft.Text(
                value=mensaje,
                color='white',
                size=14,
                weight=ft.FontWeight.W_500
            ),
            bgcolor=colores_mensaje.get(tipo, '#3498DB'),
            duration=4000,
            show_close_icon=True,
            close_icon_color='white'
        )
        
        self.page.snack_bar = banner
        banner.open = True
        self.page.update()

    def mostrar_dialogo_sala(self, titulo, sala=None):
        """Muestra el diálogo para agregar/editar sala"""
        def guardar_sala(e):
            nombre = nombre_field.value
            capacidad = capacidad_field.value
            tipo = tipo_field.value
            
            if not all([nombre, capacidad, tipo]):
                self.mostrar_mensaje("❌ Todos los campos son obligatorios.", 'error')
                return

            try:
                capacidad_int = int(capacidad)
            except ValueError:
                self.mostrar_mensaje("❌ La capacidad debe ser un número.", 'error')
                return

            try:
                sala_data = (nombre, capacidad_int, tipo)
                sala_id = sala['id'] if sala else None
                
                self.dao.guardar_sala(sala_data, sala_id)
                
                mensaje = f"✅ Sala '{nombre}' actualizada correctamente" if sala else f"✅ Sala '{nombre}' creada correctamente"
                self.mostrar_mensaje(mensaje, 'success')
                
                self.cerrar_dialogo(dialogo_sala)
                self._actualizar_vista_salas()

            except Exception as ex:
                self.mostrar_mensaje(f"❌ Error al guardar la sala: {ex}", 'error')

        
        nombre_field = ft.TextField(
            label="Nombre de la Sala",
            value=sala["nombre"] if sala else "",
            hint_text="Ej: Sala A-101",
            icon=ft.Icons.ROOM,
            border_radius=8
        )
        
        capacidad_field = ft.TextField(
            label="Capacidad",
            value=str(sala["capacidad"]) if sala else "",
            hint_text="Número de estudiantes",
            icon=ft.Icons.GROUP,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=8
        )
        
        tipo_field = ft.Dropdown(
            label="Tipo de Sala",
            value=sala.get("tipo") if sala else None,
            options=[
                ft.dropdown.Option("Aula", "🏫 Aula"),
                ft.dropdown.Option("Laboratorio", "🔬 Laboratorio"),
                ft.dropdown.Option("Auditorio", "🎭 Auditorio"),
                ft.dropdown.Option("Seminario", "💼 Seminario")
            ],
            icon=ft.Icons.CATEGORY,
            border_radius=8
        )
        
        dialogo_sala = ft.AlertDialog(
            title=ft.Text(titulo, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    nombre_field,
                    ft.Container(height=10),
                    capacidad_field,
                    ft.Container(height=10),
                    tipo_field
                ], spacing=10),
                width=400,
                height=300
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dialogo_sala)),
                ft.ElevatedButton(
                    "💾 Guardar", 
                    bgcolor='#27AE60', 
                    color='white', 
                    on_click=guardar_sala
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.abrir_dialogo(dialogo_sala)
    
    def mostrar_mensaje(self, mensaje, tipo='info'):
        """Muestra un mensaje al usuario"""
        colores_mensaje = {
            'success': '#27AE60',
            'error': '#E74C3C',
            'warning': '#F39C12',
            'info': '#3498DB'
        }
        
        banner = ft.SnackBar(
            content=ft.Text(
                value=mensaje,
                color='white',
                size=14,
                weight=ft.FontWeight.W_500
            ),
            bgcolor=colores_mensaje.get(tipo, '#3498DB'),
            duration=4000,
            show_close_icon=True,
            close_icon_color='white'
        )
        
        self.page.snack_bar = banner
        banner.open = True
        self.page.update()
    
    # ==================== CHAT AI METHODS ====================
    
    def crear_chat_ui(self):
        """Crea la interfaz del chat (botón flotante y panel)"""
        # Chat messages list
        self.chat_list_view = ft.ListView(
            expand=True,
            spacing=10,
            padding=10,
            auto_scroll=True
        )
        
        # Input field
        chat_input = ft.TextField(
            hint_text="Escribe tu pregunta...",
            multiline=False,
            expand=True,
            on_submit=lambda e: self.enviar_mensaje_chat(chat_input.value, chat_input)
        )
        
        # Send button
        send_button = ft.IconButton(
            icon=ft.Icons.SEND,
            icon_color="white",
            bgcolor=self.colores['primary'],
            on_click=lambda e: self.enviar_mensaje_chat(chat_input.value, chat_input)
        )
        
        # Chat panel
        self.chat_panel = ft.Container(
            content=ft.Column([
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SMART_TOY, color="white", size=24),
                        ft.Text("Asistente AI", size=18, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color="white",
                            on_click=lambda e: self.toggle_chat()
                        )
                    ]),
                    bgcolor=self.colores['primary'],
                    padding=15
                ),
                # Messages area
                ft.Container(
                    content=self.chat_list_view,
                    expand=True,
                    bgcolor="#F5F5F5"
                ),
                # Input area
                ft.Container(
                    content=ft.Row([
                        chat_input,
                        send_button
                    ], spacing=10),
                    padding=10,
                    bgcolor="white"
                )
            ], spacing=0),
            width=400,
            height=600,
            bgcolor="white",
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color="rgba(0,0,0,0.3)",
                offset=ft.Offset(-2, 0)
            ),
            right=20,
            bottom=90,
            visible=False
        )
        
        # Floating chat button
        chat_button = ft.FloatingActionButton(
            icon=ft.Icons.CHAT,
            bgcolor=self.colores['primary'],
            on_click=lambda e: self.toggle_chat(),
            tooltip="Abrir Asistente AI"
        )
        
        # Add to page overlay
        self.page.overlay.append(self.chat_panel)
        self.page.overlay.append(
            ft.Container(
                content=chat_button,
                right=20,
                bottom=20
            )
        )
        
        # Restore chat history or add welcome message
        if self.chat_messages:
            for msg in self.chat_messages:
                self.agregar_mensaje_chat(msg['mensaje'], es_bot=msg['es_bot'], restore=True)
        else:
            self.agregar_mensaje_chat("¡Hola! Soy tu asistente AI. Puedo ayudarte con consultas sobre docentes, carreras, módulos y generar reportes. ¿En qué puedo ayudarte?", es_bot=True)
    
    def toggle_chat(self):
        """Muestra/oculta el panel de chat"""
        self.chat_visible = not self.chat_visible
        self.chat_panel.visible = self.chat_visible
        self.page.update()
    
    def agregar_mensaje_chat(self, mensaje: str, es_bot: bool = False, restore: bool = False):
        """Agrega un mensaje al chat"""
        
        # Verificar si hay un archivo para abrir
        archivo_path = None
        mensaje_texto = mensaje
        
        if "[OPEN_PDF:" in mensaje:
            partes = mensaje.split("[OPEN_PDF:")
            mensaje_texto = partes[0].strip()
            if len(partes) > 1:
                path_part = partes[1]
                if "]" in path_part:
                    archivo_path = path_part.split("]")[0].strip()
        
        # Contenido del mensaje
        contenido_mensaje = [
            ft.Text(
                "🤖 Asistente" if es_bot else "👤 Tú",
                size=12,
                weight=ft.FontWeight.BOLD,
                color='white' if es_bot else self.colores['secondary']
            )
        ]

        if es_bot:
            # Handler for navigation links
            def handle_chat_link(e):
                if not e.data:
                    return
                
                link = e.data
                
                try:
                    # Handle docente links
                    if link.startswith('docente://'):
                        docente_id = int(link.replace('docente://',''))
                        # Get teacher data
                        docentes = self.dao.obtener_docentes()
                        docente = next((d for d in docentes if d['id'] == docente_id), None)
                        if docente:
                            # Navigate to teacher detail view
                            self.mostrar_detalle_docente(docente)
                            # Close chat panel
                            if self.chat_panel:
                                self.chat_panel.visible = False
                                self.page.update()
                        else:
                            self.mostrar_mensaje(f"Docente no encontrado", "error")
                    
                    # Handle carrera links  
                    elif link.startswith('carrera://'):
                        carrera_id = int(link.replace('carrera://',''))
                        # Navigate to assignment view for that career
                        carreras = self.dao.obtener_carreras()
                        carrera = next((c for c in carreras if c['id'] == carrera_id), None)
                        if carrera:
                            self.mostrar_vista_asignacion(carrera)
                            # Close chat panel
                            if self.chat_panel:
                                self.chat_panel.visible = False
                                self.page.update()
                        else:
                            self.mostrar_mensaje(f"Carrera no encontrada", "error")
                    
                    # Handle regular HTTP links
                    elif link.startswith('http'):
                        self.page.launch_url(link)
                        
                except ValueError as ve:
                    # Handle invalid link formats
                    logging.error(f"Error parsing link {link}: {ve}")
                    self.mostrar_mensaje(f"Error en el enlace: formato inválido", "error")
                except Exception as ex:
                    logging.error(f"Error handling link {link}: {ex}")
                    self.mostrar_mensaje(f"Error al navegar: {str(ex)}", "error")
            
            # Use Markdown to properly render formatting (bold, lists, etc.)
            contenido_mensaje.append(
                ft.Markdown(
                    mensaje_texto,
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    on_tap_link=handle_chat_link
                )
            )
        else:
            contenido_mensaje.append(
                ft.Text(
                    mensaje_texto,
                    size=14,
                    color="black"
                )
            )
        
        # Si hay archivo, agregar botón para abrir
        if archivo_path and es_bot:
            def abrir_archivo(e, path=archivo_path):
                try:
                    os.startfile(path)
                except Exception as ex:
                    self.mostrar_mensaje(f"Error al abrir archivo: {ex}", "error")
            
            contenido_mensaje.append(
                ft.ElevatedButton(
                    "📂 Abrir PDF",
                    icon=ft.Icons.PICTURE_AS_PDF,
                    bgcolor="white",
                    color=self.colores['primary'],
                    on_click=abrir_archivo
                )
            )

        # Create message bubble
        mensaje_container = ft.Container(
            content=ft.Column(contenido_mensaje, spacing=5),
            bgcolor=None if es_bot else "#E3F2FD",  # No background for bot, light blue for user
            border=ft.border.all(2, self.colores['primary']) if es_bot else None,  # Blue border for bot
            padding=12,
            border_radius=10,
            margin=ft.margin.only(left=10 if es_bot else 50, right=50 if es_bot else 10)
        )
        
        self.chat_list_view.controls.append(mensaje_container)
        
        if not restore:
            self.chat_messages.append({"mensaje": mensaje, "es_bot": es_bot})
        self.page.update()
        
        if self.chat_panel and self.chat_panel.visible:
            self.page.update()
    
    def enviar_mensaje_chat(self, mensaje: str, input_field: ft.TextField):
        """Envía un mensaje al chatbot y muestra la respuesta"""
        if not mensaje or not mensaje.strip():
            return
        
        # Clear input
        input_field.value = ""
        self.page.update()
        
        # Add user message
        self.agregar_mensaje_chat(mensaje, es_bot=False)
        
        # Show typing indicator
        typing_indicator = ft.Container(
            content=ft.Row([
                ft.ProgressRing(width=16, height=16, stroke_width=2),
                ft.Text("Escribiendo...", size=12, italic=True, color="grey")
            ], spacing=10),
            padding=10,
            margin=ft.margin.only(left=10)
        )
        self.chat_list_view.controls.append(typing_indicator)
        self.page.update()
        
        # Get bot response
        try:
            respuesta = self.chatbot.procesar_mensaje(mensaje)
        except Exception as e:
            logging.error(f"Error en chatbot: {e}")
            respuesta = f"❌ Lo siento, ocurrió un error: {str(e)}"
        
        # Remove typing indicator
        self.chat_list_view.controls.remove(typing_indicator)
        
        # Add bot response
        self.agregar_mensaje_chat(respuesta, es_bot=True)

def main(page: ft.Page):
    """Función principal"""
    app = SistemaGestionFlet(page)
    app.crear_chat_ui()  # Initialize chat UI
    app.mostrar_login()

# Ejecutar la aplicación
# Ejecutar la aplicación
if __name__ == "__main__":
    # Configuración para despliegue web - NECESARIO host="0.0.0.0" para Render
    port = int(os.getenv("PORT", 8080))
    print(f"Iniciando servidor Flet en puerto {port}...")
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, assets_dir="assets", host="0.0.0.0")
