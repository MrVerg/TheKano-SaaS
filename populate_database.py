import random
import logging
from database import SistemaDAO

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def populate_database():
    dao = SistemaDAO()
    
    print("🚀 Iniciando población de base de datos con datos de prueba...")
    
    # --- 1. Datos Base ---
    
    nombres_docentes = [
        "Juan Pérez", "María González", "Carlos López", "Ana Martínez", "Pedro Sánchez",
        "Laura Rodríguez", "Diego Fernández", "Sofía Ramírez", "Luis Torres", "Elena Flores",
        "Miguel Díaz", "Carmen Vásquez", "Javier Ruiz", "Paula Morales", "Roberto Herrera"
    ]
    
    carreras_data = [
        ("TNS en Enfermería", "Diurna", 40),
        ("TNS en Minas", "Vespertina", 35),
        ("TNS en Electricidad", "Vespertina", 30),
        ("TNS en Mecánica", "Diurna", 30),
        ("TNS en Administración", "Vespertina", 45),
        ("TNS en Párvulos", "Diurna", 35),
        ("TNS en Construcción", "Vespertina", 25),
        ("TNS en Computación", "Diurna", 30)
    ]
    
    salas_data = [
        ("Sala 101", 30, "Aula"), ("Sala 102", 30, "Aula"), ("Sala 103", 40, "Aula"),
        ("Lab Computación 1", 25, "Laboratorio"), ("Lab Computación 2", 25, "Laboratorio"),
        ("Taller Mecánico", 20, "Taller"), ("Lab Enfermería", 20, "Laboratorio"),
        ("Sala 201", 35, "Aula"), ("Sala 202", 35, "Aula"), ("Auditorio", 100, "Auditorio")
    ]
    
    nombres_modulos_base = [
        "Introducción a la Especialidad", "Matemáticas I", "Comunicación Efectiva",
        "Inglés Técnico", "Prevención de Riesgos", "Taller de Especialidad I",
        "Gestión de Proyectos", "Ética Profesional", "Software Aplicado", "Práctica Intermedia"
    ]
    
    # Bloques horarios (Lunes a Viernes, 8:30 a 18:30 aprox)
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    bloques = [
        ("08:30", "10:00"), ("10:15", "11:45"), ("12:00", "13:30"),
        ("14:30", "16:00"), ("16:15", "17:45"), ("18:00", "19:30"), ("19:45", "21:15")
    ]
    
    # --- 2. Inserción de Entidades Base ---
    
    # Docentes
    docente_ids = []
    logging.info("Insertando docentes...")
    for nombre in nombres_docentes:
        email = f"{nombre.lower().replace(' ', '.')}@ceduc.cl"
        # (nombre, titulo, contrato, horas_contratadas, email, evaluacion)
        d_id = dao.guardar_docente((nombre, "Profesional", "Plazo Fijo", 44, email, round(random.uniform(4.0, 5.0), 1)))
        if d_id:
            docente_ids.append(d_id)
            
    # Salas
    sala_ids = []
    logging.info("Insertando salas...")
    for s_data in salas_data:
        s_id = dao.guardar_sala(s_data)
        if s_id:
            sala_ids.append(s_id)
            
    # Carreras
    carrera_ids = []
    logging.info("Insertando carreras...")
    for c_data in carreras_data:
        # (nombre, jornada, alumnos)
        c_id = dao.guardar_carrera(c_data, [1, 2, 3, 4], sala_ids[:2]) # Semestres y salas dummy
        if c_id:
            carrera_ids.append(c_id)

    # --- 3. Generación de Módulos y Horarios (Sin Conflictos) ---
    
    # Estructuras para trackear ocupación:
    # docente_ocupado[docente_id][dia][bloque_index] = True
    # sala_ocupada[sala_id][dia][bloque_index] = True
    
    docente_ocupado = {d_id: {dia: [False]*len(bloques) for dia in dias} for d_id in docente_ids}
    sala_ocupada = {s_id: {dia: [False]*len(bloques) for dia in dias} for s_id in sala_ids}
    
    logging.info("Generando módulos y asignando horarios...")
    
    count_modulos = 0
    
    for c_id in carrera_ids:
        # 10 módulos por carrera
        for i, nombre_base in enumerate(nombres_modulos_base):
            nombre_modulo = f"{nombre_base}"
            codigo = f"MOD-{c_id}-{i+1:02d}"
            semestre = (i % 4) + 1
            
            # Asignar docente y sala aleatorios
            docente_id = random.choice(docente_ids)
            sala_id = random.choice(sala_ids)
            
            # Determinar carga horaria (ej: 2 bloques a la semana)
            bloques_necesarios = 2 
            horarios_asignados = []
            
            # Intentar encontrar bloques disponibles
            intentos = 0
            while len(horarios_asignados) < bloques_necesarios and intentos < 50:
                dia = random.choice(dias)
                bloque_idx = random.randint(0, len(bloques)-1)
                
                # Verificar disponibilidad
                if not docente_ocupado[docente_id][dia][bloque_idx] and \
                   not sala_ocupada[sala_id][dia][bloque_idx]:
                    
                    # Asignar
                    hora_inicio, hora_fin = bloques[bloque_idx]
                    horarios_asignados.append({
                        'dia': dia,
                        'hora_inicio': hora_inicio,
                        'hora_fin': hora_fin
                    })
                    
                    # Marcar ocupado
                    docente_ocupado[docente_id][dia][bloque_idx] = True
                    sala_ocupada[sala_id][dia][bloque_idx] = True
                
                intentos += 1
            
            if len(horarios_asignados) < bloques_necesarios:
                logging.warning(f"No se pudieron asignar todos los horarios para {nombre_modulo}. Se asignaron {len(horarios_asignados)}/{bloques_necesarios}")
            
            # Guardar módulo
            # (nombre, codigo, horas_teoricas, horas_practicas, alumnos, carrera_id, semestre, docente_id, sala_id)
            modulo_data = (
                nombre_modulo,
                codigo,
                len(horarios_asignados) * 2, # Aprox horas pedagógicas
                0,
                30,
                c_id,
                semestre,
                docente_id,
                sala_id
            )
            
            dao.guardar_modulo(modulo_data, horarios_asignados)
            count_modulos += 1

    print(f"✅ Proceso finalizado.")
    print(f"📊 Resumen:")
    print(f"   - Docentes: {len(docente_ids)}")
    print(f"   - Carreras: {len(carrera_ids)}")
    print(f"   - Salas: {len(sala_ids)}")
    print(f"   - Módulos creados: {count_modulos}")

if __name__ == "__main__":
    populate_database()
