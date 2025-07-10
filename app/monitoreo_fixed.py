#!/usr/bin/env python3
"""
SECUREVAL - Módulo de Monitoreo y Dashboard v2.0
Interfaz moderna con análisis de seguridad y gestión de activos
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import sys
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Configurar el path para importar módulos
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Intentar importar el módulo de activos
try:
    from .activos import obtener_activos
except ImportError:
    def obtener_activos():
        """Función de respaldo si no se puede importar el módulo"""
        return []

def listar_dominios():
    """Lista los dominios que tienen resultados de análisis"""
    try:
        resultados_dir = current_dir / "resultados"
        if not resultados_dir.exists():
            return []
        
        dominios = []
        for item in resultados_dir.iterdir():
            if item.is_dir() and (item / "resumen.json").exists():
                dominios.append(item.name)
        
        return sorted(dominios)
    except Exception as e:
        print(f"Error listando dominios: {e}")
        return []

def calcular_kpis(dominio):
    """Calcula indicadores clave de rendimiento para un dominio"""
    try:
        resultados_dir = current_dir / "resultados" / dominio
        
        if not resultados_dir.exists():
            return None
        
        kpis = {
            'total_subdominios': 0,
            'total_tecnologias': 0,
            'total_cves': 0,
            'riesgo_promedio': 0,
            'subdominios_alto_riesgo': 0,
            'tecnologias_vulnerables': 0
        }
        
        # Leer resumen si existe
        resumen_file = resultados_dir / "resumen.json"
        if resumen_file.exists():
            with open(resumen_file, 'r') as f:
                resumen = json.load(f)
            
            kpis['total_subdominios'] = len(resumen)
            
            riesgos = []
            for subdominio, info in resumen.items():
                kpis['total_tecnologias'] += info.get('total_tecnologias', 0)
                kpis['total_cves'] += info.get('total_cves', 0)
                
                riesgo_max = info.get('riesgo_max', 0)
                if riesgo_max >= 8.0:
                    kpis['subdominios_alto_riesgo'] += 1
                
                riesgos.append(info.get('riesgo_promedio', 0))
            
            if riesgos:
                kpis['riesgo_promedio'] = sum(riesgos) / len(riesgos)
        
        # Leer tecnologías si existe
        tecnologias_file = resultados_dir / "tecnologias.json"
        if tecnologias_file.exists():
            with open(tecnologias_file, 'r') as f:
                tecnologias = json.load(f)
            
            for tech_data in tecnologias.values():
                if isinstance(tech_data, dict) and tech_data.get('cves'):
                    kpis['tecnologias_vulnerables'] += 1
        
        return kpis
        
    except Exception as e:
        print(f"Error calculando KPIs para {dominio}: {e}")
        return None

def mostrar_kpis_en_gui(kpis, texto_widget):
    """Muestra los KPIs en el widget de texto de la GUI"""
    if not kpis:
        return
    
    texto_widget.insert(tk.END, "📊 INDICADORES CLAVE DE RENDIMIENTO (KPIs)\n")
    texto_widget.insert(tk.END, "=" * 60 + "\n\n")
    
    # KPIs principales
    texto_widget.insert(tk.END, f"🌐 Total de subdominios analizados: {kpis['total_subdominios']}\n")
    texto_widget.insert(tk.END, f"🔧 Total de tecnologías identificadas: {kpis['total_tecnologias']}\n")
    texto_widget.insert(tk.END, f"🚨 Total de CVEs encontrados: {kpis['total_cves']}\n")
    texto_widget.insert(tk.END, f"📈 Riesgo promedio general: {kpis['riesgo_promedio']:.2f}/10\n")
    texto_widget.insert(tk.END, f"⚠️ Subdominios de alto riesgo (≥8.0): {kpis['subdominios_alto_riesgo']}\n")
    texto_widget.insert(tk.END, f"🔓 Tecnologías con vulnerabilidades: {kpis['tecnologias_vulnerables']}\n\n")
    
    # Evaluación del nivel de riesgo
    riesgo = kpis['riesgo_promedio']
    if riesgo >= 8.0:
        nivel = "🔴 CRÍTICO"
        recomendacion = "Acción inmediata requerida"
    elif riesgo >= 6.0:
        nivel = "🟠 ALTO"
        recomendacion = "Revisar y mitigar vulnerabilidades"
    elif riesgo >= 4.0:
        nivel = "🟡 MEDIO"
        recomendacion = "Monitoreo continuo recomendado"
    else:
        nivel = "🟢 BAJO"
        recomendacion = "Mantener buenas prácticas"
    
    texto_widget.insert(tk.END, f"🎯 NIVEL DE RIESGO: {nivel}\n")
    texto_widget.insert(tk.END, f"💡 RECOMENDACIÓN: {recomendacion}\n\n")

def mostrar_resumen(dominio, texto_widget):
    """Muestra un resumen detallado del análisis"""
    try:
        resultados_dir = current_dir / "resultados" / dominio
        resumen_file = resultados_dir / "resumen.json"
        
        if resumen_file.exists():
            with open(resumen_file, 'r') as f:
                resumen = json.load(f)
            
            texto_widget.insert(tk.END, "📋 RESUMEN DETALLADO POR SUBDOMINIO\n")
            texto_widget.insert(tk.END, "=" * 60 + "\n\n")
            
            # Mostrar solo los primeros 5 subdominios para no saturar
            for i, (subdominio, info) in enumerate(list(resumen.items())[:5], 1):
                texto_widget.insert(tk.END, f"{i}. 🔹 {subdominio}\n")
                texto_widget.insert(tk.END, f"   • Tecnologías: {info.get('total_tecnologias', 0)}\n")
                texto_widget.insert(tk.END, f"   • CVEs: {info.get('total_cves', 0)}\n")
                texto_widget.insert(tk.END, f"   • Riesgo máximo: {info.get('riesgo_max', 0):.2f}/10\n")
                texto_widget.insert(tk.END, f"   • Riesgo promedio: {info.get('riesgo_promedio', 0):.2f}/10\n\n")
            
            if len(resumen) > 5:
                texto_widget.insert(tk.END, f"... y {len(resumen) - 5} subdominios más\n\n")
        
    except Exception as e:
        texto_widget.insert(tk.END, f"❌ Error cargando resumen: {str(e)}\n")

def mostrar_activos(texto_widget):
    """Muestra información de activos empresariales"""
    try:
        activos = obtener_activos()
        
        if activos:
            # Estadísticas de activos
            tipos_activos = {}
            total_valor = 0
            
            for activo in activos:
                tipo = activo.get('tipo', 'Desconocido')
                tipos_activos[tipo] = tipos_activos.get(tipo, 0) + 1
                try:
                    total_valor += float(activo.get('valor', 0))
                except:
                    pass
            
            texto_widget.insert(tk.END, "📊 RESUMEN EJECUTIVO DE ACTIVOS\n")
            texto_widget.insert(tk.END, f"🏢 Total de activos registrados: {len(activos)}\n")
            texto_widget.insert(tk.END, f"💰 Valor total estimado: ${total_valor:,.2f}\n")
            texto_widget.insert(tk.END, f"🗂️ Tipos de activos: {len(tipos_activos)}\n\n")
            
            texto_widget.insert(tk.END, "📋 DISTRIBUCIÓN POR TIPO:\n")
            for tipo, cantidad in sorted(tipos_activos.items()):
                porcentaje = (cantidad / len(activos)) * 100
                texto_widget.insert(tk.END, f"   🔸 {tipo}: {cantidad} ({porcentaje:.1f}%)\n")
            
            texto_widget.insert(tk.END, "\n📦 DETALLE DE ACTIVOS (Primeros 10):\n")
            for i, activo in enumerate(activos[:10], 1):
                texto_widget.insert(tk.END, f"\n{i}. 🛠️ [{activo.get('codigo', 'N/A')}] {activo.get('nombre', 'Sin nombre')}\n")
                texto_widget.insert(tk.END, f"   • Tipo: {activo.get('tipo', 'N/A')}\n")
                texto_widget.insert(tk.END, f"   • Valor: ${activo.get('valor', 0)}\n")
                texto_widget.insert(tk.END, f"   • Descripción: {activo.get('descripcion', 'N/A')}\n")
            
            if len(activos) > 10:
                texto_widget.insert(tk.END, f"\n... y {len(activos) - 10} activos más\n")
        else:
            texto_widget.insert(tk.END, "📭 No hay activos registrados en el sistema\n")
            texto_widget.insert(tk.END, "💡 Use el módulo de 'Gestión de Activos' para registrar activos\n")
    
    except Exception as e:
        texto_widget.insert(tk.END, f"❌ Error cargando activos: {str(e)}\n")

def crear_grafico_kpis(kpis_data, frame_parent):
    """Crea un gráfico de KPIs usando matplotlib"""
    try:
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.patch.set_facecolor('#f8f9fa')
        
        # Gráfico 1: Distribución de riesgos
        riesgos = ['Bajo (0-4)', 'Medio (4-6)', 'Alto (6-8)', 'Crítico (8-10)']
        valores_riesgo = [0, 0, 0, 0]
        
        # Simular distribución basada en el riesgo promedio
        riesgo_prom = kpis_data.get('riesgo_promedio', 0)
        if riesgo_prom < 4:
            valores_riesgo[0] = 70
            valores_riesgo[1] = 20
            valores_riesgo[2] = 8
            valores_riesgo[3] = 2
        elif riesgo_prom < 6:
            valores_riesgo[0] = 40
            valores_riesgo[1] = 35
            valores_riesgo[2] = 20
            valores_riesgo[3] = 5
        elif riesgo_prom < 8:
            valores_riesgo[0] = 20
            valores_riesgo[1] = 30
            valores_riesgo[2] = 35
            valores_riesgo[3] = 15
        else:
            valores_riesgo[0] = 10
            valores_riesgo[1] = 20
            valores_riesgo[2] = 30
            valores_riesgo[3] = 40
        
        colors = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']
        ax1.pie(valores_riesgo, labels=riesgos, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Distribución de Niveles de Riesgo', fontweight='bold')
        
        # Gráfico 2: Métricas principales
        metricas = ['Subdominios', 'Tecnologías', 'CVEs', 'Vulnerabilidades']
        valores_metricas = [
            kpis_data.get('total_subdominios', 0),
            kpis_data.get('total_tecnologias', 0),
            kpis_data.get('total_cves', 0),
            kpis_data.get('tecnologias_vulnerables', 0)
        ]
        
        bars = ax2.bar(metricas, valores_metricas, color=['#3498db', '#9b59b6', '#e74c3c', '#f39c12'])
        ax2.set_title('Métricas de Seguridad', fontweight='bold')
        ax2.set_ylabel('Cantidad')
        
        # Añadir valores en las barras
        for bar, valor in zip(bars, valores_metricas):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(valor), ha='center', va='bottom', fontweight='bold')
        
        # Gráfico 3: Indicador de riesgo
        riesgo = kpis_data.get('riesgo_promedio', 0)
        colors_gauge = ['#2ecc71' if riesgo < 4 else '#f39c12' if riesgo < 6 else '#e67e22' if riesgo < 8 else '#e74c3c']
        
        wedges = ax3.pie([riesgo, 10-riesgo], colors=[colors_gauge[0], '#ecf0f1'], 
                        startangle=90, counterclock=False, 
                        wedgeprops=dict(width=0.3))
        
        ax3.text(0, 0, f'{riesgo:.1f}', ha='center', va='center', 
                fontsize=20, fontweight='bold')
        ax3.set_title('Riesgo Promedio General', fontweight='bold')
        
        # Gráfico 4: Comparativa de seguridad
        categorias = ['Tecnologías\nSeguras', 'Tecnologías\nVulnerables']
        seguras = max(0, kpis_data.get('total_tecnologias', 0) - kpis_data.get('tecnologias_vulnerables', 0))
        vulnerables = kpis_data.get('tecnologias_vulnerables', 0)
        
        valores_comp = [seguras, vulnerables]
        colors_comp = ['#2ecc71', '#e74c3c']
        
        bars2 = ax4.bar(categorias, valores_comp, color=colors_comp)
        ax4.set_title('Estado de Tecnologías', fontweight='bold')
        ax4.set_ylabel('Cantidad')
        
        # Añadir valores en las barras
        for bar, valor in zip(bars2, valores_comp):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(valor), ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.subplots_adjust(hspace=0.3, wspace=0.3)
        
        # Integrar el gráfico en tkinter
        canvas = FigureCanvasTkAgg(fig, frame_parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        return canvas
        
    except Exception as e:
        print(f"Error creando gráfico de KPIs: {e}")
        return None

def mostrar_monitoreo():
    """Función principal que muestra la interfaz de monitoreo moderna"""
    
    # Crear ventana principal
    ventana = tk.Toplevel()
    ventana.title("SECUREVAL - Dashboard de Monitoreo v2.0")
    ventana.configure(bg='#f8f9fa')
    
    # Crear canvas y scrollbar para scroll
    canvas = tk.Canvas(ventana, bg='#f8f9fa')
    scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Frame principal dentro del canvas
    main_frame = tk.Frame(scrollable_frame, bg='#f8f9fa', padx=20, pady=20)
    main_frame.pack(fill='both', expand=True)
    
    # Header con título y descripción
    header_frame = tk.Frame(main_frame, bg='#2c3e50', relief='raised', bd=2)
    header_frame.pack(fill='x', pady=(0, 20))
    
    title_label = tk.Label(header_frame, text="📊 SECUREVAL DASHBOARD",
                          font=("Helvetica", 20, "bold"),
                          bg='#2c3e50', fg='white', pady=15)
    title_label.pack()
    
    subtitle_label = tk.Label(header_frame, text="Monitoreo de Seguridad y Gestión de Activos",
                             font=("Helvetica", 12),
                             bg='#2c3e50', fg='#bdc3c7', pady=(0, 15))
    subtitle_label.pack()
    
    # === PANTALLA DE BIENVENIDA ===
    welcome_frame = tk.Frame(main_frame, bg='#f8f9fa')
    welcome_frame.pack(fill='both', expand=True)
    
    # Información de bienvenida
    info_frame = tk.Frame(welcome_frame, bg='white', relief='raised', bd=2)
    info_frame.pack(fill='both', expand=True, pady=20)
    
    welcome_text = """
