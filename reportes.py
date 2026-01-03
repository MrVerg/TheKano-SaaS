from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self, output_dir="reportes"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generar_reporte_docente(self, docente, modulos, horarios_ocupados=None):
        """
        Genera un reporte PDF para un docente específico.
        """
        filename = f"Reporte_Docente_{docente['nombre'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'TitleCustom',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30
        )
        elements.append(Paragraph(f"Reporte de Docente", title_style))
        elements.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Teacher Info Section
        elements.append(Paragraph("Información Personal y Contractual", styles['Heading2']))
        
        # Data for Info Table
        info_data = [
            ["Nombre:", docente['nombre']],
            ["Título:", docente.get('titulo', 'N/A')],
            ["Email:", docente.get('email', 'N/A')],
            ["Contrato:", docente.get('contrato', 'N/A')],
            ["Horas Contratadas:", f"{docente.get('horas_contratadas', 0)} hrs cronológicas"],
            ["Evaluación:", f"{docente.get('evaluacion', 0.0)} / 5.0"]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('BACKGROUND', (0,0), (0,-1), colors.whitesmoke),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 20))
        
        # Modules Section
        elements.append(Paragraph("Módulos Asignados", styles['Heading2']))
        
        if not modulos:
            elements.append(Paragraph("No hay módulos asignados a este docente.", styles['Normal']))
        else:
            # Data for Modules Table
            headers = ["Código", "Módulo", "Carrera", "Horas (T/P)", "Horarios"]
            table_data = [headers]
            
            total_horas_academicas = 0
            
            for m in modulos:
                # Format schedules
                horarios_str = ""
                schedules = m.get('horarios', [])
                sch_lines = []
                if schedules:
                    for h in schedules:
                        sch_lines.append(f"{h['dia']} {h['hora_inicio']}-{h['hora_fin']}")
                horarios_str = "\n".join(sch_lines) if sch_lines else "Sin horario"

                # Use Paragraph for wrapping text in cells
                row = [
                    Paragraph(m.get('codigo', 'N/A'), styles['Normal']),
                    Paragraph(m.get('nombre', 'N/A'), styles['Normal']),
                    Paragraph(m.get('carrera_nombre', 'N/A'), styles['Normal']),
                    Paragraph(f"{m.get('horas_teoricas',0)}/{m.get('horas_practicas',0)}", styles['Normal']),
                    Paragraph(horarios_str.replace('\n', '<br/>'), styles['Normal'])
                ]
                table_data.append(row)
                total_horas_academicas += (m.get('horas_teoricas',0) + m.get('horas_practicas',0))

            # Create Table
            modules_table = Table(table_data, colWidths=[0.8*inch, 1.8*inch, 1.3*inch, 0.8*inch, 1.8*inch])
            modules_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 9),
                ('FONTSIZE', (0,1), (-1,-1), 8),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ]))
            elements.append(modules_table)
            
            elements.append(Spacer(1, 10))
            
            # Summary Calculation
            total_cronologicas = total_horas_academicas * 0.75
            utilization = (total_cronologicas / docente.get('horas_contratadas', 1)) * 100 if docente.get('horas_contratadas') else 0
            
            summary_text = f"<b>Total Horas Asignadas:</b> {total_horas_academicas} académicas ({total_cronologicas:.1f} cronológicas)<br/>"
            summary_text += f"<b>Utilización del Contrato:</b> {utilization:.1f}%"
            elements.append(Paragraph(summary_text, styles['Normal']))
            
            # Schedule Grid Section - Start on new page
            elements.append(PageBreak())
            elements.append(Paragraph("Horario Semanal", styles['Heading2']))
            elements.append(Spacer(1, 10))
            
            # Define standard time blocks (35-minute blocks)
            bloques_horarios = [
                "08:30", "09:05", "09:40", "10:15", "10:50", "11:25", "12:00", "12:35",
                "13:10", "13:45", "14:20", "14:55", "15:30", "16:05", "16:40", "17:15",
                "17:50", "18:25", "19:00", "19:35", "20:10", "20:45", "21:20", "21:55"
            ]
            
            dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
            
            # Helper function to check if a time is within a range
            def hora_en_rango(hora_actual, hora_inicio, hora_fin):
                """Verifica si una hora está dentro de un rango"""
                def hora_a_minutos(hora_str):
                    # Handle both string and timedelta
                    if hasattr(hora_str, 'total_seconds'):
                        total_seconds = int(hora_str.total_seconds())
                        return (total_seconds // 3600) * 60 + ((total_seconds % 3600) // 60)
                    # Remove seconds if present
                    hora_str = str(hora_str).split(':')[:2]
                    hora_str = ':'.join(hora_str)
                    partes = hora_str.split(':')
                    return int(partes[0]) * 60 + int(partes[1])
                
                try:
                    actual_min = hora_a_minutos(hora_actual)
                    inicio_min = hora_a_minutos(hora_inicio)
                    fin_min = hora_a_minutos(hora_fin)
                    return actual_min >= inicio_min and actual_min < fin_min
                except:
                    return False
            
            # Build grid data
            grid_data = []
            
            # Header row
            header_row = ["Hora"] + dias
            grid_data.append(header_row)
            
            # For each time block
            for bloque in bloques_horarios:
                row = [bloque]
                
                for dia in dias:
                    cell_content = ""
                    # Check if any module occupies this slot
                    for m in modulos:
                        schedules = m.get('horarios', [])
                        for h in schedules:
                            if h['dia'].upper() == dia and hora_en_rango(bloque, h['hora_inicio'], h['hora_fin']):
                                # Format cell content
                                codigo = m.get('codigo', 'N/A')
                                nombre = m.get('nombre', 'N/A')
                                sala = m.get('sala_nombre', 'N/A')
                                cell_content = f"{codigo}\n{nombre}\n🏢 {sala}"
                                break
                        if cell_content:
                            break
                    
                    row.append(cell_content if cell_content else "")
                
                grid_data.append(row)
            
            # Create schedule table
            schedule_table = Table(grid_data, colWidths=[0.8*inch, 1.3*inch, 1.3*inch, 1.3*inch, 1.3*inch, 1.3*inch])
            
            # Style the schedule table
            table_style = [
                # Header row
                ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 9),
                ('ALIGN', (0,0), (-1,0), 'CENTER'),
                
                # Time column
                ('BACKGROUND', (0,1), (0,-1), colors.lightgrey),
                ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
                ('FONTSIZE', (0,1), (0,-1), 8),
                ('ALIGN', (0,1), (0,-1), 'CENTER'),
                
                # All cells
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('FONTSIZE', (1,1), (-1,-1), 7),
                ('ALIGN', (1,1), (-1,-1), 'CENTER'),
                ('PADDING', (0,0), (-1,-1), 4),
            ]
            
            # Add background color for occupied cells
            for row_idx, row in enumerate(grid_data[1:], start=1):
                for col_idx, cell in enumerate(row[1:], start=1):
                    if cell:  # If cell has content (module assigned)
                        table_style.append(('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), colors.lightblue))
            
            schedule_table.setStyle(TableStyle(table_style))
            elements.append(schedule_table)

        # Build PDF
        doc.build(elements)
        return filepath

    def generar_reporte_carrera(self, carrera, modulos):
        """
        Genera un reporte PDF para una carrera específica con sus módulos organizados por semestre.
        """
        filename = f"Reporte_Carrera_{carrera['nombre'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'TitleCustom',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30
        )
        elements.append(Paragraph(f"Reporte de Carrera", title_style))
        elements.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Career Info Section
        elements.append(Paragraph("Información de la Carrera", styles['Heading2']))
        
        info_data = [
            ["Nombre:", carrera['nombre']],
            ["Jornada:", carrera.get('jornada', 'N/A')],
            ["Alumnos Proyectados:", str(carrera.get('alumnos_proyectados', 0))],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('BACKGROUND', (0,0), (0,-1), colors.whitesmoke),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 20))
        
        # Organize modules by semester
        modulos_por_semestre = {}
        for m in modulos:
            sem = m.get('semestre', 0)
            if sem not in modulos_por_semestre:
                modulos_por_semestre[sem] = []
            modulos_por_semestre[sem].append(m)
        
        # Modules by Semester
        if not modulos:
            elements.append(Paragraph("No hay módulos registrados para esta carrera.", styles['Normal']))
        else:
            total_modulos = len(modulos)
            total_horas_academicas = sum([m.get('horas_teoricas', 0) + m.get('horas_practicas', 0) for m in modulos])
            modulos_sin_docente = len([m for m in modulos if not m.get('docente_id')])
            modulos_sin_sala = len([m for m in modulos if not m.get('sala_id')])
            
            # Get unique teachers
            docentes_ids = set([m.get('docente_id') for m in modulos if m.get('docente_id')])
            
            for semestre in sorted(modulos_por_semestre.keys()):
                elements.append(Paragraph(f"Semestre {semestre}", styles['Heading2']))
                
                # Module table headers
                headers = ["Código", "Módulo", "Horas (T/P)", "Docente", "Sala"]
                table_data = [headers]
                
                for m in modulos_por_semestre[semestre]:
                    row = [
                        m.get('codigo', 'N/A'),
                        m.get('nombre', 'N/A'),
                        f"{m.get('horas_teoricas', 0)}/{m.get('horas_practicas', 0)}",
                        m.get('docente_nombre', 'Sin asignar'),
                        m.get('sala_nombre', 'Sin asignar')
                    ]
                    table_data.append(row)
                
                # Create table
                semester_table = Table(table_data, colWidths=[1*inch, 2.5*inch, 1*inch, 1.8*inch, 1.2*inch])
                semester_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0,0), (-1,0), 10),
                    ('BOTTOMPADDING', (0,0), (-1,0), 12),
                    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                    ('GRID', (0,0), (-1,-1), 1, colors.black),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('FONTSIZE', (0,1), (-1,-1), 9),
                ]))
                elements.append(semester_table)
                elements.append(Spacer(1, 15))
            
            # Summary Section
            elements.append(Paragraph("Resumen Estadístico", styles['Heading2']))
            
            summary_data = [
                ["Total de Módulos:", str(total_modulos)],
                ["Total Horas Académicas:", str(total_horas_academicas)],
                ["Docentes Involucrados:", str(len(docentes_ids))],
                ["Módulos sin Docente:", str(modulos_sin_docente)],
                ["Módulos sin Sala:", str(modulos_sin_sala)],
            ]
            
            summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch])
            summary_table.setStyle(TableStyle([
                ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('BACKGROUND', (0,0), (0,-1), colors.lightblue),
                ('PADDING', (0,0), (-1,-1), 6),
            ]))
            elements.append(summary_table)
        
        # Build PDF
        doc.build(elements)
        return filepath
