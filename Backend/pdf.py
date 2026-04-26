from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, 
Table as LayoutTable, TableStyle, Paragraph, Spacer, PageBreak, Image)
from reportlab.platypus.flowables import HRFlowable
from io import BytesIO
import os
from Backend.database import get_db
from Backend.models import Socio, Vehiculo, Avance, Sancion, Finanzas
from datetime import datetime

pdf_router = APIRouter(prefix="/pdf", tags=["PDF"])


# --------------------- FUNCIÓN GENERAR PDF ---------------------
def generar_pdf_tabla(datos, encabezados, campos, titulo, col_widths_vertical, col_widths_landscape):
    buffer = BytesIO()
    styles = getSampleStyleSheet()

    #Estilos
    subtitulo_style = ParagraphStyle(
        name="Subtitulo",
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=colors.black,
        alignment=2,  # Alineado a la derecha
        spaceAfter=1
    )

    lema_style = ParagraphStyle(
        name="Lema",
        fontName="Helvetica-Oblique",
        fontSize=10,
        textColor=colors.HexColor("#424949"),
        alignment=2,
        spaceAfter=2
    )

    titulo_style = ParagraphStyle(
        name="TituloReporte",
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=colors.HexColor("#1B2631"),
        alignment=2,
        spaceAfter=2
    )

    fecha_style = ParagraphStyle(
        name="Fecha",
        fontSize=9,
        textColor=colors.HexColor("#616A6B"),
        alignment=2
    )

    cell_style = ParagraphStyle(
        name="Cell",
        fontSize=8,
        textColor=colors.black,
        fontName="Helvetica"
    )

    #Tamaño y orientación
    total_col_width = sum(col_widths_vertical)
    if total_col_width <= 210:
        page_size = A4
        col_widths = col_widths_vertical
    elif total_col_width <= 216:
        page_size = letter
        col_widths = col_widths_vertical
    elif total_col_width <= 297:
        page_size = landscape(A4)
        col_widths = col_widths_landscape
    else:
        page_size = landscape(letter)
        col_widths = col_widths_landscape

    doc = SimpleDocTemplate(
        buffer,
        pagesize=page_size,
        leftMargin=40,
        rightMargin=40,
        topMargin=95,
        bottomMargin=50
    )

    elements = []
    max_rows_por_pagina = 25
    fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, "logo.png")
    tiene_logo = os.path.exists(logo_path)

    # Páginas
    for pagina_inicio in range(0, len(datos), max_rows_por_pagina):
        page_data = datos[pagina_inicio:pagina_inicio + max_rows_por_pagina]

        # ===== CABECERA ESTILO MEMBRETE HORIZONTAL =====
        logo = Image(logo_path, width=70, height=70) if tiene_logo else Spacer(1, 70)

        # Texto del encabezado al lado derecho del logo
        encabezado_derecha = [
            Paragraph("LÍNEA DE TAXIS - SAN AGATÓN", subtitulo_style),
            Paragraph("Transporte al servicio de la comunidad", lema_style),
            Paragraph(titulo.upper(), titulo_style),
            Paragraph(f"Fecha - Hora de generación: {fecha_hoy}", fecha_style),
        ]

        # Usamos una tabla de layout para alinear logo + texto a la misma altura
        layout = LayoutTable(
            [[logo, encabezado_derecha]],
            colWidths=[80, 400],  # Ajusta según el tamaño de tu página
            style=[
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ],
        )

        elements.append(layout)
        elements.append(Spacer(1, 6))

        # Línea gruesa bajo el membrete
        elements.append(HRFlowable(width="100%", thickness=2.5, color=colors.black))
        elements.append(Spacer(1, 8))

        # ===== TABLA =====
        table_data = [encabezados]
        for i, obj in enumerate(page_data, start=pagina_inicio + 1):
            fila = [str(i)]
            for campo in campos:
                valor = getattr(obj, campo, "")
                if hasattr(valor, "strftime"):
                    valor = valor.strftime("%Y-%m-%d")
                fila.append(Paragraph(str(valor or ""), cell_style))
            table_data.append(fila)

        table = LayoutTable(table_data, colWidths=col_widths, repeatRows=1)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.black),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#F2F3F4")]),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#B3B6B7")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
        ]))

        elements.append(table)

        if pagina_inicio + max_rows_por_pagina < len(datos):
            elements.append(PageBreak())

    # ===== PIE DE PÁGINA =====
    def pie_pagina(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(colors.black)
        canvas.setStrokeColor(colors.HexColor("#A6ACAF"))
        canvas.setLineWidth(0.5)
        canvas.line(40, 40, doc.pagesize[0] - 40, 40)
        canvas.drawString(40, 30, "Sistema de Gestión - Línea de Taxis San Agatón")
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#4D4D4D"))
        canvas.drawRightString(doc.pagesize[0] - 40, 30, f"Página {doc.page}")
        canvas.restoreState()

    doc.build(elements, onFirstPage=pie_pagina, onLaterPages=pie_pagina)
    buffer.seek(0)
    return buffer

@pdf_router.get("/socios")
def pdf_socios(db: Session = Depends(get_db)):
    try:
        socios = db.query(Socio).all()
        encabezados = ["N°", "Documento", "Nombres", "Apellidos", "Dirección",
                       "Nro. Móvil", "Control", "RIF", "F. Nac."]
        campos = ["documento", "nombres", "apellidos", "direccion", "numero_telefono",
                  "numero_control", "rif", "fecha_nacimiento"]
        buffer = generar_pdf_tabla(
            socios, encabezados, campos,
            "Listado de Socios - Línea San Agatón",
            [20, 50, 70, 70, 120, 60, 35, 55, 55],
            [25, 60, 80, 80, 120, 70, 40, 60, 65]
        )


        nombre_archivo = f"socios_{datetime.now().strftime('%Y-%m-%d')}.pdf"
        return StreamingResponse(buffer, media_type="application/pdf",
                             headers={"Content-Disposition": f'inline; filename="{nombre_archivo}"'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF de socios: {str(e)}")


@pdf_router.get("/vehiculos")
def pdf_vehiculos(db: Session = Depends(get_db)):
    try:
        vehiculos = db.query(Vehiculo).all()
        encabezados = ["N°", "Documento", "Control", "Marca", "Modelo", "Año", "Placa"]
        campos = ["documento", "numero_control", "marca", "modelo", "ano", "placa"]
        buffer = generar_pdf_tabla(
            vehiculos, encabezados, campos,
            "Listado de Vehículos - Línea San Agatón",
            [20, 60, 50, 60, 50, 30, 70],
            [25, 70, 60, 70, 60, 35, 80]
        )

        nombre_archivo = f"vehiculos_{datetime.now().strftime('%Y-%m-%d')}.pdf"
        return StreamingResponse(buffer, media_type="application/pdf",
                             headers={"Content-Disposition": f'inline; filename="{nombre_archivo}"'})

        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF de vehículos: {str(e)}")


@pdf_router.get("/avances")
def pdf_avances(db: Session = Depends(get_db)):
    try:
        avances = db.query(Avance).all()
        encabezados = ["N°", "Nombre", "Apellido", "Control", "F. Nac", "RIF", "Documento", "Teléfono"]
        campos = ["nombre", "apellido", "numero_control", "fecha_nacimiento", "rif", "documento_avance", "numero_telf"]
        buffer = generar_pdf_tabla(
            avances, encabezados, campos,
            "Listado de Avances - Línea San Agatón",
            [20, 80, 50, 40, 60, 60, 60, 60],
            [30, 100, 100, 60, 80, 80, 90, 80]
        )

        nombre_archivo = f"avances_{datetime.now().strftime('%Y-%m-%d')}.pdf"
        return StreamingResponse(buffer, media_type="application/pdf",
                             headers={"Content-Disposition": f'inline; filename="{nombre_archivo}"'})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF de avances: {str(e)}")


@pdf_router.get("/sanciones")
def pdf_sanciones(db: Session = Depends(get_db)):
    try:
        sanciones = db.query(Sancion).all()
        encabezados = ["N°", "C.I Socio", "Nombre", "Apellido", "Inicio", "Final", "Monto", "Motivo"]
        campos = ["documento", "nombre", "apellido", "inicio_sancion", "final_sancion", "monto", "motivo_sancion"]
        buffer = generar_pdf_tabla(
            sanciones, encabezados, campos,
            "Listado de Sanciones - Línea San Agatón",
            [25, 60, 70, 70, 60, 60, 50, 120],
            [30, 80, 90, 90, 80, 80, 70, 140]
        )

        nombre_archivo = f"sanciones_{datetime.now().strftime('%Y-%m-%d')}.pdf"
        return StreamingResponse(buffer, media_type="application/pdf",
                             headers={"Content-Disposition": f'inline; filename="{nombre_archivo}"'})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF de sanciones: {str(e)}")


@pdf_router.get("/finanzas")
def pdf_finanzas(db: Session = Depends(get_db)):
    try:
        finanzas = db.query(Finanzas).all()
        encabezados = ["N°", "Documento", "Pagos Mensuales", "Impuestos Anuales", "Fecha de Pago", "Número de Control"]
        campos = ["documento", "pagos_mensuales", "impuestos_anuales", "fecha_pago", "numero_contr"]
        buffer = generar_pdf_tabla(
            finanzas, encabezados, campos,
            "Listado de Finanzas - Línea San Agatón",
            [20, 90, 90, 90, 120, 90],
            [30, 100, 100, 100, 140, 100]
        )

        nombre_archivo = f"finanzas_{datetime.now().strftime('%Y-%m-%d')}.pdf"
        return StreamingResponse(buffer, media_type="application/pdf",
                             headers={"Content-Disposition": f'attachment; filename="{nombre_archivo}"'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF de finanzas: {str(e)}")