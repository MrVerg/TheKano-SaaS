# data.py
def generar_disponibilidad_base():
    """Genera una estructura de disponibilidad base con todos los horarios disponibles"""
    dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
    horas = ["8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
    
    disponibilidad = {}
    for dia in dias:
        disponibilidad[dia] = {}
        for hora in horas:
            disponibilidad[dia][hora] = True
    return disponibilidad

def cargar_datos():
    """Carga todos los datos del sistema"""
    datos = {
        "usuarios": {
            "admin@ceduc.cl": {"password": "admin", "tipo": "administrador"},
            "ebarahona@ceduc.cl": {"password": "ceduc", "tipo": "docente"}
        },
        
        "salas": [
            {"nombre": "Sala 01", "capacidad": 30, "horas_disponibles": 40, "horas_ocupadas": 25},
            {"nombre": "Sala 02", "capacidad": 25, "horas_disponibles": 40, "horas_ocupadas": 3},
            {"nombre": "Laboratorio 01", "capacidad": 20, "horas_disponibles": 40, "horas_ocupadas": 25},
            {"nombre": "Laboratorio 02", "capacidad": 15, "horas_disponibles": 40, "horas_ocupadas": 25},
            {"nombre": "Laboratorio 03", "capacidad": 20, "horas_disponibles": 40, "horas_ocupadas": 0}
        ],
        
        "docentes": [
            {"nombre": "Marcelo Oporto", "titulo": "Analista Programador", "contrato": "Planta", 
             "horas_contratadas": 40, "horas_asignadas": 25, "email": "moporto@ceduc.cl",
             "evaluacion": 4.2, "disponibilidad": generar_disponibilidad_base()},
            {"nombre": "Patricio Díaz", "titulo": "Prof. Matemáticas", "contrato": "Parcial", 
             "horas_contratadas": 3, "horas_asignadas": 3, "email": "pdiaz@ceduc.cl",
             "evaluacion": 4.5, "disponibilidad": generar_disponibilidad_base()},
            {"nombre": "Efraín Barahona", "titulo": "Ing. Informático", "contrato": "Planta", 
             "horas_contratadas": 40, "horas_asignadas": 25, "email": "ebarahona@ceduc.cl",
             "evaluacion": 4.0, "disponibilidad": generar_disponibilidad_base()}
        ],
        
        "carreras": [
            {
                "nombre": "COMPUTACIÓN E INFORMÁTICA", 
                "jornada": "Diurna", 
                "semestres": ["I", "III"], 
                "salas": ["Sala 01", "Sala 02"], 
                "alumnos": 100,
                "modulos": [
                    {"nombre": "DESARROLLO DE APLICACIONES MÓVILES", "codigo": "CP-430", "horas_teoricas": 1, 
                     "horas_practicas": 3, "docente": "Marcelo Oporto", "sala": "CP-430", "alumnos": 20,
                     "semestre": "I",
                     "horario": [
                         {"dia": "LUNES", "hora_inicio": "8:00", "hora_fin": "10:15"},
                         {"dia": "MARTES", "hora_inicio": "10:30", "hora_fin": "12:45"},
                         {"dia": "MIERCOLES", "hora_inicio": "14:00", "hora_fin": "16:15"}
                     ]},
                    {"nombre": "PROGRAMACIÓN ORIENTADA A OBJETOS I", "codigo": "CP-430", "horas_teoricas": 2, 
                     "horas_practicas": 2, "docente": "Marcelo Oporto", "sala": "CP-430", "alumnos": 20,
                     "semestre": "I",
                     "horario": [
                         {"dia": "JUEVES", "hora_inicio": "8:00", "hora_fin": "10:15"},
                         {"dia": "VIERNES", "hora_inicio": "10:30", "hora_fin": "12:45"}
                     ]},
                    {"nombre": "DESARROLLO DE APLICACIONES WEB", "codigo": "CP-410", "horas_teoricas": 2, 
                     "horas_practicas": 3, "docente": "Marcelo Oporto", "sala": "Laboratorio 02", "alumnos": 22,
                     "semestre": "III",
                     "horario": [
                         {"dia": "LUNES", "hora_inicio": "14:00", "hora_fin": "16:15"},
                         {"dia": "JUEVES", "hora_inicio": "10:30", "hora_fin": "12:45"}
                     ]}
                ]
            },
            {
                "nombre": "ADMINISTRACIÓN PÚBLICA", 
                "jornada": "Vespertina", 
                "semestres": ["II", "IV"], 
                "salas": ["Sala 01"], 
                "alumnos": 50,
                "modulos": [
                    {"nombre": "MATEMÁTICAS APLICADAS II", "codigo": "CP-430", "horas_teoricas": 1, 
                     "horas_practicas": 2, "docente": "Patricio Díaz", "sala": "Sala 01", "alumnos": 20,
                     "semestre": "II",
                     "horario": [
                         {"dia": "MARTES", "hora_inicio": "8:00", "hora_fin": "10:15"},
                         {"dia": "JUEVES", "hora_inicio": "14:00", "hora_fin": "16:15"}
                     ]}
                ]
            },
            {
                "nombre": "ELECTRICIDAD", 
                "jornada": "Diurna", 
                "semestres": ["I", "II", "III", "IV"], 
                "salas": ["Laboratorio 01"], 
                "alumnos": 30,
                "modulos": [
                    {"nombre": "CONFIGURACIÓN Y PUESTA EN MARCHA DE REDES LAN", "codigo": "CP-110", "horas_teoricas": 1, 
                     "horas_practicas": 2, "docente": "Efraín Barahona", "sala": "CP-110", "alumnos": 15,
                     "semestre": "I",
                     "horario": [
                         {"dia": "LUNES", "hora_inicio": "10:30", "hora_fin": "12:45"},
                         {"dia": "MIERCOLES", "hora_inicio": "8:00", "hora_fin": "10:15"}
                     ]}
                ]
            },
            {
                "nombre": "MAQUINARIA PESADA", 
                "jornada": "Vespertina", 
                "semestres": ["I", "III"], 
                "salas": ["Laboratorio 02"], 
                "alumnos": 25,
                "modulos": [
                    {"nombre": "DESARROLLO DE APLICACIONES DE ESCRITORIO", "codigo": "CP-420", "horas_teoricas": 2, 
                     "horas_practicas": 3, "docente": "Efraín Barahona", "sala": "Laboratorio 01", "alumnos": 18,
                     "semestre": "III",
                     "horario": [
                         {"dia": "MARTES", "hora_inicio": "14:00", "hora_fin": "16:15"},
                         {"dia": "VIERNES", "hora_inicio": "8:00", "hora_fin": "10:15"}
                     ]}
                ]
            }
        ]
    }
    
    return datos