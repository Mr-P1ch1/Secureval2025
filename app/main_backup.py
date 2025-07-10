# main.py (panel central integrado con dashboard, módulos y consola - Versión Moderna)
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
import threading
import sys
from app.activos import registrar_activo_gui
from app.analyzer import analizar_dominio, lanzar_analyzer_gui
from app.export_pdf import exportar_pdf
from app.monitoreo import mostrar_menu_monitoreo
from app.tratamiento import lanzar_tratamiento_gui

def crear_gui_principal():
    footer_frame = tk.Frame(root, bg='#34495e', height=40)
    footer_frame.pack(fill='x')
    footer_frame.pack_propagate(False)
    
    footer_text = tk.Label(footer_frame, 
                          text="📝 Desarrollado por: Bonilla • Camacho • Morales • Paqui | 📅 2025 | 🏢 SECUREVAL v2.0", 
                          font=("Helvetica", 9), 
                          bg='#34495e', fg='#ecf0f1')
    footer_text.pack(pady=10)

    root.after(100, mostrar_bienvenida)
    root.mainloop()

def main():
    """Función principal para iniciar SECUREVAL"""
    ejecutar_app()

if __name__ == "__main__":
    main()     text="📝 Desarrollado por: Bonilla • Camacho • Morales • Paqui | 📅 2025 | 🏢 SECUREVAL v2.0", 
                          font=("Helvetica", 9), 
                          bg='#34495e', fg='#ecf0f1')
    footer_text.pack(pady=10)

    root.after(100, mostrar_bienvenida)
    root.mainloop()

def main():
    """Función principal para iniciar SECUREVAL"""
    global root
    ejecutar_app()

if __name__ == "__main__":
    main()ir stdout a consola de Tkinter
class ConsoleRedirect:
    def __init__(self, text_widget):
        self.text_widget = text_widget
    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
    def flush(self):
        pass

def ejecutar_analisis():
    """Lanza la interfaz moderna de análisis de dominios."""
    lanzar_analyzer_gui()

def exportar_pdf_integrado():
    dominio = simpledialog.askstring("Exportar PDF", "📄 Ingrese el dominio para exportar informe:")
    if dominio:
        ok = exportar_pdf(dominio)
        if ok:
            messagebox.showinfo("Éxito", f"📁 PDF detallado generado para {dominio}.")
        else:
            messagebox.showerror("Error", "❌ No se encontró el análisis para ese dominio.")

