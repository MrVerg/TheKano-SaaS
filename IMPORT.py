import pandas as pd

# 1. Datos de DOCENTES
docentes_data = [
    {
        "id": 1,
        "nombre": "Cristobal Quintana Gonzalez",
        "titulo": "Abogado",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.89
    },
    {
        "id": 2,
        "nombre": "Gary Guerrero Barra",
        "titulo": "Administrador Público / Magister",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 4.0
    },
    {
        "id": 3,
        "nombre": "Roberto Leal Cofré",
        "titulo": "Ingeniero en Comercialización Int.",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.94
    },
    {
        "id": 4,
        "nombre": "Nelson Salazar Matamala",
        "titulo": "Profesor en Educación Diferencial",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.76
    },
    {
        "id": 5,
        "nombre": "Katherine Medina Suazo",
        "titulo": "Ingeniero en Prevención",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.9
    },
    {
        "id": 6,
        "nombre": "Natalia Vera Leal",
        "titulo": "Ingeniero Civil Industrial",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.71
    },
    {
        "id": 7,
        "nombre": "Oscar Muñoz Arriagada",
        "titulo": "Administrador Público",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.95
    },
    {
        "id": 8,
        "nombre": "Patricio Diaz Antinao",
        "titulo": "Profesor de Matemáticas",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.85
    },
    {
        "id": 9,
        "nombre": "Manuel Valderas",
        "titulo": "Contador Auditor",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.77
    },
    {
        "id": 10,
        "nombre": "Efrain Barahona Barahona",
        "titulo": "Ingeniero Informático",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.84
    },
    {
        "id": 11,
        "nombre": "Cristian Rodriguez Lobos",
        "titulo": "Diplomado Gestión Municipal",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.9
    },
    {
        "id": 12,
        "nombre": "Marcelo Oporto Toledo",
        "titulo": "Analista Programador",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.19
    },
    {
        "id": 13,
        "nombre": "Francisco Rodriguez Araneda",
        "titulo": "Constructor Civil",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.93
    },
    {
        "id": 14,
        "nombre": "Marcelo Rios Alarcón",
        "titulo": "Constructor Civil",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 0
    },
    {
        "id": 15,
        "nombre": "Cesar Quintana Gonzalez",
        "titulo": "Psicologo",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.91
    },
    {
        "id": 16,
        "nombre": "Martina Saldivia Muñoz",
        "titulo": "Profesora de Inglés",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.81
    },
    {
        "id": 17,
        "nombre": "Juan Larenas Hidalgo",
        "titulo": "Psicólogo",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.93
    },
    {
        "id": 18,
        "nombre": "Julia San Martin Reyes",
        "titulo": "Ingeniera Electricidad",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 0
    },
    {
        "id": 19,
        "nombre": "Diego Faúndez Oporto",
        "titulo": "TNS Electricidad",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.98
    },
    {
        "id": 20,
        "nombre": "Nelson Lagos Fuentes",
        "titulo": "TNS Electrónica",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.75
    },
    {
        "id": 21,
        "nombre": "Carlos Monsálvez Ramírez",
        "titulo": "Ingeniero Ejecución Electrónica",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.91
    },
    {
        "id": 22,
        "nombre": "Scarlette Muñoz Fuentes",
        "titulo": "Psicologa",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.9
    },
    {
        "id": 23,
        "nombre": "Ingerworld Rivera Rivera",
        "titulo": "Educadora de Párvulos",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.7
    },
    {
        "id": 24,
        "nombre": "Veronica Astudillo Vera",
        "titulo": "Enfermera",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.8
    },
    {
        "id": 25,
        "nombre": "Natacha Miranda Flores",
        "titulo": "TNS Educación Parvularia",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 0
    },
    {
        "id": 26,
        "nombre": "Daniela Montecino Lara",
        "titulo": "Educadora Diferencial",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.9
    },
    {
        "id": 27,
        "nombre": "Camila Gonzalez Ortiz",
        "titulo": "Enfermera",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 0
    },
    {
        "id": 28,
        "nombre": "Michael Peña Matamala",
        "titulo": "Tecnólogo Informática Biomédica",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.95
    },
    {
        "id": 29,
        "nombre": "Marcelo Luarte González",
        "titulo": "Enfermero",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.6
    },
    {
        "id": 30,
        "nombre": "Glenda Bahamondes Vidal",
        "titulo": "Matrona",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.85
    },
    {
        "id": 31,
        "nombre": "Victor Curinao Vidal",
        "titulo": "TNS Maquinaria Pesada",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.6
    },
    {
        "id": 32,
        "nombre": "Francisco Rivas Neira",
        "titulo": "Técnico Mecánica Automotriz",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.9
    },
    {
        "id": 33,
        "nombre": "Gerald Santa María Salazar",
        "titulo": "TNS Maquinaria Pesada",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.7
    },
    {
        "id": 34,
        "nombre": "César Palma Márquez",
        "titulo": "Técnico Electromecánico",
        "contrato": "Honorario",
        "horas_contratadas": 0,
        "email": "pendiente@ceduc.cl",
        "evaluacion": 3.7
    }
]

