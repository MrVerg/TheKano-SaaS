#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para poblar la base de datos con bloques de 45 minutos = 1 hora académica
Con nombres reales de asignaturas por carrera
"""
import logging
from database import SistemaDAO

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def limpiar_y_poblar(dao):
    logging.info("Limpiando base de datos...")
    
    tablas = ['disponibilidad_docentes', 'modulo_horarios', 'carrera_salas', 'carrera_semestres', 
              'modulos', 'docentes', 'salas', 'carreras']
    
    for tabla in tablas:
        dao.db.execute_query(f"DELETE FROM {tabla}")
    
    logging.info("✓ Base de datos limpiada")
    
    # 1. SALAS
    salas_data = [(f"Sala {100 + i}", 30 + (i % 3) * 10, "Aula Teórica" if i % 3 == 0 else "Laboratorio" if i % 2 == 0 else "Taller") for i in range(1, 21)]
    for sala in salas_data:
        dao.db.execute_query("INSERT INTO salas (nombre, capacidad, tipo) VALUES (%s, %s, %s)", sala)
    
    salas = dao.db.execute_query("SELECT id, nombre FROM salas ORDER BY id", fetch=True)
    sala_map = {s['nombre']: s['id'] for s in salas}
    logging.info(f"✓ {len(salas)} salas creadas")
    
    # 2. CARRERAS
    carreras_data = [
        ("Administración de Empresas, mención Gestión Pública", "Diurna", 120),
        ("Computación e Informática, mención Ciberseguridad", "Vespertina", 100),
        ("Educación de Párvulos", "Diurna", 80),
        ("Electricidad y Electrónica Industrial", "Vespertina", 90),
        ("Enfermería y Telemedicina", "Diurna", 110),
        ("Prevención de Riesgos", "Vespertina", 70),
        ("Maquinaria Pesada", "Diurna", 60),
        ("Mecánica de Equipo Pesado", "Vespertina", 65),
    ]
    
    for carrera in carreras_data:
        dao.db.execute_query("INSERT INTO carreras (nombre, jornada, alumnos_proyectados) VALUES (%s, %s, %s)", carrera)
    
    carreras = dao.db.execute_query("SELECT id, nombre, jornada FROM carreras ORDER BY id", fetch=True)
    carrera_map = {c['nombre']: {'id': c['id'], 'jornada': c['jornada']} for c in carreras}
    logging.info(f"✓ {len(carreras)} carreras creadas")
    
    # 3. SEMESTRES
    for carrera_id in [c['id'] for c in carrera_map.values()]:
        for semestre in range(1, 5):
            dao.db.execute_query("INSERT INTO carrera_semestres (carrera_id, semestre) VALUES (%s, %s)", (carrera_id, semestre))
    logging.info("✓ Semestres asignados")
    
    # 4. SALAS A CARRERAS
    for carrera_id in [c['id'] for c in carrera_map.values()]:
        for sala_id in sala_map.values():
            dao.db.execute_query("INSERT INTO carrera_salas (carrera_id, sala_id) VALUES (%s, %s)", (carrera_id, sala_id))
    logging.info("✓ Salas asignadas a carreras")
    
    # 5. DOCENTES
    nombres = ["María", "Juan", "Ana", "Carlos", "Laura", "Pedro", "Sofía", "Diego", "Carmen", "Roberto",
               "Elena", "Luis", "Paula", "Miguel", "Javier", "Patricia", "Fernando", "Claudia", "Ricardo", "Valentina",
               "Andrés", "Gabriela", "Rodrigo", "Camila", "Sebastián", "Daniela", "Matías", "Francisca", "Felipe", "Javiera"]
    apellidos = ["González", "Pérez", "Martínez", "López", "Rodríguez", "Sánchez", "Ramírez", "Fernández", 
                 "Vásquez", "Herrera", "Flores", "Torres", "Morales", "Díaz", "Ruiz", "Silva", "Castro", "Muñoz",
                 "Rojas", "Vargas", "Contreras", "Espinoza", "Sepúlveda", "Gutiérrez", "Reyes", "Núñez", "Pizarro", "Campos"]
    
    docentes_data = []
    for i in range(60):
        nombre = f"{nombres[i % len(nombres)]} {apellidos[i % len(apellidos)]}" if i < len(nombres) else f"{nombres[i % len(nombres)]} {apellidos[(i + 5) % len(apellidos)]}"
        titulo = f"{'Ingeniero/a' if i % 5 == 0 else 'Licenciado/a' if i % 5 == 1 else 'Técnico/a' if i % 5 == 2 else 'Magíster' if i % 5 == 3 else 'Doctor/a'}"
        contrato = "Planta" if i < 30 else "Honorarios"
        email = f"{nombres[i % len(nombres)].lower()}.{apellidos[i % len(apellidos)].lower()}{i}@ceduc.cl"
        docentes_data.append((nombre, titulo, contrato, 44, email, round(4.0 + (i % 10) * 0.1, 2)))
    
    for docente in docentes_data:
        dao.db.execute_query("INSERT INTO docentes (nombre, titulo, contrato, horas_contratadas, email, evaluacion) VALUES (%s, %s, %s, %s, %s, %s)", docente)
    
    docentes = dao.db.execute_query("SELECT id FROM docentes ORDER BY id", fetch=True)
    docente_ids = [d['id'] for d in docentes]
    logging.info(f"✓ {len(docentes)} docentes creados")
    
    # 6. DISPONIBILIDAD
    dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
    bloques = ["08:30", "09:15", "10:15", "11:00", "12:00", "12:45", "14:30", "15:15", "16:15", "17:00", "18:00", "18:45", "19:45", "20:30"]
    
    for docente_id in docente_ids:
        for dia in dias:
            for bloque in bloques:
                dao.db.execute_query("INSERT INTO disponibilidad_docentes (docente_id, dia, hora, estado) VALUES (%s, %s, %s, %s)", 
                                    (docente_id, dia, bloque, "disponible"))
    logging.info("✓ Disponibilidad configurada")
    
    # 7. MÓDULOS - Nombres reales de asignaturas por carrera
    modulos_por_carrera = {
        "Administración de Empresas, mención Gestión Pública": [
            "Fundamentos de Administración", "Contabilidad General", "Matemáticas Aplicadas", "Economía",
            "Gestión de Recursos Humanos", "Marketing", "Finanzas", "Derecho Empresarial",
            "Estadística", "Gestión Pública"
        ],
        "Computación e Informática, mención Ciberseguridad": [
            "Programación I", "Programación II", "Estructuras de Datos", "Algoritmos",
            "Bases de Datos", "Redes de Computadores", "Sistemas Operativos", "Ciberseguridad Básica",
            "Criptografía", "Seguridad en Redes"
        ],
        "Educación de Párvulos": [
            "Desarrollo Infantil", "Didáctica del Juego", "Psicología del Aprendizaje", "Neurociencia",
            "Lenguaje y Comunicación", "Matemáticas Iniciales", "Ciencias Naturales", "Artes Plásticas",
            "Música y Movimiento", "Literatura Infantil"
        ],
        "Electricidad y Electrónica Industrial": [
            "Circuitos Eléctricos", "Electrónica Digital", "Electrónica Analógica", "Máquinas Eléctricas",
            "Sistemas de Control", "Automatización Industrial", "PLC", "Instrumentación",
            "Instalaciones Eléctricas", "Sistemas de Potencia"
        ],
        "Enfermería y Telemedicina": [
            "Anatomía y Fisiología", "Enfermería Básica", "Farmacología", "Microbiología",
            "Enfermería Médica", "Enfermería Quirúrgica", "Enfermería Pediátrica", "Salud Mental",
            "Salud Pública", "Telemedicina"
        ],
        "Prevención de Riesgos": [
            "Legislación Laboral", "Higiene Industrial", "Seguridad Industrial", "Ergonomía",
            "Toxicología", "Gestión de Riesgos", "Prevención de Incendios", "Primeros Auxilios",
            "Sistemas de Gestión", "ISO 45001"
        ],
        "Maquinaria Pesada": [
            "Operación de Maquinaria", "Mantenimiento Preventivo", "Mecánica Básica", "Hidráulica",
            "Neumática", "Sistemas Eléctricos", "Motores Diesel", "Excavadoras",
            "Seguridad en Operación", "Topografía"
        ],
        "Mecánica de Equipo Pesado": [
            "Mecánica Automotriz", "Sistemas Hidráulicos", "Sistemas Neumáticos", "Motores Diesel",
            "Sistemas de Inyección", "Transmisiones Automáticas", "Electrónica Automotriz", "Soldadura Industrial",
            "Mantenimiento Predictivo", "Gestión de Repuestos"
        ]
    }
    
    # Bloques de 45 minutos (1 hora académica cada uno)
    bloques_diurna = []
    for dia in dias:
        bloques_diurna.extend([
            (dia, "08:30", "09:15"), (dia, "09:15", "10:00"),
            (dia, "10:15", "11:00"), (dia, "11:00", "11:45"),
            (dia, "12:00", "12:45"), (dia, "12:45", "13:30")
        ])
    
    bloques_vespertina = []
    for dia in dias:
        bloques_vespertina.extend([
            (dia, "18:00", "18:45"), (dia, "18:45", "19:30"),
            (dia, "19:45", "20:30"), (dia, "20:30", "21:15")
        ])
    
    horarios_ocupados = {d_id: [] for d_id in docente_ids}
    horarios_ocupados_sala = {s_id: [] for s_id in list(sala_map.values())}
    horas_asignadas = {d_id: 0 for d_id in docente_ids}
    
    modulo_count = 0
    docente_idx = 0
    sala_idx = 0
    salas_ids = list(sala_map.values())
    
    for carrera_nombre, carrera_info in carrera_map.items():
        carrera_id = carrera_info['id']
        jornada = carrera_info['jornada']
        bloques = bloques_diurna if jornada == "Diurna" else bloques_vespertina
        nombres_modulos = modulos_por_carrera[carrera_nombre]
        
        for i in range(10):  # 10 módulos por carrera
            nombre = nombres_modulos[i]
            codigo = f"{carrera_nombre[:3].upper()}{i+1:03d}"
            h_teoricas = 2 + (i % 3)
            h_practicas = 2 + ((i + 1) % 3)
            total_horas = h_teoricas + h_practicas
            
            # Buscar par (Docente, Sala) con bloques disponibles
            docente_asignado = None
            sala_asignada = None
            horarios_modulo = []
            
            # Intentar con varios docentes
            start_docente_idx = docente_idx
            found_assignment = False
            
            for _ in range(len(docente_ids)):
                docente_candidato = docente_ids[docente_idx % len(docente_ids)]
                
                # Verificar capacidad docente
                if horas_asignadas[docente_candidato] + (total_horas * 0.75) > 44:
                    docente_idx += 1
                    continue
                
                # Para este docente, buscar una sala compatible
                start_sala_idx = sala_idx
                for _ in range(len(salas_ids)):
                    sala_candidata = salas_ids[sala_idx % len(salas_ids)]
                    
                    # Buscar bloques libres comunes (Docente + Sala)
                    bloques_comunes = []
                    for bloque in bloques:
                        if (bloque not in horarios_ocupados[docente_candidato] and 
                            bloque not in horarios_ocupados_sala[sala_candidata]):
                            bloques_comunes.append(bloque)
                            if len(bloques_comunes) >= total_horas:
                                break
                    
                    if len(bloques_comunes) >= total_horas:
                        # ENCONTRADO!
                        docente_asignado = docente_candidato
                        sala_asignada = sala_candidata
                        horarios_modulo = bloques_comunes[:total_horas]
                        found_assignment = True
                        sala_idx += 1 # Rotar sala para la próxima
                        break
                    
                    sala_idx += 1 # Probar siguiente sala
                
                if found_assignment:
                    docente_idx += 1 # Rotar docente para la próxima
                    break
                    
                docente_idx += 1 # Probar siguiente docente

            if not found_assignment:
                logging.warning(f"⚠️ No se pudo asignar horario para {nombre} ({total_horas} hrs)")
                continue

            # Insertar módulo
            dao.db.execute_query("""
                INSERT INTO modulos (nombre, codigo, horas_teoricas, horas_practicas, alumnos_proyectados, semestre, carrera_id, docente_id, sala_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nombre, codigo, h_teoricas, h_practicas, 80, 1, carrera_id, docente_asignado, sala_asignada))
            
            result = dao.db.execute_query("SELECT LAST_INSERT_ID()", fetch=True)
            modulo_id = result[0]['LAST_INSERT_ID()']
            
            # Registrar horarios ocupados y guardar en DB
            for dia, inicio, fin in horarios_modulo:
                horarios_ocupados[docente_asignado].append((dia, inicio, fin))
                horarios_ocupados_sala[sala_asignada].append((dia, inicio, fin))
                dao.db.execute_query("""
                    INSERT INTO modulo_horarios (modulo_id, dia, hora_inicio, hora_fin)
                    VALUES (%s, %s, %s, %s)
                """, (modulo_id, dia, inicio, fin))
            
            horas_asignadas[docente_asignado] += (total_horas * 0.75)
            modulo_count += 1
    
    logging.info(f"✓ {modulo_count} módulos creados con nombres reales")
    max_carga = max(horas_asignadas.values()) if horas_asignadas else 0
    logging.info(f"✓ Carga máxima: {max_carga:.1f}h de 44h")
    logging.info("✅ Base de datos poblada exitosamente")

if __name__ == "__main__":
    dao = SistemaDAO()
    dao.inicializar_base_de_datos()
    limpiar_y_poblar(dao)
    
    print("\n" + "="*60)
    print("✅ PROCESO COMPLETADO")
    print("="*60)
    print("\nEstadísticas:")
    print(f"  • Carreras: 8")
    print(f"  • Docentes: 60")
    print(f"  • Salas: 20")
    print(f"  • Módulos: 80 (10 por carrera)")
    print(f"  • Nombres reales de asignaturas")
    print(f"  • Bloques de 45 minutos = 1 hora académica")
    print(f"  • Validación de conflictos de sala y docente: ACTIVA")
    print("\nCredenciales:")
    print("  Email: admin@ceduc.cl")
    print("  Password: 123456")
    print("="*60)
