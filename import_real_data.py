"""
Script para importar los datos específicos de IMPORT.py a la base de datos
"""
from database import SistemaDAO
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Importar datos desde IMPORT.py
from IMPORT import docentes_data, carreras_data, modulos_data, salas_data, horarios_data

def main():
    print("🚀 Importando datos desde IMPORT.py...")
    
    dao = SistemaDAO()
    
    # 1. Importar Salas
    print(f"\n📍 Importando {len(salas_data)} salas...")
    sala_map = {}  # Mapeo de ID original a ID en BD
    for sala in salas_data:
        try:
            # (nombre, capacidad, tipo)
            sala_tuple = (sala['nombre'], sala['capacidad'], sala['tipo'])
            new_id = dao.guardar_sala(sala_tuple)
            if new_id:
                sala_map[sala['id']] = new_id
        except Exception as e:
            print(f"  ⚠️  Error guardando sala {sala.get('nombre')}: {e}")
    print(f"✅ {len(sala_map)} salas importadas")
    
    # 2. Importar Docentes
    print(f"\n👨‍🏫 Importando {len(docentes_data)} docentes...")
    docente_map = {}
    for docente in docentes_data:
        try:
            # Generar email único basado en el nombre si es pendiente@ceduc.cl
            email = docente.get('email', 'pendiente@ceduc.cl')
            if email == 'pendiente@ceduc.cl':
                # Generar email único del nombre
                nombre_parts = docente['nombre'].lower().split()
                if len(nombre_parts) >= 2:
                    email = f"{nombre_parts[0]}.{nombre_parts[-1]}@ceduc.cl"
                else:
                    email = f"{nombre_parts[0]}.{docente['id']}@ceduc.cl"
            
            # (nombre, titulo, contrato, horas_contratadas, email, evaluacion)
            horas = docente.get('horas_contratadas', 0)
            if horas == 0:
                horas = 44
            
            docente_tuple = (
                docente['nombre'],
                docente.get('titulo', ''),
                docente.get('contrato', 'Honorario'),
                horas,
                email,
                docente.get('evaluacion', 0)
            )
            new_id = dao.guardar_docente(docente_tuple)
            if new_id:
                docente_map[docente['id']] = new_id
        except Exception as e:
            print(f"  ⚠️  Error guardando docente {docente.get('nombre')}: {e}")
    print(f"✅ {len(docente_map)} docentes importados")
    
    # 3. Importar Carreras
    print(f"\n🎓 Importando {len(carreras_data)} carreras...")
    carrera_map = {}
    for carrera in carreras_data:
        try:
            # Convertir semestres
            if isinstance(carrera.get('semestres'), int):
                semestres = list(range(1, carrera['semestres'] + 1))
            else:
                semestres = [1, 2, 3, 4]  # Default
            
            # Convertir salas_ids usando el mapeo
            salas_ids_originales = []
            if isinstance(carrera.get('salas_ids'), str):
                salas_ids_originales = [int(s.strip()) for s in carrera['salas_ids'].split(',') if s.strip()]
            
            salas_ids_nuevos = [sala_map.get(sid, sala_map[list(sala_map.keys())[0]]) for sid in salas_ids_originales if sid in sala_map]
            if not salas_ids_nuevos and sala_map:
                salas_ids_nuevos = [list(sala_map.values())[0]]
            
            # (nombre, jornada, alumnos_proyectados)
            carrera_tuple = (
                carrera['nombre'],
                carrera.get('jornada', 'Diurna'),
                carrera.get('alumnos_proyectados', 30)
            )
            
            new_id = dao.guardar_carrera(carrera_tuple, semestres, salas_ids_nuevos)
            if new_id:
                carrera_map[carrera['id']] = new_id
        except Exception as e:
            print(f"  ⚠️  Error guardando carrera {carrera.get('nombre')}: {e}")
    print(f"✅ {len(carrera_map)} carreras importadas")
    
    # 4. Agrupar horarios por módulo
    print(f"\n📚 Preparando {len(modulos_data)} módulos con horarios...")
    horarios_por_modulo = {}
    for horario in horarios_data:
        modulo_id = horario['modulo_id']
        if modulo_id not in horarios_por_modulo:
            horarios_por_modulo[modulo_id] = []
        horarios_por_modulo[modulo_id].append({
            'dia': horario['dia'],
            'hora_inicio': horario['hora_inicio'],
            'hora_fin': horario['hora_fin']
        })
    
    # 5. Importar Módulos con sus horarios
    modulo_map = {}
    modulos_importados = 0
    
    # Eliminar duplicados basados en ID
    modulos_unicos = {}
    for modulo in modulos_data:
        if modulo['id'] not in modulos_unicos:
            modulos_unicos[modulo['id']] = modulo
    
    print(f"   (Eliminados {len(modulos_data) - len(modulos_unicos)} módulos duplicados)")
    
    for modulo in modulos_unicos.values():
        try:
            # Mapear IDs
            carrera_id_nuevo = carrera_map.get(modulo['carrera_id'])
            docente_id_nuevo = docente_map.get(modulo.get('docente_id'))
            sala_id_nuevo = sala_map.get(modulo.get('sala_id'))
            
            if not carrera_id_nuevo:
                print(f"  ⚠️  Saltando módulo {modulo['nombre']}: carrera no encontrada")
                continue
            
            # Obtener horarios para este módulo
            horarios = horarios_por_modulo.get(modulo['id'], [])
            
            # (nombre, codigo, horas_teoricas, horas_practicas, alumnos, carrera_id, semestre, docente_id, sala_id)
            modulo_tuple = (
                modulo['nombre'],
                modulo.get('codigo', f"MOD-{modulo['id']}"),
                modulo.get('horas_teoricas', 0),
                modulo.get('horas_practicas', 0),
                modulo.get('alumnos_proyectados', 30),
                carrera_id_nuevo,
                modulo.get('semestre', 1),
                docente_id_nuevo,
                sala_id_nuevo
            )
            
            new_id = dao.guardar_modulo(modulo_tuple, horarios)
            if new_id:
                modulo_map[modulo['id']] = new_id
                modulos_importados += 1
        except Exception as e:
            print(f"  ⚠️  Error guardando módulo {modulo.get('nombre')}: {e}")
    
    print(f"✅ {modulos_importados} módulos importados con horarios")
    
    # Resumen final
    print("\n" + "="*60)
    print("✅ IMPORTACIÓN COMPLETADA")
    print("="*60)
    print(f"Salas: {len(dao.obtener_salas())}")
    print(f"Docentes: {len(dao.obtener_docentes())}")
    print(f"Carreras: {len(dao.obtener_carreras())}")
    print(f"Módulos: {len(dao.obtener_modulos())}")
    print("="*60)

if __name__ == "__main__":
    main()