# 2. Datos de CARRERAS
carreras_data = [
    {
        "id": 1,
        "nombre": "Administración Mención Gestión Pública",
        "jornada": "Diurna",
        "alumnos_proyectados": 10,
        "semestres": 4,
        "salas_ids": "1"
    },
    {
        "id": 2,
        "nombre": "Administración Mención Gestión Pública",
        "jornada": "Vespertina",
        "alumnos_proyectados": 20,
        "semestres": 4,
        "salas_ids": "2"
    },
    {
        "id": 3,
        "nombre": "TNS en Construcción",
        "jornada": "Diurna",
        "alumnos_proyectados": 18,
        "semestres": 4,
        "salas_ids": "3"
    },
    {
        "id": 4,
        "nombre": "Computación e Informática Mención Programación",
        "jornada": "Diurna",
        "alumnos_proyectados": 20,
        "semestres": 4,
        "salas_ids": "4"
    },
    {
        "id": 5,
        "nombre": "Electricidad y Electrónica Industrial",
        "jornada": "Diurna",
        "alumnos_proyectados": 25,
        "semestres": 4,
        "salas_ids": "5"
    },
    {
        "id": 6,
        "nombre": "TNS en Educación de Párvulos",
        "jornada": "Diurna",
        "alumnos_proyectados": 43,
        "semestres": 4,
        "salas_ids": "6"
    },
    {
        "id": 7,
        "nombre": "TNS en Educación de Párvulos",
        "jornada": "Vespertina",
        "alumnos_proyectados": 11,
        "semestres": 4,
        "salas_ids": "6"
    },
    {
        "id": 8,
        "nombre": "Enfermería y Telemedicina",
        "jornada": "Diurna",
        "alumnos_proyectados": 50,
        "semestres": 4,
        "salas_ids": "7"
    },
    {
        "id": 9,
        "nombre": "Intervención y Rehabilitación Psicosocial",
        "jornada": "Diurna",
        "alumnos_proyectados": 14,
        "semestres": 4,
        "salas_ids": "8"
    },
    {
        "id": 10,
        "nombre": "Maquinaria Pesada",
        "jornada": "Diurna",
        "alumnos_proyectados": 35,
        "semestres": 4,
        "salas_ids": "9"
    },
    {
        "id": 11,
        "nombre": "Mecánica de Equipo Pesado",
        "jornada": "Diurna",
        "alumnos_proyectados": 30,
        "semestres": 4,
        "salas_ids": "10"
    }
]