def mostrar_info_modulos():
    """Muestra información detallada sobre cada módulo con diseño moderno."""
    info = tk.Toplevel(root)
    info.title("📋 Información de Módulos - SECUREVAL")
    info.geometry("650x500")
    info.configure(bg='#f0f0f0')
    info.resizable(False, False)
    
    # Frame principal con padding
    main_frame = tk.Frame(info, bg='#f0f0f0')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Título
    titulo = tk.Label(main_frame, text="🔧 Módulos del Sistema SECUREVAL", 
                     font=("Helvetica", 16, "bold"), 
                     bg='#f0f0f0', fg='#2c3e50')
    titulo.pack(pady=(0, 20))
    
    # Frame para los módulos
    modulos_frame = tk.Frame(main_frame, bg='#f0f0f0')
    modulos_frame.pack(fill='both', expand=True)
    
    modulos = [
        ("➕ Registrar Activo", "Gestión de Inventario", 
         "Permite registrar y valorar activos de la organización\ncon criterios de Confidencialidad, Integridad y Disponibilidad.", 
         "#3498db"),
        ("🔍 Analizar Dominio", "Análisis de Seguridad", 
         "Realiza escaneo automático detectando tecnologías,\nvulnerabilidades (CVEs), puertos abiertos y configuración TLS.", 
         "#e74c3c"),
        ("🎯 Tratamiento de Riesgo", "Gestión de Riesgos", 
         "Evalúa y sugiere estrategias de tratamiento basadas\nen el nivel de criticidad de cada amenaza identificada.", 
         "#f39c12"),
        ("📊 Monitoreo de KPIs", "Dashboard Ejecutivo", 
         "Visualiza indicadores clave de rendimiento y métricas\nde riesgo para la toma de decisiones estratégicas.", 
         "#9b59b6"),
        ("📄 Exportar Informe", "Generar Informe Ejecutivo", 
         "Genera informes PDF completos con análisis detallado,\ngráficos y recomendaciones para directivos.", 
         "#27ae60")
    ]
    
    for i, (icono, titulo_mod, descripcion, color) in enumerate(modulos):
        # Frame para cada módulo
        mod_frame = tk.Frame(modulos_frame, bg='white', relief='solid', borderwidth=1)
        mod_frame.pack(fill='x', pady=5, padx=10)
        
        # Barra de color
        barra_color = tk.Frame(mod_frame, bg=color, height=4)
        barra_color.pack(fill='x')
        
        # Contenido del módulo
        content_frame = tk.Frame(mod_frame, bg='white')
        content_frame.pack(fill='x', padx=15, pady=10)
        
        # Título del módulo
        tk.Label(content_frame, text=f"{icono} {titulo_mod}", 
                font=("Helvetica", 12, "bold"), 
                bg='white', fg=color).pack(anchor='w')
        
        # Descripción
        tk.Label(content_frame, text=descripcion, 
                font=("Helvetica", 9), 
                bg='white', fg='#7f8c8d', 
                justify='left').pack(anchor='w', pady=(2, 0))
    
    # Frame para desarrolladores
    dev_frame = tk.Frame(main_frame, bg='#34495e', relief='solid', borderwidth=1)
    dev_frame.pack(fill='x', pady=(20, 0))
    
    tk.Label(dev_frame, text="👥 Equipo de Desarrollo", 
            font=("Helvetica", 11, "bold"), 
            bg='#34495e', fg='white').pack(pady=5)
    
    desarrolladores = "💻 Bonilla • Camacho • Morales • Paqui"
    tk.Label(dev_frame, text=desarrolladores, 
            font=("Helvetica", 9), 
            bg='#34495e', fg='#ecf0f1').pack(pady=(0, 8))
    
    # Botón de cerrar
    btn_frame = tk.Frame(main_frame, bg='#f0f0f0')
    btn_frame.pack(pady=(15, 0))
    
    cerrar_btn = tk.Button(btn_frame, text="✅ Entendido", 
                          command=info.destroy,
                          font=("Helvetica", 10, "bold"),
                          bg='#27ae60', fg='white',
                          relief='flat', padx=20, pady=8)
    cerrar_btn.pack()
    
    # Centrar ventana
    info.transient(root)
    info.grab_set()
    info.update_idletasks()
    x = (info.winfo_screenwidth() // 2) - (650 // 2)
    y = (info.winfo_screenheight() // 2) - (500 // 2)
    info.geometry(f"650x500+{x}+{y}")

def mostrar_bienvenida():
    """Muestra ventana de bienvenida con diseño moderno y profesional."""
    bienvenida = tk.Toplevel(root)
    bienvenida.title("🚀 Bienvenido a SECUREVAL")
    bienvenida.geometry("700x550")
    bienvenida.configure(bg='#2c3e50')
    bienvenida.resizable(False, False)
    
    # Frame principal
    main_frame = tk.Frame(bienvenida, bg='#2c3e50')
    main_frame.pack(fill='both', expand=True, padx=30, pady=30)
    
    # Logo/Título principal
    titulo_frame = tk.Frame(main_frame, bg='#2c3e50')
    titulo_frame.pack(pady=(0, 20))
    
    tk.Label(titulo_frame, text="🔐 SECUREVAL", 
            font=("Helvetica", 28, "bold"), 
            bg='#2c3e50', fg='#ecf0f1').pack()
    
    tk.Label(titulo_frame, text="Plataforma Avanzada de Evaluación de Riesgos Cibernéticos", 
            font=("Helvetica", 12), 
            bg='#2c3e50', fg='#bdc3c7').pack()
    
    # Frame de contenido con fondo blanco
    content_frame = tk.Frame(main_frame, bg='white', relief='solid', borderwidth=1)
    content_frame.pack(fill='both', expand=True, pady=20)
    
    # Padding interno
    inner_frame = tk.Frame(content_frame, bg='white')
    inner_frame.pack(fill='both', expand=True, padx=25, pady=25)
    
    # Mensaje de bienvenida
    welcome_text = tk.Label(inner_frame, 
                           text="¡Bienvenido a la nueva era de la ciberseguridad empresarial!", 
                           font=("Helvetica", 14, "bold"), 
                           bg='white', fg='#2c3e50')
    welcome_text.pack(pady=(0, 15))
    
    # Proceso paso a paso
    proceso_frame = tk.Frame(inner_frame, bg='white')
    proceso_frame.pack(fill='x', pady=10)
    
    tk.Label(proceso_frame, text="📋 Proceso de Evaluación Guiado:", 
            font=("Helvetica", 12, "bold"), 
            bg='white', fg='#34495e').pack(anchor='w')
    
    pasos = [
        ("1️⃣", "Registrar Activos", "Inventaría y valora los activos críticos de tu organización"),
        ("2️⃣", "Analizar Dominios", "Detecta vulnerabilidades, tecnologías y configuraciones de seguridad"),
        ("3️⃣", "Evaluar Tratamiento", "Obtén estrategias específicas para cada riesgo identificado"),
        ("4️⃣", "Monitorear KPIs", "Visualiza métricas ejecutivas y tendencias de riesgo"),
        ("5️⃣", "Generar Informes", "Exporta reportes profesionales para directivos y auditores")
    ]
    
    for emoji, titulo, descripcion in pasos:
        paso_frame = tk.Frame(proceso_frame, bg='white')
        paso_frame.pack(fill='x', pady=3)
        
        # Frame para emoji y contenido
        paso_content = tk.Frame(paso_frame, bg='white')
        paso_content.pack(fill='x', padx=10)
        
        tk.Label(paso_content, text=emoji, font=("Helvetica", 12), bg='white').pack(side='left')
        
        text_frame = tk.Frame(paso_content, bg='white')
        text_frame.pack(side='left', fill='x', expand=True, padx=(8, 0))
        
        tk.Label(text_frame, text=titulo, font=("Helvetica", 10, "bold"), 
                bg='white', fg='#3498db').pack(anchor='w')
        tk.Label(text_frame, text=descripcion, font=("Helvetica", 9), 
                bg='white', fg='#7f8c8d').pack(anchor='w')
    
    # Frame de botones
    btn_frame = tk.Frame(inner_frame, bg='white')
    btn_frame.pack(pady=(20, 0))
    
    # Crear frame interno para centrar los botones
    btn_container = tk.Frame(btn_frame, bg='white')
    btn_container.pack(anchor='center')
    
    # Botón comenzar
    comenzar_btn = tk.Button(btn_container, text="🚀 Comenzar Evaluación", 
                            command=bienvenida.destroy,
                            font=("Helvetica", 12, "bold"),
                            bg='#3498db', fg='white',
                            relief='flat', padx=25, pady=15,
                            cursor='hand2',
                            width=18,
                            activebackground='#2980b9',
                            activeforeground='white')
    comenzar_btn.pack(side='left', padx=5)
    
    # Efectos hover para botón comenzar
    def on_enter_comenzar(event):
        comenzar_btn.configure(bg='#2980b9')
    
    def on_leave_comenzar(event):
        comenzar_btn.configure(bg='#3498db')
    
    comenzar_btn.bind("<Enter>", on_enter_comenzar)
    comenzar_btn.bind("<Leave>", on_leave_comenzar)
    
    # Botón info
    info_btn = tk.Button(btn_container, text="📋 Ver Módulos", 
                        command=lambda: [bienvenida.destroy(), mostrar_info_modulos()],
                        font=("Helvetica", 12),
                        bg='#95a5a6', fg='white',
                        relief='flat', padx=25, pady=15,
                        cursor='hand2',
                        width=15,
                        activebackground='#7f8c8d',
                        activeforeground='white')
    info_btn.pack(side='left', padx=5)
    
    # Efectos hover para botón info
    def on_enter_info(event):
        info_btn.configure(bg='#7f8c8d')
    
    def on_leave_info(event):
        info_btn.configure(bg='#95a5a6')
    
    info_btn.bind("<Enter>", on_enter_info)
    info_btn.bind("<Leave>", on_leave_info)
    
    # Información de desarrolladores en footer
    footer_frame = tk.Frame(main_frame, bg='#34495e')
    footer_frame.pack(fill='x', pady=(15, 0))
    
    tk.Label(footer_frame, text="💼 Desarrollado por el Equipo SECUREVAL", 
            font=("Helvetica", 10, "bold"), 
            bg='#34495e', fg='white').pack(pady=8)
    
    # Centrar ventana
    bienvenida.transient(root)
    bienvenida.grab_set()
    bienvenida.update_idletasks()
    x = (bienvenida.winfo_screenwidth() // 2) - (700 // 2)
    y = (bienvenida.winfo_screenheight() // 2) - (550 // 2)
    bienvenida.geometry(f"700x550+{x}+{y}")

# Ventana principal con diseño moderno
if __name__ == "__main__":
    root = tk.Tk()
    root.title("🔐 SECUREVAL - Plataforma de Evaluación de Riesgos Cibernéticos")
    
    # Configurar pantalla completa de manera compatible
    root.withdraw()  # Ocultar temporalmente la ventana
    root.update_idletasks()  # Asegurar que se calculen los tamaños
    
    # Obtener dimensiones de la pantalla
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    
    # Configurar geometría para pantalla completa
    root.geometry(f"{width}x{height}+0+0")
    root.state('normal')  # Mostrar la ventana
    root.deiconify()  # Asegurar que se muestre
    
    root.configure(bg='#ecf0f1')
    root.minsize(800, 600)
    
    # Permitir control de pantalla completa
    def toggle_fullscreen(event=None):
        current_state = root.attributes('-fullscreen')
        root.attributes('-fullscreen', not current_state)
    
    def exit_fullscreen(event=None):
        root.attributes('-fullscreen', False)
    
    # Bindings para control de pantalla completa
    root.bind('<F11>', toggle_fullscreen)
    root.bind('<Escape>', exit_fullscreen)

    # Configurar estilos modernos
    estilo = ttk.Style()
    estilo.theme_use('clam')
    
    # Configurar estilos personalizados para botones
    estilo.configure("Modern.TButton", 
                    font=("Helvetica", 11, "bold"), 
                    padding=(15, 10),
                    borderwidth=0,
                    focuscolor='none')
    
    estilo.map("Modern.TButton",
              background=[('active', '#3498db'),
                         ('!active', '#2c3e50')],
              foreground=[('active', 'white'),
                         ('!active', 'white')])
    
    # Configurar estilos para LabelFrame (usando el estilo por defecto)
    estilo.configure("TLabelFrame", 
                    background='#ecf0f1',
                    borderwidth=2,
                    relief='solid')
    
    estilo.configure("TLabelFrame.Label", 
                    background='#ecf0f1',
                    foreground='#2c3e50',
                    font=("Helvetica", 12, "bold"))

    # Header frame
    header_frame = tk.Frame(root, bg='#2c3e50', height=80)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)
    
    # Título principal en header
    titulo_header = tk.Label(header_frame, 
                            text="🔐 SECUREVAL", 
                            font=("Helvetica", 20, "bold"), 
                            bg='#2c3e50', fg='#ecf0f1')
    titulo_header.pack(side='left', padx=20, pady=20)
    
    subtitulo_header = tk.Label(header_frame, 
                               text="Evaluación Profesional de Riesgos Cibernéticos", 
                               font=("Helvetica", 10), 
                               bg='#2c3e50', fg='#bdc3c7')
    subtitulo_header.pack(side='left', padx=(0, 20), pady=(25, 15))

    # Frame principal con padding
    main_container = tk.Frame(root, bg='#ecf0f1')
    main_container.pack(fill='both', expand=True, padx=20, pady=20)

    # Frame de botones modernizado
    frame_botones = ttk.LabelFrame(main_container, 
                                  text="🔧 Panel de Control Principal", 
                                  padding=20)
    frame_botones.pack(fill="x", pady=(0, 15))

    # Frame de consola modernizado
    frame_consola = ttk.LabelFrame(main_container, 
                                  text="📺 Monitor de Actividad del Sistema", 
                                  padding=15)
    frame_consola.pack(fill="both", expand=True)

    # Consola con estilo moderno
    consola_frame = tk.Frame(frame_consola, bg='#2c3e50', relief='solid', borderwidth=1)
    consola_frame.pack(fill="both", expand=True)
    
    consola = tk.Text(consola_frame, 
                     height=18, 
                     wrap="word",
                     bg='#2c3e50',
                     fg='#ecf0f1',
                     font=("Consolas", 9),
                     insertbackground='#ecf0f1',
                     selectbackground='#3498db',
                     relief='flat',
                     padx=10,
                     pady=10)
    consola.pack(fill="both", expand=True, padx=2, pady=2)
    
    # Scrollbar para consola
    scrollbar = ttk.Scrollbar(consola_frame, orient="vertical", command=consola.yview)
    scrollbar.pack(side="right", fill="y")
    consola.configure(yscrollcommand=scrollbar.set)

    # Redirigir stdout
    sys.stdout = ConsoleRedirect(consola)
    
    # Mensaje inicial en consola
    consola.insert(tk.END, "🚀 SECUREVAL v2.0 - Sistema iniciado correctamente\n")
    consola.insert(tk.END, "📋 Utilice el panel de control para comenzar la evaluación\n")
    consola.insert(tk.END, "🖥️  F11: Alternar pantalla completa | Escape: Salir pantalla completa\n")
    consola.insert(tk.END, "=" * 50 + "\n\n")

    # Definir botones con nuevos estilos
    botones = [
        ("❓ Información de Módulos", mostrar_info_modulos, "#9b59b6"),
        ("➕ Registrar Activo Empresarial", registrar_activo_gui, "#3498db"),
        ("🔍 Ejecutar Análisis de Dominio", ejecutar_analisis, "#e74c3c"),
        ("🎯 Estrategias de Tratamiento", lanzar_tratamiento_gui, "#f39c12"),
        ("📊 Dashboard de Monitoreo", mostrar_menu_monitoreo, "#9b59b6"),
        ("📄 Generar Informe Ejecutivo", exportar_pdf_integrado, "#27ae60"),
        ("❌ Cerrar Sistema", root.destroy, "#95a5a6")
    ]

    # Crear botones modernos
    for i, (texto, comando, color) in enumerate(botones):
        btn = tk.Button(frame_botones, 
                       text=texto, 
                       command=comando,
                       font=("Helvetica", 11, "bold"),
                       bg=color,
                       fg='white',
                       relief='flat',
                       padx=20,
                       pady=12,
                       cursor='hand2',
                       activebackground='#34495e',
                       activeforeground='white')
        
        # Efectos hover
        def on_enter(event, btn=btn, color=color):
            btn.configure(bg='#34495e')
        
        def on_leave(event, btn=btn, color=color):
            btn.configure(bg=color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        # Organizar en grid 2x4
        row = i // 2
        col = i % 2
        btn.grid(row=row, column=col, sticky="ew", padx=8, pady=6)
    
    # Configurar grid
    frame_botones.grid_columnconfigure(0, weight=1)
    frame_botones.grid_columnconfigure(1, weight=1)

    # Footer modernizado
    footer_frame = tk.Frame(root, bg='#34495e', height=40)
    footer_frame.pack(fill='x')
    footer_frame.pack_propagate(False)
    
    footer_text = tk.Label(footer_frame, 
                          text="� Desarrollado por: Bonilla • Camacho • Morales • Paqui | 📅 2025 | 🏢 SECUREVAL v2.0", 
                          font=("Helvetica", 9), 
                          bg='#34495e', fg='#ecf0f1')
    footer_text.pack(pady=10)

    root.after(100, mostrar_bienvenida)
    root.mainloop()
