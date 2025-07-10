# app/main.py (Aplicación principal de SECUREVAL v2.0)
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Importaciones locales con rutas relativas del paquete app
from app.activos import registrar_activo_gui
from app.analyzer import lanzar_analyzer_gui
from app.export_pdf import abrir_selector_exportacion_pdf
from app.monitoreo import mostrar_menu_monitoreo
from app.tratamiento import lanzar_tratamiento_gui

# Variables globales
root = None
console_text = None
original_stdout = None

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)

    def flush(self):
        pass

def ejecutar_analisis():
    """Lanza el módulo de análisis"""
    print("🔍 Iniciando módulo de Análisis de Seguridad...")
    print("📋 Abriendo interfaz de configuración de análisis")
    lanzar_analyzer_gui()

def gestionar_activos():
    """Lanza el módulo de gestión de activos"""
    print("🎯 Iniciando módulo de Gestión de Activos")
    print("📝 Abriendo formulario de registro de activos")
    registrar_activo_gui()

def mostrar_monitoreo():
    """Lanza el módulo de monitoreo"""
    print("📊 Iniciando módulo de Monitoreo")
    print("📈 Cargando dashboard de análisis")
    mostrar_menu_monitoreo()

def ejecutar_tratamiento():
    """Lanza el módulo de tratamiento de riesgos"""
    print("🛡️ Iniciando módulo de Tratamiento de Riesgos")
    print("📄 Preparando análisis textual de vulnerabilidades")
    lanzar_tratamiento_gui()

def exportar_pdf_integrado():
    """Exporta los resultados del análisis a PDF con selector de dominio"""
    print("📄 Iniciando módulo de Exportación PDF")
    print("📋 Abriendo selector de dominios disponibles")
    abrir_selector_exportacion_pdf(root)

