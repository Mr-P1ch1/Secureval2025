# app/export_pdf.py (versión final integrada con reporte ampliado)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak
from datetime import datetime
import os
import json

def exportar_pdf(dominio):
    ruta_resultado = os.path.join("resultados", dominio, "riesgo.json")
    ruta_pdf = os.path.join("resultados", dominio, "riesgo.pdf")
    ruta_activos = os.path.join("resultados", dominio, "activos.json")
    ruta_monitor = os.path.join("resultados", dominio, "monitor.json")

    if not os.path.exists(ruta_resultado):
        return False

    with open(ruta_resultado, "r") as f:
        data = json.load(f)

    activos = []
    if os.path.exists(ruta_activos):
        with open(ruta_activos, "r") as f:
            activos = json.load(f)

    monitor = []
    if os.path.exists(ruta_monitor):
        with open(ruta_monitor, "r") as f:
            monitor = json.load(f)

    doc = SimpleDocTemplate(ruta_pdf, pagesize=A4)
    styles = getSampleStyleSheet()
    elementos = []

    # Título
    elementos.append(Paragraph("<b>Informe de Riesgo - SECUREVAL</b>", styles['Title']))
    elementos.append(Paragraph(f"Dominio: {dominio}", styles['Heading3']))
    elementos.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal']))
    elementos.append(Spacer(1, 12))

    # Tabla de riesgos
    encabezado = ["Subdominio", "Tecnología", "CVSS", "VA", "P", "VUL", "Riesgo"]
    filas = [encabezado]
    for r in data:
        fila = [
            r.get("subdominio", "")[:40],
            r.get("tecnologia", "")[:18],
            f"{r['cvss_max']:.1f}",
            r['valor_activo'],
            r['probabilidad'],
            r['vulnerabilidad'],
            f"{r['riesgo']:.1f}"
        ]
        filas.append(fila)

    tabla = Table(filas, repeatRows=1, colWidths=[130, 85, 40, 25, 25, 30, 45])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
    ]))
    elementos.append(tabla)

    # Activos
    if activos:
        elementos.append(PageBreak())
        elementos.append(Paragraph("<b>Activos Registrados</b>", styles['Heading2']))
        filas_activos = [["ID", "Nombre", "Tipo", "Valor", "Impacto Empresa"]]
        for a in activos:
            filas_activos.append([
                a.get("id", ""), a.get("nombre", ""), a.get("tipo", ""), a.get("valor", ""), a.get("impacto_empresa", "")
            ])
        tabla_activos = Table(filas_activos, repeatRows=1, colWidths=[30, 100, 100, 40, 100])
        tabla_activos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ]))
        elementos.append(tabla_activos)

    # Monitoreo
    if monitor:
        elementos.append(PageBreak())
        elementos.append(Paragraph("<b>Historial de Monitoreo</b>", styles['Heading2']))
        filas_monitor = [["Fecha", "Dominio", "Tecnologías Detectadas", "Riesgo Promedio"]]
        for m in monitor:
            filas_monitor.append([
                m.get("fecha", ""), m.get("dominio", ""), str(m.get("tecnologias", "")), str(m.get("riesgo_promedio", ""))
            ])
        tabla_monitor = Table(filas_monitor, repeatRows=1, colWidths=[100, 100, 80, 60])
        tabla_monitor.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.aliceblue),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ]))
        elementos.append(tabla_monitor)

    doc.build(elementos)
    return True
