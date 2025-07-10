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
try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
    NAVIGATION_AVAILABLE = True
except ImportError:
    NAVIGATION_AVAILABLE = False
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

def leer_json_seguro(archivo_path):
    """Lee un archivo JSON de forma segura, manejando errores de formato"""
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read().strip()
        
        # Intentar parsear JSON directamente
        try:
            return json.loads(contenido)
        except json.JSONDecodeError as e:
            print(f"Error parseando JSON {archivo_path}: {e}")
            
            # Intentar reparar JSON común: múltiples objetos concatenados
            if "Extra data" in str(e):
                # Buscar el primer objeto JSON válido
                brace_count = 0
                for i, char in enumerate(contenido):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            # Encontramos el final del primer objeto JSON
                            json_valido = contenido[:i+1]
                            try:
                                return json.loads(json_valido)
                            except:
                                continue
            
            # Intentar reparar JSON con comas faltantes
            elif "delimiter" in str(e):
                # Buscar patrones comunes de JSON mal formateado
                lineas = contenido.split('\n')
                contenido_reparado = []
                
                for i, linea in enumerate(lineas):
                    contenido_reparado.append(linea)
                    # Si la línea termina con } y la siguiente empieza con ", agregar coma
                    if (i < len(lineas) - 1 and 
                        linea.strip().endswith('}') and 
                        lineas[i+1].strip().startswith('"') and
                        not linea.strip().endswith(',}')):
                        contenido_reparado[-1] = linea.rstrip() + ','
                
                try:
                    return json.loads('\n'.join(contenido_reparado))
                except:
                    pass
            
            print(f"No se pudo reparar automáticamente el JSON en {archivo_path}")
            return {}
            
    except Exception as e:
        print(f"Error leyendo archivo {archivo_path}: {e}")
        return {}

def listar_dominios():
    """Lista los dominios que tienen resultados de análisis"""
    try:
        # Buscar en el directorio resultados del nivel padre
        resultados_dir = current_dir.parent / "resultados"
        if not resultados_dir.exists():
            print(f"Directorio de resultados no encontrado: {resultados_dir}")
            return []
        
        dominios = []
        for item in resultados_dir.iterdir():
            if item.is_dir() and (item / "resumen.json").exists():
                dominios.append(item.name)
                print(f"Dominio encontrado: {item.name}")
        
        return sorted(dominios)
    except Exception as e:
        print(f"Error listando dominios: {e}")
        return []