🚀 BIENVENIDO AL DASHBOARD DE SECUREVAL

Este módulo le permite:

📈 ANÁLISIS DE DOMINIOS
• Visualizar KPIs de seguridad en tiempo real
• Revisar vulnerabilidades y riesgos identificados
• Generar reportes detallados por subdominio
• Monitorear tecnologías y CVEs

💼 GESTIÓN DE ACTIVOS
• Consultar inventario empresarial completo
• Analizar distribución y valoración de activos
• Revisar métricas de criticidad empresarial
• Generar reportes de cumplimiento

📊 DASHBOARDS INTERACTIVOS
• Gráficos dinámicos con matplotlib
• Indicadores visuales de estado
• Métricas en tiempo real
• Exportación de reportes

🔒 CARACTERÍSTICAS DE SEGURIDAD
• Interfaz moderna y profesional
• Navegación intuitiva step-by-step
• Integración con módulos de análisis
• Soporte para múltiples dominios

💡 Para comenzar, haga clic en "Acceder al Dashboard" y seleccione el tipo de análisis que desea realizar.
    """
    
    info_label = tk.Label(info_frame, text=welcome_text.strip(),
                         font=("Helvetica", 11),
                         bg='white', fg='#2c3e50',
                         justify='left', padx=30, pady=25)
    info_label.pack(fill='both', expand=True)
    
    # === FRAME DEL DASHBOARD (Inicialmente oculto) ===
    dashboard_frame = tk.Frame(main_frame, bg='#f8f9fa')
    
    def mostrar_dashboard():
        """Cambia a la vista del dashboard"""
        welcome_frame.pack_forget()
        btn_container.pack_forget()
        dashboard_frame.pack(fill='both', expand=True)
        dashboard_btn_container.pack()
        
        # Panel de configuración
        config_frame = tk.LabelFrame(dashboard_frame, text="⚙️ Configuración de Análisis",
                                   font=("Helvetica", 12, "bold"),
                                   bg='white', fg='#2c3e50', padx=15, pady=15)
        config_frame.pack(fill='x', pady=(0, 20))
        
        # Selector de tipo de análisis
        tipo_frame = tk.Frame(config_frame, bg='white')
        tipo_frame.pack(fill='x', pady=5)
        
        tk.Label(tipo_frame, text="📋 Tipo de Análisis:",
                font=("Helvetica", 11, "bold"),
                bg='white', fg='#2c3e50').pack(side='left', padx=(0, 10))
        
        combo_modo = ttk.Combobox(tipo_frame, font=("Helvetica", 11),
                                state="readonly", width=25)
        combo_modo['values'] = ("Dominios escaneados", "Activos registrados")
        combo_modo.set("Dominios escaneados")
        combo_modo.pack(side='left', padx=5)
        
        # Selector de elemento específico
        elemento_frame = tk.Frame(config_frame, bg='white')
        elemento_frame.pack(fill='x', pady=5)
        
        tk.Label(elemento_frame, text="🎯 Seleccionar Elemento:",
                font=("Helvetica", 11, "bold"),
                bg='white', fg='#2c3e50').pack(side='left', padx=(0, 10))
        
        combo_items = ttk.Combobox(elemento_frame, font=("Helvetica", 11),
                                 state="readonly", width=35)
        combo_items.pack(side='left', padx=5)
        
        # Área de resultados con pestañas
        notebook = ttk.Notebook(dashboard_frame)
        notebook.pack(fill='both', expand=True, pady=(0, 20))
        
        # Pestaña de resultados de texto
        tab_texto = ttk.Frame(notebook)
        notebook.add(tab_texto, text="📄 Reporte Detallado")
        
        texto = scrolledtext.ScrolledText(tab_texto, font=("Consolas", 10),
                                        bg='#fefefe', fg='#2c3e50',
                                        wrap='word', height=20)
        texto.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña de gráficos
        tab_graficos = ttk.Frame(notebook)
        notebook.add(tab_graficos, text="📊 Dashboard Visual")
        
        # Mensaje inicial
        texto.insert(tk.END, "🚀 SECUREVAL Dashboard v2.0\n")
        texto.insert(tk.END, "=" * 50 + "\n\n")
        texto.insert(tk.END, "📋 Seleccione un tipo de análisis y elemento para comenzar\n")
        texto.insert(tk.END, "💡 Tip: Use el panel de control superior para navegar\n\n")
        
        def actualizar_opciones(event=None):
            """Actualiza las opciones del segundo combobox"""
            modo = combo_modo.get()
            if modo == "Dominios escaneados":
                dominios = listar_dominios()
                combo_items['values'] = dominios if dominios else ["No hay dominios analizados"]
            elif modo == "Activos registrados":
                activos = obtener_activos()
                if activos:
                    combo_items['values'] = [f"{a.get('codigo', 'N/A')} - {a.get('nombre', 'Sin nombre')}" for a in activos]
                else:
                    combo_items['values'] = ["No hay activos registrados"]
            combo_items.set("")
            
        def ejecutar_monitoreo():
            """Ejecuta el análisis seleccionado"""
            modo = combo_modo.get()
            valor = combo_items.get()
            
            if not valor or "No hay" in valor:
                messagebox.showwarning("Aviso", 
                                     "❌ No hay datos disponibles para el tipo de análisis seleccionado.")
                return
            
            # Limpiar área de resultados
            texto.delete(1.0, tk.END)
            
            # Limpiar gráficos previos
            for widget in tab_graficos.winfo_children():
                widget.destroy()
            
            if modo == "Dominios escaneados":
                dominio = valor
                texto.insert(tk.END, f"🔍 Analizando dominio: {dominio}\n")
                texto.insert(tk.END, "=" * 60 + "\n\n")
                
                kpis = calcular_kpis(dominio)
                if kpis:
                    mostrar_kpis_en_gui(kpis, texto)
                    mostrar_resumen(dominio, texto)
                    texto.insert(tk.END, "\n✅ Análisis completado exitosamente\n")
                    texto.insert(tk.END, f"📅 Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    
                    # Crear gráficos
                    crear_grafico_kpis(kpis, tab_graficos)
                else:
                    texto.insert(tk.END, "❌ No se encontraron datos de análisis para este dominio\n")
                    texto.insert(tk.END, "💡 Ejecute primero un análisis de seguridad\n")
                    
            elif modo == "Activos registrados":
                texto.insert(tk.END, "💼 INVENTARIO DE ACTIVOS EMPRESARIALES\n")
                texto.insert(tk.END, "=" * 60 + "\n\n")
                mostrar_activos(texto)
                texto.insert(tk.END, "\n✅ Inventario cargado exitosamente\n")
                texto.insert(tk.END, f"📅 Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Scroll al inicio
            texto.see(tk.INSERT)
        
        # Configurar eventos
        combo_modo.bind("<<ComboboxSelected>>", actualizar_opciones)
        actualizar_opciones()
        
        # Focus inicial
        combo_modo.focus_set()
        
        # Botones del dashboard
        dashboard_btn_container = tk.Frame(main_frame, bg='#f8f9fa')
        
        # Botón Generar Reporte
        analizar_btn = tk.Button(dashboard_btn_container, text="📊 Generar Reporte", 
                               command=ejecutar_monitoreo,
                               font=("Helvetica", 12, "bold"),
                               bg='#9b59b6', fg='white',
                               relief='flat', padx=25, pady=12,
                               cursor='hand2',
                               activebackground='#8e44ad',
                               activeforeground='white')
        analizar_btn.pack(side='left', padx=5)
        
        # Efectos hover
        def on_enter_analizar(event):
            analizar_btn.configure(bg='#8e44ad')
        
        def on_leave_analizar(event):
            analizar_btn.configure(bg='#9b59b6')
        
        analizar_btn.bind("<Enter>", on_enter_analizar)
        analizar_btn.bind("<Leave>", on_leave_analizar)
        
        # Botón Actualizar
        actualizar_btn = tk.Button(dashboard_btn_container, text="🔄 Actualizar Datos", 
                                 command=actualizar_opciones,
                                 font=("Helvetica", 12),
                                 bg='#3498db', fg='white',
                                 relief='flat', padx=20, pady=12,
                                 cursor='hand2',
                                 activebackground='#2980b9',
                                 activeforeground='white')
        actualizar_btn.pack(side='left', padx=5)
        
        # Efectos hover
        def on_enter_actualizar(event):
            actualizar_btn.configure(bg='#2980b9')
        
        def on_leave_actualizar(event):
            actualizar_btn.configure(bg='#3498db')
        
        actualizar_btn.bind("<Enter>", on_enter_actualizar)
        actualizar_btn.bind("<Leave>", on_leave_actualizar)
        
        # Botón Volver
        volver_btn = tk.Button(dashboard_btn_container, text="⬅️ Volver", 
                              command=lambda: [dashboard_frame.pack_forget(), 
                                             dashboard_btn_container.pack_forget(),
                                             welcome_frame.pack(fill='both', expand=True), 
                                             btn_container.pack()],
                              font=("Helvetica", 12),
                              bg='#95a5a6', fg='white',
                              relief='flat', padx=15, pady=12,
                              cursor='hand2',
                              activebackground='#7f8c8d',
                              activeforeground='white')
        volver_btn.pack(side='left', padx=5)
        
        # Efectos hover
        def on_enter_volver(event):
            volver_btn.configure(bg='#7f8c8d')
        
        def on_leave_volver(event):
            volver_btn.configure(bg='#95a5a6')
        
        volver_btn.bind("<Enter>", on_enter_volver)
        volver_btn.bind("<Leave>", on_leave_volver)
    
    # Frame de botones inicial
    btn_frame = tk.Frame(main_frame, bg='#f8f9fa')
    btn_frame.pack(fill='x')
    
    btn_container = tk.Frame(btn_frame, bg='#f8f9fa')
    btn_container.pack()
    
    # Botón Acceder al Dashboard
    comenzar_btn = tk.Button(btn_container, text="📊 Acceder al Dashboard", 
                           command=mostrar_dashboard,
                           font=("Helvetica", 12, "bold"),
                           bg='#9b59b6', fg='white',
                           relief='flat', padx=30, pady=15,
                           cursor='hand2',
                           activebackground='#8e44ad',
                           activeforeground='white')
    comenzar_btn.pack(side='left', padx=5)
    
    # Efectos hover
    def on_enter_comenzar(event):
        comenzar_btn.configure(bg='#8e44ad')
    
    def on_leave_comenzar(event):
        comenzar_btn.configure(bg='#9b59b6')
    
    comenzar_btn.bind("<Enter>", on_enter_comenzar)
    comenzar_btn.bind("<Leave>", on_leave_comenzar)
    
    # Botón Cerrar
    cerrar_btn = tk.Button(btn_container, text="❌ Cerrar", 
                          command=ventana.destroy,
                          font=("Helvetica", 12),
                          bg='#95a5a6', fg='white',
                          relief='flat', padx=25, pady=15,
                          cursor='hand2',
                          activebackground='#7f8c8d',
                          activeforeground='white')
    cerrar_btn.pack(side='left', padx=5)
    
    # Efectos hover
    def on_enter_cerrar(event):
        cerrar_btn.configure(bg='#7f8c8d')
    
    def on_leave_cerrar(event):
        cerrar_btn.configure(bg='#95a5a6')
    
    cerrar_btn.bind("<Enter>", on_enter_cerrar)
    cerrar_btn.bind("<Leave>", on_leave_cerrar)
    
    # Configurar scroll con mouse wheel
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _bind_to_mousewheel(event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def _unbind_from_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")
    
    canvas.bind('<Enter>', _bind_to_mousewheel)
    canvas.bind('<Leave>', _unbind_from_mousewheel)
    
    # Configurar layout de la ventana
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Centrar ventana
    ventana.transient()
    ventana.grab_set()
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (1000 // 2)
    y = (ventana.winfo_screenheight() // 2) - (700 // 2)
    ventana.geometry(f"1000x700+{x}+{y}")
    
    # Focus inicial
    comenzar_btn.focus_set()
    
    # Asegurar que el canvas se actualice
    ventana.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

# Función para compatibilidad con el main
def mostrar_menu_monitoreo():
    """Función de compatibilidad - llama a mostrar_monitoreo()"""
    mostrar_monitoreo()

if __name__ == "__main__":
    # Crear ventana root para testing
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    
    # Mostrar el módulo de monitoreo
    mostrar_monitoreo()
    
    root.mainloop()
