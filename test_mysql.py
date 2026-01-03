import mysql.connector
from mysql.connector import Error
import sys

print("=== Diagnóstico de Conexión MySQL ===")
print()

# Test connection
try:
    print("Intentando conectar a MySQL...")
    print("Host: localhost")
    print("User: root")
    print("Password: (vacío)")
    print("Timeout: 5 segundos")
    print()
    
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        connection_timeout=5
    )
    
    print("✅ CONEXIÓN EXITOSA!")
    print(f"Versión de MySQL: {conn.get_server_info()}")
    
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    
    print("\nBases de datos disponibles:")
    for db in databases:
        print(f"  - {db[0]}")
    
    cursor.close()
    conn.close()
    
except Error as e:
    print(f"❌ ERROR DE CONEXIÓN:")
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {e}")
    print()
    print("Posibles causas:")
    print("1. XAMPP no está corriendo")
    print("2. MySQL no está iniciado en XAMPP")
    print("3. El puerto 3306 está bloqueado")
    print("4. Configuración incorrecta de MySQL")
    
except Exception as e:
    print(f"❌ ERROR INESPERADO:")
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {e}")

print()
print("Presiona Enter para salir...")
input()