def calcular_kpis(dominio):
    """Calcula indicadores clave de rendimiento para un dominio"""
    try:
        # Buscar en el directorio resultados del nivel padre
        resultados_dir = current_dir.parent / "resultados" / dominio
        
        if not resultados_dir.exists():
            print(f"Directorio del dominio no encontrado: {resultados_dir}")
            return None
        
        kpis = {
            'total_subdominios': 0,
            'total_tecnologias': 0,
            'total_cves': 0,
            'riesgo_promedio': 0,
            'subdominios_alto_riesgo': 0,
            'tecnologias_vulnerables': 0,
            'cvss_max': 0.0
        }
        
        # Leer resumen si existe
        resumen_file = resultados_dir / "resumen.json"
        if resumen_file.exists():
            resumen = leer_json_seguro(resumen_file)
            if not resumen:
                print(f"No se pudo leer el archivo de resumen para {dominio}")
                return None
            
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
        
        # Leer archivo de riesgos detallado para extraer CVSS máximo
        riesgo_file = resultados_dir / "riesgo.json"
        if riesgo_file.exists():
            riesgo_data = leer_json_seguro(riesgo_file)
            if riesgo_data and isinstance(riesgo_data, list):
                cvss_scores = []
                for item in riesgo_data:
                    if isinstance(item, dict):
                        cvss_max_item = item.get('cvss_max', 0)
                        if cvss_max_item and cvss_max_item > 0:
                            cvss_scores.append(cvss_max_item)
                
                if cvss_scores:
                    kpis['cvss_max'] = max(cvss_scores)
                    print(f"🔍 CVSS máximo extraído para {dominio}: {kpis['cvss_max']}")
                else:
                    print(f"⚠️ No se encontraron valores CVSS válidos en {dominio}")
            else:
                print(f"❌ No se pudo leer el archivo riesgo.json para {dominio}")
        else:
            print(f"📄 Archivo riesgo.json no encontrado para {dominio}")
        
        # Leer tecnologías si existe
        tecnologias_file = resultados_dir / "tecnologias.json"
        if tecnologias_file.exists():
            tecnologias = leer_json_seguro(tecnologias_file)
            
            # Verificar que tecnologias sea un diccionario
            if isinstance(tecnologias, dict):
                for tech_data in tecnologias.values():
                    if isinstance(tech_data, dict) and tech_data.get('cves'):
                        kpis['tecnologias_vulnerables'] += 1
            elif isinstance(tecnologias, list):
                # Si es una lista, iterar sobre los elementos
                for tech_data in tecnologias:
                    if isinstance(tech_data, dict) and tech_data.get('cves'):
                        kpis['tecnologias_vulnerables'] += 1
            else:
                print(f"Formato inesperado en tecnologias.json para {dominio}: {type(tecnologias)}")
        
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
    texto_widget.insert(tk.END, f"⚡ CVSS máximo detectado: {kpis.get('cvss_max', 0):.1f}/10\n")
    texto_widget.insert(tk.END, f"⚠️ Subdominios de alto riesgo (≥8.0): {kpis['subdominios_alto_riesgo']}\n")
    texto_widget.insert(tk.END, f"🔓 Tecnologías con vulnerabilidades: {kpis['tecnologias_vulnerables']}\n\n")
    
    # Evaluación del nivel de riesgo
    riesgo = kpis['riesgo_promedio']
    cvss_max = kpis.get('cvss_max', 0)
    
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
    texto_widget.insert(tk.END, f"💡 RECOMENDACIÓN: {recomendacion}\n")
    
    # Evaluación adicional basada en CVSS máximo
    if cvss_max >= 9.0:
        criticidad_cvss = "🔴 CRÍTICO"
        alerta_cvss = "¡VULNERABILIDADES CRÍTICAS DETECTADAS!"
    elif cvss_max >= 7.0:
        criticidad_cvss = "🟠 ALTO"
        alerta_cvss = "Vulnerabilidades de alto impacto presentes"
    elif cvss_max >= 4.0:
        criticidad_cvss = "🟡 MEDIO"
        alerta_cvss = "Vulnerabilidades de impacto medio detectadas"
    elif cvss_max > 0:
        criticidad_cvss = "🟢 BAJO"
        alerta_cvss = "Vulnerabilidades de bajo impacto"
    else:
        criticidad_cvss = "✅ SIN CVSS"
        alerta_cvss = "No se detectaron vulnerabilidades con CVSS"
    
    texto_widget.insert(tk.END, f"⚡ NIVEL CVSS MÁXIMO: {criticidad_cvss} ({cvss_max:.1f}/10)\n")
    texto_widget.insert(tk.END, f"🚨 ALERTA: {alerta_cvss}\n\n")

