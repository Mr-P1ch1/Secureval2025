# app/tratamiento.py - Versión modernizada con navegación interactiva v2.0
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
    NAVIGATION_AVAILABLE = True
except ImportError:
    NAVIGATION_AVAILABLE = False
import numpy as np

RESULTADOS_DIR = "resultados"

# ============================
# Lógica de tratamiento
# ============================

def determinar_tratamiento(riesgo):
    """Retorna la estrategia de tratamiento según el nivel de riesgo."""
    if riesgo < 10:
        return "Aceptar"
    elif riesgo < 25:
        return "Aceptar o Mitigar"
    elif riesgo < 50:
        return "Mitigar o Transferir"
    elif riesgo < 80:
        return "Mitigar"
    else:
        return "Evitar"

def listar_dominios():
    """Retorna la lista de dominios escaneados con resultados."""
    if not os.path.exists(RESULTADOS_DIR):
        return []
    return [d for d in os.listdir(RESULTADOS_DIR) if os.path.isdir(os.path.join(RESULTADOS_DIR, d))]

def cargar_riesgos(dominio):
    """Carga los riesgos del análisis de un dominio."""
    ruta = os.path.join(RESULTADOS_DIR, dominio, "riesgo.json")
    if not os.path.exists(ruta):
        return []
    with open(ruta, "r") as f:
        return json.load(f)

# ============================
# Interfaz gráfica
# ============================

