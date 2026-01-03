"""
Script de Importación de Datos desde Excel
Importa datos de propuestas docentes desde archivos Excel a la base de datos
"""

import pandas as pd
import os
import re
from database import SistemaDAO
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataImporter:
    def __init__(self):
        self.dao = SistemaDAO()
        self.dao.inicializar_base_de_datos()
        
    def limpiar_base_datos(self):
        """Elimina todos los registros de las tablas principales"""
        logging.info("Limpiando base de datos...")
        
        try:
            # Orden importante: primero las tablas dependientes
            self.dao.db.execute_query("DELETE FROM modulo_horarios", fetch=False)
            self.dao.db.execute_query("DELETE FROM disponibilidad_docente", fetch=False)
            self.dao.db.execute_query("DELETE FROM modulos", fetch=False)
            self.dao.db.execute_query("DELETE FROM carrera_salas", fetch=False)
            self.dao.db.execute_query("DELETE FROM carrera_semestres", fetch=False)
            self.dao.db.execute_query("DELETE FROM docentes", fetch=False)
            self.dao.db.execute_query("DELETE FROM carreras", fetch=False)
            self.dao.db.execute_query("DELETE FROM salas", fetch=False)
            
            logging.info("✅ Base de datos limpiada exitosamente")
        except Exception as e:
            logging.error(f"❌ Error al limpiar base de datos: {e}")
            raise
    
    def extraer_nombre_carrera(self, filename):
        """Extrae el nombre de la carrera del nombre del archivo"""
        # Mapeo de códigos a nombres completos
        carreras_map = {
            'AP': 'Administración Pública',
            'CC': 'Contador Contador',
            'CP': 'Contador Público',
            'EI': 'Educación de Párvulos',
            'EP': 'Educación Parvularia',
            'ET': 'Educación de Párvulos',
            'IR': 'Ingeniería en Recursos Naturales',
            'ME_MP': 'Medicina Veterinaria / Medicina Preventiva',
        }
        
        # Extraer código del nombre del archivo
        for codigo, nombre in carreras_map.items():
            if filename.startswith(codigo):
                return nombre
        
        # Si no encuentra mapeo, usar el código
        match = re.match(r'^([A-Z_]+)', filename)
        if match:
            return match.group(1).replace('_', ' ')
        
        return filename.split('_')[0]
    
    def importar_archivo(self, filepath):
        """Importa datos de un archivo Excel"""
        filename = os.path.basename(filepath)
        logging.info(f"📄 Procesando: {filename}")
        
        try:
            # Leer Excel (puede tener múltiples hojas)
            excel_file = pd.ExcelFile(filepath)
            
            # Extraer nombre de carrera
            nombre_carrera = self.extraer_nombre_carrera(filename)
            
            # Determinar jornada del nombre del archivo
            jornada = "Diurna" if "DIURNO" in filename.upper() else "Vespertina"
            
            # Crear carrera
            carrera_data = (nombre_carrera, jornada, 0)  # alumnos_proyectados se actualizará
            carrera_id = self.dao.guardar_carrera(carrera_data, [], [], None)
            logging.info(f"  ✅ Carrera creada: {nombre_carrera} (ID: {carrera_id})")
            
            # Procesar cada hoja del Excel
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(filepath, sheet_name=sheet_name)
                self.procesar_hoja(df, carrera_id, nombre_carrera)
            
        except Exception as e:
            logging.error(f"  ❌ Error procesando {filename}: {e}")
            import traceback
            traceback.print_exc()
    
    def procesar_hoja(self, df, carrera_id, nombre_carrera):
        """Procesa una hoja del Excel e importa los datos"""
        
        # Diccionario para almacenar docentes únicos
        docentes_cache = {}
        
        # Buscar la fila de encabezados (puede no estar en la primera fila)
        header_row = None
        for idx, row in df.iterrows():
            if 'Código' in str(row.values) or 'Codigo' in str(row.values):
                header_row = idx
                break
        
        if header_row is None:
            logging.warning("  ⚠️ No se encontró fila de encabezados")
            return
        
        # Usar la fila encontrada como encabezados
        df.columns = df.iloc[header_row]
        df = df.iloc[header_row + 1:]  # Datos después del encabezado
        
        # Limpiar nombres de columnas
        df.columns = df.columns.str.strip()
        
        # Procesar cada fila (módulo)
        for idx, row in df.iterrows():
            try:
                # Saltar filas vacías
                if pd.isna(row.get('Código')) or pd.isna(row.get('Módulo')):
                    continue
                
                # Extraer datos del módulo
                codigo = str(row.get('Código', '')).strip()
                nombre_modulo = str(row.get('Módulo', '')).strip()
                semestre = self.extraer_semestre(row.get('Semestre', 'I'))
                
                # Helper to parse hours (handles cases like "6+6")
                def safe_parse_hours(value):
                    if pd.isna(value):
                        return 0
                    value_str = str(value).strip()
                    if '+' in value_str:
                        # Handle expressions like "6+6"
                        try:
                            return int(eval(value_str))
                        except:
                            return 0
                    try:
                        return int(float(value_str))
                    except:
                        return 0
                
                # Horas
                horas_teoricas = safe_parse_hours(row.get('Hrs Teóricas') or row.get('Hrs Teoricas'))
                horas_practicas = safe_parse_hours(row.get('Hrs Prácticas') or row.get('Hrs Practicas'))
                alumnos = safe_parse_hours(row.get('Alumnos Proyectados'))
                
                # Docente
                nombre_docente = str(row.get('Docente', '')).strip()
                titulo_docente = str(row.get('Título', '') or row.get('Titulo', '') or '').strip()
                evaluacion = float(row.get('Puntaje Promedio de Evaluación Ex. Docente', 0) or 
                                 row.get('Puntaje Promedio de Evaluación', 0) or 0)
                
                # Crear o recuperar docente
                if nombre_docente and nombre_docente != 'nan' and nombre_docente.strip():
                    if nombre_docente not in docentes_cache:
                        # Orden correcto: nombre, titulo, contrato, horas_contratadas, email, evaluacion
                        docente_data = (
                            nombre_docente,
                            titulo_docente if titulo_docente and titulo_docente != 'nan' else '',
                            "Honorarios",  # Tipo de contrato por defecto
                            40,  # Horas contratadas por defecto
                            f"{nombre_docente.lower().replace(' ', '.')}@ceduc.cl",
                            evaluacion if evaluacion > 0 else 4.0
                        )
                        docente_id = self.dao.guardar_docente(docente_data)
                        docentes_cache[nombre_docente] = docente_id
                        logging.info(f"    👤 Docente creado: {nombre_docente}")
                    else:
                        docente_id = docentes_cache[nombre_docente]
                else:
                    docente_id = None
                
                # Crear módulo
                modulo_data = (
                    nombre_modulo,
                    codigo,
                    horas_teoricas,
                    horas_practicas,
                    alumnos,
                    carrera_id,
                    semestre,
                    docente_id,
                    None  # sala_id (no especificada en Excel)
                )
                
                modulo_id = self.dao.guardar_modulo(modulo_data, [], None)
                logging.info(f"    📚 Módulo creado: {codigo} - {nombre_modulo}")
                
            except Exception as e:
                logging.error(f"    ❌ Error procesando fila {idx}: {e}")
                continue
    
    def extraer_semestre(self, semestre_str):
        """Extrae el número de semestre de una cadena"""
        if pd.isna(semestre_str):
            return 1
        
        semestre_str = str(semestre_str).upper().strip()
        
        # Mapeo de números romanos
        romanos = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8}
        
        if semestre_str in romanos:
            return romanos[semestre_str]
        
        # Intentar extraer número
        match = re.search(r'(\d+)', semestre_str)
        if match:
            return int(match.group(1))
        
        return 1
    
    def importar_todos(self, directorio='datosNuevos'):
        """Importa todos los archivos Excel del directorio"""
        logging.info("🚀 Iniciando importación de datos...")
        
        # Limpiar base de datos
        self.limpiar_base_datos()
        
        # Obtener todos los archivos Excel
        archivos = [f for f in os.listdir(directorio) if f.endswith('.xlsx')]
        
        logging.info(f"📁 Encontrados {len(archivos)} archivos Excel")
        
        for archivo in archivos:
            filepath = os.path.join(directorio, archivo)
            self.importar_archivo(filepath)
        
        logging.info("✅ Importación completada!")

if __name__ == "__main__":
    importer = DataImporter()
    importer.importar_todos()
