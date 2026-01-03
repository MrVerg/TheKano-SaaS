"""
Módulo de Chatbot con IA usando Google Gemini
Permite consultas a la base de datos y generación de reportes
"""

import google.generativeai as genai
import json
import logging
from typing import Optional, Dict, List
import os
from dotenv import load_dotenv

import unicodedata
import difflib

# Cargar variables de entorno
load_dotenv()

class AIChatbot:
    def __init__(self, dao, report_generator):
        """
        Inicializa el chatbot con acceso a DAO y generador de reportes
        
        Args:
            dao: Instancia de SistemaDAO para consultas a BD
            report_generator: Instancia de ReportGenerator para PDFs
        """
        self.dao = dao
        self.report_generator = report_generator
        
        # Configurar Gemini API
        # Intentar cargar desde .env primero, luego usar fallback embebido
        api_key = os.getenv('GEMINI_API_KEY')
        
        # Si no hay API key en .env, usar la embebida como fallback
        if not api_key:
            logging.info("GEMINI_API_KEY no encontrada en .env, usando API key embebida")
            api_key = "AIzaSyCDJ5BH2Z4MtkbLloJ65isBGDkXAZkEf8s"  # API key embebida para ejecutable
        
        if not api_key:
            logging.warning("No se pudo obtener GEMINI_API_KEY. El chatbot no funcionará.")
            self.model = None
            return
        
        genai.configure(api_key=api_key)
        
        # Configurar el modelo - usar Gemini 2.5 Flash Lite
        try:
            # Definir instrucciones del sistema para ANÁLISIS CONTEXTUAL
            system_instruction = """Eres el asistente inteligente del sistema de gestión académica CEDUC.

Tu misión es ayudar a los usuarios respondiendo preguntas sobre docentes, carreras, módulos y salas.

IMPORTANTE:
- Recibirás el contexto completo de la base de datos en cada consulta
- Analiza los datos y responde de forma clara y concisa
- Usa formato markdown para mejor legibilidad (listas, negritas, etc.)
- **INCLUYE LINKS NAVEGABLES** cuando menciones docentes o carreras
- Si la pregunta requiere generar un reporte PDF, indica claramente que el usuario puede generarlo desde la interfaz
- Sé conversacional y amigable
- Si no encuentras información relevante, dilo claramente

FORMATO DE LINKS NAVEGABLES:
Cuando menciones entidades, usa estos formatos de link:
- Docentes: [Nombre del Docente](docente://ID) - SIEMPRE usa el ID numérico del docente
- Carreras: [Nombre de la Carrera](carrera://ID) - SIEMPRE usa el ID numérico de la carrera
- Módulos: NO uses links, solo menciona el nombre en negritas

FORMATO DE RESPUESTA:
- Usa listas con viñetas (•) para enumerar items
- Usa negritas (**texto**) para destacar información importante
- **SIEMPRE incluye links clicables** para docentes y carreras mencionados
- Para módulos, usa solo negritas sin links
- Mantén las respuestas concisas pero completas
- Incluye números y estadísticas cuando sean relevantes

EJEMPLOS DE BUENAS RESPUESTAS CON LINKS:
Usuario: "¿Qué docentes imparten en Enfermería?"
Respuesta: "📚 **Docentes de [Enfermería y Telemedicina](carrera://5):**

• [Elena Muñoz](docente://15) - **Anatomía y Fisiología**
• [Luis Rojas](docente://23) - **Enfermería Básica**
• [Paula Vargas](docente://31) - **Farmacología**

Total: 3 docentes. Haz clic en cualquier nombre para ver más detalles."

Usuario: "¿Cuántas salas hay disponibles?"
Respuesta: "🏢 Hay **15 salas** registradas en el sistema, con capacidades que van desde 20 hasta 50 personas."

Usuario: "Información sobre Juan Pérez"
Respuesta: "👨‍🏫 **[Juan Pérez](docente://42)**

• **Título:** Ingeniero Civil
• **Carga:** 14h/44h (31.8%)
• **Evaluación:** 4.5/5.0

**Módulos asignados:**
• **Resistencia de Materiales** - [Ingeniería Civil](carrera://3)
• **Estructuras** - [Ingeniería Civil](carrera://3)

Haz clic en los links para navegar a cada sección."
"""

            # Usar el nombre sin el prefijo "models/" y pasar system_instruction
            self.model = genai.GenerativeModel('gemini-2.5-flash-lite', system_instruction=system_instruction)
            logging.info("Modelo Gemini 2.5 Flash Lite inicializado correctamente con modo ANÁLISIS CONTEXTUAL")
        except Exception as e:
            logging.error(f"No se pudo inicializar el modelo de Gemini: {e}")
            self.model = None
            return
        
        # Configuración de generación
        self.generation_config = {
            "temperature": 0.7,  # Más creativo para respuestas naturales
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        
        # Iniciar chat
        self.chat = self.model.start_chat(history=[])
        
        # Definir funciones disponibles
        self.functions = {
            'buscar_docentes': self.buscar_docentes,
            'buscar_carreras': self.buscar_carreras,
            'buscar_modulos': self.buscar_modulos,
            'obtener_info_docente': self.obtener_info_docente,
            'obtener_estadisticas': self.obtener_estadisticas,
            'obtener_ranking_docentes': self.obtener_ranking_docentes,
            'generar_reporte_docente': self.generar_reporte_docente,
            'generar_reporte_carrera': self.generar_reporte_carrera,
        }
        
        logging.info("Chatbot AI inicializado correctamente")
    
    def normalize_text(self, text: str) -> str:
        """Normaliza el texto eliminando tildes y convirtiendo a minúsculas"""
        if not text:
            return ""
        return ''.join(c for c in unicodedata.normalize('NFD', text)
                      if unicodedata.category(c) != 'Mn').lower()

    def fuzzy_search(self, query: str, items: List[Dict], key_field: str, threshold: float = 0.6) -> List[Dict]:
        """
        Realiza una búsqueda difusa en una lista de diccionarios.
        
        Args:
            query: Texto a buscar
            items: Lista de items (diccionarios)
            key_field: Campo del diccionario donde buscar (ej: 'nombre')
            threshold: Umbral de similitud (0.0 a 1.0)
            
        Returns:
            Lista de items que coinciden
        """
        if not query:
            return items
            
        query_norm = self.normalize_text(query)
        matches = []
        
        for item in items:
            item_value = item.get(key_field, "")
            item_norm = self.normalize_text(item_value)
            
            # 1. Coincidencia exacta o contenida (normalizada)
            if query_norm in item_norm:
                matches.append((1.0, item))
                continue
                
            # 2. Coincidencia difusa (Levenshtein ratio)
            ratio = difflib.SequenceMatcher(None, query_norm, item_norm).ratio()
            if ratio >= threshold:
                matches.append((ratio, item))
        
        # Ordenar por mejor coincidencia
        matches.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in matches]

    def buscar_docentes(self, nombre: str = "") -> str:
        """Busca docentes por nombre usando búsqueda difusa"""
        try:
            docentes = self.dao.obtener_docentes()
            
            if nombre:
                docentes = self.fuzzy_search(nombre, docentes, 'nombre')
            
            if not docentes:
                return f"No se encontraron docentes similares a '{nombre}'"
            
            resultado = f"Encontré {len(docentes)} docente(s) para '{nombre}':\n\n"
            for d in docentes[:10]:  # Limitar a 10 resultados
                horas_asignadas = self.dao.obtener_horas_asignadas_docente(d['id'])
                horas_contratadas = d.get('horas_contratadas', 0)
                porcentaje = (horas_asignadas / horas_contratadas * 100) if horas_contratadas > 0 else 0
                
                # Usar link markdown
                resultado += f"• [{d['nombre']}](docente://{d['id']})\n"
                resultado += f"  - Título: {d.get('titulo', 'N/A')}\n"
                resultado += f"  - Carga: {horas_asignadas}h/{horas_contratadas}h ({porcentaje:.1f}%)\n"
                resultado += f"  - ID: {d['id']}\n\n"
            
            return resultado
        except Exception as e:
            logging.error(f"Error buscando docentes: {e}")
            return f"Error al buscar docentes: {str(e)}"
    
    def buscar_carreras(self, nombre: str = "") -> str:
        """Busca carreras por nombre usando búsqueda difusa"""
        try:
            carreras = self.dao.obtener_carreras()
            
            if nombre:
                carreras = self.fuzzy_search(nombre, carreras, 'nombre')
            
            if not carreras:
                return f"No se encontraron carreras similares a '{nombre}'"
            
            resultado = f"Encontré {len(carreras)} carrera(s):\n\n"
            for c in carreras:
                modulos = self.dao.obtener_modulos_carrera(c['id'])
                resultado += f"• {c['nombre']}\n"
                resultado += f"  - Jornada: {c.get('jornada', 'N/A')}\n"
                resultado += f"  - Alumnos proyectados: {c.get('alumnos_proyectados', 0)}\n"
                resultado += f"  - Módulos: {len(modulos)}\n"
                resultado += f"  - ID: {c['id']}\n\n"
            
            return resultado
        except Exception as e:
            logging.error(f"Error buscando carreras: {e}")
            return f"Error al buscar carreras: {str(e)}"
    
    def buscar_modulos(self, nombre: str = "", carrera_id: int = None) -> str:
        """Busca módulos por nombre y/o carrera usando búsqueda difusa"""
        try:
            if carrera_id:
                modulos = self.dao.obtener_modulos_carrera(carrera_id)
            else:
                # Obtener todos los módulos de todas las carreras
                carreras = self.dao.obtener_carreras()
                modulos = []
                for c in carreras:
                    modulos.extend(self.dao.obtener_modulos_carrera(c['id']))
            
            if nombre:
                modulos = self.fuzzy_search(nombre, modulos, 'nombre')
            
            if not modulos:
                return "No se encontraron módulos con esos criterios"
            
            resultado = f"Encontré {len(modulos)} módulo(s):\n\n"
            for m in modulos[:15]:  # Limitar a 15 resultados
                resultado += f"• {m['nombre']} ({m.get('codigo', 'N/A')})\n"
                resultado += f"  - Carrera: {m.get('carrera_nombre', 'N/A')}\n"
                resultado += f"  - Horas: {m.get('horas_teoricas', 0)}T + {m.get('horas_practicas', 0)}P\n"
                resultado += f"  - Docente: {m.get('docente_nombre', 'Sin asignar')}\n\n"
            
            return resultado
        except Exception as e:
            logging.error(f"Error buscando módulos: {e}")
            return f"Error al buscar módulos: {str(e)}"
    
    def buscar_salas(self, nombre: str = "") -> str:
        """Busca salas por nombre usando búsqueda difusa"""
        try:
            salas = self.dao.obtener_salas()
            
            if nombre:
                salas = self.fuzzy_search(nombre, salas, 'nombre')
            
            if not salas:
                return f"No se encontraron salas similares a '{nombre}'"
            
            resultado = f"Encontré {len(salas)} sala(s):\n\n"
            for s in salas[:20]:  # Limitar a 20 resultados
                resultado += f"• {s['nombre']}\n"
                resultado += f"  - Capacidad: {s.get('capacidad', 'N/A')} personas\n"
                resultado += f"  - Tipo: {s.get('tipo', 'N/A')}\n"
                resultado += f"  - ID: {s['id']}\n\n"
            
            return resultado
        except Exception as e:
            logging.error(f"Error buscando salas: {e}")
            return f"Error al buscar salas: {str(e)}"
    
    def obtener_docentes_carrera(self, nombre_carrera: str) -> str:
        """Obtiene los docentes que imparten en una carrera específica"""
        try:
            # Buscar la carrera
            carreras = self.dao.obtener_carreras()
            carreras_match = self.fuzzy_search(nombre_carrera, carreras, 'nombre')
            
            if not carreras_match:
                return f"No se encontró la carrera '{nombre_carrera}'"
            
            carrera = carreras_match[0]
            
            # Obtener módulos de la carrera
            modulos = self.dao.obtener_modulos_carrera(carrera['id'])
            
            if not modulos:
                return f"La carrera '{carrera['nombre']}' no tiene módulos asignados"
            
            # Obtener docentes únicos
            docentes_ids = set()
            docentes_info = {}
            
            for m in modulos:
                docente_id = m.get('docente_id')
                if docente_id:
                    docentes_ids.add(docente_id)
                    if docente_id not in docentes_info:
                        docentes_info[docente_id] = {
                            'nombre': m.get('docente_nombre', 'N/A'),
                            'modulos': []
                        }
                    docentes_info[docente_id]['modulos'].append(m['nombre'])
            
            if not docentes_info:
                return f"La carrera '{carrera['nombre']}' no tiene docentes asignados aún"
            
            resultado = f"📚 Docentes que imparten en {carrera['nombre']}\n\n"
            resultado += f"Total: {len(docentes_info)} docente(s)\n\n"
            
            for docente_id, info in docentes_info.items():
                resultado += f"• {info['nombre']}\n"
                resultado += f"  Módulos ({len(info['modulos'])}):\n"
                for modulo in info['modulos']:
                    resultado += f"    - {modulo}\n"
                resultado += "\n"
            
            return resultado
        except Exception as e:
            logging.error(f"Error obteniendo docentes de carrera: {e}")
            return f"Error al obtener docentes: {str(e)}"
    
    def obtener_modulos_carrera_detallado(self, nombre_carrera: str) -> str:
        """Obtiene los módulos de una carrera con información detallada"""
        try:
            # Buscar la carrera
            carreras = self.dao.obtener_carreras()
            carreras_match = self.fuzzy_search(nombre_carrera, carreras, 'nombre')
            
            if not carreras_match:
                return f"No se encontró la carrera '{nombre_carrera}'"
            
            carrera = carreras_match[0]
            
            # Obtener módulos de la carrera
            modulos = self.dao.obtener_modulos_carrera(carrera['id'])
            
            if not modulos:
                return f"La carrera '{carrera['nombre']}' no tiene módulos registrados"
            
            resultado = f"📖 Módulos de {carrera['nombre']}\n\n"
            resultado += f"Total: {len(modulos)} módulo(s)\n\n"
            
            # Agrupar por semestre
            modulos_por_semestre = {}
            for m in modulos:
                sem = m.get('semestre', 0)
                if sem not in modulos_por_semestre:
                    modulos_por_semestre[sem] = []
                modulos_por_semestre[sem].append(m)
            
            for semestre in sorted(modulos_por_semestre.keys()):
                resultado += f"Semestre {semestre}:\n"
                for m in modulos_por_semestre[semestre]:
                    resultado += f"• {m['nombre']} ({m.get('codigo', 'N/A')})\n"
                    resultado += f"  - Horas: {m.get('horas_teoricas', 0)}T + {m.get('horas_practicas', 0)}P\n"
                    resultado += f"  - Docente: {m.get('docente_nombre', 'Sin asignar')}\n"
                    resultado += f"  - Sala: {m.get('sala_nombre', 'Sin asignar')}\n\n"
            
            return resultado
        except Exception as e:
            logging.error(f"Error obteniendo módulos de carrera: {e}")
            return f"Error al obtener módulos: {str(e)}"
    
    def obtener_info_docente(self, docente_id: int) -> str:
        """Obtiene información detallada de un docente"""
        try:
            docentes = self.dao.obtener_docentes()
            docente = next((d for d in docentes if d['id'] == docente_id), None)
            
            if not docente:
                return f"No se encontró el docente con ID {docente_id}"
            
            modulos = self.dao.obtener_modulos_docente(docente_id)
            horas_asignadas = self.dao.obtener_horas_asignadas_docente(docente_id)
            horas_contratadas = docente.get('horas_contratadas', 0)
            porcentaje = (horas_asignadas / horas_contratadas * 100) if horas_contratadas > 0 else 0
            
            resultado = f"📋 Información de [{docente['nombre']}](docente://{docente['id']})\n\n"
            resultado += f"Título: {docente.get('titulo', 'N/A')}\n"
            resultado += f"Email: {docente.get('email', 'N/A')}\n"
            resultado += f"Contrato: {docente.get('contrato', 'N/A')}\n"
            resultado += f"Evaluación: {docente.get('evaluacion', 0)}/5.0\n\n"
            resultado += f"📊 Carga Horaria:\n"
            resultado += f"- Horas asignadas: {horas_asignadas}h\n"
            resultado += f"- Horas contratadas: {horas_contratadas}h\n"
            resultado += f"- Utilización: {porcentaje:.1f}%\n\n"
            resultado += f"📚 Módulos asignados ({len(modulos)}):\n"
            for m in modulos:
                resultado += f"• {m['nombre']} - {m.get('carrera_nombre', 'N/A')}\n"
            
            return resultado
        except Exception as e:
            logging.error(f"Error obteniendo info de docente: {e}")
            return f"Error al obtener información: {str(e)}"
    
    def obtener_estadisticas(self) -> str:
        """Obtiene estadísticas generales del sistema"""
        try:
            docentes = self.dao.obtener_docentes()
            carreras = self.dao.obtener_carreras()
            
            total_modulos = 0
            for c in carreras:
                total_modulos += len(self.dao.obtener_modulos_carrera(c['id']))
            
            # Calcular docentes por carga
            docentes_sobrecargados = 0
            docentes_disponibles = 0
            
            for d in docentes:
                horas_asignadas = self.dao.obtener_horas_asignadas_docente(d['id'])
                horas_contratadas = d.get('horas_contratadas', 0)
                porcentaje = (horas_asignadas / horas_contratadas * 100) if horas_contratadas > 0 else 0
                
                if porcentaje >= 90:
                    docentes_sobrecargados += 1
                elif porcentaje < 50:
                    docentes_disponibles += 1
            
            resultado = "📊 Estadísticas del Sistema\n\n"
            resultado += f"👥 Docentes: {len(docentes)}\n"
            resultado += f"   - Con alta carga (≥90%): {docentes_sobrecargados}\n"
            resultado += f"   - Con disponibilidad (<50%): {docentes_disponibles}\n\n"
            resultado += f"🎓 Carreras: {len(carreras)}\n"
            resultado += f"📚 Módulos totales: {total_modulos}\n"
            
            return resultado
        except Exception as e:
            logging.error(f"Error obteniendo estadísticas: {e}")
            return f"Error al obtener estadísticas: {str(e)}"

    def obtener_ranking_docentes(self, criterio: str = "CARGA") -> str:
        """Obtiene un ranking de docentes por carga horaria o evaluación"""
        try:
            docentes = self.dao.obtener_docentes()
            ranking = []
            
            for d in docentes:
                horas_asignadas = self.dao.obtener_horas_asignadas_docente(d['id'])
                horas_contratadas = d.get('horas_contratadas', 0)
                porcentaje = (horas_asignadas / horas_contratadas * 100) if horas_contratadas > 0 else 0
                evaluacion = d.get('evaluacion', 0.0)
                
                ranking.append({
                    'id': d['id'],
                    'nombre': d['nombre'],
                    'asignadas': horas_asignadas,
                    'contratadas': horas_contratadas,
                    'porcentaje': porcentaje,
                    'evaluacion': evaluacion
                })
            
            if criterio == "EVALUACION":
                # Ordenar por evaluación descendente
                ranking.sort(key=lambda x: x['evaluacion'], reverse=True)
                titulo = "🏆 Ranking de Evaluación Docente (Top 10)"
                
                resultado = f"{titulo}\n\n"
                for i, r in enumerate(ranking[:10], 1):
                    estrellas = "⭐" * int(round(r['evaluacion']))
                    resultado += f"{i}. [{r['nombre']}](docente://{r['id']}): {r['evaluacion']:.1f}/5.0 {estrellas}\n"
            
            else: # Default: CARGA
                # Ordenar por porcentaje descendente
                ranking.sort(key=lambda x: x['porcentaje'], reverse=True)
                titulo = "🏆 Ranking de Carga Docente (Top 10)"
                
                resultado = f"{titulo}\n\n"
                for i, r in enumerate(ranking[:10], 1):
                    icono = "🔴" if r['porcentaje'] >= 90 else "🟢" if r['porcentaje'] < 50 else "🟡"
                    resultado += f"{i}. {icono} [{r['nombre']}](docente://{r['id']}): {r['porcentaje']:.1f}% ({r['asignadas']}h/{r['contratadas']}h)\n"
            
            return resultado
        except Exception as e:
            logging.error(f"Error obteniendo ranking: {e}")
            return f"Error al obtener ranking: {str(e)}"
    
    def generar_reporte_docente(self, docente_id: int) -> str:
        """Genera un reporte PDF de un docente"""
        try:
            docentes = self.dao.obtener_docentes()
            docente = next((d for d in docentes if d['id'] == docente_id), None)
            
            if not docente:
                return f"No se encontró el docente con ID {docente_id}"
            
            # Obtener módulos con horarios
            modulos = self.dao.obtener_modulos_docente(docente_id)
            for m in modulos:
                m['horarios'] = self.dao.obtener_horarios_modulo(m['id'])
            
            # Generar reporte
            filepath = self.report_generator.generar_reporte_docente(docente, modulos)
            
            return f"✅ Reporte generado exitosamente para {docente['nombre']}\n📄 Archivo: {filepath}\n[OPEN_PDF:{filepath}]"
        except Exception as e:
            logging.error(f"Error generando reporte de docente: {e}")
            return f"❌ Error al generar reporte: {str(e)}"
    
    def generar_reporte_carrera(self, carrera_id: int) -> str:
        """Genera un reporte PDF de una carrera"""
        try:
            carreras = self.dao.obtener_carreras()
            carrera = next((c for c in carreras if c['id'] == carrera_id), None)
            
            if not carrera:
                return f"No se encontró la carrera con ID {carrera_id}"
            
            # Obtener módulos con información de docentes y salas
            modulos = self.dao.obtener_modulos_carrera(carrera_id)
            
            # Enriquecer datos
            docentes_list = self.dao.obtener_docentes()
            salas_list = self.dao.obtener_salas()
            
            for m in modulos:
                if m.get('docente_id'):
                    docente = next((d for d in docentes_list if d['id'] == m['docente_id']), None)
                    m['docente_nombre'] = docente['nombre'] if docente else 'Sin asignar'
                else:
                    m['docente_nombre'] = 'Sin asignar'
                
                if m.get('sala_id'):
                    sala = next((s for s in salas_list if s['id'] == m['sala_id']), None)
                    m['sala_nombre'] = sala['nombre'] if sala else 'Sin asignar'
                else:
                    m['sala_nombre'] = 'Sin asignar'
            
            # Generar reporte
            filepath = self.report_generator.generar_reporte_carrera(carrera, modulos)
            
            return f"✅ Reporte generado exitosamente para {carrera['nombre']}\n📄 Archivo: {filepath}\n[OPEN_PDF:{filepath}]"
        except Exception as e:
            logging.error(f"Error generando reporte de carrera: {e}")
            return f"❌ Error al generar reporte: {str(e)}"
    
    
    def obtener_contexto_completo(self) -> str:
        """Obtiene todo el contexto de la base de datos en formato legible"""
        try:
            contexto = "=== CONTEXTO DE LA BASE DE DATOS ===\n\n"
            
            # Docentes
            docentes = self.dao.obtener_docentes()
            contexto += f"## DOCENTES ({len(docentes)} total):\n"
            for d in docentes:
                horas_asignadas = self.dao.obtener_horas_asignadas_docente(d['id'])
                modulos = self.dao.obtener_modulos_docente(d['id'])
                contexto += f"\n• {d['nombre']} (ID: {d['id']})\n"
                contexto += f"  - Título: {d.get('titulo', 'N/A')}\n"
                contexto += f"  - Email: {d.get('email', 'N/A')}\n"
                contexto += f"  - Contrato: {d.get('contrato', 'N/A')}\n"
                contexto += f"  - Horas: {horas_asignadas}h asignadas / {d.get('horas_contratadas', 0)}h contratadas\n"
                contexto += f"  - Evaluación: {d.get('evaluacion', 0)}/5.0\n"
                if modulos:
                    contexto += f"  - Módulos: {', '.join([m['nombre'] for m in modulos])}\n"
            
            # Carreras
            carreras = self.dao.obtener_carreras()
            contexto += f"\n## CARRERAS ({len(carreras)} total):\n"
            for c in carreras:
                modulos = self.dao.obtener_modulos_carrera(c['id'])
                contexto += f"\n• {c['nombre']} (ID: {c['id']})\n"
                contexto += f"  - Jornada: {c.get('jornada', 'N/A')}\n"
                contexto += f"  - Alumnos proyectados: {c.get('alumnos_proyectados', 0)}\n"
                contexto += f"  - Módulos: {len(modulos)}\n"
            
            # Módulos (resumido por carrera)
            contexto += f"\n## MÓDULOS POR CARRERA:\n"
            for c in carreras:
                modulos = self.dao.obtener_modulos_carrera(c['id'])
                if modulos:
                    contexto += f"\n### {c['nombre']}:\n"
                    for m in modulos:
                        contexto += f"  • {m['nombre']} ({m.get('codigo', 'N/A')})\n"
                        contexto += f"    - Semestre: {m.get('semestre', 'N/A')}\n"
                        contexto += f"    - Horas: {m.get('horas_teoricas', 0)}T + {m.get('horas_practicas', 0)}P\n"
                        contexto += f"    - Docente: {m.get('docente_nombre', 'Sin asignar')}\n"
                        contexto += f"    - Sala: {m.get('sala_nombre', 'Sin asignar')}\n"
            
            # Salas
            salas = self.dao.obtener_salas()
            contexto += f"\n## SALAS ({len(salas)} total):\n"
            for s in salas:
                contexto += f"• {s['nombre']} - Capacidad: {s.get('capacidad', 'N/A')} - Tipo: {s.get('tipo', 'N/A')}\n"
            
            return contexto
        except Exception as e:
            logging.error(f"Error obteniendo contexto: {e}")
            return "Error al cargar el contexto de la base de datos"
    
    def procesar_mensaje(self, mensaje_usuario: str) -> str:
        """
        Procesa un mensaje del usuario usando Gemini API con ANÁLISIS CONTEXTUAL
        """
        if not self.model:
            return "⚠️ El chatbot no está configurado. Por favor, verifica tu GEMINI_API_KEY en el archivo .env"
        
        try:
            # Detectar si el usuario pide un reporte PDF
            mensaje_lower = mensaje_usuario.lower()
            
            # Keywords para detectar solicitudes de reportes
            keywords_reporte = ['reporte', 'pdf', 'generar', 'genera', 'crear', 'informe', 'documento']
            keywords_docente = ['docente', 'profesor', 'maestro', 'teacher']
            keywords_carrera = ['carrera', 'programa', 'especialidad']
            
            # Verificar si es una solicitud de reporte
            es_solicitud_reporte = any(kw in mensaje_lower for kw in keywords_reporte)
            
            if es_solicitud_reporte:
                # Intentar identificar si es para docente o carrera
                es_docente = any(kw in mensaje_lower for kw in keywords_docente)
                es_carrera = any(kw in mensaje_lower for kw in keywords_carrera)
                
                if es_docente:
                    # Extraer nombre del docente usando fuzzy search
                    # Eliminar palabras clave para obtener el nombre
                    nombre_busqueda = mensaje_usuario
                    for kw in keywords_reporte + keywords_docente + ['de', 'del', 'para', 'sobre']:
                        nombre_busqueda = nombre_busqueda.lower().replace(kw, '')
                    nombre_busqueda = nombre_busqueda.strip()
                    
                    if nombre_busqueda:
                        # Buscar docente
                        docentes = self.dao.obtener_docentes()
                        matches = self.fuzzy_search(nombre_busqueda, docentes, 'nombre', threshold=0.4)
                        
                        if matches:
                            docente = matches[0]
                            # Generar reporte
                            return self.generar_reporte_docente(docente['id'])
                        else:
                            return f"❌ No se encontró ningún docente similar a '{nombre_busqueda}'. Por favor, verifica el nombre."
                    
                elif es_carrera:
                    # Extraer nombre de la carrera usando fuzzy search
                    nombre_busqueda = mensaje_usuario
                    for kw in keywords_reporte + keywords_carrera + ['de', 'del', 'para', 'sobre', 'la']:
                        nombre_busqueda = nombre_busqueda.lower().replace(kw, '')
                    nombre_busqueda = nombre_busqueda.strip()
                    
                    if nombre_busqueda:
                        # Buscar carrera
                        carreras = self.dao.obtener_carreras()
                        matches = self.fuzzy_search(nombre_busqueda, carreras, 'nombre', threshold=0.4)
                        
                        if matches:
                            carrera = matches[0]
                            # Generar reporte
                            return self.generar_reporte_carrera(carrera['id'])
                        else:
                            return f"❌ No se encontró ninguna carrera similar a '{nombre_busqueda}'. Por favor, verifica el nombre."
            
            # Si no es solicitud de reporte, proceder con análisis normal
            contexto = self.obtener_contexto_completo()
            
            # Construir el mensaje completo con contexto
            mensaje_completo = f"{contexto}\n\n=== PREGUNTA DEL USUARIO ===\n{mensaje_usuario}\n\nResponde de forma clara y concisa basándote en los datos anteriores."
            
            # Enviar a Gemini para análisis
            response = self.chat.send_message(mensaje_completo, generation_config=self.generation_config)
            respuesta_texto = response.text.strip()
            
            logging.info(f"Respuesta Gemini (contextual): {respuesta_texto[:100]}...")
            
            return respuesta_texto
            
        except Exception as e:
            logging.error(f"Error con Gemini API: {e}")
            return f"❌ Error: {str(e)}"
