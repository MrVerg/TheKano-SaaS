"""
Script para eliminar conflictos de horarios en los datos existentes
"""
import mysql.connector
from collections import defaultdict

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='sistema_gestion_academica'
    )

def limpiar_conflictos():
    """Elimina horarios conflictivos dejando solo el primer módulo en cada slot"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    print("Buscando conflictos de horarios...")
    
    # Obtener todos los módulos con sus horarios
    cursor.execute("""
        SELECT m.id as modulo_id, m.nombre, m.docente_id, m.sala_id,
               mh.dia, mh.hora_inicio, mh.hora_fin
        FROM modulos m
        JOIN modulo_horarios mh ON m.id = mh.modulo_id
        ORDER BY m.id
    """)
    
    horarios = cursor.fetchall()
    
    # Detectar conflictos por docente
    conflictos_docente = defaultdict(list)
    for h in horarios:
        if h['docente_id']:
            key = (h['docente_id'], h['dia'], str(h['hora_inicio']))
            conflictos_docente[key].append(h)
    
    # Detectar conflictos por sala
    conflictos_sala = defaultdict(list)
    for h in horarios:
        if h['sala_id']:
            key = (h['sala_id'], h['dia'], str(h['hora_inicio']))
            conflictos_sala[key].append(h)
    
    horarios_a_eliminar = set()
    
    # Procesar conflictos de docente
    print("\n=== Conflictos de Docente ===")
    for key, modulos in conflictos_docente.items():
        if len(modulos) > 1:
            docente_id, dia, hora = key
            print(f"\nDocente {docente_id}, {dia} {hora}:")
            for i, mod in enumerate(modulos):
                if i == 0:
                    print(f"  ✓ MANTENER: {mod['nombre']}")
                else:
                    print(f"  ✗ ELIMINAR horario de: {mod['nombre']}")
                    horarios_a_eliminar.add((mod['modulo_id'], dia, hora))
    
    # Procesar conflictos de sala
    print("\n=== Conflictos de Sala ===")
    for key, modulos in conflictos_sala.items():
        if len(modulos) > 1:
            sala_id, dia, hora = key
            print(f"\nSala {sala_id}, {dia} {hora}:")
            for i, mod in enumerate(modulos):
                if i == 0:
                    print(f"  ✓ MANTENER: {mod['nombre']}")
                else:
                    print(f"  ✗ ELIMINAR horario de: {mod['nombre']}")
                    horarios_a_eliminar.add((mod['modulo_id'], dia, hora))
    
    # Eliminar horarios conflictivos
    if horarios_a_eliminar:
        print(f"\n🔧 Eliminando {len(horarios_a_eliminar)} horarios conflictivos...")
        for modulo_id, dia, hora_inicio in horarios_a_eliminar:
            cursor.execute("""
                DELETE FROM modulo_horarios
                WHERE modulo_id = %s AND dia = %s AND TIME(hora_inicio) = TIME(%s)
            """, (modulo_id, dia, hora_inicio))
        
        conn.commit()
        print("✅ Conflictos eliminados")
    else:
        print("\n✅ No se encontraron conflictos")
    
    cursor.close()
    conn.close()

def mostrar_resumen():
    """Muestra resumen de horarios después de limpieza"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    print("\n" + "="*50)
    print("RESUMEN DESPUÉS DE LIMPIEZA")
    print("="*50)
    
    cursor.execute("""
        SELECT COUNT(*) as total FROM modulo_horarios
    """)
    print(f"Total horarios: {cursor.fetchone()['total']}")
    
    cursor.execute("""
        SELECT COUNT(DISTINCT modulo_id) as total FROM modulo_horarios
    """)
    print(f"Módulos con horarios: {cursor.fetchone()['total']}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("Iniciando limpieza de conflictos...")
    print()
    
    try:
        limpiar_conflictos()
        mostrar_resumen()
        print()
        print("✅ ¡Limpieza completada exitosamente!")
        print("Ahora puedes probar el sistema sin conflictos preexistentes.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
