"""
Gestión de Datos - Importación y Exportación
Interfaz de usuario para importar y exportar datos masivos
"""


import flet as ft
import logging
from pathlib import Path
 # from data_export import DataExporter # REPLACED: Module removed
 # from data_import import DataImporter # REPLACED: Module removed
from database import SistemaDAO

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GestionDatos:
    def __init__(self, page: ft.Page, dao: SistemaDAO):
        """
        Inicializa la vista de gestión de datos
        
        Args:
            page: Página de Flet
            dao: Instancia de SistemaDAO
        """
        self.page = page
        self.dao = dao
        # self.exporter = DataExporter(dao) # REPLACED: Feature disabled
        # self.importer = DataImporter(dao) # REPLACED: Feature disabled
        
        # Componentes UI
        self.progress_bar = None
        self.status_text = None
        self.resultado_text = None
    
    def crear_vista(self) -> ft.Container:
        """Crea la vista de gestión de datos"""
        
        # Título
        titulo = ft.Text(
            "Gestión de Datos",
            size=28,
            weight=ft.FontWeight.BOLD,
            color="#1a237e"
        )
        
        # MENSAJE DE MANTENIMIENTO
        mensaje_mant = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.BUILD_CIRCLE_OUTLINED, color="orange", size=48),
                ft.Text("Módulo en Mantenimiento", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Las funciones de importación/exportación masiva están deshabilitadas en esta versión web.", text_align=ft.TextAlign.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.colors.ORANGE_50,
            padding=30,
            border_radius=10,
            alignment=ft.alignment.center
        )

        return ft.Container(
            content=ft.Column([
                titulo,
                ft.Divider(),
                mensaje_mant
            ]),
            padding=30,
            expand=True
        )

    # Métodos legacy eliminados para limpieza
    def exportar_excel(self, e): pass
    def exportar_csv(self, e): pass
    def importar_excel(self, e): pass
    def importar_csv_folder(self, e): pass
    def descargar_plantilla(self, e): pass

def main(page: ft.Page):
    """Función principal para prueba standalone"""
    page.title = "Gestión de Datos"
    # page.window_width = 900
    # page.window_height = 800
    
    dao = SistemaDAO()
    gestion = GestionDatos(page, dao)
    
    page.add(gestion.crear_vista())


if __name__ == "__main__":
    ft.app(target=main)

