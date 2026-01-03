"""
Script para poblar la base de datos con datos de prueba completos
"""
import mysql.connector
from datetime import time

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='sistema_gestion_academica'
    )

def completar_disponibilidad_docentes():
    """Completa la disponibilidad para docentes que no tienen definida"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Obtener docentes sin disponibilidad
    cursor.execute("""
        SELECT DISTINCT d.id, d.nombre 
        FROM docentes d
        LEFT JOIN disponibilidad_docentes dd ON d.id = dd.docente_id
        WHERE dd.docente_id IS NULL
    """)
    docentes_sin_disp = cursor.fetchall()
    
    print(f"Docentes sin disponibilidad: {len(docentes_sin_disp)}")
    
    dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
    bloques = ["08:30", "09:15", "10:15", "11:00", "12:00", "12:45", 
               "14:30", "15:15", "16:15", "17:00", "18:00", "18:45", 
               "19:45", "20:30", "21:30", "22:15"]
    
    for docente in docentes_sin_disp:
        print(f"  Completando disponibilidad para: {docente['nombre']}")
        for dia in dias:
            for hora in bloques:
                # Marcar como disponible (pueden editarse después)
                cursor.execute("""
                    INSERT INTO disponibilidad_docentes (docente_id, dia, hora, estado)
                    VALUES (%s, %s, %s, 'disponible')
                """, (docente['id'], dia, hora))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Disponibilidad completada")

def completar_horarios_modulos():
    """Completa horarios para módulos que no tienen"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Obtener módulos sin horarios
    cursor.execute("""
        SELECT DISTINCT m.id, m.nombre, m.codigo
        FROM modulos m
        LEFT JOIN modulo_horarios mh ON m.id = mh.modulo_id
        WHERE mh.modulo_id IS NULL
    """)
    modulos_sin_horario = cursor.fetchall()
    
    print(f"Módulos sin horarios: {len(modulos_sin_horario)}")
    
    # Horarios de ejemplo (2 sesiones por semana)
    horarios_ejemplo = [
        ("LUNES", "08:30", "10:15"),
        ("MIERCOLES", "08:30", "10:15"),
    ]
    
    for modulo in modulos_sin_horario:
        print(f"  Asignando horarios a: {modulo['nombre']}")
        for dia, inicio, fin in horarios_ejemplo:
            cursor.execute("""
                INSERT INTO modulo_horarios (modulo_id, dia, hora_inicio, hora_fin)
                VALUES (%s, %s, %s, %s)
            """, (modulo['id'], dia, inicio, fin))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Horarios completados")

def completar_codigos_modulos():
    """Completa códigos faltantes en módulos"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT id, nombre, codigo
        FROM modulos
        WHERE codigo IS NULL OR codigo = ''
    """)
    modulos_sin_codigo = cursor.fetchall()
    
    print(f"Módulos sin código: {len(modulos_sin_codigo)}")
    
    for i, modulo in enumerate(modulos_sin_codigo, 1):
        codigo = f"MOD{modulo['id']:03d}"
        print(f"  Asignando código {codigo} a: {modulo['nombre']}")
        cursor.execute("""
            UPDATE modulos
            SET codigo = %s
            WHERE id = %s
        """, (codigo, modulo['id']))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Códigos completados")

def mostrar_resumen():
    """Muestra un resumen de los datos"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    print("\n" + "="*50)
    print("RESUMEN DE DATOS")
    print("="*50)
    
    # Módulos
    cursor.execute("SELECT COUNT(*) as total FROM modulos")
    print(f"Total módulos: {cursor.fetchone()['total']}")
    
    cursor.execute("SELECT COUNT(*) as total FROM modulo_horarios")
    print(f"Total horarios de módulos: {cursor.fetchone()['total']}")
    
    # Docentes
    cursor.execute("SELECT COUNT(*) as total FROM docentes")
    print(f"Total docentes: {cursor.fetchone()['total']}")
    
    cursor.execute("SELECT COUNT(DISTINCT docente_id) as total FROM disponibilidad_docentes")
    print(f"Docentes con disponibilidad: {cursor.fetchone()['total']}")
    
    # Salas
    cursor.execute("SELECT COUNT(*) as total FROM salas")
    print(f"Total salas: {cursor.fetchone()['total']}")
    
    # Carreras
    cursor.execute("SELECT COUNT(*) as total FROM carreras")
    print(f"Total carreras: {cursor.fetchone()['total']}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("Iniciando población de datos de prueba...")
    print()
    
    try:
        completar_codigos_modulos()
        print()
        completar_horarios_modulos()
        print()
        completar_disponibilidad_docentes()
        print()
        mostrar_resumen()
        print()
        print("✅ ¡Datos de prueba completados exitosamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