def lanzar_tratamiento_gui():
    """Lanza la interfaz gráfica moderna para el tratamiento de riesgos."""
    ventana = tk.Toplevel()
    ventana.title("🎯 Tratamiento de Riesgos - SECUREVAL v2.0")
    ventana.configure(bg='#f8f9fa')
    ventana.resizable(True, True)
    
    # Maximizar ventana para uso completo del espacio disponible
    try:
        ventana.state('zoomed')  # Windows/Linux
    except tk.TclError:
        try:
            ventana.attributes('-zoomed', True)  # Alternativo para Linux
        except:
            # Usar tamaño amplio por defecto
            ventana.geometry('1800x1000')
    
    # Frame principal sin restricciones para máxima visualización
    main_frame = tk.Frame(ventana, bg='#f8f9fa')
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Header modernizado con diseño actualizado
    header_frame = tk.Frame(main_frame, bg='#2c3e50', relief='raised', bd=2)
    header_frame.pack(fill='x', pady=(0, 20))
    
    titulo_header = tk.Label(header_frame, 
                            text="🎯 TRATAMIENTO DE RIESGOS", 
                            font=("Helvetica", 20, "bold"), 
                            bg='#2c3e50', fg='white')
    titulo_header.pack(pady=15)
    
    subtitulo = tk.Label(header_frame, 
                        text="Estrategias de Mitigación y Evaluación de Criticidad", 
                        font=("Helvetica", 12), 
                        bg='#2c3e50', fg='#bdc3c7')
    subtitulo.pack(pady=(0, 15))
    
    # Frame contenedor con scroll
    scroll_container = tk.Frame(main_frame, bg='white', relief='solid', borderwidth=1)
    scroll_container.pack(fill='both', expand=True, pady=(0, 20))
    
    # Canvas y Scrollbar para scroll vertical
    canvas = tk.Canvas(scroll_container, bg='white', highlightthickness=0)
    scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='white')
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Padding interno
    inner_frame = tk.Frame(scrollable_frame, bg='white')
    inner_frame.pack(fill='both', expand=True, padx=30, pady=25)
    
    # Panel de selección modernizado con estilo actualizado
    seleccion_frame = tk.LabelFrame(inner_frame, text="⚙️ Configuración de Análisis",
                                   font=("Helvetica", 12, "bold"),
                                   bg='white', fg='#2c3e50', padx=15, pady=15)
    seleccion_frame.pack(fill='x', pady=(0, 20))
    
    # Frame para controles con diseño moderno
    controles_frame = tk.Frame(seleccion_frame, bg='white')
    controles_frame.pack(fill='x', padx=10, pady=10)
    
    # Dominio
    tk.Label(controles_frame, text="🌐 Dominio objetivo:", 
            font=("Helvetica", 11, "bold"), 
            bg='white', fg='#2c3e50').grid(row=0, column=0, sticky='w', pady=5, padx=(0, 10))
    
    combo_dom = ttk.Combobox(controles_frame, values=listar_dominios(), 
                           state="readonly", width=35, font=("Helvetica", 11))
    combo_dom.grid(row=0, column=1, pady=5, sticky='w')
    
    # Riesgo
    tk.Label(controles_frame, text="⚠️ Riesgo a evaluar:", 
            font=("Helvetica", 11, "bold"), 
            bg='white', fg='#2c3e50').grid(row=1, column=0, sticky='w', pady=5, padx=(0, 10))
    
    combo_riesgos = ttk.Combobox(controles_frame, values=[], 
                               state="readonly", width=50, font=("Helvetica", 10))
    combo_riesgos.grid(row=1, column=1, pady=5, sticky='w')
    
    # Botón de análisis modernizado
    btn_tratar = tk.Button(controles_frame, text="🧪 Evaluar Tratamiento",
                          font=("Helvetica", 12, "bold"),
                          bg='#9b59b6', fg='white',
                          relief='flat', padx=25, pady=12,
                          cursor='hand2',
                          activebackground='#8e44ad',
                          activeforeground='white')
    btn_tratar.grid(row=1, column=2, padx=(15, 0), pady=5)
    
    # Efectos hover para el botón modernizados
    def on_enter_btn(event):
        btn_tratar.configure(bg='#8e44ad')
    
    def on_leave_btn(event):
        btn_tratar.configure(bg='#9b59b6')
    
    btn_tratar.bind("<Enter>", on_enter_btn)
    btn_tratar.bind("<Leave>", on_leave_btn)
    
    # Panel de resultados con pestañas como monitoreo para visualización completa
    resultados_frame = tk.Frame(inner_frame, bg='white')
    resultados_frame.pack(fill='both', expand=True)
    
    # Crear notebook para pestañas igual que monitoreo
    notebook = ttk.Notebook(resultados_frame)
    notebook.pack(fill='both', expand=True, pady=(0, 20))
    
    # Pestaña de análisis de texto
    tab_texto = ttk.Frame(notebook)
    notebook.add(tab_texto, text="📄 Análisis Detallado")
    
    # Pestaña de gráficos (sin restricciones de ancho)
    tab_graficos = ttk.Frame(notebook)
    notebook.add(tab_graficos, text="📊 Dashboard Visual")
    
    # Área de texto en su pestaña
    texto_frame = tk.Frame(tab_texto, bg='#2c3e50', relief='solid', borderwidth=1)
    texto_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    texto = tk.Text(texto_frame, 
                   height=25, 
                   wrap="word",
                   bg='#2c3e50',
                   fg='#ecf0f1',
                   font=("Consolas", 10),
                   relief='flat',
                   padx=15,
                   pady=15)
    texto.pack(fill='both', expand=True, padx=2, pady=2)
    
    # Scrollbar para texto
    texto_scroll = ttk.Scrollbar(texto_frame, orient="vertical", command=texto.yview)
    texto.configure(yscrollcommand=texto_scroll.set)
    
    # Configurar matplotlib para mejor integración
    plt.style.use('default')
    
    def crear_grafico_inicial():
        """Crea un gráfico inicial vacío con navegación interactiva."""
        # Limpiar cualquier gráfico anterior
        for widget in tab_graficos.winfo_children():
            widget.destroy()
        
        # Usar tamaño igual que monitoreo para visualización completa
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), facecolor='#f8f9fa')
        
        # Márgenes igual que monitoreo sin recortes
        fig.subplots_adjust(left=0.08, bottom=0.08, right=0.95, top=0.92, hspace=0.35)
        
        fig.suptitle('📊 Análisis de Riesgos - Dashboard Interactivo', fontsize=16, fontweight='bold', color='#2c3e50')
        
        # Gráfico de criticidad (placeholder)
        criticidades = ['Bajo', 'Medio', 'Alto', 'Crítico']
        valores = [0, 0, 0, 0]
        colores = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']
        
        wedges, texts, autotexts = ax1.pie(valores if sum(valores) > 0 else [1], 
                                          labels=criticidades if sum(valores) > 0 else ['Sin datos'],
                                          colors=colores if sum(valores) > 0 else ['#bdc3c7'],
                                          autopct='%1.1f%%' if sum(valores) > 0 else '',
                                          startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax1.set_title('🎯 Distribución por Criticidad', fontweight='bold', fontsize=14, color='#2c3e50', pad=20)
        
        # Gráfico de riesgos por tecnología (placeholder)
        bars = ax2.bar(['Sin datos'], [1], color='#bdc3c7', edgecolor='#34495e', linewidth=1.5)
        ax2.set_title('🔧 Riesgos por Tecnología', fontweight='bold', fontsize=14, color='#2c3e50', pad=20)
        ax2.set_ylabel('Nivel de Riesgo', fontsize=12, fontweight='bold', color='#2c3e50')
        ax2.tick_params(axis='x', labelsize=10)
        ax2.tick_params(axis='y', labelsize=10)
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.set_facecolor('#fcfcfc')
        
        return fig
    
    def integrar_canvas_con_navegacion(fig):
        """Integra el canvas con navegación interactiva completa igual que monitoreo."""
        # Limpiar contenido previo
        for widget in tab_graficos.winfo_children():
            widget.destroy()
        
        # Crear canvas de matplotlib usando todo el ancho disponible
        canvas_grafico = FigureCanvasTkAgg(fig, tab_graficos)
        canvas_grafico.draw()
        canvas_widget = canvas_grafico.get_tk_widget()
        
        # Canvas que usa todo el espacio disponible sin restricciones
        canvas_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame para navegación interactiva
        nav_frame = tk.Frame(tab_graficos, bg='#f8f9fa', height=35)
        nav_frame.pack(fill='x', pady=(0, 5))
        nav_frame.pack_propagate(False)
        
        # Barra de navegación interactiva igual que monitoreo
        if NAVIGATION_AVAILABLE:
            try:
                toolbar = NavigationToolbar2Tk(canvas_grafico, nav_frame)
                toolbar.update()
                toolbar.config(bg='#f8f9fa', relief='flat')
                
                # Etiqueta informativa moderna
                info_label = tk.Label(nav_frame, 
                                    text="🔍 Use los botones para navegar y hacer zoom en los gráficos",
                                    font=("Helvetica", 9),
                                    bg='#f8f9fa', fg='#34495e')
                info_label.pack(side='bottom', pady=2)
            except Exception as e:
                print(f"Error creando toolbar: {e}")
                # Mensaje alternativo si falla la toolbar
                tk.Label(nav_frame, 
                        text="📊 Dashboard Interactivo de Tratamiento de Riesgos",
                        font=("Helvetica", 10, "bold"),
                        bg='#f8f9fa', fg='#2c3e50').pack(pady=5)
        else:
            tk.Label(nav_frame, 
                    text="📊 Dashboard de Tratamiento de Riesgos",
                    font=("Helvetica", 10, "bold"),
                    bg='#f8f9fa', fg='#2c3e50').pack(pady=5)
        
        return canvas_grafico
    
    fig = crear_grafico_inicial()
    canvas_grafico = integrar_canvas_con_navegacion(fig)
    
    def actualizar_graficos(datos):
        """Actualiza los gráficos con datos reales y navegación mejorada."""
        # Limpiar figura anterior
        fig.clear()
        
        # Configurar subplots con espaciado óptimo para visualización completa
        fig.subplots_adjust(left=0.08, bottom=0.08, right=0.95, top=0.92, hspace=0.35)
        
        # Crear subplots
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)
        
        # Título principal mejorado
        fig.suptitle('📊 Dashboard de Tratamiento de Riesgos', fontsize=16, fontweight='bold', color='#2c3e50')
        
        # Datos para gráfico de criticidad
        criticidades_count = {'Bajo': 0, 'Medio': 0, 'Alto': 0, 'Crítico': 0}
        tecnologias_riesgo = {}
        
        for item in datos:
            criticidad = item.get('criticidad', 'Bajo')
            if criticidad in criticidades_count:
                criticidades_count[criticidad] += 1
            
            tecnologia = item.get('tecnologia', 'Desconocido')
            riesgo = item.get('riesgo', 0)
            if tecnologia not in tecnologias_riesgo:
                tecnologias_riesgo[tecnologia] = []
            tecnologias_riesgo[tecnologia].append(riesgo)
        
        # Gráfico de criticidad con diseño profesional mejorado
        labels = list(criticidades_count.keys())
        sizes = list(criticidades_count.values())
        colores = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']  # Colores modernos consistentes
        
        if sum(sizes) > 0:
            wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colores, 
                                              autopct='%1.1f%%', startangle=90,
                                              textprops={'fontsize': 11, 'fontweight': 'bold'},
                                              explode=(0.05, 0.05, 0.05, 0.05))  # Separación para mejor vista
        else:
            ax1.pie([1], labels=['Sin datos'], colors=['#bdc3c7'], 
                   textprops={'fontsize': 11, 'fontweight': 'bold'})
        
        ax1.set_title('🎯 Distribución por Criticidad', fontweight='bold', fontsize=14, color='#2c3e50', pad=20)
        
        # Gráfico de riesgos por tecnología (top 5) con diseño profesional mejorado
        if tecnologias_riesgo:
            tech_promedio = {tech: np.mean(riesgos) for tech, riesgos in tecnologias_riesgo.items()}
            top_tech = sorted(tech_promedio.items(), key=lambda x: x[1], reverse=True)[:5]
            
            tecnologias = [tech[:20] + '...' if len(tech) > 20 else tech for tech, _ in top_tech]
            riesgos = [riesgo for _, riesgo in top_tech]
            
            # Colores dinámicos según nivel de riesgo
            colores_bar = ['#e74c3c' if r >= 70 else '#e67e22' if r >= 50 else '#f39c12' if r >= 25 else '#2ecc71' for r in riesgos]
            
            bars = ax2.bar(tecnologias, riesgos, color=colores_bar, edgecolor='#34495e', linewidth=1.5, alpha=0.8)
            ax2.set_title('🔧 Top 5 Tecnologías por Riesgo', fontweight='bold', fontsize=14, color='#2c3e50', pad=20)
            ax2.set_ylabel('Riesgo Promedio', fontsize=12, fontweight='bold', color='#2c3e50')
            ax2.tick_params(axis='x', labelsize=10, rotation=45)
            ax2.tick_params(axis='y', labelsize=10)
            ax2.grid(True, alpha=0.3, linestyle='--')
            ax2.set_facecolor('#fcfcfc')
            
            # Añadir valores en las barras con mejor formato
            for bar, valor in zip(bars, riesgos):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(riesgos)*0.02,
                        f'{valor:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=10, color='#2c3e50')
        else:
            bars = ax2.bar(['Sin datos'], [1], color='#bdc3c7', edgecolor='#34495e', linewidth=1.5)
            ax2.set_title('🔧 Riesgos por Tecnología', fontweight='bold', fontsize=14, color='#2c3e50', pad=20)
            ax2.tick_params(axis='x', labelsize=10)
            ax2.tick_params(axis='y', labelsize=10)
            ax2.grid(True, alpha=0.3, linestyle='--')
            ax2.set_facecolor('#fcfcfc')
        
        # Redibujar canvas
        canvas_grafico.draw()
    
    # Mensaje inicial en el área de texto
    texto.insert(tk.END, "🎯 MÓDULO DE TRATAMIENTO DE RIESGOS\n")
    texto.insert(tk.END, "=" * 50 + "\n\n")
    texto.insert(tk.END, "📋 Instrucciones:\n")
    texto.insert(tk.END, "1. Seleccione un dominio de la lista desplegable\n")
    texto.insert(tk.END, "2. Elija un riesgo específico para evaluar\n")
    texto.insert(tk.END, "3. Haga clic en 'Evaluar Tratamiento'\n\n")
    texto.insert(tk.END, "💡 Los gráficos se actualizarán automáticamente\n")
    texto.insert(tk.END, "   mostrando la distribución de riesgos.\n\n")
    texto.insert(tk.END, "🔍 Esperando selección de dominio...\n")

    def actualizar_riesgos_local(event=None):
        """Actualiza la lista de riesgos disponibles para el dominio seleccionado."""
        dominio = combo_dom.get()
        if not dominio:
            return
        
        datos = cargar_riesgos(dominio)
        if not datos:
            messagebox.showwarning("Aviso", f"No hay resultados para el dominio '{dominio}'.")
            return
        
        valores = [f"{r['subdominio']} | {r['tecnologia']} | Riesgo: {r['riesgo']}" for r in datos]
        combo_riesgos['values'] = valores
        combo_riesgos.set("")
        
        # Actualizar gráficos con todos los datos del dominio
        actualizar_graficos(datos)
        
        # Actualizar área de texto
        texto.delete(1.0, tk.END)
        texto.insert(tk.END, f"📊 RESUMEN DEL DOMINIO: {dominio}\n")
        texto.insert(tk.END, "=" * 50 + "\n\n")
        texto.insert(tk.END, f"🔍 Total de riesgos detectados: {len(datos)}\n")
        
        # Estadísticas por criticidad
        criticidades = {}
        for item in datos:
            crit = item.get('criticidad', 'Bajo')
            criticidades[crit] = criticidades.get(crit, 0) + 1
        
        texto.insert(tk.END, "\n📈 Distribución por criticidad:\n")
        for crit, count in sorted(criticidades.items()):
            emoji = {"Bajo": "🟢", "Medio": "🟡", "Alto": "🟠", "Crítico": "🔴"}.get(crit, "⚪")
            texto.insert(tk.END, f"   {emoji} {crit}: {count}\n")
        
        riesgo_promedio = sum(item.get('riesgo', 0) for item in datos) / len(datos)
        texto.insert(tk.END, f"\n⚖️ Riesgo promedio: {riesgo_promedio:.2f}\n")
        texto.insert(tk.END, "\n🎯 Seleccione un riesgo específico para análisis detallado.\n")

    def analizar_tratamiento_local():
        """Evalúa el tratamiento recomendado según el riesgo del ítem seleccionado."""
        dominio = combo_dom.get()
        indice = combo_riesgos.current()

        if not dominio or indice < 0:
            messagebox.showinfo("Aviso", "Selecciona un dominio y un riesgo a evaluar.")
            return

        datos = cargar_riesgos(dominio)
        if indice >= len(datos):
            messagebox.showerror("Error", "Índice fuera de rango.")
            return

        item = datos[indice]
        riesgo = item['riesgo']
        estrategia = determinar_tratamiento(riesgo)

        # Determinar emoji y color según criticidad
        criticidad = item.get('criticidad', 'Bajo')
        emoji_crit = {"Bajo": "🟢", "Medio": "🟡", "Alto": "🟠", "Crítico": "🔴"}.get(criticidad, "⚪")
        
        # Determinar estrategia detallada
        estrategias_detalladas = {
            "Aceptar": "✅ ACEPTAR: El riesgo es mínimo y puede ser tolerado sin medidas adicionales.",
            "Aceptar o Mitigar": "⚖️ ACEPTAR O MITIGAR: Riesgo moderado. Evaluar costo-beneficio de medidas preventivas.",
            "Mitigar o Transferir": "🛡️ MITIGAR O TRANSFERIR: Implementar controles o transferir responsabilidad (seguros, terceros).",
            "Mitigar": "🚨 MITIGAR: Riesgo alto. Implementar controles de seguridad inmediatamente.",
            "Evitar": "🚫 EVITAR: Riesgo crítico. Discontinuar el servicio o implementar medidas drásticas."
        }

        texto.delete(1.0, tk.END)
        texto.insert(tk.END, "🎯 EVALUACIÓN DETALLADA DE TRATAMIENTO\n")
        texto.insert(tk.END, "=" * 60 + "\n\n")
        
        # Información del activo
        texto.insert(tk.END, "📋 INFORMACIÓN DEL ACTIVO:\n")
        texto.insert(tk.END, f"🌐 Subdominio: {item['subdominio']}\n")
        texto.insert(tk.END, f"🔧 Tecnología: {item['tecnologia']}\n")
        texto.insert(tk.END, f"🏷️ Tipo de servicio: {item.get('tipo_servicio', 'Desconocido')}\n")
        texto.insert(tk.END, f"🖥️ Sistema operativo: {item.get('sistema_operativo', 'N/A')}\n")
        
        # Evaluación de riesgo
        texto.insert(tk.END, f"\n⚠️ EVALUACIÓN DE RIESGO:\n")
        texto.insert(tk.END, f"📊 CVSS Máximo: {item.get('cvss_max', 0)}\n")
        texto.insert(tk.END, f"🔒 TLS/SSL: {item.get('tls', {}).get('tls_version', 'N/A')}\n")
        texto.insert(tk.END, f"🎯 Nivel de riesgo: {riesgo}\n")
        texto.insert(tk.END, f"{emoji_crit} Criticidad: {criticidad}\n")
        
        # CVEs
        cves = item.get('cves', [])
        if cves:
            texto.insert(tk.END, f"🚨 CVEs detectados: {', '.join(cves)}\n")
        else:
            texto.insert(tk.END, "✅ No se detectaron CVEs conocidos\n")
        
        # Estrategia recomendada
        texto.insert(tk.END, f"\n🛡️ ESTRATEGIA RECOMENDADA:\n")
        texto.insert(tk.END, f"{estrategias_detalladas.get(estrategia, estrategia)}\n")
        
        # Recomendaciones específicas
        texto.insert(tk.END, f"\n💡 RECOMENDACIONES ESPECÍFICAS:\n")
        if riesgo >= 80:
            texto.insert(tk.END, "• Desactivar inmediatamente el servicio si es posible\n")
            texto.insert(tk.END, "• Implementar WAF (Web Application Firewall)\n")
            texto.insert(tk.END, "• Auditoría de seguridad completa\n")
        elif riesgo >= 50:
            texto.insert(tk.END, "• Aplicar parches de seguridad urgentes\n")
            texto.insert(tk.END, "• Implementar monitoreo 24/7\n")
            texto.insert(tk.END, "• Revisar configuraciones de seguridad\n")
        elif riesgo >= 25:
            texto.insert(tk.END, "• Programar actualizaciones de seguridad\n")
            texto.insert(tk.END, "• Implementar monitoreo básico\n")
            texto.insert(tk.END, "• Revisar logs regularmente\n")
        else:
            texto.insert(tk.END, "• Mantener monitoreo rutinario\n")
            texto.insert(tk.END, "• Aplicar actualizaciones según cronograma\n")
        
        texto.insert(tk.END, f"\n📅 Fecha de evaluación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        texto.insert(tk.END, f"👨‍💼 Analista: Sistema SECUREVAL\n")

    # Asignar eventos
    combo_dom.bind("<<ComboboxSelected>>", actualizar_riesgos_local)
    btn_tratar.configure(command=analizar_tratamiento_local)
    
    # Frame de botones inferior
    btn_frame = tk.Frame(main_frame, bg='#f0f0f0')
    btn_frame.pack(fill='x')
    
    btn_container = tk.Frame(btn_frame, bg='#f0f0f0')
    btn_container.pack()
    
    # Botón Cerrar
    cerrar_btn = tk.Button(btn_container, text="❌ Cerrar", 
                          command=ventana.destroy,
                          font=("Helvetica", 12),
                          bg='#95a5a6', fg='white',
                          relief='flat', padx=25, pady=12,
                          cursor='hand2',
                          activebackground='#7f8c8d',
                          activeforeground='white')
    cerrar_btn.pack(padx=5)
    
    # Efectos hover para botón cerrar
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
    
    # Centrar y configurar ventana para máxima visualización
    ventana.transient()
    ventana.grab_set()
    ventana.update_idletasks()
    
    # Asegurar que el canvas se actualice correctamente
    canvas.configure(scrollregion=canvas.bbox("all"))

# Función para compatibilidad y testing
def main():
    """Función principal para testing del módulo de tratamiento"""
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    
    # Mostrar el módulo de tratamiento
    lanzar_tratamiento_gui()
    
    root.mainloop()

if __name__ == "__main__":
    main()
