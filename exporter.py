import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generar_pdf(itinerario_data, titulo="Itinerario CDMX Travel Planner"):
    """
    Genera un archivo PDF en memoria alineando correctamente las columnas y textos.
    """
    buffer = io.BytesIO()
    # 612 ancho carta - (36 margen izq + 36 margen der) = 540 puntos de área útil
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        rightMargin=36, 
        leftMargin=36, 
        topMargin=36, 
        bottomMargin=36
    )
    styles = getSampleStyleSheet()
    
    # Estilos de títulos
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=12
    )
    
    day_style = ParagraphStyle(
        'DayStyle',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#0D9488'),
        spaceBefore=12,
        spaceAfter=6
    )
    
    # Estilos de texto de tabla
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.HexColor('#1F2937')
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#374151')
    )
    
    time_style = ParagraphStyle(
        'TimeStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#1E3A8A')
    )
    
    story = []
    
    # Título principal
    story.append(Paragraph(titulo, title_style))
    story.append(Spacer(1, 10))
    
    # Recorrer los días e itinerario
    if isinstance(itinerario_data, dict) and "dias" in itinerario_data:
        for dia in itinerario_data["dias"]:
            num_dia = dia.get("dia", 1)
            story.append(Paragraph(f"Día {num_dia}", day_style))
            
            actividades = dia.get("actividades", [])
            
            # Encabezados con estilo Paragraph
            table_data = [[
                Paragraph("Horario", header_style), 
                Paragraph("Lugar / Actividad", header_style), 
                Paragraph("Descripción", header_style)
            ]]
            
            # Filas envolviendo CADA texto en Paragraph para forzar salto de línea
            for act in actividades:
                hora = act.get("hora", "")
                lugar = act.get("lugar", "")
                desc = act.get("descripcion", "")
                
                table_data.append([
                    Paragraph(hora, time_style),
                    Paragraph(lugar, body_style),
                    Paragraph(desc, body_style)
                ])
            
            # Asignación exacta de los 540 puntos útiles
            t = Table(table_data, colWidths=[70, 150, 320])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F3F4F6')),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(t)
            story.append(Spacer(1, 10))
            
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def generar_txt(itinerario_data):
    """
    Genera un archivo de texto plano descargable con el formato del itinerario.
    """
    texto = "=== ITINERARIO CDMX TRAVEL PLANNER ===\n\n"
    if isinstance(itinerario_data, dict) and "dias" in itinerario_data:
        for dia in itinerario_data["dias"]:
            texto += f"--- DÍA {dia.get('dia', 1)} ---\n"
            for act in dia.get("actividades", []):
                texto += f"• [{act.get('hora', '')}] {act.get('lugar', '')}: {act.get('descripcion', '')}\n"
            texto += "\n"
    return texto