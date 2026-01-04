import os
import logging
import pymysql
from pymysql.err import Error
from dotenv import load_dotenv

# Cargar variables de entorno si existen
load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.database = os.getenv('DB_NAME', 'sistema_gestion_academica')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.connection = None
    
    def get_connection(self):
        if self.connection is None or not self.connection.open:
            try:
                self.connection = pymysql.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    port=int(os.getenv('DB_PORT', 3306)),
                    connect_timeout=5,  # 5 second timeout
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
            except Exception as e:
                logging.error(f"Error al conectar: {e}")
                return None
        return self.connection
    
    
    def execute_query(self, query, params=None, fetch=False):
        connection = self.get_connection()
        if connection is None:
            return None
        
        cursor = None
        try:
            cursor = connection.cursor()  # Already DictCursor from get_connection
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                return cursor.rowcount
        except Exception as e:
            logging.error(f"Error ejecutando consulta: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

class SistemaDAO:
    def __init__(self):
        self.db = Database()

    def inicializar_base_de_datos(self):
        logging.info("Inicializando base de datos...")
        db_existe = False
        db_tiene_datos = False
        
        try:
            # Add connection timeout to prevent freezing
            conn = pymysql.connect(
                host=self.db.host,
                user=self.db.user,
                password=self.db.password,
                connect_timeout=5,  # 5 second timeout
                charset='utf8mb4'
            )
            cursor = conn.cursor()
            
            # Verificar si la base de datos existe
            cursor.execute(f"SHOW DATABASES LIKE '{self.db.database}'")
            db_existe = cursor.fetchone() is not None
            
            if db_existe:
                logging.info(f"Base de datos '{self.db.database}' ya existe.")
            else:
                logging.info(f"Base de datos '{self.db.database}' no existe. Creando...")
                cursor.execute(f"CREATE DATABASE {self.db.database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                logging.info(f"Base de datos '{self.db.database}' creada exitosamente.")
            
            cursor.close()
            conn.close()
        except Exception as e:
            error_msg = f"FATAL: No se pudo crear o asegurar la base de datos: {e}"
            logging.error(error_msg)
            raise Exception(f"Error de conexión a MySQL. Asegúrate de que XAMPP esté corriendo.\\nDetalle: {e}")

        logging.info("Creando/verificando tablas...")
        tablas_sql = [
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                nombre VARCHAR(255),
                rol VARCHAR(50)
            ) ENGINE=InnoDB;
            """,
            """
            CREATE TABLE IF NOT EXISTS salas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                capacidad INT,
                tipo VARCHAR(100)
            ) ENGINE=InnoDB;
            """,
            """
            CREATE TABLE IF NOT EXISTS carreras (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                jornada VARCHAR(50),
                alumnos_proyectados INT
            ) ENGINE=InnoDB;
            """,
            """
            CREATE TABLE IF NOT EXISTS docentes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                titulo VARCHAR(255),
                contrato VARCHAR(50),
                horas_contratadas INT,
                email VARCHAR(255) UNIQUE,
                evaluacion DECIMAL(3,2)
            ) ENGINE=InnoDB;
            """,
            """
            CREATE TABLE IF NOT EXISTS modulos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                codigo VARCHAR(50),
                horas_teoricas INT,
                horas_practicas INT,
                alumnos_proyectados INT,
                semestre INT,
                carrera_id INT,
                docente_id INT,
                sala_id INT,
                FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE SET NULL,
                FOREIGN KEY (docente_id) REFERENCES docentes(id) ON DELETE SET NULL,
                FOREIGN KEY (sala_id) REFERENCES salas(id) ON DELETE SET NULL
            ) ENGINE=InnoDB;
            """,
            """
            CREATE TABLE IF NOT EXISTS carrera_semestres (
                carrera_id INT,
                semestre INT,
                PRIMARY KEY (carrera_id, semestre),
                FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
            """,
            """
            CREATE TABLE IF NOT EXISTS carrera_salas (
                carrera_id INT,
                sala_id INT,
                PRIMARY KEY (carrera_id, sala_id),
                FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE,
                FOREIGN KEY (sala_id) REFERENCES salas(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
            """,
            """
            CREATE TABLE IF NOT EXISTS modulo_horarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                modulo_id INT,
                dia VARCHAR(20),
                hora_inicio VARCHAR(10),
                hora_fin VARCHAR(10),
                FOREIGN KEY (modulo_id) REFERENCES modulos(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
            """,
            """
            CREATE TABLE IF NOT EXISTS disponibilidad_docentes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                docente_id INT,
                dia VARCHAR(20),
                hora VARCHAR(10),
                estado VARCHAR(20),
                FOREIGN KEY (docente_id) REFERENCES docentes(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
            """
        ]
        
        for tabla_query in tablas_sql:
            try:
                self.db.execute_query(tabla_query)
            except Exception as e:
                logging.error(f"Error creando tabla: {e} | Query: {tabla_query[:50]}...")

        logging.info("Tablas creadas o verificadas exitosamente.")

        # Verificar si existe el usuario admin
        try:
            admin_user = self.db.execute_query("SELECT * FROM usuarios WHERE email = %s", ('admin@ceduc.cl',), fetch=True)
            if not admin_user:
                logging.info("Creando usuario administrador por defecto...")
                self.db.execute_query(
                    "INSERT INTO usuarios (email, password, nombre, rol) VALUES (%s, %s, %s, %s)",
                    ('admin@ceduc.cl', '123456', 'Administrador', 'admin')
                )
                logging.info("Usuario administrador creado.")
            else:
                logging.info("Usuario administrador ya existe.")
                db_tiene_datos = True
        except Exception as e:
            logging.error(f"Error al verificar/crear usuario admin: {e}")
        
        # Si la base de datos no existía o no tiene datos, poblarla con datos iniciales
        if not db_existe or not db_tiene_datos:
            logging.info("Base de datos nueva o vacía detectada. Intentando cargar datos iniciales...")
            if not self.cargar_datos_iniciales():
                logging.info("No se pudieron cargar datos iniciales. Poblando con datos de prueba por defecto...")
                try:
                    self.poblar_datos_prueba()
                    logging.info("✅ Datos de prueba poblados exitosamente.")
                except Exception as e:
                    logging.error(f"Error al poblar datos de prueba: {e}")

    def cargar_datos_iniciales(self):
        """Carga datos iniciales desde initial_data.json si existe"""
        import json
        import os
        
        json_path = 'initial_data.json'
        # Check in current directory first
        if not os.path.exists(json_path):
            # Try looking in the same directory as the executable/script
            base_path = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(base_path, 'initial_data.json')
            
        # Also check in sys._MEIPASS if running as executable
        import sys
        if not os.path.exists(json_path) and hasattr(sys, '_MEIPASS'):
            json_path = os.path.join(sys._MEIPASS, 'initial_data.json')
            
        if os.path.exists(json_path):
            try:
                logging.info(f"Cargando datos desde {json_path}...")
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Order of insertion matters due to foreign keys
                tables_order = [
                    'salas', 'carreras', 'docentes', 'modulos', 
                    'carrera_semestres', 'carrera_salas', 
                    'disponibilidad_docentes', 'modulo_horarios'
                ]
                
                for table in tables_order:
                    if table in data and data[table]:
                        logging.info(f"Poblando tabla {table} ({len(data[table])} registros)...")
                        rows = data[table]
                        if not rows:
                            continue
                            
                        # Get columns from first row
                        columns = list(rows[0].keys())
                        placeholders = ', '.join(['%s'] * len(columns))
                        col_names = ', '.join(columns)
                        
                        query = f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})"
                        
                        for row in rows:
                            values = [row[col] for col in columns]
                            self.db.execute_query(query, tuple(values))
                            
                logging.info("Datos iniciales cargados exitosamente.")
                return True
            except Exception as e:
                logging.error(f"Error cargando datos iniciales: {e}")
                return False
        else:
            logging.warning("No se encontró initial_data.json.")
            return False
    
    def poblar_datos_prueba(self):
        """Puebla la base de datos con datos de prueba completos"""
        logging.info("Iniciando población de datos de prueba...")
        
        # Verificar si ya hay datos
        salas_count = self.db.execute_query("SELECT COUNT(*) as count FROM salas", fetch=True)
        if salas_count and salas_count[0]['count'] > 0:
            logging.info("Ya existen datos en la base de datos. Omitiendo población.")
            return
        
        # Poblar datos usando la lógica de populate_test_data.py
        self._poblar_salas()
        self._poblar_docentes()
        self._poblar_carreras()
        self._poblar_modulos()
        self._completar_disponibilidad_docentes()
        self._completar_horarios_modulos()
        self._completar_codigos_modulos()
        
        logging.info("Población de datos de prueba completada.")
    
    def _poblar_salas(self):
        """Crea salas de ejemplo"""
        salas = [
            ("Sala A101", 30, "Teórica"),
            ("Sala A102", 30, "Teórica"),
            ("Sala A103", 35, "Teórica"),
            ("Sala B201", 25, "Teórica"),
            ("Sala B202", 25, "Teórica"),
            ("Lab Computación 1", 20, "Laboratorio"),
            ("Lab Computación 2", 20, "Laboratorio"),
            ("Lab Enfermería", 15, "Laboratorio"),
            ("Taller Mecánica", 18, "Taller"),
            ("Sala C301", 40, "Teórica"),
            ("Sala C302", 40, "Teórica"),
            ("Auditorio", 100, "Auditorio"),
            ("Sala D401", 30, "Teórica"),
            ("Lab Química", 20, "Laboratorio"),
            ("Gimnasio", 50, "Deportivo")
        ]
        
        for nombre, capacidad, tipo in salas:
            self.db.execute_query(
                "INSERT INTO salas (nombre, capacidad, tipo) VALUES (%s, %s, %s)",
                (nombre, capacidad, tipo)
            )
        logging.info(f"✅ {len(salas)} salas creadas")
    
    def _poblar_docentes(self):
        """Crea docentes de ejemplo"""
        docentes = [
            ("Juan Pérez González", "Ingeniero Civil", "Planta", 44, "juan.perez@ceduc.cl", 4.5),
            ("María García López", "Profesora de Matemáticas", "Planta", 44, "maria.garcia@ceduc.cl", 4.8),
            ("Carlos Rodríguez", "Ingeniero en Computación", "Honorarios", 20, "carlos.rodriguez@ceduc.cl", 4.2),
            ("Ana Martínez", "Enfermera", "Planta", 44, "ana.martinez@ceduc.cl", 4.7),
            ("Luis Fernández", "Mecánico Industrial", "Honorarios", 30, "luis.fernandez@ceduc.cl", 4.3),
            ("Carmen Sánchez", "Profesora de Inglés", "Planta", 44, "carmen.sanchez@ceduc.cl", 4.6),
            ("Roberto Torres", "Ingeniero Eléctrico", "Planta", 44, "roberto.torres@ceduc.cl", 4.4),
            ("Patricia Ramírez", "Contadora", "Honorarios", 25, "patricia.ramirez@ceduc.cl", 4.1),
            ("Diego Flores", "Profesor de Física", "Planta", 44, "diego.flores@ceduc.cl", 4.9),
            ("Laura Morales", "Diseñadora Gráfica", "Honorarios", 20, "laura.morales@ceduc.cl", 4.0),
            ("Fernando Castro", "Ingeniero Mecánico", "Planta", 44, "fernando.castro@ceduc.cl", 4.5),
            ("Sofía Vargas", "Psicóloga", "Honorarios", 15, "sofia.vargas@ceduc.cl", 4.8),
            ("Miguel Ángel Ruiz", "Profesor de Química", "Planta", 44, "miguel.ruiz@ceduc.cl", 4.6),
            ("Isabel Ortiz", "Administradora", "Honorarios", 25, "isabel.ortiz@ceduc.cl", 4.2),
            ("Andrés Jiménez", "Técnico Electrónico", "Planta", 44, "andres.jimenez@ceduc.cl", 4.3)
        ]
        
        for nombre, titulo, contrato, horas, email, evaluacion in docentes:
            self.db.execute_query(
                "INSERT INTO docentes (nombre, titulo, contrato, horas_contratadas, email, evaluacion) VALUES (%s, %s, %s, %s, %s, %s)",
                (nombre, titulo, contrato, horas, email, evaluacion)
            )
        logging.info(f"✅ {len(docentes)} docentes creados")
    
    def _poblar_carreras(self):
        """Crea carreras de ejemplo con sus semestres y salas"""
        carreras = [
            ("Ingeniería en Informática", "Diurna", 120, 8, [1, 2, 6, 7]),
            ("Enfermería y Telemedicina", "Vespertina", 80, 8, [3, 4, 8]),
            ("Técnico en Mecánica Industrial", "Diurna", 60, 6, [5, 9]),
            ("Administración de Empresas", "Vespertina", 100, 8, [10, 11, 12]),
            ("Técnico en Electricidad", "Diurna", 50, 6, [13, 14])
        ]
        
        for nombre, jornada, alumnos, duracion, salas_ids in carreras:
            # Insertar carrera
            result = self.db.execute_query(
                "INSERT INTO carreras (nombre, jornada, alumnos_proyectados) VALUES (%s, %s, %s)",
                (nombre, jornada, alumnos)
            )
            
            # Obtener el ID de la carrera recién creada
            carrera_id = self.db.execute_query("SELECT LAST_INSERT_ID() as id", fetch=True)[0]['id']
            
            # Insertar semestres
            for sem in range(1, duracion + 1):
                self.db.execute_query(
                    "INSERT INTO carrera_semestres (carrera_id, semestre) VALUES (%s, %s)",
                    (carrera_id, sem)
                )
            
            # Asignar salas
            for sala_id in salas_ids:
                self.db.execute_query(
                    "INSERT INTO carrera_salas (carrera_id, sala_id) VALUES (%s, %s)",
                    (carrera_id, sala_id)
                )
        
        logging.info(f"✅ {len(carreras)} carreras creadas con semestres y salas")
    
    def _poblar_modulos(self):
        """Crea módulos de ejemplo para cada carrera"""
        # Módulos para Ingeniería en Informática (carrera_id=1)
        modulos_informatica = [
            ("Programación I", "INF101", 4, 2, 30, 1, 1, 1, 6),
            ("Matemáticas I", "MAT101", 6, 0, 30, 1, 1, 2, 1),
            ("Introducción a la Ingeniería", "ING101", 2, 2, 30, 1, 1, 3, 1),
            ("Programación II", "INF201", 4, 2, 30, 2, 1, 1, 6),
            ("Matemáticas II", "MAT201", 6, 0, 30, 2, 1, 2, 1),
            ("Estructuras de Datos", "INF301", 4, 2, 30, 3, 1, 3, 7),
        ]
        
        # Módulos para Enfermería (carrera_id=2)
        modulos_enfermeria = [
            ("Anatomía y Fisiología", "ENF101", 4, 2, 25, 1, 2, 4, 3),
            ("Enfermería Básica", "ENF102", 3, 3, 25, 1, 2, 4, 8),
            ("Farmacología", "ENF201", 4, 2, 25, 2, 2, 13, 3),
        ]
        
        # Módulos para Mecánica Industrial (carrera_id=3)
        modulos_mecanica = [
            ("Dibujo Técnico", "MEC101", 2, 4, 20, 1, 3, 5, 9),
            ("Resistencia de Materiales", "MEC201", 4, 2, 20, 2, 3, 11, 5),
        ]
        
        # Módulos para Administración (carrera_id=4)
        modulos_admin = [
            ("Contabilidad I", "ADM101", 4, 2, 30, 1, 4, 8, 10),
            ("Economía", "ADM102", 4, 0, 30, 1, 4, 14, 10),
        ]
        
        # Módulos para Electricidad (carrera_id=5)
        modulos_electricidad = [
            ("Circuitos Eléctricos", "ELE101", 4, 2, 18, 1, 5, 7, 13),
            ("Electrónica Básica", "ELE201", 3, 3, 18, 2, 5, 15, 14),
        ]
        
        todos_modulos = modulos_informatica + modulos_enfermeria + modulos_mecanica + modulos_admin + modulos_electricidad
        
        for nombre, codigo, h_teoricas, h_practicas, alumnos, semestre, carrera_id, docente_id, sala_id in todos_modulos:
            self.db.execute_query(
                """INSERT INTO modulos (nombre, codigo, horas_teoricas, horas_practicas, 
                   alumnos_proyectados, semestre, carrera_id, docente_id, sala_id) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (nombre, codigo, h_teoricas, h_practicas, alumnos, semestre, carrera_id, docente_id, sala_id)
            )
        
        logging.info(f"✅ {len(todos_modulos)} módulos creados")
    
    def _completar_disponibilidad_docentes(self):
        """Completa la disponibilidad para todos los docentes"""
        docentes = self.db.execute_query("SELECT id FROM docentes", fetch=True)
        dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
        bloques = ["08:30", "09:05", "09:40", "10:15", "10:50", "11:25", "12:00", "12:35",
                   "13:10", "13:45", "14:20", "14:55", "15:30", "16:05", "16:40", "17:15",
                   "17:50", "18:25", "19:00", "19:35", "20:10", "20:45", "21:20", "21:55"]
        
        for docente in docentes:
            for dia in dias:
                for hora in bloques:
                    self.db.execute_query(
                        "INSERT INTO disponibilidad_docentes (docente_id, dia, hora, estado) VALUES (%s, %s, %s, 'disponible')",
                        (docente['id'], dia, hora)
                    )
        
        logging.info(f"✅ Disponibilidad completada para {len(docentes)} docentes")
    
    def _completar_horarios_modulos(self):
        """Completa horarios para todos los módulos"""
        modulos = self.db.execute_query("SELECT id FROM modulos", fetch=True)
        horarios_ejemplo = [
            ("LUNES", "08:30", "10:15"),
            ("MIERCOLES", "08:30", "10:15"),
        ]
        
        for modulo in modulos:
            for dia, inicio, fin in horarios_ejemplo:
                self.db.execute_query(
                    "INSERT INTO modulo_horarios (modulo_id, dia, hora_inicio, hora_fin) VALUES (%s, %s, %s, %s)",
                    (modulo['id'], dia, inicio, fin)
                )
        
        logging.info(f"✅ Horarios completados para {len(modulos)} módulos")
    
    def _completar_codigos_modulos(self):
        """Completa códigos faltantes en módulos (si los hay)"""
        modulos_sin_codigo = self.db.execute_query(
            "SELECT id, nombre FROM modulos WHERE codigo IS NULL OR codigo = ''",
            fetch=True
        )
        
        if modulos_sin_codigo:
            for modulo in modulos_sin_codigo:
                codigo = f"MOD{modulo['id']:03d}"
                self.db.execute_query(
                    "UPDATE modulos SET codigo = %s WHERE id = %s",
                    (codigo, modulo['id'])
                )
            logging.info(f"✅ Códigos completados para {len(modulos_sin_codigo)} módulos")
        else:
            logging.info("✅ Todos los módulos ya tienen código")


    def verificar_usuario(self, email, password):
        """Valida las credenciales de un usuario contra la base de datos."""
        logging.info(f"Verificando al usuario '{email}' en la base de datos.")
        query = "SELECT * FROM usuarios WHERE email = %s AND password = %s"
        result = self.db.execute_query(query, (email, password), fetch=True)
        return result[0] if result else None
    
    def obtener_salas(self):
        query = "SELECT * FROM salas ORDER BY nombre"
        return self.db.execute_query(query, fetch=True)
    
    def obtener_docentes(self):
        query = "SELECT * FROM docentes ORDER BY nombre"
        return self.db.execute_query(query, fetch=True)
    
    def obtener_carreras(self):
        query = "SELECT * FROM carreras ORDER BY nombre"
        return self.db.execute_query(query, fetch=True)

    def obtener_semestres_carrera(self, carrera_id):
        """Obtiene los semestres de una carrera específica"""
        query = """SELECT semestre FROM carrera_semestres 
                  WHERE carrera_id = %s ORDER BY semestre"""
        result = self.db.execute_query(query, (carrera_id,), fetch=True)
        return [item['semestre'] for item in result] if result else []

    def obtener_salas_carrera(self, carrera_id):
        """Obtiene las salas asignadas a una carrera"""
        query = """SELECT s.* FROM salas s 
                  INNER JOIN carrera_salas cs ON s.id = cs.sala_id
                  WHERE cs.carrera_id = %s ORDER BY s.nombre"""
        return self.db.execute_query(query, (carrera_id,), fetch=True)

    def obtener_horarios_modulo(self, modulo_id):
        """Obtiene los horarios de un módulo"""
        query = """SELECT dia, hora_inicio, hora_fin FROM modulo_horarios 
                  WHERE modulo_id = %s ORDER BY dia, hora_inicio"""
        return self.db.execute_query(query, (modulo_id,), fetch=True)

    def obtener_modulos_carrera(self, carrera_id):
        """Obtiene todos los módulos de una carrera específica"""
        query = """SELECT m.*, d.nombre as docente_nombre, s.nombre as sala_nombre 
                   FROM modulos m 
                   LEFT JOIN docentes d ON m.docente_id = d.id 
                   LEFT JOIN salas s ON m.sala_id = s.id 
                   WHERE m.carrera_id = %s"""
        return self.db.execute_query(query, (carrera_id,), fetch=True)

    def obtener_modulos(self):
        """Obtiene todos los módulos registrados"""
        query = """SELECT m.*, d.nombre as docente_nombre, s.nombre as sala_nombre 
                   FROM modulos m 
                   LEFT JOIN docentes d ON m.docente_id = d.id 
                   LEFT JOIN salas s ON m.sala_id = s.id"""
        return self.db.execute_query(query, fetch=True)

    def obtener_disponibilidad_docente(self, docente_id):
        """Obtiene la disponibilidad horaria de un docente"""
        query = "SELECT dia, hora, estado FROM disponibilidad_docentes WHERE docente_id = %s"
        result = self.db.execute_query(query, (docente_id,), fetch=True)
        # Convertir a formato de diccionario
        disponibilidad = {}
        if result:
            for row in result:
                dia = row['dia']
                hora = row['hora']
                if dia not in disponibilidad:
                    disponibilidad[dia] = {}
                # Convertir estado string a booleano
                disponibilidad[dia][hora] = (row['estado'] == 'disponible')
        return disponibilidad

    def guardar_modulo(self, modulo_data, horarios, modulo_id=None):
        """Guarda un módulo (nuevo o existente) con sus horarios"""
        connection = self.db.get_connection()
        if not connection:
            return None
        
        cursor = None
        try:
            cursor = connection.cursor()
            
            if modulo_id:
                # Actualizar módulo
                query = """UPDATE modulos SET nombre = %s, codigo = %s, horas_teoricas = %s,
                          horas_practicas = %s, alumnos_proyectados = %s, carrera_id = %s,
                          semestre = %s, docente_id = %s, sala_id = %s WHERE id = %s"""
                cursor.execute(query, (*modulo_data, modulo_id))
            else:
                # Insertar nuevo módulo
                query = """INSERT INTO modulos (nombre, codigo, horas_teoricas, horas_practicas,
                          alumnos_proyectados, carrera_id, semestre, docente_id, sala_id) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, modulo_data)
                modulo_id = cursor.lastrowid
            
            # Actualizar horarios
            cursor.execute("DELETE FROM modulo_horarios WHERE modulo_id = %s", (modulo_id,))
            horario_data = [(modulo_id, horario['dia'], horario['hora_inicio'], horario['hora_fin']) 
                           for horario in horarios]
            if horario_data:
                cursor.executemany("""INSERT INTO modulo_horarios 
                                    (modulo_id, dia, hora_inicio, hora_fin) 
                                    VALUES (%s, %s, %s, %s)""", horario_data)
            
            connection.commit()
            return modulo_id
            
        except Error as e:
            # Check if error is "Table doesn't exist" (1146)
            logging.error(f"Error en guardar_modulo - errno: {getattr(e, 'errno', 'N/A')}, mensaje: {str(e)}")
            if hasattr(e, 'errno') and e.errno == 1146 and "modulo_horarios" in str(e):
                logging.warning("⚠️ Tabla 'modulo_horarios' no existe. Creando automáticamente...")
                try:
                    create_table_query = """
                    CREATE TABLE IF NOT EXISTS modulo_horarios (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        modulo_id INT,
                        dia VARCHAR(20),
                        hora_inicio VARCHAR(10),
                        hora_fin VARCHAR(10),
                        FOREIGN KEY (modulo_id) REFERENCES modulos(id) ON DELETE CASCADE
                    ) ENGINE=InnoDB;
                    """
                    cursor.execute(create_table_query)
                    connection.commit()
                    logging.info("✅ Tabla 'modulo_horarios' creada exitosamente. Reintentando guardado...")
                    
                    # Retry insertion
                    cursor.execute("DELETE FROM modulo_horarios WHERE modulo_id = %s", (modulo_id,))
                    if horario_data:
                        cursor.executemany("""INSERT INTO modulo_horarios 
                                            (modulo_id, dia, hora_inicio, hora_fin) 
                                            VALUES (%s, %s, %s, %s)""", horario_data)
                    connection.commit()
                    logging.info(f"✅ Guardado exitoso después de crear tabla. modulo_id={modulo_id}")
                    return modulo_id
                except Exception as ex:
                    logging.error(f"❌ Error fatal creando/guardando en modulo_horarios: {ex}")
                    connection.rollback()
                    return None
            
            logging.error(f"Error guardando módulo (no es tabla faltante): {e}")
            connection.rollback()
            return None
        except Exception as e:
            logging.error(f"Error inesperado en guardar_modulo: {type(e).__name__} - {str(e)}")
            if connection:
                connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def eliminar_modulo(self, modulo_id):
        """Elimina un módulo y sus horarios asociados"""
        connection = self.db.get_connection()
        if not connection:
            return False
        
        cursor = None
        try:
            cursor = connection.cursor()
            
            # 1. Eliminar horarios asociados
            cursor.execute("DELETE FROM modulo_horarios WHERE modulo_id = %s", (modulo_id,))
            
            # 2. Eliminar el módulo
            cursor.execute("DELETE FROM modulos WHERE id = %s", (modulo_id,))
            
            connection.commit()
            return True
            
        except Error as e:
            logging.error(f"Error eliminando módulo: {e}")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def obtener_horas_asignadas_docente(self, docente_id):
        """Calcula el total de horas asignadas a un docente"""
        query = """
            SELECT SUM(horas_teoricas + horas_practicas) as total_horas
            FROM modulos
            WHERE docente_id = %s
        """
        result = self.db.execute_query(query, (docente_id,), fetch=True)
        if result and result[0]['total_horas'] is not None:
            return int(result[0]['total_horas'])
        return 0

    def guardar_disponibilidad_docente(self, docente_id, disponibilidad):
        """Guarda la disponibilidad horaria de un docente"""
        connection = self.db.get_connection()
        if not connection:
            return False
        
        cursor = None
        try:
            cursor = connection.cursor()
            
            # Eliminar disponibilidad existente
            cursor.execute("DELETE FROM disponibilidad_docentes WHERE docente_id = %s", (docente_id,))
            
            # Insertar nueva disponibilidad
            insert_data = []
            for dia, horas in disponibilidad.items():
                for hora, disponible in horas.items():
                    insert_data.append((docente_id, dia, hora, disponible))
            
            if insert_data:
                cursor.executemany("""INSERT INTO disponibilidad_docentes 
                                    (docente_id, dia, hora, disponible) 
                                    VALUES (%s, %s, %s, %s)""", insert_data)
            
            connection.commit()
            return True
            
        except Error as e:
            logging.error(f"Error guardando disponibilidad: {e}")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def guardar_docente(self, docente_data, docente_id=None):
        """Guarda un docente (nuevo o existente)"""
        connection = self.db.get_connection()
        if not connection:
            return None
        
        cursor = None
        try:
            cursor = connection.cursor()
            
            if docente_id:
                # Actualizar docente existente
                query = """UPDATE docentes SET nombre = %s, titulo = %s, contrato = %s,
                          horas_contratadas = %s, email = %s, evaluacion = %s WHERE id = %s"""
                cursor.execute(query, (*docente_data, docente_id))
            else:
                # Insertar nuevo docente
                query = """INSERT INTO docentes (nombre, titulo, contrato, horas_contratadas, email, evaluacion) 
                          VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, docente_data)
                docente_id = cursor.lastrowid
            
            connection.commit()
            return docente_id
            
        except Error as e:
            logging.error(f"Error guardando docente: {e}")
            connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def guardar_carrera(self, carrera_data, semestres_seleccionados, salas_seleccionadas, carrera_id=None):
        """Guarda una carrera (nueva o existente) - VERSIÓN CORREGIDA"""
        connection = self.db.get_connection()
        if not connection:
            return None
        
        cursor = None
        try:
            cursor = connection.cursor()
            
            if carrera_id:
                # Actualizar carrera existente
                query = """UPDATE carreras SET nombre = %s, jornada = %s, alumnos_proyectados = %s 
                          WHERE id = %s"""
                cursor.execute(query, (*carrera_data, carrera_id))
            else:
                # Insertar nueva carrera
                query = """INSERT INTO carreras (nombre, jornada, alumnos_proyectados) 
                          VALUES (%s, %s, %s)"""
                cursor.execute(query, carrera_data)
                carrera_id = cursor.lastrowid
            
            # ACTUALIZACIÓN CORREGIDA: Manejo inteligente de semestres
            # Primero obtenemos los semestres actuales
            cursor.execute("SELECT semestre FROM carrera_semestres WHERE carrera_id = %s", (carrera_id,))
            semestres_actuales = [row['semestre'] for row in cursor.fetchall()]
            
            # Identificar semestres a eliminar y a agregar
            semestres_a_eliminar = [sem for sem in semestres_actuales if sem not in semestres_seleccionados]
            semestres_a_agregar = [sem for sem in semestres_seleccionados if sem not in semestres_actuales]
            
            # Eliminar semestres que ya no están seleccionados
            if semestres_a_eliminar:
                placeholders = ','.join(['%s'] * len(semestres_a_eliminar))
                query_eliminar = f"DELETE FROM carrera_semestres WHERE carrera_id = %s AND semestre IN ({placeholders})"
                cursor.execute(query_eliminar, (carrera_id, *semestres_a_eliminar))
            
            # Agregar nuevos semestres (usando INSERT IGNORE para evitar duplicados)
            for semestre in semestres_a_agregar:
                cursor.execute("INSERT IGNORE INTO carrera_semestres (carrera_id, semestre) VALUES (%s, %s)", 
                              (carrera_id, semestre))
            
            # ACTUALIZACIÓN CORREGIDA: Manejo inteligente de salas
            # Primero obtenemos las salas actuales
            cursor.execute("SELECT sala_id FROM carrera_salas WHERE carrera_id = %s", (carrera_id,))
            salas_actuales = [row['sala_id'] for row in cursor.fetchall()]
            
            # Identificar salas a eliminar y a agregar
            salas_a_eliminar = [sala_id for sala_id in salas_actuales if sala_id not in salas_seleccionadas]
            salas_a_agregar = [sala_id for sala_id in salas_seleccionadas if sala_id not in salas_actuales]
            
            # Eliminar salas que ya no están seleccionadas
            if salas_a_eliminar:
                placeholders = ','.join(['%s'] * len(salas_a_eliminar))
                query_eliminar = f"DELETE FROM carrera_salas WHERE carrera_id = %s AND sala_id IN ({placeholders})"
                cursor.execute(query_eliminar, (carrera_id, *salas_a_eliminar))
            
            # Agregar nuevas salas (usando INSERT IGNORE para evitar duplicados)
            for sala_id in salas_a_agregar:
                cursor.execute("INSERT IGNORE INTO carrera_salas (carrera_id, sala_id) VALUES (%s, %s)", 
                              (carrera_id, sala_id))
            
            connection.commit()
            return carrera_id
            
        except Error as e:
            logging.error(f"Error guardando carrera: {e}")
            connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def guardar_sala(self, sala_data, sala_id=None):
        """Guarda una sala (nueva o existente)"""
        connection = self.db.get_connection()
        if not connection:
            return None
        
        cursor = None
        try:
            cursor = connection.cursor()
            
            if sala_id:
                # Actualizar sala existente
                query = "UPDATE salas SET nombre = %s, capacidad = %s, tipo = %s WHERE id = %s"
                cursor.execute(query, (*sala_data, sala_id))
            else:
                # Insertar nueva sala
                query = "INSERT INTO salas (nombre, capacidad, tipo) VALUES (%s, %s, %s)"
                cursor.execute(query, sala_data)
                sala_id = cursor.lastrowid
            
            connection.commit()
            return sala_id
            
        except Error as e:
            logging.error(f"Error guardando sala: {e}")
            connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def eliminar_sala(self, sala_id):
        """Elimina una sala por su id"""
        query = "DELETE FROM salas WHERE id = %s"
        return self.db.execute_query(query, (sala_id,))

    def eliminar_carrera(self, carrera_id):
        """Elimina una carrera por su id."""
        query = "DELETE FROM carreras WHERE id = %s"
        return self.db.execute_query(query, (carrera_id,))

    def eliminar_docente(self, docente_id):
        """Elimina un docente por su id."""
        query = "DELETE FROM docentes WHERE id = %s"
        return self.db.execute_query(query, (docente_id,))

    def obtener_docente_por_id(self, docente_id):
        """Obtiene un docente por su ID"""
        query = "SELECT * FROM docentes WHERE id = %s"
        result = self.db.execute_query(query, (docente_id,), fetch=True)
        return result[0] if result else None

    def obtener_modulos_docente(self, docente_id):
        """Obtiene todos los módulos asignados a un docente específico"""
        query = """SELECT m.*, c.nombre as carrera_nombre, s.nombre as sala_nombre 
               FROM modulos m 
               LEFT JOIN carreras c ON m.carrera_id = c.id 
               LEFT JOIN salas s ON m.sala_id = s.id
               WHERE m.docente_id = %s"""
        return self.db.execute_query(query, (docente_id,), fetch=True)

    def obtener_horarios_modulo(self, modulo_id):
        """Obtiene los horarios asignados a un módulo"""
        query = "SELECT * FROM modulo_horarios WHERE modulo_id = %s"
        return self.db.execute_query(query, (modulo_id,), fetch=True)

    def obtener_disponibilidad_docente(self, docente_id):
        """Obtiene la disponibilidad de un docente"""
        # Esta tabla 'disponibilidad_docentes' debe existir o crearse. 
        # Asumiremos una estructura simple: docente_id, dia, hora, estado (disponible/no)
        # Si no existe, retornamos un dict vacío por ahora para no romper la app
        try:
            query = "SELECT * FROM disponibilidad_docentes WHERE docente_id = %s"
            resultados = self.db.execute_query(query, (docente_id,), fetch=True)
            
            # Convertir a estructura de diccionario anidado: {dia: {hora: estado}}
            disponibilidad = {}
            if resultados:
                for fila in resultados:
                    dia = fila['dia']
                    hora = fila['hora']
                    estado = fila['estado']
                    if dia not in disponibilidad:
                        disponibilidad[dia] = {}
                    disponibilidad[dia][hora] = (estado == 'disponible')
            return disponibilidad
        except Exception:
            return {}

    def guardar_disponibilidad_docente(self, docente_id, disponibilidad_dict):
        """Guarda la disponibilidad de un docente
        Args:
            docente_id: ID del docente
            disponibilidad_dict: Diccionario en formato {dia: {hora: bool}}
        """
        connection = self.db.get_connection()
        if not connection:
            return False
        
        cursor = None
        try:
            cursor = connection.cursor()
            
            # Primero eliminar la disponibilidad existente
            cursor.execute("DELETE FROM disponibilidad_docentes WHERE docente_id = %s", (docente_id,))
            
            # Insertar la nueva disponibilidad
            for dia, horas_dict in disponibilidad_dict.items():
                for hora, disponible in horas_dict.items():
                    # Convertir booleano a string para la columna 'estado'
                    estado = 'disponible' if disponible else 'no_disponible'
                    cursor.execute(
                        "INSERT INTO disponibilidad_docentes (docente_id, dia, hora, estado) VALUES (%s, %s, %s, %s)",
                        (docente_id, dia, hora, estado)
                    )
            
            connection.commit()
            return True
            
        except Error as e:
            logging.error(f"Error guardando disponibilidad: {e}")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def validar_conflicto_horario_docente(self, docente_id, nuevos_horarios, modulo_id_actual=None):
        """
        Valida que no haya conflictos de horario para un docente.
        Retorna (tiene_conflicto, mensaje_error, modulo_conflicto)
        """
        if not docente_id or not nuevos_horarios:
            return (False, "", None)
        
        # Obtener módulos del docente
        query = """
            SELECT m.id, m.nombre, m.codigo
            FROM modulos m
            WHERE m.docente_id = %s
        """
        if modulo_id_actual:
            query += " AND m.id != %s"
            modulos = self.db.execute_query(query, (docente_id, modulo_id_actual), fetch=True)
        else:
            modulos = self.db.execute_query(query, (docente_id,), fetch=True)
        
        if not modulos:
            return (False, "", None)
        
        # Helper para convertir hora a minutos
        def hora_a_minutos(hora_str):
            if hasattr(hora_str, 'total_seconds'):
                return int(hora_str.total_seconds() // 60)
            partes = str(hora_str).split(':')[:2]
            return int(partes[0]) * 60 + int(partes[1])
        
        # Helper para verificar solapamiento
        def se_solapan(dia1, inicio1, fin1, dia2, inicio2, fin2):
            if dia1.upper() != dia2.upper():
                return False
            
            inicio1_min = hora_a_minutos(inicio1)
            fin1_min = hora_a_minutos(fin1)
            inicio2_min = hora_a_minutos(inicio2)
            fin2_min = hora_a_minutos(fin2)
            
            # Verificar solapamiento
            return not (fin1_min <= inicio2_min or fin2_min <= inicio1_min)
        
        # Verificar cada nuevo horario contra horarios existentes
        for nuevo_h in nuevos_horarios:
            nuevo_dia = nuevo_h['dia'] if isinstance(nuevo_h, dict) else nuevo_h[0]
            nuevo_inicio = nuevo_h['hora_inicio'] if isinstance(nuevo_h, dict) else nuevo_h[1]
            nuevo_fin = nuevo_h['hora_fin'] if isinstance(nuevo_h, dict) else nuevo_h[2]
            
            for modulo in modulos:
                horarios_existentes = self.obtener_horarios_modulo(modulo['id'])
                if not horarios_existentes:
                    continue
                
                for h_exist in horarios_existentes:
                    if se_solapan(nuevo_dia, nuevo_inicio, nuevo_fin,
                                h_exist['dia'], h_exist['hora_inicio'], h_exist['hora_fin']):
                        mensaje = f"Conflicto de horario: El docente ya dicta '{modulo['nombre']}' ({modulo['codigo']}) el {h_exist['dia']} a las {h_exist['hora_inicio']}"
                        return (True, mensaje, modulo)
        
        return (False, "", None)

    def obtener_horarios_ocupados_docente(self, docente_id, semestre_actual=None):
        """
        Obtiene todos los horarios ocupados por módulos asignados a un docente.
        Si se proporciona semestre_actual, solo retorna módulos del mismo grupo (par/impar).
        Retorna una lista de diccionarios con dia, hora_inicio, hora_fin y nombre del módulo.
        """
        query = """
            SELECT mh.dia, mh.hora_inicio, mh.hora_fin, m.nombre as modulo_nombre, 
                   m.codigo as modulo_codigo, m.id as modulo_id, m.semestre
            FROM modulo_horarios mh
            JOIN modulos m ON mh.modulo_id = m.id
            WHERE m.docente_id = %s
        """
        params = [docente_id]
        
        # Filtrar por grupo de semestre (par/impar) si se proporciona
        if semestre_actual is not None:
            query += " AND MOD(m.semestre, 2) = %s"
            params.append(semestre_actual % 2)
        
        return self.db.execute_query(query, tuple(params), fetch=True)

    def obtener_horarios_ocupados_sala(self, sala_id, semestre_actual=None):
        """
        Obtiene todos los horarios ocupados por módulos asignados a una sala.
        Si se proporciona semestre_actual, solo retorna módulos del mismo grupo (par/impar).
        Retorna una lista de diccionarios con dia, hora_inicio, hora_fin y nombre del módulo.
        """
        query = """
            SELECT mh.dia, mh.hora_inicio, mh.hora_fin, m.nombre as modulo_nombre, 
                   m.codigo as modulo_codigo, m.id as modulo_id, m.semestre
            FROM modulo_horarios mh
            JOIN modulos m ON mh.modulo_id = m.id
            WHERE m.sala_id = %s
        """
        params = [sala_id]
        
        # Filtrar por grupo de semestre (par/impar) si se proporciona
        if semestre_actual is not None:
            query += " AND MOD(m.semestre, 2) = %s"
            params.append(semestre_actual % 2)
        
        return self.db.execute_query(query, tuple(params), fetch=True)

    def validar_conflicto_sala(self, sala_id, nuevos_horarios, modulo_id_actual=None):
        """
        Valida que no haya conflictos de sala.
        Retorna (tiene_conflicto, mensaje_error, modulo_conflicto)
        """
        if not sala_id or not nuevos_horarios:
            return (False, "", None)
        
        # Obtener módulos que usan esta sala
        query = """
            SELECT m.id, m.nombre, m.codigo
            FROM modulos m
            WHERE m.sala_id = %s
        """
        if modulo_id_actual:
            query += " AND m.id != %s"
            modulos = self.db.execute_query(query, (sala_id, modulo_id_actual), fetch=True)
        else:
            modulos = self.db.execute_query(query, (sala_id,), fetch=True)
        
        if not modulos:
            return (False, "", None)
        
        # Helper para convertir hora a minutos
        def hora_a_minutos(hora_str):
            if hasattr(hora_str, 'total_seconds'):
                return int(hora_str.total_seconds() // 60)
            partes = str(hora_str).split(':')[:2]
            return int(partes[0]) * 60 + int(partes[1])
        
        # Helper para verificar solapamiento
        def se_solapan(dia1, inicio1, fin1, dia2, inicio2, fin2):
            if dia1.upper() != dia2.upper():
                return False
            
            inicio1_min = hora_a_minutos(inicio1)
            fin1_min = hora_a_minutos(fin1)
            inicio2_min = hora_a_minutos(inicio2)
            fin2_min = hora_a_minutos(fin2)
            
            return not (fin1_min <= inicio2_min or fin2_min <= inicio1_min)
        
        # Verificar cada nuevo horario contra horarios existentes
        for nuevo_h in nuevos_horarios:
            nuevo_dia = nuevo_h['dia'] if isinstance(nuevo_h, dict) else nuevo_h[0]
            nuevo_inicio = nuevo_h['hora_inicio'] if isinstance(nuevo_h, dict) else nuevo_h[1]
            nuevo_fin = nuevo_h['hora_fin'] if isinstance(nuevo_h, dict) else nuevo_h[2]
            
            for modulo in modulos:
                horarios_existentes = self.obtener_horarios_modulo(modulo['id'])
                if not horarios_existentes:
                    continue
                
                for h_exist in horarios_existentes:
                    if se_solapan(nuevo_dia, nuevo_inicio, nuevo_fin,
                                h_exist['dia'], h_exist['hora_inicio'], h_exist['hora_fin']):
                        mensaje = f"Conflicto de sala: La sala ya está ocupada por '{modulo['nombre']}' ({modulo['codigo']}) el {h_exist['dia']} a las {h_exist['hora_inicio']}"
                        return (True, mensaje, modulo)
        
        return (False, "", None)

    def validar_conflicto_semestre_par_impar(self, carrera_id, semestre, nuevos_horarios, modulo_id_actual=None):
        """
        Valida que no haya topes de horario entre semestres pares e impares de la misma carrera.
        Si el semestre actual es impar (1, 3, 5...), no debe topar con módulos de semestres pares (2, 4, 6...).
        Si el semestre actual es par, no debe topar con módulos de semestres impares.
        """
        if not carrera_id or not semestre or not nuevos_horarios:
            return (False, "", None)
        
        es_impar = (int(semestre) % 2 != 0)
        
        # Determinar qué semestres verificar (el grupo opuesto)
        # Si soy impar, busco conflictos con pares. Si soy par, busco conflictos con impares.
        # La consulta SQL filtrará por (semestre % 2 = 0) o (semestre % 2 != 0)
        
        operador_mod = "=" if es_impar else "!="
        
        query = f"""
            SELECT m.id, m.nombre, m.codigo, m.semestre
            FROM modulos m
            WHERE m.carrera_id = %s
            AND m.semestre %% 2 {operador_mod} 0
        """
        
        params = [carrera_id]
        
        if modulo_id_actual:
            query += " AND m.id != %s"
            params.append(modulo_id_actual)
            
        modulos_opuestos = self.db.execute_query(query, tuple(params), fetch=True)
        
        if not modulos_opuestos:
            return (False, "", None)
            
        # Helper para convertir hora a minutos (reutilizado)
        def hora_a_minutos(hora_str):
            if hasattr(hora_str, 'total_seconds'):
                return int(hora_str.total_seconds() // 60)
            partes = str(hora_str).split(':')[:2]
            return int(partes[0]) * 60 + int(partes[1])
        
        # Helper para verificar solapamiento (reutilizado)
        def se_solapan(dia1, inicio1, fin1, dia2, inicio2, fin2):
            if dia1.upper() != dia2.upper():
                return False
            
            inicio1_min = hora_a_minutos(inicio1)
            fin1_min = hora_a_minutos(fin1)
            inicio2_min = hora_a_minutos(inicio2)
            fin2_min = hora_a_minutos(fin2)
            
            return not (fin1_min <= inicio2_min or fin2_min <= inicio1_min)
            
        # Verificar cada nuevo horario contra horarios de módulos del grupo opuesto
        for nuevo_h in nuevos_horarios:
            nuevo_dia = nuevo_h['dia'] if isinstance(nuevo_h, dict) else nuevo_h[0]
            nuevo_inicio = nuevo_h['hora_inicio'] if isinstance(nuevo_h, dict) else nuevo_h[1]
            nuevo_fin = nuevo_h['hora_fin'] if isinstance(nuevo_h, dict) else nuevo_h[2]
            
            for modulo in modulos_opuestos:
                horarios_existentes = self.obtener_horarios_modulo(modulo['id'])
                if not horarios_existentes:
                    continue
                
                for h_exist in horarios_existentes:
                    if se_solapan(nuevo_dia, nuevo_inicio, nuevo_fin,
                                h_exist['dia'], h_exist['hora_inicio'], h_exist['hora_fin']):
                        tipo_semestre_opuesto = "par" if es_impar else "impar"
                        mensaje = f"Conflicto de Semestre: El módulo '{modulo['nombre']}' es del semestre {modulo['semestre']} ({tipo_semestre_opuesto}) y tiene tope de horario el {h_exist['dia']} a las {h_exist['hora_inicio']}."
                        return (True, mensaje, modulo)
        
        return (False, "", None)

# Instancia global
db_manager = SistemaDAO()