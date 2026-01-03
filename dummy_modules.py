
# Este archivo actúa como placeholder para módulos eliminados
class DataExporter:
    def __init__(self, *args, **kwargs): pass
    def exportar_todo_excel(self): return "Función desactivada"
    def exportar_todo_csv(self): return {}

class DataImporter:
    def __init__(self, *args, **kwargs): 
        self.errores = []
    def importar_desde_excel(self, *args, **kwargs): return {}
    def importar_docentes_csv(self, *args, **kwargs): return 0
    def importar_salas_csv(self, *args, **kwargs): return 0
    def importar_carreras_csv(self, *args, **kwargs): return 0
    def importar_modulos_csv(self, *args, **kwargs): return 0
    def importar_horarios_modulos_csv(self, *args, **kwargs): return 0