# 3. Datos de MÓDULOS
modulos_data = [
    {
        "id": 1,
        "nombre": "Gestión de Personas en el Sector Privado",
        "codigo": "AP-310-2",
        "horas_teoricas": 1,
        "horas_practicas": 2,
        "alumnos_proyectados": 10,
        "semestre": 4,
        "carrera_id": 1,
        "docente_id": 1,
        "sala_id": 1
    },
    {
        "id": 2,
        "nombre": "Administración Pública III",
        "codigo": "AP-120-4",
        "horas_teoricas": 2,
        "horas_practicas": 2,
        "alumnos_proyectados": 10,
        "semestre": 4,
        "carrera_id": 1,
        "docente_id": 2,
        "sala_id": 1
    },
    {
        "id": 3,
        "nombre": "Marketing de productos y servicios",
        "codigo": "AP-410-0",
        "horas_teoricas": 1,
        "horas_practicas": 3,
        "alumnos_proyectados": 10,
        "semestre": 4,
        "carrera_id": 1,
        "docente_id": 3,
        "sala_id": 1
    },
    {
        "id": 4,
        "nombre": "Ética",
        "codigo": "AP-430-0",
        "horas_teoricas": 1,
        "horas_practicas": 1,
        "alumnos_proyectados": 10,
        "semestre": 4,
        "carrera_id": 1,
        "docente_id": 4,
        "sala_id": 1
    },
    {
        "id": 5,
        "nombre": "Salud Ocupacional",
        "codigo": "AP-420-0",
        "horas_teoricas": 1,
        "horas_practicas": 1,
        "alumnos_proyectados": 10,
        "semestre": 4,
        "carrera_id": 1,
        "docente_id": 5,
        "sala_id": 1
    },
    {
        "id": 6,
        "nombre": "Taller de Emprendimiento",
        "codigo": "AP-440-0",
        "horas_teoricas": 0,
        "horas_practicas": 3,
        "alumnos_proyectados": 10,
        "semestre": 4,
        "carrera_id": 1,
        "docente_id": 6,
        "sala_id": 1
    },
    {
        "id": 7,
        "nombre": "Legislación Laboral",
        "codigo": "AP-210-0",
        "horas_teoricas": 2,
        "horas_practicas": 2,
        "alumnos_proyectados": 20,
        "semestre": 2,
        "carrera_id": 2,
        "docente_id": 1,
        "sala_id": 2
    },
    {
        "id": 8,
        "nombre": "Administración I",
        "codigo": "AP-120-2",
        "horas_teoricas": 2,
        "horas_practicas": 2,
        "alumnos_proyectados": 20,
        "semestre": 2,
        "carrera_id": 2,
        "docente_id": 7,
        "sala_id": 2
    },
    {
        "id": 9,
        "nombre": "Introducción a la Micro y Macroeconomía",
        "codigo": "AP-220-0",
        "horas_teoricas": 2,
        "horas_practicas": 2,
        "alumnos_proyectados": 20,
        "semestre": 2,
        "carrera_id": 2,
        "docente_id": 8,
        "sala_id": 2
    },
    {
        "id": 10,
        "nombre": "Presupuesto y Contabilidad Gubernamental",
        "codigo": "AP-140-2",
        "horas_teoricas": 2,
        "horas_practicas": 2,
        "alumnos_proyectados": 20,
        "semestre": 2,
        "carrera_id": 2,
        "docente_id": 9,
        "sala_id": 2
    },
    {
        "id": 11,
        "nombre": "Herramientas Digitales para la Gestión I",
        "codigo": "AP-230-1",
        "horas_teoricas": 0,
        "horas_practicas": 3,
        "alumnos_proyectados": 20,
        "semestre": 2,
        "carrera_id": 2,
        "docente_id": 10,
        "sala_id": 2
    },
    {
        "id": 12,
        "nombre": "Documentación Administrativa y Comercial",
        "codigo": "AP-240-0",
        "horas_teoricas": 0,
        "horas_practicas": 3,
        "alumnos_proyectados": 20,
        "semestre": 2,
        "carrera_id": 2,
        "docente_id": 11,
        "sala_id": 2
    },
    {
        "id": 13,
        "nombre": "Taller de Proyecto y Emprendimiento I",
        "codigo": "AP-250-1",
        "horas_teoricas": 0,
        "horas_practicas": 2,
        "alumnos_proyectados": 20,
        "semestre": 2,
        "carrera_id": 2,
        "docente_id": 12,
        "sala_id": 2
    },
    {
        "id": 14,
        "nombre": "Taller de Albañilería",
        "codigo": "CC-311-3",
        "horas_teoricas": 1,
        "horas_practicas": 4,
        "alumnos_proyectados": 18,
        "semestre": 4,
        "carrera_id": 3,
        "docente_id": 13,
        "sala_id": 3
    },
    {
        "id": 15,
        "nombre": "Presupuesto",
        "codigo": "CC-321-2",
        "horas_teoricas": 1,
        "horas_practicas": 2,
        "alumnos_proyectados": 18,
        "semestre": 4,
        "carrera_id": 3,
        "docente_id": 13,
        "sala_id": 3
    },
    {
        "id": 16,
        "nombre": "Taller de Terminaciones",
        "codigo": "CC-411-0",
        "horas_teoricas": 1,
        "horas_practicas": 4,
        "alumnos_proyectados": 18,
        "semestre": 4,
        "carrera_id": 3,
        "docente_id": 13,
        "sala_id": 3
    },
    {
        "id": 17,
        "nombre": "Planificación de Obras de Edificación",
        "codigo": "CC-421-0",
        "horas_teoricas": 1,
        "horas_practicas": 3,
        "alumnos_proyectados": 18,
        "semestre": 4,
        "carrera_id": 3,
        "docente_id": 14,
        "sala_id": 3
    },
    {
        "id": 18,
        "nombre": "Ética Profesional",
        "codigo": "CC-431-2",
        "horas_teoricas": 2,
        "horas_practicas": 0,
        "alumnos_proyectados": 18,
        "semestre": 4,
        "carrera_id": 3,
        "docente_id": 15,
        "sala_id": 3
    },
    {
        "id": 19,
        "nombre": "Psicología Personal y Laboral",
        "codigo": "CC 420-2",
        "horas_teoricas": 1,
        "horas_practicas": 1,
        "alumnos_proyectados": 18,
        "semestre": 4,
        "carrera_id": 3,
        "docente_id": 15,
        "sala_id": 3
    },
    {
        "id": 20,
        "nombre": "Innovación y Emprendimiento IV",
        "codigo": "CC-171-4",
        "horas_teoricas": 1,
        "horas_practicas": 2,
        "alumnos_proyectados": 18,
        "semestre": 4,
        "carrera_id": 3,
        "docente_id": 11,
        "sala_id": 3
    },
    {
        "id": 21,
        "nombre": "Configuración y Puesta en marcha de Redes LAN",
        "codigo": "CP-110-2",
        "horas_teoricas": 1,
        "horas_practicas": 2,
        "alumnos_proyectados": 20,
        "semestre": 2,
        "carrera_id": 4,
        "docente_id": 10,
        "sala_id": 4
    },
    {
        "id": 22,
        "nombre": "Matemáticas Aplicadas II",
        "codigo": "CP-120-2",
        "horas_teoricas": 2,
        "horas_practicas": 1,
        "alumnos_proyectados": 20,
        "semestre": 2,
        "carrera_id": 4,
        "docente_id": 8,
        "sala_id": 4
    },
    {
        "id": 23,
        "nombre": "Programación Orientada a Objetos I",
        "codigo": "CP-130-2",
        "horas_teoricas": 2,
        "horas_practicas": 2,
        "alumnos_proyectados": 18,
        "semestre": 2,
        "carrera_id": 4,
        "docente_id": 12,
        "sala_id": 4
    },
    {
        "id": 24,
        "nombre": "Sistemas Operativos I",
        "codigo": "CP-140-2",
        "horas_teoricas": 1,
        "horas_practicas": 2,
        "alumnos_proyectados": 20,
        "semestre": 2,
        "carrera_id": 4,
        "docente_id": 10,
        "sala_id": 4
    },
    {
        "id": 25,
        "nombre": "Inglés II",
        "codigo": "CP-170-2",
        "horas_teoricas": 1,
        "horas_practicas": 2,
        "alumnos_proyectados": 20,
        "semestre": 2,
        "carrera_id": 4,
        "docente_id": 16,
        "sala_id": 4
    },
    {
        "id": 26,
        "nombre": "Bases de Datos I",
        "codigo": "CP-210-1",
        "horas_teoricas": 2,
        "horas_practicas": 1,
        "alumnos_proyectados": 20,
        "semestre": 2,
        "carrera_id": 4,
        "docente_id": 10,
        "sala_id": 4
    },
    {
        "id": 27,
        "nombre": "Taller Práctico I",
        "codigo": "CP-220-1",
        "horas_teoricas": 0,
        "horas_practicas": 2,
        "alumnos_proyectados": 20,
        "semestre": 2,
        "carrera_id": 4,
        "docente_id": 3,
        "sala_id": 4
    },
    {
        "id": 28,
        "nombre": "Desarrollo de Aplicaciones Web",
        "codigo": "CP-410-0",
        "horas_teoricas": 1,
        "horas_practicas": 3,
        "alumnos_proyectados": 15,
        "semestre": 4,
        "carrera_id": 4,
        "docente_id": 12,
        "sala_id": 4
    },
    {
        "id": 29,
        "nombre": "Ética Profesional",
        "codigo": "CP-440-1",
        "horas_teoricas": 2,
        "horas_practicas": 0,
        "alumnos_proyectados": 22,
        "semestre": 4,
        "carrera_id": 4,
        "docente_id": 17,
        "sala_id": 4
    },
    {
        "id": 30,
        "nombre": "Tecnología y Control de Máquinas Eléctricas I",
        "codigo": "EI-201-1",
        "horas_teoricas": 1,
        "horas_practicas": 3,
        "alumnos_proyectados": 25,
        "semestre": 2,
        "carrera_id": 5,
        "docente_id": 18,
        "sala_id": 5
    },
    {
        "id": 31,
        "nombre": "Software de Diseño e Interpretación de Planos",
        "codigo": "EI-202-0",
        "horas_teoricas": 0,
        "horas_practicas": 4,
        "alumnos_proyectados": 25,
        "semestre": 2,
        "carrera_id": 5,
        "docente_id": 19,
        "sala_id": 5
    },
    {
        "id": 32,
        "nombre": "Electrotecnia II",
        "codigo": "EI-103-2",
        "horas_teoricas": 3,
        "horas_practicas": 2,
        "alumnos_proyectados": 25,
        "semestre": 2,
        "carrera_id": 5,
        "docente_id": 19,
        "sala_id": 5
    },
    {
        "id": 33,
        "nombre": "Instalaciones Eléctricas II",
        "codigo": "EI-104-2",
        "horas_teoricas": 1,
        "horas_practicas": 2,
        "alumnos_proyectados": 25,
        "semestre": 2,
        "carrera_id": 5,
        "docente_id": 20,
        "sala_id": 5
    },
    {
        "id": 34,
        "nombre": "Electronica Básica",
        "codigo": "EI-203-1",
        "horas_teoricas": 1,
        "horas_practicas": 2,
        "alumnos_proyectados": 25,
        "semestre": 2,
        "carrera_id": 5,
        "docente_id": 21,
        "sala_id": 5
    },
    {
        "id": 35,
        "nombre": "Aprendizaje y Desarrollo II",
        "codigo": "EP-111-2",
        "horas_teoricas": 2,
        "horas_practicas": 1,
        "alumnos_proyectados": 43,
        "semestre": 2,
        "carrera_id": 6,
        "docente_id": 22,
        "sala_id": 6
    },
    {
        "id": 36,
        "nombre": "Bases Curriculares para la Educ Parvularia I",
        "codigo": "EP-211-1",
        "horas_teoricas": 2,
        "horas_practicas": 3,
        "alumnos_proyectados": 43,
        "semestre": 2,
        "carrera_id": 6,
        "docente_id": 23,
        "sala_id": 6
    },
    {
        "id": 37,
        "nombre": "Salud y Cuidados de Párvulos",
        "codigo": "EP-231-0",
        "horas_teoricas": 2,
        "horas_practicas": 2,
        "alumnos_proyectados": 43,
        "semestre": 2,
        "carrera_id": 6,
        "docente_id": 24,
        "sala_id": 6
    },
    {
        "id": 38,
        "nombre": "Corporalidad y Movimiento",
        "codigo": "EP-241-0",
        "horas_teoricas": 1,
        "horas_practicas": 2,
        "alumnos_proyectados": 43,
        "semestre": 2,
        "carrera_id": 6,
        "docente_id": 25,
        "sala_id": 6
    },
    {
        "id": 39,
        "nombre": "Diversidad e Inclusión en la Educ Parvularia",
        "codigo": "EP-411-0",
        "horas_teoricas": 2,
        "horas_practicas": 2,
        "alumnos_proyectados": 33,
        "semestre": 4,
        "carrera_id": 6,
        "docente_id": 26,
        "sala_id": 6
    },
    {
        "id": 40,
        "nombre": "Prepráctica",
        "codigo": "EP-421-0",
        "horas_teoricas": 0,
        "horas_practicas": 5,
        "alumnos_proyectados": 33,
        "semestre": 4,
        "carrera_id": 6,
        "docente_id": 23,
        "sala_id": 6
    },
    {
        "id": 41,
        "nombre": "Cuidados Integrales de Enfermería",
        "codigo": "ET 212-0",
        "horas_teoricas": 6,
        "horas_practicas": 9,
        "alumnos_proyectados": 50,
        "semestre": 2,
        "carrera_id": 8,
        "docente_id": 27,
        "sala_id": 7
    },
    {
        "id": 42,
        "nombre": "Salud Familiar y Comunitaria",
        "codigo": "ET 152-2",
        "horas_teoricas": 1.5,
        "horas_practicas": 3,
        "alumnos_proyectados": 50,
        "semestre": 2,
        "carrera_id": 8,
        "docente_id": 24,
        "sala_id": 7
    },
    {
        "id": 43,
        "nombre": "Sistemas Informáticos en Salud",
        "codigo": "ET 232-0",
        "horas_teoricas": 2,
        "horas_practicas": 2,
        "alumnos_proyectados": 50,
        "semestre": 2,
        "carrera_id": 8,
        "docente_id": 28,
        "sala_id": 7
    },
    {
        "id": 44,
        "nombre": "Administración de Fármacos",
        "codigo": "ET 22-0",
        "horas_teoricas": 6,
        "horas_practicas": 9,
        "alumnos_proyectados": 50,
        "semestre": 2,
        "carrera_id": 8,
        "docente_id": 29,
        "sala_id": 7
    },
    {
        "id": 45,
        "nombre": "Psicología Social Comunitaria y Familiar",
        "codigo": "IR-210-0",
        "horas_teoricas": 3,
        "horas_practicas": 1,
        "alumnos_proyectados": 14,
        "semestre": 2,
        "carrera_id": 9,
        "docente_id": 15,
        "sala_id": 8
    },
    {
        "id": 46,
        "nombre": "Primeros Auxilios",
        "codigo": "IR-410-0",
        "horas_teoricas": 0,
        "horas_practicas": 3,
        "alumnos_proyectados": 29,
        "semestre": 4,
        "carrera_id": 9,
        "docente_id": 29,
        "sala_id": 8
    },
    {
        "id": 47,
        "nombre": "Motoniveladora Bulldozer y Cargador",
        "codigo": "MP-101-2",
        "horas_teoricas": 1,
        "horas_practicas": 3,
        "alumnos_proyectados": 35,
        "semestre": 2,
        "carrera_id": 10,
        "docente_id": 31,
        "sala_id": 9
    },
    {
        "id": 48,
        "nombre": "Operación de Maquinaria Pesada Media",
        "codigo": "MP-102-2",
        "horas_teoricas": 0,
        "horas_practicas": 12,
        "alumnos_proyectados": 35,
        "semestre": 2,
        "carrera_id": 10,
        "docente_id": 31,
        "sala_id": 9
    },
    {
        "id": 49,
        "nombre": "Motores de Combustión Interna",
        "codigo": "MP-201-0",
        "horas_teoricas": 2,
        "horas_practicas": 2,
        "alumnos_proyectados": 35,
        "semestre": 2,
        "carrera_id": 10,
        "docente_id": 32,
        "sala_id": 9
    },
    {
        "id": 50,
        "nombre": "Motores de Combustión Diesel",
        "codigo": "ME-111-2",
        "horas_teoricas": 1,
        "horas_practicas": 2,
        "alumnos_proyectados": 30,
        "semestre": 2,
        "carrera_id": 11,
        "docente_id": 32,
        "sala_id": 10
    },
    {
        "id": 51,
        "nombre": "Frenos",
        "codigo": "ME-121-2",
        "horas_teoricas": 1,
        "horas_practicas": 2,
        "alumnos_proyectados": 30,
        "semestre": 2,
        "carrera_id": 11,
        "docente_id": 33,
        "sala_id": 10
    },
    {
        "id": 52,
        "nombre": "Control Electronico de Motores Diesel",
        "codigo": "ME-311-2",
        "horas_teoricas": 1,
        "horas_practicas": 2,
        "alumnos_proyectados": 23,
        "semestre": 4,
        "carrera_id": 11,
        "alumnos_proyectados": 43,
        "semestre": 2,
        "carrera_id": 6,
        "docente_id": 23,
        "sala_id": 6
    },
    {
        "id": 37,
        "nombre": "Salud y Cuidados de Párvulos",
        "codigo": "EP-231-0",
        "horas_teoricas": 2,
        "horas_practicas": 2,
        "alumnos_proyectados": 43,
        "semestre": 2,
        "carrera_id": 6,
        "docente_id": 24,
        "sala_id": 6
    },
    {
        "id": 38,
        "nombre": "Corporalidad y Movimiento",
        "codigo": "EP-241-0",
        "horas_teoricas": 1,
        "horas_practicas": 2,
        "alumnos_proyectados": 43,
        "semestre": 2,
        "carrera_id": 6,
        "docente_id": 25,
        "sala_id": 6
    },
    {
        "id": 39,
        "nombre": "Diversidad e Inclusión en la Educ Parvularia",
        "codigo": "EP-411-0",
        "horas_teoricas": 2,
        "horas_practicas": 2,
        "alumnos_proyectados": 33,
        "semestre": 4,
        "carrera_id": 6,
        "docente_id": 26,
        "sala_id": 6
    },
    {
        "id": 40,
        "nombre": "Prepráctica",
        "codigo": "EP-421-0",
        "horas_teoricas": 0,
        "horas_practicas": 5,
        "alumnos_proyectados": 33,
        "semestre": 4,
        "carrera_id": 6,
        "docente_id": 23,
        "sala_id": 6
    },
    {
        "id": 41,
        "nombre": "Cuidados Integrales de Enfermería",
        "codigo": "ET 212-0",
        "horas_teoricas": 6,
        "horas_practicas": 9,
        "alumnos_proyectados": 50,
        "semestre": 2,
        "carrera_id": 8,
        "docente_id": 27,
        "sala_id": 7
    },
    {
        "id": 42,
        "nombre": "Salud Familiar y Comunitaria",
        "codigo": "ET 152-2",
        "horas_teoricas": 1.5,
        "horas_practicas": 3,
        "alumnos_proyectados": 50,
        "semestre": 2,
        "carrera_id": 8,
        "docente_id": 24,
        "sala_id": 7
    },
    {
        "id": 43,
        "nombre": "Sistemas Informáticos en Salud",
        "codigo": "ET 232-0",
        "horas_teoricas": 2,
        "horas_practicas": 2,
        "alumnos_proyectados": 50,
        "semestre": 2,
        "carrera_id": 8,
        "docente_id": 28,
        "sala_id": 7
    },
    {
        "id": 44,
        "nombre": "Administración de Fármacos",
        "codigo": "ET 22-0",
        "horas_teoricas": 6,
        "horas_practicas": 9,
        "alumnos_proyectados": 50,
        "semestre": 2,
        "carrera_id": 8,
        "docente_id": 29,
        "sala_id": 7
    },
    {
        "id": 45,
        "nombre": "Psicología Social Comunitaria y Familiar",
        "codigo": "IR-210-0",
        "horas_teoricas": 3,
        "horas_practicas": 1,
        "alumnos_proyectados": 14,
        "semestre": 2,
        "carrera_id": 9,
        "docente_id": 15,
        "sala_id": 8
    },
    {
        "id": 46,
        "nombre": "Primeros Auxilios",
        "codigo": "IR-410-0",
        "horas_teoricas": 0,
        "horas_practicas": 3,
        "alumnos_proyectados": 29,
        "semestre": 4,
        "carrera_id": 9,
        "docente_id": 29,
        "sala_id": 8
    },
    {
        "id": 47,
        "nombre": "Motoniveladora Bulldozer y Cargador",
        "codigo": "MP-101-2",
        "horas_teoricas": 1,
        "horas_practicas": 3,
        "alumnos_proyectados": 35,
        "semestre": 2,
        "carrera_id": 10,
        "docente_id": 31,
        "sala_id": 9
    },
    {
        "id": 48,
        "nombre": "Operación de Maquinaria Pesada Media",
        "codigo": "MP-102-2",
        "horas_teoricas": 0,
        "horas_practicas": 12,
        "alumnos_proyectados": 35,
        "semestre": 2,
        "carrera_id": 10,
        "docente_id": 31,
        "sala_id": 9
    },
    {
        "id": 49,
        "nombre": "Motores de Combustión Interna",
        "codigo": "MP-201-0",
        "horas_teoricas": 2,
        "horas_practicas": 2,
        "alumnos_proyectados": 35,
        "semestre": 2,
        "carrera_id": 10,
        "docente_id": 32,
        "sala_id": 9
    },
    {
        "id": 50,
        "nombre": "Motores de Combustión Diesel",
        "codigo": "ME-111-2",
        "horas_teoricas": 1,
        "horas_practicas": 2,
        "alumnos_proyectados": 30,
        "semestre": 2,
        "carrera_id": 11,
        "docente_id": 32,
        "sala_id": 10
    },
    {
        "id": 51,
        "nombre": "Frenos",
        "codigo": "ME-121-2",
        "horas_teoricas": 1,
        "horas_practicas": 2,
        "alumnos_proyectados": 30,
        "semestre": 2,
        "carrera_id": 11,
        "docente_id": 33,
        "sala_id": 10
    },
    {
        "id": 52,
        "nombre": "Control Electronico de Motores Diesel",
        "codigo": "ME-311-2",
        "horas_teoricas": 1,
        "horas_practicas": 2,
        "alumnos_proyectados": 23,
        "semestre": 4,
        "carrera_id": 11,
        "docente_id": 34,
        "sala_id": 10
    }
]

