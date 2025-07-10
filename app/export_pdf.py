# app/export_pdf.py (versión profesional completa con selector de dominio y exportación)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from datetime import datetime
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

def calcular_kpis_para_pdf(data):
    """Calcula los KPIs de riesgo para incluir en el PDF."""
    if not data:
        return None
    
    total = len(data)
    bajos = sum(1 for r in data if r["riesgo"] < 10)
    medios = sum(1 for r in data if 10 <= r["riesgo"] < 25)
    mitigables = sum(1 for r in data if 25 <= r["riesgo"] < 80)
    criticos = sum(1 for r in data if r["riesgo"] >= 80)
    
    return {
        "total_amenazas": total,
        "riesgo_bajo": (bajos, round(bajos * 100 / total, 1) if total > 0 else 0),
        "riesgo_medio": (medios, round(medios * 100 / total, 1) if total > 0 else 0),
        "riesgo_mitigable": (mitigables, round(mitigables * 100 / total, 1) if total > 0 else 0),
        "riesgo_critico": (criticos, round(criticos * 100 / total, 1) if total > 0 else 0),
        "riesgo_promedio": round(sum(r["riesgo"] for r in data) / total, 2) if total > 0 else 0,
        "riesgo_maximo": max(r["riesgo"] for r in data) if data else 0
    }

def determinar_tratamiento_para_pdf(riesgo):
    """Determina la estrategia de tratamiento según el nivel de riesgo."""
    if riesgo < 10:
        return "Aceptar", "El riesgo es bajo y puede ser aceptado con monitoreo básico."
    elif riesgo < 25:
        return "Aceptar/Mitigar", "Riesgo moderado. Se puede aceptar o implementar controles menores."
    elif riesgo < 50:
        return "Mitigar/Transferir", "Riesgo significativo. Requiere medidas de mitigación o transferencia."
    elif riesgo < 80:
        return "Mitigar", "Riesgo alto. Implementar controles de mitigación inmediatamente."
    else:
        return "Evitar/Mitigar", "Riesgo crítico. Evitar la exposición o mitigar urgentemente."