def mostrar_resumen(dominio, texto_widget):
    """Muestra un resumen detallado del análisis"""
    try:
        # Buscar en el directorio resultados del nivel padre
        resultados_dir = current_dir.parent / "resultados" / dominio
        resumen_file = resultados_dir / "resumen.json"
        riesgo_file = resultados_dir / "riesgo.json"
        
        # Crear diccionario de CVSS por subdominio
        cvss_por_subdominio = {}
        if riesgo_file.exists():
            riesgo_data = leer_json_seguro(riesgo_file)
            if riesgo_data and isinstance(riesgo_data, list):
                for item in riesgo_data:
                    if isinstance(item, dict):
                        subdominio = item.get('subdominio', '')
                        cvss_max = item.get('cvss_max', 0)
                        if subdominio:
                            if subdominio not in cvss_por_subdominio:
                                cvss_por_subdominio[subdominio] = []
                            cvss_por_subdominio[subdominio].append(cvss_max)
                
                # Calcular CVSS máximo por subdominio
                for sub in cvss_por_subdominio:
                    cvss_por_subdominio[sub] = max(cvss_por_subdominio[sub]) if cvss_por_subdominio[sub] else 0
        
        if resumen_file.exists():
            resumen = leer_json_seguro(resumen_file)
            
            if resumen:
                texto_widget.insert(tk.END, "📋 RESUMEN DETALLADO POR SUBDOMINIO\n")
                texto_widget.insert(tk.END, "=" * 60 + "\n\n")
                
                # Mostrar solo los primeros 5 subdominios para no saturar
                for i, (subdominio, info) in enumerate(list(resumen.items())[:5], 1):
                    cvss_max_sub = cvss_por_subdominio.get(subdominio, 0)
                    
                    texto_widget.insert(tk.END, f"{i}. 🔹 {subdominio}\n")
                    texto_widget.insert(tk.END, f"   • Tecnologías: {info.get('total_tecnologias', 0)}\n")
                    texto_widget.insert(tk.END, f"   • CVEs: {info.get('total_cves', 0)}\n")
                    texto_widget.insert(tk.END, f"   • CVSS máximo: {cvss_max_sub:.1f}/10\n")
                    texto_widget.insert(tk.END, f"   • Riesgo máximo: {info.get('riesgo_max', 0):.2f}/10\n")
                    texto_widget.insert(tk.END, f"   • Riesgo promedio: {info.get('riesgo_promedio', 0):.2f}/10\n\n")
                
                if len(resumen) > 5:
                    texto_widget.insert(tk.END, f"... y {len(resumen) - 5} subdominios más\n\n")
            else:
                texto_widget.insert(tk.END, "❌ Error: No se pudo leer el archivo de resumen\n")
        
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
    """Crea un gráfico de KPIs usando matplotlib con visualización completa e interactiva"""
    try:
        # Limpiar cualquier gráfico anterior
        for widget in frame_parent.winfo_children():
            widget.destroy()
        
        # Usar un tamaño más manejable pero que se vea completo
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 10))
        fig.patch.set_facecolor('#f8f9fa')
        
        # Ajustar márgenes para que se vea todo el contenido
        plt.subplots_adjust(left=0.08, bottom=0.08, right=0.95, top=0.92, 
                           hspace=0.35, wspace=0.25)
        
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
        wedges, texts, autotexts = ax1.pie(valores_riesgo, labels=riesgos, colors=colors, 
                                          autopct='%1.1f%%', startangle=90,
                                          textprops={'fontsize': 10})
        ax1.set_title('Distribución de Niveles de Riesgo', fontweight='bold', fontsize=12)
        
        # Gráfico 2: Métricas principales
        metricas = ['Subdominios', 'Tecnologías', 'CVEs', 'Vulnerabilidades']
        valores_metricas = [
            kpis_data.get('total_subdominios', 0),
            kpis_data.get('total_tecnologias', 0),
            kpis_data.get('total_cves', 0),
            kpis_data.get('tecnologias_vulnerables', 0)
        ]
        
        bars = ax2.bar(metricas, valores_metricas, color=['#3498db', '#9b59b6', '#e74c3c', '#f39c12'])
        ax2.set_title('Métricas de Seguridad', fontweight='bold', fontsize=12)
        ax2.set_ylabel('Cantidad', fontsize=10)
        ax2.tick_params(axis='x', labelsize=9)
        ax2.tick_params(axis='y', labelsize=9)
        
        # Añadir valores en las barras
        for bar, valor in zip(bars, valores_metricas):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(valores_metricas)*0.02,
                    str(valor), ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        # Gráfico 3: Indicadores de riesgo y CVSS
        riesgo = kpis_data.get('riesgo_promedio', 0)
        cvss_max = kpis_data.get('cvss_max', 0)
        
        # Subgráfico para riesgo promedio
        colors_gauge = ['#2ecc71' if riesgo < 4 else '#f39c12' if riesgo < 6 else '#e67e22' if riesgo < 8 else '#e74c3c']
        
        wedges = ax3.pie([riesgo, 10-riesgo], colors=[colors_gauge[0], '#ecf0f1'], 
                        startangle=90, counterclock=False, 
                        wedgeprops=dict(width=0.3))
        
        # Texto del riesgo promedio
        ax3.text(0, 0.3, f'{riesgo:.1f}', ha='center', va='center', 
                fontsize=14, fontweight='bold')
        ax3.text(0, -0.3, 'Riesgo', ha='center', va='center', 
                fontsize=10, fontweight='bold')
        
        # Indicador adicional de CVSS máximo como barra
        cvss_colors = ['#2ecc71' if cvss_max < 4 else '#f39c12' if cvss_max < 7 else '#e67e22' if cvss_max < 9 else '#e74c3c']
        ax3.text(0, -0.7, f'CVSS Max: {cvss_max:.1f}', ha='center', va='center', 
                fontsize=10, fontweight='bold', color=cvss_colors[0])
        
        ax3.set_title('Indicadores de Seguridad', fontweight='bold', fontsize=12)
        
        # Gráfico 4: Comparativa de seguridad
        categorias = ['Tecnologías\nSeguras', 'Tecnologías\nVulnerables']
        seguras = max(0, kpis_data.get('total_tecnologias', 0) - kpis_data.get('tecnologias_vulnerables', 0))
        vulnerables = kpis_data.get('tecnologias_vulnerables', 0)
        
        valores_comp = [seguras, vulnerables]
        colors_comp = ['#2ecc71', '#e74c3c']
        
        bars2 = ax4.bar(categorias, valores_comp, color=colors_comp)
        ax4.set_title('Estado de Tecnologías', fontweight='bold', fontsize=12)
        ax4.set_ylabel('Cantidad', fontsize=10)
        ax4.tick_params(axis='x', labelsize=9)
        ax4.tick_params(axis='y', labelsize=9)
        
        # Añadir valores en las barras
        for bar, valor in zip(bars2, valores_comp):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(valores_comp)*0.02,
                    str(valor), ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        # No usar tight_layout para evitar recortes
        # plt.tight_layout()
        # plt.subplots_adjust(hspace=0.3, wspace=0.3)
        
        # Widget del canvas que se ajuste automáticamente
        canvas = FigureCanvasTkAgg(fig, frame_parent)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        
        # Configurar el canvas para que se ajuste al contenido
        canvas_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame para información de navegación (más simple)
        info_frame = tk.Frame(frame_parent, bg='#f8f9fa', height=30)
        info_frame.pack(fill='x', pady=(0, 5))
        info_frame.pack_propagate(False)
        
        # Crear barra de navegación si está disponible
        if NAVIGATION_AVAILABLE:
            try:
                toolbar = NavigationToolbar2Tk(canvas, info_frame)
                toolbar.update()
                toolbar.config(bg='#f8f9fa', relief='flat')
                
                # Etiqueta informativa
                info_label = tk.Label(info_frame, 
                                    text="� Use los botones para navegar y hacer zoom en los gráficos",
                                    font=("Helvetica", 9),
                                    bg='#f8f9fa', fg='#34495e')
                info_label.pack(side='bottom', pady=2)
            except:
                # Si hay error con la toolbar, mostrar mensaje simple
                tk.Label(info_frame, 
                        text="📊 Gráficos de KPIs - Dashboard Interactivo",
                        font=("Helvetica", 10, "bold"),
                        bg='#f8f9fa', fg='#2c3e50').pack(pady=5)
        else:
            tk.Label(info_frame, 
                    text="📊 Gráficos de KPIs - Dashboard Interactivo",
                    font=("Helvetica", 10, "bold"),
                    bg='#f8f9fa', fg='#2c3e50').pack(pady=5)
        
        return canvas
        
    except Exception as e:
        print(f"Error creando gráfico de KPIs: {e}")
        return None

