# app/main.py (Aplicación principal de SECUREVAL v2.0)
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Importaciones locales con rutas relativas del paquete app
from app.activos import registrar_activo_gui
from app.analyzer import lanzar_analyzer_gui
from app.export_pdf import exportar_pdf
from app.monitoreo import mostrar_menu_monitoreo
from app.tratamiento import lanzar_tratamiento_gui

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
    lanzar_analyzer_gui()

def exportar_pdf_integrado():
    """Exporta los resultados del análisis a PDF"""
    try:
        exportar_pdf()
        messagebox.showinfo("Exportación Exitosa", 
                           "✅ El reporte PDF ha sido generado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error de Exportación", 
                           f"❌ Error al generar el PDF:\n{str(e)}")

def mostrar_info_modulos():
    """Muestra información detallada sobre los módulos del sistema"""
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
    btn_frame = tk.Frame(main_frame, bg='#f8f9fa')
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
        ("🎯 Gestión de Activos", "#27ae60", registrar_activo_gui),
        ("🔍 Análisis de Seguridad", "#e74c3c", ejecutar_analisis),
        ("📊 Monitoreo", "#3498db", mostrar_menu_monitoreo),
        ("🛡️ Tratamiento de Riesgos", "#9b59b6", lanzar_tratamiento_gui),
        ("📄 Exportar PDF", "#f39c12", exportar_pdf_integrado),
        ("ℹ️ Información", "#17a2b8", mostrar_info_modulos)
    ]
    
    # Crear botones en grid 2x3
    for i, (texto, color, comando) in enumerate(botones_config):
        row = i // 3
        col = i % 3
        
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
        if messagebox.askokcancel("Salir", "¿Está seguro de que desea salir de SECUREVAL?"):
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

def main():
    """Función principal para iniciar SECUREVAL"""
    ejecutar_app()

if __name__ == "__main__":
    main()
