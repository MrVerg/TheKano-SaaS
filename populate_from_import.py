"""
Script para poblar la base de datos directamente desde los datos de IMPORT.py
"""
from database import SistemaDAO
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Importar los datos desde IMPORT.py
import sys
sys.path.append('.')
from IMPORT import docentes_data, carreras_data, modulos_data, salas_data, horarios_data

def main():
    print("🚀 Poblando base de datos desde IMPORT.py...")
    
    dao = SistemaDAO()
    
    # 1. Importar Salas
    print(f"\n📍 Importando {len(salas_data)} salas...")
    for sala in salas_data:
        try:
            dao.guardar_sala(sala)
        except Exception as e:
            print(f"  ⚠️  Error guardando sala {sala.get('nombre')}: {e}")
    print(f"✅ Salas importadas")
    
    # 2. Importar Docentes
    print(f"\n👨‍🏫 Importando {len(docentes_data)} docentes...")
    for docente in docentes_data:
        try:
            dao.guardar_docente(docente)
        except Exception as e:
            print(f"  ⚠️  Error guardando docente {docente.get('nombre')}: {e}")
    print(f"✅ Docentes importados")
    
    # 3. Importar Carreras
    print(f"\n🎓 Importando {len(carreras_data)} carreras...")
    for carrera in carreras_data:
        try:
            # Convertir semestres y salas_ids de string a lista
            if isinstance(carrera.get('semestres'), (int, str)):
                if isinstance(carrera['semestres'], str):
                    carrera['semestres'] = [int(s.strip()) for s in str(carrera['semestres']).split(',') if s.strip()]
                else:
                    carrera['semestres'] = list(range(1, carrera['semestres'] + 1))
            
            if isinstance(carrera.get('salas_ids'), str):
                carrera['salas_ids'] = [int(s.strip()) for s in carrera['salas_ids'].split(',') if s.strip()]
            
            dao.guardar_carrera(carrera)
        except Exception as e:
            print(f"  ⚠️  Error guardando carrera {carrera.get('nombre')}: {e}")
    print(f"✅ Carreras importadas")
    
    # 4. Importar Módulos
    print(f"\n📚 Importando {len(modulos_data)} módulos...")
    for modulo in modulos_data:
        try:
            dao.guardar_modulo(modulo)
        except Exception as e:
            print(f"  ⚠️  Error guardando módulo {modulo.get('nombre')}: {e}")
    print(f"✅ Módulos importados")
    
    # 5. Importar Horarios
    print(f"\n⏰ Importando {len(horarios_data)} horarios...")
    # Agrupar horarios por módulo
    horarios_por_modulo = {}
    for horario in horarios_data:
        modulo_id = horario['modulo_id']
        if modulo_id not in horarios_por_modulo:
            horarios_por_modulo[modulo_id] = []
        horarios_por_modulo[modulo_id].append(horario)
    
    for modulo_id, horarios in horarios_por_modulo.items():
        try:
            dao.guardar_horarios_modulo(modulo_id, horarios)
        except Exception as e:
            print(f"  ⚠️  Error guardando horarios del módulo {modulo_id}: {e}")
    print(f"✅ Horarios importados")
    
    # Resumen final
    print("\n" + "="*50)
    print("✅ IMPORTACIÓN COMPLETADA")
    print("="*50)
    print(f"Salas: {len(dao.obtener_salas())}")
    print(f"Docentes: {len(dao.obtener_docentes())}")
    print(f"Carreras: {len(dao.obtener_carreras())}")
    print(f"Módulos: {len(dao.obtener_modulos())}")
    print("="*50)

if __name__ == "__main__":
    main()