def mostrar_info_modulos():
    """Muestra información detallada sobre los módulos del sistema"""
    print("ℹ️ Abriendo información de módulos del sistema")
    print("📋 Mostrando detalles de funcionalidades disponibles")
    ventana_info = tk.Toplevel()
    ventana_info.title("ℹ️ Información de Módulos - SECUREVAL")
    ventana_info.geometry("800x600")
    ventana_info.configure(bg='#f8f9fa')
    ventana_info.resizable(True, True)
    
    # Frame principal con scroll
    main_frame = tk.Frame(ventana_info, bg='#f8f9fa')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Header
    header_frame = tk.Frame(main_frame, bg='#17a2b8', relief='solid', borderwidth=1)
    header_frame.pack(fill='x', pady=(0, 20))
    
    tk.Label(header_frame, 
             text="ℹ️ INFORMACIÓN DE MÓDULOS SECUREVAL", 
             font=("Helvetica", 16, "bold"), 
             bg='#17a2b8', fg='white').pack(pady=15)
    
    # Canvas para scroll
    canvas = tk.Canvas(main_frame, bg='#f8f9fa', highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Contenido de información
    content_frame = tk.Frame(scrollable_frame, bg='#f8f9fa')
    content_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    modulos_info = [
        {
            "nombre": "🎯 Gestión de Activos",
            "descripcion": "Registro y administración del inventario de activos organizacionales",
            "funciones": [
                "📝 Registro de activos con formulario completo",
                "📊 Evaluación CIA (Confidencialidad, Integridad, Disponibilidad)",
                "🏷️ Clasificación por tipo y estado",
                "👤 Asignación de propietarios y áreas responsables",
                "💾 Almacenamiento en formato JSON estructurado"
            ]
        },
        {
            "nombre": "🔍 Análisis de Seguridad",
            "descripcion": "Evaluación automatizada de vulnerabilidades y tecnologías",
            "funciones": [
                "🔎 Descubrimiento de subdominios con AssetFinder",
                "🛠️ Identificación de tecnologías con WhatWeb",
                "🛡️ Escaneo de puertos con Nmap",
                "🔒 Verificación de certificados TLS/SSL",
                "⚠️ Búsqueda de CVEs en base NIST NVD",
                "📊 Evaluación de riesgos según metodología SECUREVAL"
            ]
        },
        {
            "nombre": "📊 Monitoreo",
            "descripcion": "Visualización en tiempo real del estado de seguridad",
            "funciones": [
                "📈 Dashboard interactivo de métricas",
                "🎨 Gráficos de distribución de riesgos",
                "📋 Tablas de activos y vulnerabilidades",
                "🔄 Actualización automática de datos",
                "🎯 Indicadores de estado en tiempo real"
            ]
        },
        {
            "nombre": "🛡️ Tratamiento de Riesgos",
            "descripcion": "Análisis textual y recomendaciones de mitigación",
            "funciones": [
                "📄 Análisis textual detallado de vulnerabilidades",
                "🎯 Evaluación de criticidad por activo",
                "📋 Listado de CVEs y puntuaciones CVSS",
                "💡 Recomendaciones de tratamiento",
                "🔍 Navegación por subdominios analizados"
            ]
        },
        {
            "nombre": "📄 Exportación PDF",
            "descripcion": "Generación de reportes profesionales",
            "funciones": [
                "📊 Reporte ejecutivo con métricas clave",
                "📋 Tablas detalladas de vulnerabilidades",
                "🎨 Gráficos de distribución de riesgos",
                "📈 Estadísticas de tecnologías detectadas",
                "🔒 Información de certificados TLS",
                "📱 Formato responsive y profesional"
            ]
        }
    ]
    
    for modulo in modulos_info:
        # Frame para cada módulo
        modulo_frame = tk.Frame(content_frame, bg='white', relief='solid', borderwidth=1)
        modulo_frame.pack(fill='x', pady=10)
        
        # Header del módulo
        header_modulo = tk.Frame(modulo_frame, bg='#495057')
        header_modulo.pack(fill='x')
        
        tk.Label(header_modulo, 
                 text=modulo["nombre"], 
                 font=("Helvetica", 12, "bold"), 
                 bg='#495057', fg='white').pack(pady=10)
        
        # Descripción
        tk.Label(modulo_frame, 
                 text=modulo["descripcion"], 
                 font=("Helvetica", 10, "italic"), 
                 bg='white', fg='#6c757d').pack(pady=(10, 5), padx=15)
        
        # Funciones
        func_frame = tk.Frame(modulo_frame, bg='white')
        func_frame.pack(fill='x', padx=15, pady=(5, 15))
        
        for funcion in modulo["funciones"]:
            tk.Label(func_frame, 
                     text=f"  • {funcion}", 
                     font=("Helvetica", 9), 
                     bg='white', fg='#495057').pack(anchor='w', pady=1)
    
    # Botón cerrar
    btn_frame = tk.Frame(main_frame, bg='#f9f9fa')
    btn_frame.pack(fill='x', pady=(20, 0))
    
    cerrar_btn = tk.Button(btn_frame, 
                          text="❌ Cerrar", 
                          command=ventana_info.destroy,
                          font=("Helvetica", 11, "bold"),
                          bg='#6c757d', fg='white',
                          relief='flat', padx=20, pady=8,
                          cursor='hand2')
    cerrar_btn.pack()
    
    # Configurar scroll con mouse wheel
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _bind_to_mousewheel(event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def _unbind_from_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")
    
    canvas.bind('<Enter>', _bind_to_mousewheel)
    canvas.bind('<Leave>', _unbind_from_mousewheel)
    
    # Centrar ventana
    ventana_info.transient()
    ventana_info.grab_set()
    ventana_info.update_idletasks()
    x = (ventana_info.winfo_screenwidth() // 2) - (800 // 2)
    y = (ventana_info.winfo_screenheight() // 2) - (600 // 2)
    ventana_info.geometry(f"800x600+{x}+{y}")

def mostrar_bienvenida():
    """Muestra la pantalla de bienvenida principal"""
    # Limpiar ventana principal
    for widget in root.winfo_children():
        widget.destroy()
    
    # Configurar ventana principal
    root.configure(bg='#2c3e50')
    
    # Frame principal
    main_frame = tk.Frame(root, bg='#2c3e50')
    main_frame.pack(fill='both', expand=True)
    
    # Header principal con gradiente visual
    header_frame = tk.Frame(main_frame, bg='#34495e', height=120)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)
    
    # Logo y título principal
    logo_frame = tk.Frame(header_frame, bg='#34495e')
    logo_frame.pack(expand=True)
    
    titulo_principal = tk.Label(logo_frame, 
                               text="🔐 SECUREVAL", 
                               font=("Helvetica", 28, "bold"), 
                               bg='#34495e', fg='#ecf0f1')
    titulo_principal.pack(pady=(20, 5))
    
    subtitulo = tk.Label(logo_frame, 
                        text="Sistema Integral de Evaluación de Seguridad v2.0", 
                        font=("Helvetica", 12), 
                        bg='#34495e', fg='#bdc3c7')
    subtitulo.pack()
    
    # Frame de contenido principal
    content_frame = tk.Frame(main_frame, bg='#ecf0f1')
    content_frame.pack(fill='both', expand=True, padx=40, pady=30)
    
    # Mensaje de bienvenida
    welcome_frame = tk.Frame(content_frame, bg='#ecf0f1')
    welcome_frame.pack(fill='x', pady=(0, 30))
    
    welcome_text = tk.Label(welcome_frame, 
                           text="¡Bienvenido al Sistema de Evaluación de Seguridad más Avanzado!", 
                           font=("Helvetica", 16, "bold"), 
                           bg='#ecf0f1', fg='#2c3e50')
    welcome_text.pack(pady=(0, 10))
    
    desc_text = tk.Label(welcome_frame, 
                        text="SECUREVAL le permite realizar análisis completos de vulnerabilidades,\n"
                             "gestionar activos organizacionales y generar reportes profesionales.", 
                        font=("Helvetica", 11), 
                        bg='#ecf0f1', fg='#34495e')
    desc_text.pack()
    
    # Botones de módulos principales
    botones_frame = tk.Frame(content_frame, bg='#ecf0f1')
    botones_frame.pack(expand=True)
    
    # Configuración de botones con sus colores y funciones
    botones_config = [
        ("🎯 Gestión de Activos", "#27ae60", gestionar_activos),
        ("🔍 Análisis de Seguridad", "#e74c3c", ejecutar_analisis),
        ("📊 Monitoreo", "#3498db", mostrar_monitoreo),
        ("🛡️ Tratamiento de Riesgos", "#9b59b6", ejecutar_tratamiento),
        ("📄 Exportar PDF", "#f39c12", exportar_pdf_integrado),
        ("📈 Monitor Sistema", "#e67e22", mostrar_monitor_actividad),
        ("ℹ️ Información", "#17a2b8", mostrar_info_modulos)
    ]
    
    # Crear botones en grid 3x3 (ajustado para 7 botones)
    for i, (texto, color, comando) in enumerate(botones_config):
        if i < 6:  # Primeros 6 botones en grid 2x3
            row = i // 3
            col = i % 3
        else:  # Último botón centrado en la fila inferior
            row = 2
            col = 1
        
        btn = tk.Button(botones_frame, 
                       text=texto,
                       command=comando,
                       font=("Helvetica", 12, "bold"),
                       bg=color, fg='white',
                       relief='flat',
                       padx=20, pady=15,
                       cursor='hand2',
                       width=18)
        btn.grid(row=row, column=col, padx=15, pady=10, sticky='ew')
        
        # Efectos hover
        def on_enter(event, btn=btn, color=color):
            # Oscurecer el color para el hover
            if color == "#27ae60": hover_color = "#219a52"
            elif color == "#e74c3c": hover_color = "#c0392b"
            elif color == "#3498db": hover_color = "#2980b9"
            elif color == "#9b59b6": hover_color = "#8e44ad"
            elif color == "#f39c12": hover_color = "#e67e22"
            elif color == "#17a2b8": hover_color = "#138496"
            else: hover_color = "#34495e"
            btn.configure(bg=hover_color)
        
        def on_leave(event, btn=btn, color=color):
            btn.configure(bg=color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    # Configurar grid weights para responsividad
    botones_frame.grid_columnconfigure(0, weight=1)
    botones_frame.grid_columnconfigure(1, weight=1)
    botones_frame.grid_columnconfigure(2, weight=1)
    
    # Consola de salida
    console_frame = tk.Frame(main_frame, bg='#2c3e50')
    console_frame.pack(fill='x', padx=20, pady=(20, 10))
    
    # Header de la consola
    console_header = tk.Frame(console_frame, bg='#34495e', height=30)
    console_header.pack(fill='x')
    console_header.pack_propagate(False)
    
    tk.Label(console_header, 
             text="💻 Consola del Sistema", 
             font=("Helvetica", 10, "bold"), 
             bg='#34495e', fg='#ecf0f1').pack(side='left', padx=10, pady=5)
    
    # Botón para limpiar consola
    clear_btn = tk.Button(console_header, 
                         text="🗑️ Limpiar", 
                         command=lambda: console_text.delete(1.0, tk.END),
                         font=("Helvetica", 8),
                         bg='#95a5a6', fg='white',
                         relief='flat', padx=8, pady=2,
                         cursor='hand2')
    clear_btn.pack(side='right', padx=10, pady=3)
    
    # Area de texto de la consola
    console_text_frame = tk.Frame(console_frame, bg='#2c3e50')
    console_text_frame.pack(fill='x')
    
    global console_text
    console_text = tk.Text(console_text_frame,
                          height=8,
                          font=("Consolas", 9),
                          bg='#1e1e1e', fg='#00ff00',
                          relief='solid', borderwidth=1,
                          wrap='word')
    
    console_scrollbar = ttk.Scrollbar(console_text_frame, orient="vertical", command=console_text.yview)
    console_text.configure(yscrollcommand=console_scrollbar.set)
    
    console_text.pack(side="left", fill="both", expand=True)
    console_scrollbar.pack(side="right", fill="y")
    
    # Configurar redirección de stdout
    global original_stdout
    original_stdout = sys.stdout
    sys.stdout = TextRedirector(console_text)
    
    # Mensaje de bienvenida en la consola
    print("🔐 SECUREVAL v2.0 - Sistema de Evaluación de Seguridad")
    print("=" * 50)
    print("✅ Sistema iniciado correctamente")
    print("📋 Seleccione un módulo del menú superior para comenzar")
    print("💡 Los mensajes del sistema aparecerán aquí")
    print("")
    
    # Footer
    footer_frame = tk.Frame(main_frame, bg='#34495e', height=40)
    footer_frame.pack(fill='x')
    footer_frame.pack_propagate(False)
    
    footer_text = tk.Label(footer_frame, 
                          text="📝 Desarrollado por: Bonilla • Camacho • Morales • Paqui | 📅 2025 | 🏢 SECUREVAL v2.0", 
                          font=("Helvetica", 9), 
                          bg='#34495e', fg='#ecf0f1')
    footer_text.pack(pady=10)

def ejecutar_app():
    """Función principal que inicia la aplicación"""
    global root
    
    # Crear ventana principal
    root = tk.Tk()
    root.title("🔐 SECUREVAL - Sistema de Evaluación de Seguridad v2.0")
    root.geometry("1000x700")
    root.configure(bg='#2c3e50')
    
    # Configurar ventana
    root.minsize(800, 600)
    
    # Configurar cierre de aplicación
    def on_closing():
        global original_stdout
        if messagebox.askokcancel("Salir", "¿Está seguro de que desea salir de SECUREVAL?"):
            # Restaurar stdout original
            if original_stdout:
                sys.stdout = original_stdout
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Centrar ventana
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Atajos de teclado
    def toggle_fullscreen(event=None):
        root.attributes("-fullscreen", not root.attributes("-fullscreen"))
    
    def exit_fullscreen(event=None):
        root.attributes("-fullscreen", False)
    
    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Escape>", exit_fullscreen)
    
    # Mostrar pantalla de bienvenida
    root.after(100, mostrar_bienvenida)
    
    # Iniciar bucle principal
    root.mainloop()

def mostrar_monitor_actividad():
    """Monitor de actividad del sistema en tiempo real"""
    print("📊 Iniciando Monitor de Actividad del Sistema")
    print("⚙️ Verificando disponibilidad de dependencias...")
    
    import os
    import json
    import threading
    import time
    from datetime import datetime
    
    # Intentar importar psutil, usar alternativas si no está disponible
    try:
        import psutil
        PSUTIL_DISPONIBLE = True
        print("✅ psutil disponible - Monitor completo habilitado")
    except ImportError:
        PSUTIL_DISPONIBLE = False
        print("⚠️ psutil no disponible - Monitor con funcionalidad limitada")
        messagebox.showwarning("Dependencia Faltante", 
                              "⚠️ La librería 'psutil' no está instalada.\n"
                              "El monitor mostrará información limitada.\n\n"
                              "Para funcionalidad completa, instale: pip install psutil")
    
    monitor_window = tk.Toplevel()
    monitor_window.title("📊 Monitor de Actividad del Sistema - SECUREVAL")
    monitor_window.geometry("900x700")
    monitor_window.configure(bg='#2c3e50')
    monitor_window.resizable(True, True)
    
    # Frame principal
    main_frame = tk.Frame(monitor_window, bg='#2c3e50')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Header
    header_frame = tk.Frame(main_frame, bg='#34495e', relief='solid', borderwidth=1)
    header_frame.pack(fill='x', pady=(0, 20))
    
    tk.Label(header_frame, 
             text="📊 MONITOR DE ACTIVIDAD DEL SISTEMA", 
             font=("Helvetica", 16, "bold"), 
             bg='#34495e', fg='#ecf0f1').pack(pady=15)
    
    # Crear notebook para pestañas
    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill='both', expand=True)
    
    # Pestaña 1: Estado del Sistema
    sistema_frame = tk.Frame(notebook, bg='white')
    notebook.add(sistema_frame, text="💻 Sistema")
    
    # Pestaña 2: Análisis Realizados
    analisis_frame = tk.Frame(notebook, bg='white')
    notebook.add(analisis_frame, text="🔍 Análisis")
    
    # Pestaña 3: Estadísticas
    stats_frame = tk.Frame(notebook, bg='white')
    notebook.add(stats_frame, text="📈 Estadísticas")
    
    # === PESTAÑA SISTEMA ===
    sistema_content = tk.Frame(sistema_frame, bg='white')
    sistema_content.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Información del sistema
    sys_info_frame = tk.Frame(sistema_content, bg='#f8f9fa', relief='solid', borderwidth=1)
    sys_info_frame.pack(fill='x', pady=(0, 20))
    
    tk.Label(sys_info_frame, 
             text="💻 Información del Sistema", 
             font=("Helvetica", 12, "bold"), 
             bg='#f8f9fa', fg='#495057').pack(pady=(10, 5))
    
    # Labels para información del sistema
    cpu_label = tk.Label(sys_info_frame, text="🔲 CPU: Cargando...", 
                        font=("Consolas", 10), bg='#f8f9fa', fg='#495057')
    cpu_label.pack(anchor='w', padx=15, pady=2)
    
    memoria_label = tk.Label(sys_info_frame, text="🧠 Memoria: Cargando...", 
                            font=("Consolas", 10), bg='#f8f9fa', fg='#495057')
    memoria_label.pack(anchor='w', padx=15, pady=2)
    
    disco_label = tk.Label(sys_info_frame, text="💾 Disco: Cargando...", 
                          font=("Consolas", 10), bg='#f8f9fa', fg='#495057')
    disco_label.pack(anchor='w', padx=15, pady=2)
    
    uptime_label = tk.Label(sys_info_frame, text="⏰ Tiempo activo: Cargando...", 
                           font=("Consolas", 10), bg='#f8f9fa', fg='#495057')
    uptime_label.pack(anchor='w', padx=15, pady=2)
    
    # Progreso de recursos
    progress_frame = tk.Frame(sys_info_frame, bg='#f8f9fa')
    progress_frame.pack(fill='x', padx=15, pady=10)
    
    # Barra de CPU
    tk.Label(progress_frame, text="CPU:", font=("Helvetica", 9), 
             bg='#f8f9fa', fg='#495057').grid(row=0, column=0, sticky='w', padx=(0, 10))
    cpu_progress = ttk.Progressbar(progress_frame, length=200, mode='determinate')
    cpu_progress.grid(row=0, column=1, sticky='ew', padx=5)
    
    # Barra de Memoria
    tk.Label(progress_frame, text="RAM:", font=("Helvetica", 9), 
             bg='#f8f9fa', fg='#495057').grid(row=1, column=0, sticky='w', padx=(0, 10), pady=(5, 0))
    mem_progress = ttk.Progressbar(progress_frame, length=200, mode='determinate')
    mem_progress.grid(row=1, column=1, sticky='ew', padx=5, pady=(5, 0))
    
    progress_frame.grid_columnconfigure(1, weight=1)
    
    # === PESTAÑA ANÁLISIS ===
    analisis_content = tk.Frame(analisis_frame, bg='white')
    analisis_content.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Lista de análisis
    tk.Label(analisis_content, 
             text="🔍 Análisis Realizados", 
             font=("Helvetica", 12, "bold"), 
             bg='white', fg='#495057').pack(pady=(0, 10))
    
    # Frame con scroll para la lista
    list_frame = tk.Frame(analisis_content, bg='white')
    list_frame.pack(fill='both', expand=True)
    
    # Canvas para scroll
    canvas_analisis = tk.Canvas(list_frame, bg='white', highlightthickness=0)
    scrollbar_analisis = ttk.Scrollbar(list_frame, orient="vertical", command=canvas_analisis.yview)
    scrollable_analisis = tk.Frame(canvas_analisis, bg='white')
    
    scrollable_analisis.bind(
        "<Configure>",
        lambda e: canvas_analisis.configure(scrollregion=canvas_analisis.bbox("all"))
    )
    
    canvas_analisis.create_window((0, 0), window=scrollable_analisis, anchor="nw")
    canvas_analisis.configure(yscrollcommand=scrollbar_analisis.set)
    
    canvas_analisis.pack(side="left", fill="both", expand=True)
    scrollbar_analisis.pack(side="right", fill="y")
    
    # === PESTAÑA ESTADÍSTICAS ===
    stats_content = tk.Frame(stats_frame, bg='white')
    stats_content.pack(fill='both', expand=True, padx=20, pady=20)
    
    tk.Label(stats_content, 
             text="📈 Estadísticas del Sistema", 
             font=("Helvetica", 12, "bold"), 
             bg='white', fg='#495057').pack(pady=(0, 20))
    
    # Frame para estadísticas
    stats_info_frame = tk.Frame(stats_content, bg='#f8f9fa', relief='solid', borderwidth=1)
    stats_info_frame.pack(fill='both', expand=True)
    
    stats_text = tk.Text(stats_info_frame, 
                        font=("Consolas", 10),
                        bg='#f8f9fa', fg='#495057',
                        relief='flat', wrap='word')
    stats_scroll = ttk.Scrollbar(stats_info_frame, orient="vertical", command=stats_text.yview)
    stats_text.configure(yscrollcommand=stats_scroll.set)
    
    stats_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    stats_scroll.pack(side="right", fill="y")
    
    # Variables de control
    monitor_activo = {'activo': True}
    
    def actualizar_sistema():
        """Actualiza la información del sistema"""
        try:
            if PSUTIL_DISPONIBLE:
                # CPU
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_label.config(text=f"🔲 CPU: {cpu_percent:.1f}%")
                cpu_progress['value'] = cpu_percent
                
                # Memoria
                memoria = psutil.virtual_memory()
                mem_percent = memoria.percent
                mem_used = memoria.used / (1024**3)  # GB
                mem_total = memoria.total / (1024**3)  # GB
                memoria_label.config(text=f"🧠 Memoria: {mem_used:.1f}GB / {mem_total:.1f}GB ({mem_percent:.1f}%)")
                mem_progress['value'] = mem_percent
                
                # Disco
                disco = psutil.disk_usage('/')
                disk_percent = (disco.used / disco.total) * 100
                disk_used = disco.used / (1024**3)  # GB
                disk_total = disco.total / (1024**3)  # GB
                disco_label.config(text=f"💾 Disco: {disk_used:.1f}GB / {disk_total:.1f}GB ({disk_percent:.1f}%)")
                
                # Tiempo activo
                boot_time = datetime.fromtimestamp(psutil.boot_time())
                uptime = datetime.now() - boot_time
                dias = uptime.days
                horas, remainder = divmod(uptime.seconds, 3600)
                minutos, _ = divmod(remainder, 60)
                uptime_label.config(text=f"⏰ Tiempo activo: {dias}d {horas}h {minutos}m")
            else:
                # Información limitada sin psutil
                cpu_label.config(text="🔲 CPU: Información no disponible (instalar psutil)")
                cpu_progress['value'] = 0
                memoria_label.config(text="🧠 Memoria: Información no disponible (instalar psutil)")
                mem_progress['value'] = 0
                disco_label.config(text="💾 Disco: Información no disponible (instalar psutil)")
                uptime_label.config(text="⏰ Tiempo activo: Información no disponible (instalar psutil)")
            
        except Exception as e:
            print(f"Error actualizando sistema: {e}")
            cpu_label.config(text=f"🔲 CPU: Error - {str(e)[:30]}...")
            memoria_label.config(text=f"🧠 Memoria: Error - {str(e)[:30]}...")
            disco_label.config(text=f"💾 Disco: Error - {str(e)[:30]}...")
            uptime_label.config(text=f"⏰ Tiempo activo: Error - {str(e)[:30]}...")
    
    def cargar_analisis():
        """Carga la lista de análisis realizados"""
        try:
            resultados_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resultados")
            
            # Limpiar frame
            for widget in scrollable_analisis.winfo_children():
                widget.destroy()
            
            if not os.path.exists(resultados_dir):
                tk.Label(scrollable_analisis, 
                        text="❌ No se encontró carpeta de resultados", 
                        bg='white', fg='#e74c3c').pack(pady=20)
                return
            
            dominios_encontrados = []
            for item in os.listdir(resultados_dir):
                item_path = os.path.join(resultados_dir, item)
                if os.path.isdir(item_path) and item != "__pycache__":
                    if os.path.exists(os.path.join(item_path, "riesgo.json")):
                        dominios_encontrados.append(item)
            
            if not dominios_encontrados:
                tk.Label(scrollable_analisis, 
                        text="📭 No se encontraron análisis previos", 
                        bg='white', fg='#6c757d').pack(pady=20)
                return
            
            for dominio in dominios_encontrados:
                # Frame para cada análisis
                item_frame = tk.Frame(scrollable_analisis, bg='#e9ecef', relief='solid', borderwidth=1)
                item_frame.pack(fill='x', padx=10, pady=5)
                
                # Header del dominio
                header_dom = tk.Frame(item_frame, bg='#495057')
                header_dom.pack(fill='x')
                
                tk.Label(header_dom, 
                        text=f"🌐 {dominio}", 
                        font=("Helvetica", 11, "bold"), 
                        bg='#495057', fg='white').pack(pady=8)
                
                # Información del análisis
                info_dom = tk.Frame(item_frame, bg='#e9ecef')
                info_dom.pack(fill='x', padx=10, pady=10)
                
                # Cargar metadatos si existen
                try:
                    metadata_path = os.path.join(resultados_dir, dominio, "metadata.json")
                    if os.path.exists(metadata_path):
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                        
                        resultados = metadata.get('total_resultados', 'N/A')
                        errores = metadata.get('total_errores', 'N/A')
                        opciones = metadata.get('opciones_utilizadas', {})
                        
                        info_text = f"📊 Resultados: {resultados} | ❌ Errores: {errores}"
                        tk.Label(info_dom, text=info_text, 
                                font=("Helvetica", 9), bg='#e9ecef', fg='#495057').pack(anchor='w')
                        
                        opciones_activas = [k.capitalize() for k, v in opciones.items() if v]
                        if opciones_activas:
                            tk.Label(info_dom, text=f"⚙️ Opciones: {', '.join(opciones_activas)}", 
                                    font=("Helvetica", 9), bg='#e9ecef', fg='#6c757d').pack(anchor='w')
                    
                    # Verificar archivos generados
                    archivos = []
                    dominio_path = os.path.join(resultados_dir, dominio)
                    for archivo in ['riesgo.json', 'metadata.json', 'resumen.json', 'riesgo.pdf']:
                        if os.path.exists(os.path.join(dominio_path, archivo)):
                            archivos.append(archivo)
                    
                    if archivos:
                        tk.Label(info_dom, text=f"📁 Archivos: {', '.join(archivos)}", 
                                font=("Helvetica", 8), bg='#e9ecef', fg='#6c757d').pack(anchor='w')
                    
                except Exception as e:
                    tk.Label(info_dom, text=f"❌ Error cargando información: {str(e)[:50]}...", 
                            font=("Helvetica", 9), bg='#e9ecef', fg='#e74c3c').pack(anchor='w')
                
        except Exception as e:
            tk.Label(scrollable_analisis, 
                    text=f"❌ Error cargando análisis: {str(e)}", 
                    bg='white', fg='#e74c3c').pack(pady=20)
    
    def cargar_estadisticas():
        """Carga estadísticas generales del sistema"""
        try:
            stats_text.delete(1.0, tk.END)
            
            # Estadísticas del sistema SECUREVAL
            stats_text.insert(tk.END, "═══════════════════════════════════════\n")
            stats_text.insert(tk.END, "📊 ESTADÍSTICAS DEL SISTEMA SECUREVAL\n")
            stats_text.insert(tk.END, "═══════════════════════════════════════\n\n")
            
            # Información de archivos
            resultados_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resultados")
            
            if os.path.exists(resultados_dir):
                # Contar dominios analizados
                dominios = [d for d in os.listdir(resultados_dir) 
                           if os.path.isdir(os.path.join(resultados_dir, d)) and d != "__pycache__"]
                
                stats_text.insert(tk.END, f"🌐 Dominios analizados: {len(dominios)}\n")
                
                # Estadísticas de activos
                activos_path = os.path.join(resultados_dir, "activos.json")
                if os.path.exists(activos_path):
                    with open(activos_path, 'r') as f:
                        activos = json.load(f)
                    stats_text.insert(tk.END, f"🎯 Activos registrados: {len(activos)}\n")
                else:
                    stats_text.insert(tk.END, "🎯 Activos registrados: 0\n")
                
                # Estadísticas por dominio
                stats_text.insert(tk.END, "\n📋 DETALLES POR DOMINIO:\n")
                stats_text.insert(tk.END, "─" * 50 + "\n")
                
                total_resultados = 0
                total_errores = 0
                
                for dominio in dominios:
                    dominio_path = os.path.join(resultados_dir, dominio)
                    metadata_path = os.path.join(dominio_path, "metadata.json")
                    
                    if os.path.exists(metadata_path):
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                        
                        resultados = metadata.get('total_resultados', 0)
                        errores = metadata.get('total_errores', 0)
                        
                        total_resultados += resultados
                        total_errores += errores
                        
                        stats_text.insert(tk.END, f"\n🌐 {dominio}:\n")
                        stats_text.insert(tk.END, f"   📊 Resultados: {resultados}\n")
                        stats_text.insert(tk.END, f"   ❌ Errores: {errores}\n")
                        
                        # Archivos generados
                        archivos = []
                        for archivo in os.listdir(dominio_path):
                            if archivo.endswith(('.json', '.txt', '.pdf', '.log')):
                                archivos.append(archivo)
                        
                        stats_text.insert(tk.END, f"   📁 Archivos: {len(archivos)}\n")
                
                # Totales
                stats_text.insert(tk.END, "\n" + "═" * 50 + "\n")
                stats_text.insert(tk.END, "📈 TOTALES GENERALES:\n")
                stats_text.insert(tk.END, f"   📊 Total resultados: {total_resultados}\n")
                stats_text.insert(tk.END, f"   ❌ Total errores: {total_errores}\n")
                
                if total_resultados > 0:
                    tasa_error = (total_errores / (total_resultados + total_errores)) * 100
                    stats_text.insert(tk.END, f"   📉 Tasa de errores: {tasa_error:.2f}%\n")
            
            else:
                stats_text.insert(tk.END, "❌ No se encontró carpeta de resultados\n")
            
            # Información del directorio actual
            stats_text.insert(tk.END, f"\n📁 Directorio de trabajo: {os.getcwd()}\n")
            stats_text.insert(tk.END, f"🕐 Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
        except Exception as e:
            stats_text.delete(1.0, tk.END)
            stats_text.insert(tk.END, f"❌ Error cargando estadísticas: {str(e)}\n")
    
    def monitor_loop():
        """Bucle principal del monitor"""
        while monitor_activo['activo']:
            try:
                if monitor_window.winfo_exists():
                    actualizar_sistema()
                    time.sleep(3)  # Actualizar cada 3 segundos
                else:
                    break
            except:
                break
    
    def on_closing():
        """Manejar cierre de ventana"""
        monitor_activo['activo'] = False
        monitor_window.destroy()
    
    # Configurar cierre
    monitor_window.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Cargar datos iniciales
    cargar_analisis()
    cargar_estadisticas()
    
    # Iniciar thread de monitoreo
    monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    monitor_thread.start()
    
    # Configurar scroll con mouse wheel para análisis
    def _on_mousewheel_analisis(event):
        canvas_analisis.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _bind_to_mousewheel_analisis(event):
        canvas_analisis.bind_all("<MouseWheel>", _on_mousewheel_analisis)
    
    def _unbind_from_mousewheel_analisis(event):
        canvas_analisis.unbind_all("<MouseWheel>")
    
    canvas_analisis.bind('<Enter>', _bind_to_mousewheel_analisis)
    canvas_analisis.bind('<Leave>', _unbind_from_mousewheel_analisis)
    
    # Centrar ventana
    monitor_window.transient()
    monitor_window.grab_set()
    monitor_window.update_idletasks()
    x = (monitor_window.winfo_screenwidth() // 2) - (900 // 2)
    y = (monitor_window.winfo_screenheight() // 2) - (700 // 2)
    monitor_window.geometry(f"900x700+{x}+{y}")

def main():
    """Función principal para iniciar SECUREVAL"""
    ejecutar_app()

if __name__ == "__main__":
    main()