def crear_estilos_personalizados():
    """Crea estilos personalizados para el documento."""
    styles = getSampleStyleSheet()
    
    # Estilo para el título principal
    styles.add(ParagraphStyle(
        name='TituloPersonalizado',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.darkblue,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    # Estilo para secciones
    styles.add(ParagraphStyle(
        name='SeccionTitulo',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    ))
    
    # Estilo para resumen ejecutivo
    styles.add(ParagraphStyle(
        name='ResumenEjecutivo',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leftIndent=20,
        rightIndent=20
    ))
    
    return styles

def crear_grafica_pastel_riesgos(kpis):
    """Crea una gráfica de pastel con la distribución de riesgos."""
    if not kpis:
        return None
    
    drawing = Drawing(400, 300)
    
    # Datos para la gráfica
    data = [
        kpis["riesgo_bajo"][0],      # Cantidad de riesgos bajos
        kpis["riesgo_medio"][0],     # Cantidad de riesgos medios  
        kpis["riesgo_mitigable"][0], # Cantidad de riesgos mitigables
        kpis["riesgo_critico"][0]    # Cantidad de riesgos críticos
    ]
    
    # Solo incluir categorías que tienen datos
    labels = []
    colors_list = []
    filtered_data = []
    
    if data[0] > 0:
        labels.append(f"Bajo ({kpis['riesgo_bajo'][1]}%)")
        colors_list.append(colors.green)
        filtered_data.append(data[0])
    
    if data[1] > 0:
        labels.append(f"Medio ({kpis['riesgo_medio'][1]}%)")
        colors_list.append(colors.yellow)
        filtered_data.append(data[1])
    
    if data[2] > 0:
        labels.append(f"Alto ({kpis['riesgo_mitigable'][1]}%)")
        colors_list.append(colors.orange)
        filtered_data.append(data[2])
    
    if data[3] > 0:
        labels.append(f"Crítico ({kpis['riesgo_critico'][1]}%)")
        colors_list.append(colors.red)
        filtered_data.append(data[3])
    
    if not filtered_data:
        return None
    
    # Crear gráfica de pastel
    pie = Pie()
    pie.x = 50
    pie.y = 50
    pie.width = 200
    pie.height = 200
    pie.data = filtered_data
    pie.labels = labels
    pie.slices.strokeColor = colors.white
    pie.slices.strokeWidth = 2
    
    # Asignar colores
    for i, color in enumerate(colors_list):
        pie.slices[i].fillColor = color
    
    drawing.add(pie)
    
    # Crear leyenda
    legend = Legend()
    legend.x = 280
    legend.y = 150
    legend.deltax = 15
    legend.deltay = 15
    legend.fontName = 'Helvetica'
    legend.fontSize = 9
    legend.boxAnchor = 'w'
    legend.columnMaximum = 4
    legend.strokeWidth = 1
    legend.strokeColor = colors.black
    legend.deltax = 75
    legend.deltay = 10
    legend.dx = 8
    legend.dy = 8
    legend.fontName = 'Helvetica'
    legend.fontSize = 8
    legend.leading = 12
    
    legend.colorNamePairs = [(colors_list[i], labels[i]) for i in range(len(labels))]
    drawing.add(legend)
    
    return drawing

def crear_subdominio_seguro(subdominio):
    """Crea un Paragraph para subdominios largos que se ajusten correctamente con saltos de línea."""
    if not subdominio:
        return ""
    
    if len(subdominio) <= 25:
        return subdominio
    
    # Para subdominios largos, crear saltos de línea inteligentes
    if len(subdominio) > 25:
        # Dividir por puntos y crear líneas
        parts = subdominio.split('.')
        lines = []
        current_line = ""
        
        for i, part in enumerate(parts):
            test_line = current_line + ('.' if current_line else '') + part
            
            if len(test_line) <= 25:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = part
                else:
                    # Si una parte es muy larga, dividirla
                    while len(part) > 25:
                        lines.append(part[:22] + '...')
                        part = '...' + part[22:]
                    current_line = part
        
        if current_line:
            lines.append(current_line)
        
        texto_formateado = '<br/>'.join(lines)
        return Paragraph(f"<font size=6>{texto_formateado}</font>", getSampleStyleSheet()['Normal'])
    
    return subdominio

def crear_puertos_formateados(puertos_lista):
    """Crea un Paragraph para listas de puertos que se ajusten correctamente en celdas."""
    if not puertos_lista:
        return "-"
    
    # Si es una lista, convertir a string
    if isinstance(puertos_lista, list):
        puertos_str = ", ".join(str(p) for p in puertos_lista)
    else:
        puertos_str = str(puertos_lista)
    
    # Si es corto, devolver como string normal
    if len(puertos_str) <= 20:
        return puertos_str
    
    # Para listas largas, dividir inteligentemente
    puertos_individuales = puertos_str.split(', ')
    lines = []
    current_line = ""
    
    for puerto in puertos_individuales:
        test_line = current_line + (', ' if current_line else '') + puerto
        
        if len(test_line) <= 20:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
                current_line = puerto
            else:
                # Si un puerto individual es muy largo, truncar
                if len(puerto) > 20:
                    lines.append(puerto[:17] + '...')
                else:
                    lines.append(puerto)
                current_line = ""
    
    if current_line:
        lines.append(current_line)
    
    # Crear paragraph con saltos de línea
    texto_formateado = '<br/>'.join(lines)
    return Paragraph(f"<font size=6>{texto_formateado}</font>", getSampleStyleSheet()['Normal'])

def crear_texto_ajustable(texto, max_chars=25):
    """Función genérica para crear texto que se ajuste en celdas de tabla."""
    if not texto:
        return "-"
    
    texto_str = str(texto)
    
    # Si es corto, devolver como string normal
    if len(texto_str) <= max_chars:
        return texto_str
    
    # Para texto largo, dividir en líneas
    lines = []
    words = texto_str.split(' ')
    current_line = ""
    
    for word in words:
        test_line = current_line + (' ' if current_line else '') + word
        
        if len(test_line) <= max_chars:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
                current_line = word
            else:
                # Si una palabra es muy larga, dividirla
                while len(word) > max_chars:
                    lines.append(word[:max_chars-3] + '...')
                    word = '...' + word[max_chars-3:]
                current_line = word
    
    if current_line:
        lines.append(current_line)
    
    # Crear paragraph con saltos de línea
    texto_formateado = '<br/>'.join(lines)
    return Paragraph(f"<font size=6>{texto_formateado}</font>", getSampleStyleSheet()['Normal'])

def exportar_pdf(dominio):
    ruta_resultado = os.path.join("resultados", dominio, "riesgo.json")
    ruta_resumen = os.path.join("resultados", dominio, "resumen.json")
    ruta_pdf = os.path.join("resultados", dominio, "riesgo.pdf")
    ruta_activos = os.path.join("resultados", "activos.json")

    if not os.path.exists(ruta_resultado):
        return False

    with open(ruta_resultado, "r") as f:
        data = json.load(f)

    resumen_data = []
    if os.path.exists(ruta_resumen):
        with open(ruta_resumen, "r") as f:
            resumen_data = json.load(f)

    activos = []
    if os.path.exists(ruta_activos):
        with open(ruta_activos, "r") as f:
            activos = json.load(f)

    # Configurar documento con márgenes profesionales
    doc = SimpleDocTemplate(
        ruta_pdf, 
        pagesize=A4,
        topMargin=1*inch,
        bottomMargin=1*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    
    styles = crear_estilos_personalizados()
    elementos = []
    
    # Calcular KPIs
    kpis = calcular_kpis_para_pdf(data)

    # ============================
    # PORTADA PROFESIONAL
    # ============================
    elementos.append(Paragraph("<b>INFORME DE EVALUACIÓN DE RIESGOS<br/>DE CIBERSEGURIDAD</b>", styles['TituloPersonalizado']))
    elementos.append(Spacer(1, 30))
    
    elementos.append(Paragraph(f"<b>Organización evaluada:</b> {dominio}", styles['Heading2']))
    elementos.append(Spacer(1, 20))
    
    elementos.append(Paragraph(f"<b>Fecha de análisis:</b> {datetime.now().strftime('%d de %B de %Y')}", styles['Normal']))
    elementos.append(Paragraph(f"<b>Herramienta:</b> SECUREVAL v2.0", styles['Normal']))
    elementos.append(Paragraph(f"<b>Tipo de evaluación:</b> Análisis automatizado de superficie de ataque", styles['Normal']))
    elementos.append(Spacer(1, 40))
    
    # Tabla de información general
    info_general = [
        ["Métrica", "Valor"],
        ["Total de amenazas detectadas", str(kpis["total_amenazas"]) if kpis else "0"],
        ["Nivel de riesgo promedio", f"{kpis['riesgo_promedio']:.1f}" if kpis else "0"],
        ["Riesgo máximo identificado", f"{kpis['riesgo_maximo']:.1f}" if kpis else "0"],
        ["Subdominios analizados", str(len(set(r['subdominio'] for r in data))) if data else "0"]
    ]
    
    tabla_info = Table(info_general, colWidths=[200, 100])
    tabla_info.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
    ]))
    elementos.append(tabla_info)
    
    elementos.append(PageBreak())

    # ============================
    # RESUMEN EJECUTIVO
    # ============================
    elementos.append(Paragraph("RESUMEN EJECUTIVO", styles['SeccionTitulo']))
    
    resumen_texto = f"""
    Este informe presenta los resultados del análisis de ciberseguridad realizado sobre el dominio <b>{dominio}</b> 
    utilizando la plataforma SECUREVAL. Se han identificado <b>{kpis['total_amenazas'] if kpis else 0} amenazas potenciales</b> 
    distribuidas across múltiples subdominios y servicios.
    
    El análisis revela un nivel de riesgo promedio de <b>{kpis['riesgo_promedio']:.1f}</b> puntos, con un riesgo máximo 
    de <b>{kpis['riesgo_maximo']:.1f}</b> puntos. La distribución de riesgos muestra:
    """ + (f"""
    • <b>{kpis['riesgo_critico'][0]} amenazas críticas</b> ({kpis['riesgo_critico'][1]}%) que requieren atención inmediata
    • <b>{kpis['riesgo_mitigable'][0]} amenazas de riesgo alto</b> ({kpis['riesgo_mitigable'][1]}%) que necesitan mitigación
    • <b>{kpis['riesgo_medio'][0]} amenazas de riesgo medio</b> ({kpis['riesgo_medio'][1]}%) bajo monitoreo
    • <b>{kpis['riesgo_bajo'][0]} amenazas de riesgo bajo</b> ({kpis['riesgo_bajo'][1]}%) con riesgo aceptable
    """ if kpis else "No se detectaron amenazas en el análisis.")
    
    elementos.append(Paragraph(resumen_texto, styles['ResumenEjecutivo']))
    elementos.append(Spacer(1, 20))

    # Agregar gráfica de pastel de distribución de riesgos
    if kpis:
        elementos.append(Paragraph("<b>Distribución de Riesgos por Categoría</b>", styles['Heading3']))
        grafica_pastel = crear_grafica_pastel_riesgos(kpis)
        if grafica_pastel:
            elementos.append(grafica_pastel)
            elementos.append(Spacer(1, 20))

    # ============================
    # DASHBOARD DE MONITOREO
    # ============================
    elementos.append(PageBreak())
    elementos.append(Paragraph("DASHBOARD DE MONITOREO DE RIESGOS", styles['SeccionTitulo']))
    
    if kpis:
        # Tabla de KPIs
        kpi_data = [
            ["Indicador de Riesgo", "Cantidad", "Porcentaje", "Estado"],
            ["Amenazas Críticas (≥80)", str(kpis['riesgo_critico'][0]), f"{kpis['riesgo_critico'][1]}%", "🔴 CRÍTICO"],
            ["Amenazas Altas (25-79)", str(kpis['riesgo_mitigable'][0]), f"{kpis['riesgo_mitigable'][1]}%", "🟠 ALTO"],
            ["Amenazas Medias (10-24)", str(kpis['riesgo_medio'][0]), f"{kpis['riesgo_medio'][1]}%", "🟡 MEDIO"],
            ["Amenazas Bajas (<10)", str(kpis['riesgo_bajo'][0]), f"{kpis['riesgo_bajo'][1]}%", "🟢 BAJO"],
        ]
        
        tabla_kpis = Table(kpi_data, colWidths=[180, 60, 80, 80])
        tabla_kpis.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 1), (0, 1), colors.red),
            ('BACKGROUND', (0, 2), (0, 2), colors.orange),
            ('BACKGROUND', (0, 3), (0, 3), colors.yellow),
            ('BACKGROUND', (0, 4), (0, 4), colors.lightgreen),
            ('BACKGROUND', (1, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (1, 1), (2, -1), 'CENTER'),
        ]))
        elementos.append(tabla_kpis)
        elementos.append(Spacer(1, 20))
        
        # Recomendaciones de monitoreo
        elementos.append(Paragraph("<b>Recomendaciones de Monitoreo:</b>", styles['Heading3']))
        
        recomendaciones = []
        if kpis['riesgo_critico'][0] > 0:
            recomendaciones.append("• <b>URGENTE:</b> Implementar monitoreo continuo 24/7 para amenazas críticas")
        if kpis['riesgo_mitigable'][0] > 0:
            recomendaciones.append("• Establecer alertas automáticas para amenazas de riesgo alto")
        if kpis['riesgo_medio'][0] > 0:
            recomendaciones.append("• Programar revisiones semanales para amenazas de riesgo medio")
        
        recomendaciones.append("• Generar reportes de tendencias mensuales")
        recomendaciones.append("• Implementar métricas de tiempo de respuesta ante incidentes")
        
        for rec in recomendaciones:
            elementos.append(Paragraph(rec, styles['Normal']))
        
        elementos.append(Spacer(1, 20))

        # Gráfica de pastel de distribución de riesgos
        elementos.append(Paragraph("<b>Distribución de Riesgos por Categoría</b>", styles['Heading3']))
        grafica_riesgos = crear_grafica_pastel_riesgos(kpis)
        if grafica_riesgos:
            elementos.append(grafica_riesgos)
        elementos.append(Spacer(1, 20))

    # ============================
    # ANÁLISIS DETALLADO DE AMENAZAS
    # ============================
    elementos.append(PageBreak())
    elementos.append(Paragraph("ANÁLISIS DETALLADO DE AMENAZAS", styles['SeccionTitulo']))
    
    # Tabla detallada de subdominios
    encabezado = ["Subdominio", "Tecnología", "Servicio", "OS", "CVSS", "VA", "Riesgo", "Criticidad"]
    filas = [encabezado]
    for r in data:
        fila = [
            crear_subdominio_seguro(r.get("subdominio", "")),
            crear_texto_ajustable(r.get("tecnologia", ""), 15),  # Formatear tecnología
            crear_texto_ajustable(r.get("tipo_servicio", ""), 12),  # Formatear servicio
            crear_texto_ajustable(r.get("sistema_operativo", ""), 10),  # Formatear OS
            f"{r['cvss_max']:.1f}",
            r['valor_activo'],
            f"{r['riesgo']:.1f}",
            r['criticidad']
        ]
        filas.append(fila)

    tabla = Table(filas, repeatRows=1, colWidths=[130, 65, 50, 45, 35, 30, 40, 50])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (4, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('WORDWRAP', (0, 0), (-1, -1), True),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.white]),
    ]))
    
    # Ajustar altura de filas dinámicamente basado en contenido multilínea
    for i in range(1, len(filas)):
        # Verificar si alguna celda tiene Paragraph (contenido multilínea)
        tiene_paragraph = any(isinstance(celda, Paragraph) for celda in filas[i])
        if tiene_paragraph:
            tabla.setStyle(TableStyle([('ROWHEIGHT', (0, i), (-1, i), 45)]))  # Altura mayor para multilínea
    
    elementos.append(tabla)

    # ============================
    # DETALLES TÉCNICOS DE SEGURIDAD
    # ============================
    elementos.append(PageBreak())
    elementos.append(Paragraph("DETALLES TÉCNICOS DE SEGURIDAD", styles['SeccionTitulo']))
    
    # TLS y Puertos
    elementos.append(Paragraph("<b>Configuraciones TLS y Puertos Expuestos</b>", styles['Heading3']))
    filas_tls = [["Subdominio", "TLS", "Cifrado", "Válido Hasta", "Puertos Detectados"]]
    for r in data:
        tls_info = r.get("tls", {})
        
        # Manejar TLS como string o dict
        if isinstance(tls_info, dict):
            tls_version = tls_info.get("tls_version", "-")
            cifrado = crear_texto_ajustable(tls_info.get("cifrado", "-"), 15)
            valido_hasta = tls_info.get("valido_hasta", "-")
        else:
            tls_version = str(tls_info)
            cifrado = "-"
            valido_hasta = "-"
        
        filas_tls.append([
            crear_subdominio_seguro(r.get("subdominio", "")),
            tls_version,
            cifrado,
            valido_hasta,
            crear_puertos_formateados(r.get("puertos", []))
        ])

    tabla_tls = Table(filas_tls, repeatRows=1, colWidths=[120, 45, 85, 65, 125])
    tabla_tls.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('BACKGROUND', (0, 1), (-1, -1), colors.aliceblue),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('WORDWRAP', (0, 0), (-1, -1), True),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.aliceblue, colors.white]),
    ]))
    
    # Ajustar altura de filas para contenido con múltiples líneas
    for i in range(1, len(filas_tls)):
        # Verificar si alguna celda tiene Paragraph (texto multilínea)
        tiene_paragraph = any(isinstance(celda, Paragraph) for celda in filas_tls[i])
        if tiene_paragraph:
            # Altura mayor para filas con contenido multilínea
            tabla_tls.setStyle(TableStyle([('ROWHEIGHT', (0, i), (-1, i), 40)]))  # Altura fija mayor
    
    elementos.append(tabla_tls)
    elementos.append(Spacer(1, 20))

    # ============================
    # INVENTARIO DE ACTIVOS
    # ============================
    if activos:
        elementos.append(Paragraph("<b>Inventario de Activos Registrados</b>", styles['Heading3']))
        filas_activos = [["ID", "Nombre", "Tipo", "Valor", "Impacto en la Organización"]]
        for a in activos:
            filas_activos.append([
                a.get("id", ""), 
                a.get("nombre", ""), 
                a.get("tipo", ""), 
                a.get("valor", ""), 
                a.get("impacto_empresa", "")
            ])
        tabla_activos = Table(filas_activos, repeatRows=1, colWidths=[30, 120, 80, 40, 210])
        tabla_activos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('WORDWRAP', (0, 0), (-1, -1), True),
        ]))
        elementos.append(tabla_activos)
        elementos.append(Spacer(1, 20))

    # ============================
    # ESTRATEGIAS DE TRATAMIENTO DE RIESGOS
    # ============================
    elementos.append(PageBreak())
    elementos.append(Paragraph("ESTRATEGIAS DE TRATAMIENTO DE RIESGOS", styles['SeccionTitulo']))
    
    # Agrupar amenazas por estrategia de tratamiento
    tratamientos = {}
    for r in data:
        estrategia, descripcion = determinar_tratamiento_para_pdf(r['riesgo'])
        if estrategia not in tratamientos:
            tratamientos[estrategia] = {'amenazas': [], 'descripcion': descripcion}
        tratamientos[estrategia]['amenazas'].append(r)
    
    for estrategia, info in tratamientos.items():
        elementos.append(Paragraph(f"<b>{estrategia}</b>", styles['Heading3']))
        elementos.append(Paragraph(info['descripcion'], styles['Normal']))
        
        # Tabla de amenazas para esta estrategia
        filas_tratamiento = [["Subdominio", "Tecnología", "Riesgo", "Acciones Recomendadas"]]
        
        for amenaza in info['amenazas']:
            acciones = []
            if amenaza['riesgo'] >= 80:
                acciones = ["Desactivar servicio temporalmente", "Aplicar parches urgentes", "Monitoreo 24/7"]
            elif amenaza['riesgo'] >= 50:
                acciones = ["Aplicar controles de seguridad", "Actualizar configuraciones", "Monitoreo frecuente"]
            elif amenaza['riesgo'] >= 25:
                acciones = ["Revisar configuraciones", "Considerar actualizaciones", "Monitoreo regular"]
            else:
                acciones = ["Mantener monitoreo básico", "Revisar en auditorías programadas"]
            
            filas_tratamiento.append([
                crear_subdominio_seguro(amenaza.get("subdominio", "")),
                crear_texto_ajustable(amenaza.get("tecnologia", ""), 18),  # Formatear tecnología
                f"{amenaza['riesgo']:.1f}",
                "\n".join(acciones)
            ])
        
        tabla_tratamiento = Table(filas_tratamiento, repeatRows=1, colWidths=[120, 80, 50, 230])
        tabla_tratamiento.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('BACKGROUND', (0, 1), (-1, -1), colors.mistyrose),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('WORDWRAP', (0, 0), (-1, -1), True),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.mistyrose, colors.white]),
        ]))
        
        # Ajustar altura de filas para contenido multilínea en tabla tratamiento
        for i in range(1, len(filas_tratamiento)):
            # Verificar si alguna celda tiene Paragraph (contenido multilínea)
            tiene_paragraph = any(isinstance(celda, Paragraph) for celda in filas_tratamiento[i])
            if tiene_paragraph:
                tabla_tratamiento.setStyle(TableStyle([('ROWHEIGHT', (0, i), (-1, i), 40)]))
        
        elementos.append(tabla_tratamiento)
        elementos.append(Spacer(1, 15))

    # ============================
    # RESUMEN ESTADÍSTICO POR SUBDOMINIO
    # ============================
    if resumen_data:
        elementos.append(PageBreak())
        elementos.append(Paragraph("RESUMEN ESTADÍSTICO POR SUBDOMINIO", styles['SeccionTitulo']))
        
        filas_resumen = [["Subdominio", "Tecnologías", "CVEs", "Riesgo Máximo", "Riesgo Promedio", "Estado"]]
        for sub, val in resumen_data.items():
            # Determinar estado basado en riesgo máximo
            if val['riesgo_max'] >= 80:
                estado = "🔴 CRÍTICO"
            elif val['riesgo_max'] >= 50:
                estado = "🟠 ALTO"
            elif val['riesgo_max'] >= 25:
                estado = "🟡 MEDIO"
            else:
                estado = "🟢 BAJO"
                
            filas_resumen.append([
                crear_subdominio_seguro(sub), 
                str(val['total_tecnologias']), 
                str(val['total_cves']), 
                f"{val['riesgo_max']:.1f}", 
                f"{val['riesgo_promedio']:.1f}",
                estado
            ])
            
        tabla_resumen = Table(filas_resumen, repeatRows=1, colWidths=[160, 60, 50, 70, 70, 70])
        tabla_resumen.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('WORDWRAP', (0, 0), (-1, -1), True),
            ('ALIGN', (1, 1), (4, -1), 'CENTER'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lavender, colors.white]),
        ]))
        
        # Ajustar altura de filas para subdominios largos en tabla resumen
        for i in range(1, len(filas_resumen)):
            if isinstance(filas_resumen[i][0], Paragraph):
                tabla_resumen.setStyle(TableStyle([('ROWHEIGHT', (0, i), (-1, i), 30)]))
        
        elementos.append(tabla_resumen)
        elementos.append(Spacer(1, 20))

    # ============================
    # CONCLUSIONES Y RECOMENDACIONES FINALES
    # ============================
    elementos.append(PageBreak())
    elementos.append(Paragraph("CONCLUSIONES Y RECOMENDACIONES", styles['SeccionTitulo']))
    
    conclusiones_texto = f"""
    <b>Conclusiones del Análisis:</b><br/><br/>
    
    1. <b>Exposición General:</b> Se identificaron {kpis['total_amenazas'] if kpis else 0} amenazas potenciales 
    en la infraestructura de {dominio}, con un nivel de riesgo promedio de {kpis['riesgo_promedio']:.1f} puntos.
    
    2. <b>Prioridades de Atención:</b> Se recomienda atención inmediata para {kpis['riesgo_critico'][0] if kpis else 0} 
    amenazas críticas y {kpis['riesgo_mitigable'][0] if kpis else 0} amenazas de riesgo alto.
    
    3. <b>Superficie de Ataque:</b> La organización tiene {len(set(r['subdominio'] for r in data)) if data else 0} 
    subdominios expuestos que requieren monitoreo continuo.
    
    <b>Recomendaciones Estratégicas:</b><br/><br/>
    
    • <b>Inmediato (0-30 días):</b> Mitigar todas las amenazas críticas identificadas
    • <b>Corto plazo (1-3 meses):</b> Implementar controles para amenazas de riesgo alto
    • <b>Mediano plazo (3-6 meses):</b> Establecer programa de monitoreo continuo
    • <b>Largo plazo (6-12 meses):</b> Desarrollar plan de respuesta a incidentes integral
    
    <b>Próximos Pasos:</b><br/><br/>
    
    1. Establecer un equipo de respuesta para amenazas críticas
    2. Implementar herramientas de monitoreo automatizado
    3. Desarrollar políticas de gestión de riesgos
    4. Programar evaluaciones de seguimiento trimestrales
    5. Capacitar al personal en mejores prácticas de ciberseguridad
    """
    
    elementos.append(Paragraph(conclusiones_texto, styles['ResumenEjecutivo']))
    elementos.append(Spacer(1, 20))
    
    # Pie de página del informe
    elementos.append(Paragraph("---", styles['Normal']))
    elementos.append(Paragraph(f"<i>Informe generado por SECUREVAL v2.0 el {datetime.now().strftime('%d de %B de %Y a las %H:%M:%S')}</i>", styles['Normal']))
    elementos.append(Paragraph("<i>Para consultas técnicas o soporte, contacte al equipo de ciberseguridad.</i>", styles['Normal']))

    doc.build(elementos)
    return True