def mostrar_monitoreo():
    """Función principal que muestra la interfaz de monitoreo moderna"""
    
    # Crear ventana principal con tamaño completo
    ventana = tk.Toplevel()
    ventana.title("SECUREVAL - Dashboard de Monitoreo v2.0")
    ventana.configure(bg='#f8f9fa')
    
    # Configurar ventana para usar todo el espacio disponible
    try:
        ventana.state('zoomed')  # Maximizar ventana en Windows/Linux
    except tk.TclError:
        # Alternativa para sistemas que no soportan 'zoomed'
        ventana.attributes('-zoomed', True)
    except:
        # Usar tamaño amplio por defecto
        ventana.geometry('1600x900')
        
    # Centrar ventana si no se puede maximizar
    ventana.update_idletasks()
    width = ventana.winfo_width()
    height = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana.winfo_screenheight() // 2) - (height // 2)
    ventana.geometry(f'{width}x{height}+{x}+{y}')
    
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
    
    # Frame principal dentro del canvas con padding mínimo
    main_frame = tk.Frame(scrollable_frame, bg='#f8f9fa', padx=5, pady=5)
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
                             bg='#2c3e50', fg='#bdc3c7', pady=15)
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
    
    # Botones del dashboard (definir antes de mostrar_dashboard)
    dashboard_btn_container = tk.Frame(main_frame, bg='#f8f9fa')
    
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
        
        # Configurar botones del dashboard
        
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
