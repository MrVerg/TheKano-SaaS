import mysql.connector
from mysql.connector import Error
import sys

def verify_connection():
    print("Verificando conexión a MySQL (XAMPP)...")
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': ''
    }
    
    try:
        # Intentar conectar al servidor
        print(f"Intentando conectar a {config['host']} con usuario '{config['user']}'...")
        conn = mysql.connector.connect(**config)
        
        if conn.is_connected():
            print("✅ Conexión exitosa al servidor MySQL.")
            print(f"Versión del servidor: {conn.get_server_info()}")
            
            cursor = conn.cursor()
            
            # Verificar base de datos
            db_name = 'sistema_gestion_academica'
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
            result = cursor.fetchone()
            
            if result:
                print(f"✅ La base de datos '{db_name}' existe.")
            else:
                print(f"⚠️ La base de datos '{db_name}' NO existe. Se creará automáticamente al iniciar la app.")
                
            cursor.close()
            conn.close()
            return True
            
    except Error as e:
        print(f"❌ Error al conectar a MySQL: {e}")
        print("\nPosibles soluciones:")
        print("1. Asegúrate de que XAMPP (MySQL) esté corriendo.")
        print("2. Verifica que el puerto 3306 esté libre.")
        print("3. Verifica que el usuario sea 'root' y no tenga contraseña (default de XAMPP).")
        return False

if __name__ == "__main__":
    success = verify_connection()
    sys.exit(0 if success else 1)