def obtener_dominios_disponibles():
    """Obtiene la lista de dominios que tienen análisis completados."""
    dominios_disponibles = []
    ruta_resultados = "resultados"
    
    if not os.path.exists(ruta_resultados):
        return dominios_disponibles
    
    for item in os.listdir(ruta_resultados):
        ruta_dominio = os.path.join(ruta_resultados, item)
        
        # Verificar que sea un directorio y no el archivo activos.json
        if os.path.isdir(ruta_dominio) and item != "__pycache__":
            # Verificar que tenga el archivo riesgo.json
            ruta_riesgo = os.path.join(ruta_dominio, "riesgo.json")
            if os.path.exists(ruta_riesgo):
                # Obtener metadatos si existen
                ruta_metadata = os.path.join(ruta_dominio, "metadata.json")
                metadata = {}
                if os.path.exists(ruta_metadata):
                    try:
                        with open(ruta_metadata, 'r') as f:
                            metadata = json.load(f)
                    except:
                        pass
                
                # Contar amenazas
                try:
                    with open(ruta_riesgo, 'r') as f:
                        data = json.load(f)
                        total_amenazas = len(data)
                        riesgo_max = max(r['riesgo'] for r in data) if data else 0
                except:
                    total_amenazas = 0
                    riesgo_max = 0
                
                fecha_analisis = metadata.get('fecha_fin', 'Fecha desconocida')
                
                dominios_disponibles.append({
                    'dominio': item,
                    'fecha_analisis': fecha_analisis,
                    'total_amenazas': total_amenazas,
                    'riesgo_max': riesgo_max,
                    'metadata': metadata
                })
    
    # Ordenar por fecha de análisis (más reciente primero)
    dominios_disponibles.sort(key=lambda x: x['fecha_analisis'], reverse=True)
    return dominios_disponibles