# 4. Datos de SALAS (Genéricas)
salas_data = [
    {
        "id": i,
        "nombre": f"Sala {i}",
        "capacidad": 40,
        "tipo": "Teórica"
    } for i in range(1, 11)
]

# 5. Datos de HORARIOS
# Asignación inteligente de horarios para evitar conflictos
# Distribuidos por sala, día y bloque horario
horarios_data = [
    # CARRERA 1: Administración Mención Gestión Pública (Diurna) - Sala 1
    # Módulo 1: Gestión de Personas (1T + 2P = 3h) - Lunes y Miércoles
    {"modulo_id": 1, "dia": "LUNES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 1, "dia": "MIERCOLES", "hora_inicio": "08:30", "hora_fin": "09:15"},
    
    # Módulo 2: Administración Pública III (2T + 2P = 4h) - Lunes y Miércoles
    {"modulo_id": 2, "dia": "LUNES", "hora_inicio": "10:15", "hora_fin": "12:00"},
    {"modulo_id": 2, "dia": "MIERCOLES", "hora_inicio": "10:15", "hora_fin": "12:00"},
    
    # Módulo 3: Marketing (1T + 3P = 4h) - Martes y Jueves
    {"modulo_id": 3, "dia": "MARTES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 3, "dia": "JUEVES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    
    # Módulo 4: Ética (1T + 1P = 2h) - Martes
    {"modulo_id": 4, "dia": "MARTES", "hora_inicio": "10:15", "hora_fin": "12:00"},
    
    # Módulo 5: Salud Ocupacional (1T + 1P = 2h) - Jueves
    {"modulo_id": 5, "dia": "JUEVES", "hora_inicio": "10:15", "hora_fin": "12:00"},
    
    # Módulo 6: Taller de Emprendimiento (0T + 3P = 3h) - Viernes
    {"modulo_id": 6, "dia": "VIERNES", "hora_inicio": "08:30", "hora_fin": "11:00"},
    
    # CARRERA 2: Administración Mención Gestión Pública (Vespertina) - Sala 2
    # Módulo 7-13: Horarios vespertinos
    {"modulo_id": 7, "dia": "LUNES", "hora_inicio": "18:00", "hora_fin": "19:45"},
    {"modulo_id": 7, "dia": "MIERCOLES", "hora_inicio": "18:00", "hora_fin": "19:45"},
    {"modulo_id": 8, "dia": "LUNES", "hora_inicio": "19:45", "hora_fin": "21:30"},
    {"modulo_id": 8, "dia": "MIERCOLES", "hora_inicio": "19:45", "hora_fin": "21:30"},
    {"modulo_id": 9, "dia": "MARTES", "hora_inicio": "18:00", "hora_fin": "19:45"},
    {"modulo_id": 9, "dia": "JUEVES", "hora_inicio": "18:00", "hora_fin": "19:45"},
    {"modulo_id": 10, "dia": "MARTES", "hora_inicio": "19:45", "hora_fin": "21:30"},
    {"modulo_id": 10, "dia": "JUEVES", "hora_inicio": "19:45", "hora_fin": "21:30"},
    {"modulo_id": 11, "dia": "VIERNES", "hora_inicio": "18:00", "hora_fin": "20:30"},
    {"modulo_id": 12, "dia": "VIERNES", "hora_inicio": "14:30", "hora_fin": "17:00"},
    {"modulo_id": 13, "dia": "VIERNES", "hora_inicio": "20:30", "hora_fin": "22:15"},
    
    # CARRERA 3: TNS en Construcción (Diurna) - Sala 3
    {"modulo_id": 14, "dia": "LUNES", "hora_inicio": "08:30", "hora_fin": "11:00"},
    {"modulo_id": 14, "dia": "MIERCOLES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 15, "dia": "MARTES", "hora_inicio": "08:30", "hora_fin": "11:00"},
    {"modulo_id": 16, "dia": "JUEVES", "hora_inicio": "08:30", "hora_fin": "11:00"},
    {"modulo_id": 16, "dia": "VIERNES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 17, "dia": "LUNES", "hora_inicio": "11:00", "hora_fin": "12:45"},
    {"modulo_id": 17, "dia": "MIERCOLES", "hora_inicio": "10:15", "hora_fin": "12:00"},
    {"modulo_id": 18, "dia": "MARTES", "hora_inicio": "11:00", "hora_fin": "12:45"},
    {"modulo_id": 19, "dia": "JUEVES", "hora_inicio": "11:00", "hora_fin": "12:45"},
    {"modulo_id": 20, "dia": "VIERNES", "hora_inicio": "10:15", "hora_fin": "12:45"},
    
    # CARRERA 4: Computación e Informática (Diurna) - Sala 4
    {"modulo_id": 21, "dia": "LUNES", "hora_inicio": "08:30", "hora_fin": "11:00"},
    {"modulo_id": 22, "dia": "LUNES", "hora_inicio": "11:00", "hora_fin": "12:45"},
    {"modulo_id": 23, "dia": "MARTES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 23, "dia": "MIERCOLES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 24, "dia": "MARTES", "hora_inicio": "10:15", "hora_fin": "12:45"},
    {"modulo_id": 25, "dia": "MIERCOLES", "hora_inicio": "10:15", "hora_fin": "12:45"},
    {"modulo_id": 26, "dia": "JUEVES", "hora_inicio": "08:30", "hora_fin": "11:00"},
    {"modulo_id": 27, "dia": "JUEVES", "hora_inicio": "11:00", "hora_fin": "12:45"},
    {"modulo_id": 28, "dia": "VIERNES", "hora_inicio": "08:30", "hora_fin": "12:00"},
    {"modulo_id": 29, "dia": "VIERNES", "hora_inicio": "12:00", "hora_fin": "12:45"},
    
    # CARRERA 5: Electricidad y Electrónica Industrial (Diurna) - Sala 5
    {"modulo_id": 30, "dia": "LUNES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 30, "dia": "MARTES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 31, "dia": "MIERCOLES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 31, "dia": "JUEVES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 32, "dia": "LUNES", "hora_inicio": "10:15", "hora_fin": "12:00"},
    {"modulo_id": 32, "dia": "MARTES", "hora_inicio": "10:15", "hora_fin": "12:00"},
    {"modulo_id": 32, "dia": "MIERCOLES", "hora_inicio": "10:15", "hora_fin": "11:00"},
    {"modulo_id": 33, "dia": "MIERCOLES", "hora_inicio": "11:00", "hora_fin": "12:00"},
    {"modulo_id": 33, "dia": "JUEVES", "hora_inicio": "10:15", "hora_fin": "12:00"},
    {"modulo_id": 34, "dia": "VIERNES", "hora_inicio": "08:30", "hora_fin": "12:00"},
    {"modulo_id": 35, "dia": "VIERNES", "hora_inicio": "12:00", "hora_fin": "12:45"},
    
    # Resto de módulos con horarios básicos
    {"modulo_id": 36, "dia": "LUNES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 37, "dia": "MARTES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 38, "dia": "MIERCOLES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 39, "dia": "JUEVES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 40, "dia": "VIERNES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 41, "dia": "LUNES", "hora_inicio": "10:15", "hora_fin": "12:00"},
    {"modulo_id": 42, "dia": "LUNES", "hora_inicio": "18:00", "hora_fin": "19:45"},
    {"modulo_id": 43, "dia": "MARTES", "hora_inicio": "18:00", "hora_fin": "19:45"},
    {"modulo_id": 44, "dia": "LUNES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 45, "dia": "MARTES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 46, "dia": "MIERCOLES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 47, "dia": "JUEVES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 48, "dia": "VIERNES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 49, "dia": "LUNES", "hora_inicio": "08:30", "hora_fin": "10:15"},
    {"modulo_id": 50, "dia": "LUNES", "hora_inicio": "08:30", "hora_fin": "11:00"},
    {"modulo_id": 51, "dia": "LUNES", "hora_inicio": "08:30", "hora_fin": "11:00"},
    {"modulo_id": 52, "dia": "MARTES", "hora_inicio": "08:30", "hora_fin": "11:00"},
]

# Crear DataFrames
df_docentes = pd.DataFrame(docentes_data)
df_carreras = pd.DataFrame(carreras_data)
df_modulos = pd.DataFrame(modulos_data)
df_salas = pd.DataFrame(salas_data)
df_horarios = pd.DataFrame(horarios_data, columns=[
    "modulo_id",
    "dia",
    "hora_inicio",
    "hora_fin"
])

# Guardar en un archivo Excel con múltiples hojas
output_file = "propuesta_importacion_completa.xlsx"
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df_docentes.to_excel(writer, sheet_name='Docentes', index=False)
    df_carreras.to_excel(writer, sheet_name='Carreras', index=False)
    df_modulos.to_excel(writer, sheet_name='Módulos', index=False)
    df_salas.to_excel(writer, sheet_name='Salas', index=False)
    df_horarios.to_excel(writer, sheet_name='Horarios Módulos', index=False)

output_file