import mysql.connector
from mysql.connector import Error
import logging
from database import SistemaDAO

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clear_database():
    """
    Elimina todos los registros de la base de datos respetando las restricciones de clave foránea.
    """
    dao = SistemaDAO()
    db = dao.db
    
    print("⚠️  ADVERTENCIA: ESTA ACCIÓN ELIMINARÁ TODOS LOS DATOS DEL SISTEMA ⚠️")
    print("Se borrarán: Docentes, Carreras, Módulos, Salas, Horarios, etc.")
    print("Solo se conservará/recreará el usuario Administrador.")
    
    confirm = input("¿Estás seguro de que quieres continuar? (escribe 'SI' para confirmar): ")
    
    if confirm != "SI":
        print("Operación cancelada.")
        return

    connection = db.get_connection()
    if not connection:
        logging.error("No se pudo conectar a la base de datos.")
        return

    cursor = None
    try:
        cursor = connection.cursor()
        
        # Desactivar chequeo de claves foráneas para facilitar el borrado
        logging.info("Desactivando chequeo de claves foráneas...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Lista de tablas a vaciar
        tablas = [
            "modulo_horarios",
            "disponibilidad_docentes",
            "carrera_semestres",
            "carrera_salas",
            "modulos",
            "docentes",
            "carreras",
            "salas",
            "usuarios"
        ]
        
        for tabla in tablas:
            logging.info(f"Vaciando tabla: {tabla}...")
            cursor.execute(f"TRUNCATE TABLE {tabla}")
        
        # Reactivar chequeo de claves foráneas
        logging.info("Reactivando chequeo de claves foráneas...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        connection.commit()
        logging.info("✅ Todas las tablas han sido vaciadas.")
        
        # Recrear usuario administrador
        logging.info("Recreando usuario administrador...")
        cursor.execute(
            "INSERT INTO usuarios (email, password, nombre, rol) VALUES (%s, %s, %s, %s)",
            ('admin@ceduc.cl', '123456', 'Administrador', 'admin')
        )
        connection.commit()
        logging.info("✅ Usuario administrador restaurado (admin@ceduc.cl / 123456).")
        
    except Error as e:
        logging.error(f"❌ Error durante el proceso: {e}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    clear_database()