class SelectorExportacionPDF:
    """Interfaz gráfica para seleccionar el dominio a exportar en PDF."""
    
    def __init__(self, parent=None):
        self.dominio_seleccionado = None
        self.ventana = tk.Toplevel(parent) if parent else tk.Tk()
        self.configurar_ventana()
        self.crear_interfaz()
        self.cargar_dominios()
        
    def configurar_ventana(self):
        """Configura la ventana principal."""
        self.ventana.title("SECUREVAL - Exportar Reporte PDF")
        self.ventana.geometry("800x600")
        self.ventana.configure(bg='#f0f0f0')
        
        # Centrar ventana
        self.ventana.transient()
        self.ventana.grab_set()
        
    def crear_interfaz(self):
        """Crea la interfaz de usuario."""
        # Frame principal
        main_frame = ttk.Frame(self.ventana, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        titulo = ttk.Label(main_frame, text="Exportar Reporte PDF de Ciberseguridad", 
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Selector de dominio
        ttk.Label(main_frame, text="Seleccionar Dominio:", 
                 font=('Arial', 12, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        self.combo_dominios = ttk.Combobox(main_frame, width=40, font=('Arial', 10))
        self.combo_dominios.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.combo_dominios.bind('<<ComboboxSelected>>', self.on_dominio_seleccionado)
        
        # Frame para vista previa
        preview_frame = ttk.LabelFrame(main_frame, text="Vista Previa del Análisis", padding="10")
        preview_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Text widget para mostrar información del dominio seleccionado
        self.text_preview = scrolledtext.ScrolledText(preview_frame, height=15, width=80, 
                                                     font=('Courier', 9), state=tk.DISABLED)
        self.text_preview.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(20, 0))
        
        # Botones
        self.btn_exportar = ttk.Button(button_frame, text="📄 Exportar PDF", 
                                      command=self.exportar_pdf, state=tk.DISABLED)
        self.btn_exportar.grid(row=0, column=0, padx=(0, 10))
        
        self.btn_actualizar = ttk.Button(button_frame, text="🔄 Actualizar Lista", 
                                        command=self.cargar_dominios)
        self.btn_actualizar.grid(row=0, column=1, padx=(0, 10))
        
        self.btn_cancelar = ttk.Button(button_frame, text="❌ Cancelar", 
                                      command=self.cancelar)
        self.btn_cancelar.grid(row=0, column=2)
        
        # Configurar expansión
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.rowconfigure(0, weight=1)
        
    def cargar_dominios(self):
        """Carga los dominios disponibles en el combobox."""
        print("🔍 Cargando dominios disponibles para exportación...")
        
        dominios = obtener_dominios_disponibles()
        
        # Limpiar combobox
        self.combo_dominios['values'] = ()
        self.combo_dominios.set('')
        
        if not dominios:
            self.combo_dominios['values'] = ('No hay dominios analizados disponibles',)
            self.mostrar_info_preview("ℹ️ No se encontraron dominios con análisis completados.\n\n" +
                                    "Para exportar un reporte PDF, primero debe ejecutar un análisis " +
                                    "de seguridad en el módulo 'Analyzer'.")
            self.btn_exportar.config(state=tk.DISABLED)
            return
        
        # Crear lista de opciones para el combobox
        opciones = []
        for dom in dominios:
            fecha = dom['fecha_analisis'][:19] if len(dom['fecha_analisis']) > 19 else dom['fecha_analisis']
            opcion = f"{dom['dominio']} - {dom['total_amenazas']} amenazas - {fecha}"
            opciones.append(opcion)
        
        self.combo_dominios['values'] = opciones
        self.dominios_data = dominios
        
        # Seleccionar el primero por defecto
        if opciones:
            self.combo_dominios.current(0)
            self.on_dominio_seleccionado(None)
        
        print(f"✅ Cargados {len(dominios)} dominios disponibles")
        
    def on_dominio_seleccionado(self, event):
        """Maneja la selección de un dominio."""
        indice = self.combo_dominios.current()
        if indice >= 0 and hasattr(self, 'dominios_data'):
            dominio_info = self.dominios_data[indice]
            self.dominio_seleccionado = dominio_info['dominio']
            self.mostrar_preview_dominio(dominio_info)
            self.btn_exportar.config(state=tk.NORMAL)
        else:
            self.btn_exportar.config(state=tk.DISABLED)
            
    def mostrar_preview_dominio(self, dominio_info):
        """Muestra la vista previa del dominio seleccionado."""
        try:
            # Cargar datos del dominio
            ruta_riesgo = os.path.join("resultados", dominio_info['dominio'], "riesgo.json")
            ruta_resumen = os.path.join("resultados", dominio_info['dominio'], "resumen.json")
            ruta_metadata = os.path.join("resultados", dominio_info['dominio'], "metadata.json")
            
            # Información básica
            info_text = f"📊 VISTA PREVIA DEL ANÁLISIS\n"
            info_text += "=" * 60 + "\n\n"
            info_text += f"🌐 Dominio: {dominio_info['dominio']}\n"
            info_text += f"📅 Fecha de análisis: {dominio_info['fecha_analisis']}\n"
            info_text += f"⚠️  Total de amenazas: {dominio_info['total_amenazas']}\n"
            info_text += f"🔴 Riesgo máximo: {dominio_info['riesgo_max']:.1f}\n\n"
            
            # Metadata
            if dominio_info['metadata']:
                meta = dominio_info['metadata']
                info_text += "📋 METADATOS DEL ANÁLISIS\n"
                info_text += "-" * 30 + "\n"
                if 'fecha_inicio' in meta:
                    info_text += f"⏰ Inicio: {meta['fecha_inicio']}\n"
                if 'fecha_fin' in meta:
                    info_text += f"🏁 Fin: {meta['fecha_fin']}\n"
                if 'duracion_total' in meta:
                    info_text += f"⏱️  Duración: {meta['duracion_total']}\n"
                if 'total_subdominios' in meta:
                    info_text += f"🔍 Subdominios escaneados: {meta['total_subdominios']}\n"
                if 'total_puertos_escaneados' in meta:
                    info_text += f"🚪 Puertos escaneados: {meta['total_puertos_escaneados']}\n"
                if 'herramientas_usadas' in meta:
                    info_text += f"🛠️  Herramientas: {', '.join(meta['herramientas_usadas'])}\n"
                info_text += "\n"
            
            # Cargar datos de riesgo para estadísticas
            if os.path.exists(ruta_riesgo):
                with open(ruta_riesgo, 'r') as f:
                    data_riesgo = json.load(f)
                
                # Calcular distribución de riesgos
                criticos = sum(1 for r in data_riesgo if r['riesgo'] >= 80)
                altos = sum(1 for r in data_riesgo if 25 <= r['riesgo'] < 80)
                medios = sum(1 for r in data_riesgo if 10 <= r['riesgo'] < 25)
                bajos = sum(1 for r in data_riesgo if r['riesgo'] < 10)
                
                info_text += "📈 DISTRIBUCIÓN DE RIESGOS\n"
                info_text += "-" * 30 + "\n"
                info_text += f"🔴 Críticos (≥80): {criticos}\n"
                info_text += f"🟠 Altos (25-79): {altos}\n"
                info_text += f"🟡 Medios (10-24): {medios}\n"
                info_text += f"🟢 Bajos (<10): {bajos}\n\n"
                
                # Mostrar algunas tecnologías detectadas
                tecnologias = set()
                for r in data_riesgo[:10]:  # Primeras 10 amenazas
                    if r.get('tecnologia'):
                        tecnologias.add(r['tecnologia'])
                
                if tecnologias:
                    info_text += "🔧 TECNOLOGÍAS DETECTADAS (muestra)\n"
                    info_text += "-" * 30 + "\n"
                    for tech in list(tecnologias)[:8]:  # Mostrar máximo 8
                        info_text += f"• {tech}\n"
                    if len(tecnologias) > 8:
                        info_text += f"• ... y {len(tecnologias) - 8} más\n"
                    info_text += "\n"
            
            # Cargar resumen por subdominios si existe
            if os.path.exists(ruta_resumen):
                with open(ruta_resumen, 'r') as f:
                    data_resumen = json.load(f)
                
                info_text += "🌐 SUBDOMINIOS ANALIZADOS\n"
                info_text += "-" * 30 + "\n"
                for subdom, stats in list(data_resumen.items())[:5]:  # Primeros 5
                    info_text += f"• {subdom}: {stats.get('total_cves', 0)} CVEs, "
                    info_text += f"Riesgo máx: {stats.get('riesgo_max', 0):.1f}\n"
                
                if len(data_resumen) > 5:
                    info_text += f"• ... y {len(data_resumen) - 5} subdominios más\n"
            
            info_text += "\n" + "=" * 60 + "\n"
            info_text += "✅ Listo para exportar a PDF profesional"
            
            self.mostrar_info_preview(info_text)
            
        except Exception as e:
            error_text = f"❌ Error al cargar vista previa:\n{str(e)}\n\n"
            error_text += "El dominio puede tener archivos de análisis corruptos."
            self.mostrar_info_preview(error_text)
    
    def mostrar_info_preview(self, texto):
        """Muestra texto en el área de vista previa."""
        self.text_preview.config(state=tk.NORMAL)
        self.text_preview.delete(1.0, tk.END)
        self.text_preview.insert(1.0, texto)
        self.text_preview.config(state=tk.DISABLED)
        
    def exportar_pdf(self):
        """Exporta el PDF del dominio seleccionado."""
        if not self.dominio_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un dominio para exportar")
            return
        
        try:
            print(f"📄 Iniciando exportación PDF para {self.dominio_seleccionado}...")
            
            # Llamar a la función de exportación
            exito = exportar_pdf(self.dominio_seleccionado)
            
            if exito:
                ruta_pdf = os.path.join("resultados", self.dominio_seleccionado, "riesgo.pdf")
                messagebox.showinfo("Éxito", 
                                  f"✅ PDF exportado exitosamente!\n\n"
                                  f"Archivo guardado en:\n{ruta_pdf}\n\n"
                                  f"El reporte incluye análisis completo de riesgos, "
                                  f"recomendaciones de tratamiento y estrategias de monitoreo.")
                print(f"✅ PDF exportado exitosamente: {ruta_pdf}")
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", 
                                   "❌ Error al exportar PDF.\n\n"
                                   "Verifique que el dominio tenga análisis completados.")
                print(f"❌ Error al exportar PDF para {self.dominio_seleccionado}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado al exportar PDF:\n{str(e)}")
            print(f"❌ Error inesperado: {str(e)}")
    
    def cancelar(self):
        """Cancela la exportación y cierra la ventana."""
        self.ventana.destroy()
    
    def mostrar(self):
        """Muestra la ventana modal."""
        self.ventana.mainloop()

def abrir_selector_exportacion_pdf(parent=None):
    """Función principal para abrir el selector de exportación PDF."""
    print("📄 Abriendo selector de exportación PDF...")
    
    try:
        selector = SelectorExportacionPDF(parent)
        selector.mostrar()
    except Exception as e:
        print(f"❌ Error al abrir selector PDF: {str(e)}")
        if parent:
            messagebox.showerror("Error", f"Error al abrir exportador PDF:\n{str(e)}")
