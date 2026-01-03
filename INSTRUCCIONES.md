ESTRUCTURA DE PROYECTO 
 Este proyecto será desarrollado en Python.
 Es un administrador de equipo docente en una institución de educación superior.

 Pantalla sencilla de login donde el usuario ingresa correo y contraseña para acceder al sistema.

2. Panel principal

Menú de navegación donde se muestran las diferentes salas (SALA 1, SALA 2, LABORATORIO).

En la parte superior hay opciones para ver carreras y módulos.

Se muestra el nombre de la institución (CEDUC).

3. Gestión de carreras

Sección para visualizar carreras disponibles (“ADMINISTRACIÓN PÚBLICA”, “COMPETENCIA E INFORMACIÓN”, etc.).

Se permite acceder al creador de carreras, donde se puede registrar una nueva carrera especificando nombre, jornada (diurna/vespertina), semestres, salas disponibles y cantidad de alumnos proyectados.

4. Gestión de módulos

Vista donde se visualizan los módulos de cada carrera, asociados a docentes y horarios.

Se puede ingresar a detalles de cada módulo para editar información relevante (docente, alumnos, horas teóricas/prácticas, sala asignada).

5. Gestión de docentes

Panel para editar información del docente: nombre, título, horas asignadas, evaluación, disponibilidad horaria (se muestra una grilla donde se marcan las disponibilidades).

Muestra la relación de módulos asignados al docente.

6. Asignación de módulos al docente

Relación entre módulos y carreras gestionada mediante la interfaz. Permite visualizar los módulos que dicta cada docente y en qué horario/sala.

7. Horario general

Tabla-resumen con el horario semanal donde se visualizan los módulos con su distribución y asignación a los docentes y salas. Sirve para detectar solapamientos y optimizar la programación académica.



Objetivo General:
Automatizar y centralizar la gestión académica en una institución educativa—including control de carreras, módulos, docentes, disponibilidad horaria, asignación de salas y generación de horarios—todo desde una plataforma amigable web.

Características principales:
Control centralizado de carreras, salas y módulos.

Gestión de docentes con información detallada, disponibilidad y evaluación.

Asignación automatizada de módulos y recursos para evitar solapamientos.

Visualización clara de la estructura semanal y relaciones entre módulos, docentes y salas.

Interfaz intuitiva que facilita la administración y edición de datos académicos.

Este sistema podría ser la base para el desarrollo de una aplicación en python que permita automatizar y centralizar la gestión académica de establecimientos de educación técnica/profesional, permitiendo mejorar la planificación, eficiencia y trazabilidad de recursos humanos y materiales.

------
login

    TENEMOS PRIMERO LA PANTALLA DE LOGIN EN LA CUAL SI INGRESAMOS CON UN USUARIO (email) QUE ESTÉ CLASIFICADO COMO ADMINISTRADOR LO CONDUCIRÁ A LA SIGUIENTE VISTA

PANEL PRINCIPAL
GESTION DE SALAS Y CARRERAS
 tenemos una vista dividida por un lado (izquierda), las salas y sus horas disponibles mostradas con un grafico de barra horizontal ordenadas en una sola columna que use el 25% del ancho de la pantalla  al final abajo en esta columna un botón para crear una nueva sala. El 75% del ancho en la columna derecha una vista de cajas de 5 cajas de alto por 3 cajas de ancho, en cada una de estas leemos el nombre de la carrera. Al final abajo de la columna derecha teneos un botón que dice “añadir carrera”

GESTION DE SALAS Y CARRERAS

Estructura de la vista de gestión de salas y carreras:

    Vista dividida en 2 columnas 25%/75% de ancho.
    Columna izquierda:
        Lista de tarjetas de salas con nombre de la sala y una barra horizontal que grafica las horas disponibles.
            Al hacer clic en una tarjeta de sala, se abre un formulario con los siguientes campos:
                Nombre de la sala (campo de texto)
                Capacidad (campo numérico)
                Horas disponibles (campo numérico)

        Al final abajo un botón para añadir sala.
    Columna derecha:
        una vista de mosaico 3x5 de tarjetas de carreras.
            Al hacer clic en una tarjeta de carrera, se abre la vista ASIGNACIÓN DE MÓDULOS AL DOCENTE (descripta más abajo).
        y al final abajo un botón para añadir carrera.
            Al hacer clic en el botón de añadir carrera, se abre un formulario con los siguientes campos:
                Nombre de la carrera (campo de texto)
                Jornada (selector desplegable: diurna/vespertina)
                Semestres (selector múltiple: I, II, III, IV)
                Salas disponibles (selector múltiple con las salas creadas)
                Cantidad de alumnos proyectados (campo numérico)


 


ASIGNACIÓN DE MÓDULOS AL DOCENTE


Estructura de la vista de asignación de módulos al docente:

    Vista dividida en 2 columnas 25%/75% de ancho.
    Columna izquierda:
        Nombre de la institución (CEDUC) en la parte superior.
        Nombre de la carrera seleccionada debajo del nombre de la institución, a la derecha un botón para editar la carrera.
            Al hacer clic en el botón de editar carrera, se abre un formulario con los siguientes campos:
        Dos selectores
            Uno para definir si estamos configurando la carrera diurna o vespertina.
            Otro para seleccionar el semestre de la carrera. (I y III / II y IV)
        Lista de tarjetas de docentes con fotografía de perfil, Nombre y Apellido, Título académico, Tipo de contrato y una barra horizontal que grafica las horas disponibles y contratadas.
        Al final abajo un botón para añadir docente.
           Abre un formulario con los siguientes campos:
                Nombre (campo de texto)
                Título académico (campo de texto)
                Tipo de contrato (selector desplegable)
                Horas contratadas (campo numérico)
                Disponibilidad horaria (grilla donde se marcan las disponibilidades)


        Al hacer clic en una tarjeta de docente, se abre una vista detallada del docente seleccionado divididida en 2 columnas 25%/75% de ancho.
            Columna izquierda:
                Información del docente seleccionado.
                Lista de tarjetas de módulos asignados al docente.
                y al final abajo un botón para añadir módulo.
            Columna derecha:
                Grilla semanal donde se visualizan los módulos asignados al docente con su distribución y asignación a las salas.
            

    Columna derecha:
        una vista de mosaico 3x5 de tarjetas de módulos.
        Al hacer clic en una tarjeta de módulo, se abre una formulario con los siguientes campos:
            Nombre del módulo (campo de texto)
            Docente asignado (selector desplegable con los nombres de los docentes disponibles)
            Cantidad de alumnos (campo numérico)
            Horas teóricas (campo numérico)
            Horas prácticas (campo numérico)
            Sala asignada (selector desplegable con las salas disponibles)
        Al final del formulario un botón para guardar los cambios realizados y otro para cancelar.
    
