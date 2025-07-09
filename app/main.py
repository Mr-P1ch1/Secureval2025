# main.py (versión con pantalla de bienvenida amigable e interfaz completa)
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from app.activos import registrar_activo_gui
from app.analyzer import analizar_dominio
from app.export_pdf import exportar_pdf
from app.tratamiento import determinar_tratamiento
from app.monitoreo import calcular_kpis
import time
import threading
import sys
import os

# Redirigir stdout a la consola de Tkinter
class ConsoleRedirect:
    def __init__(self, text_widget):
        self.text_widget = text_widget
    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
    def flush(self):
        pass

# =====================
# Funciones por módulo
# =====================
def ejecutar_analisis():
    dominio = simpledialog.askstring("Dominio", "🔍 Ingrese el dominio a analizar:")
    if dominio:
        def tarea():
            try:
                inicio = time.time()
                consola.insert(tk.END, f"\n⏳ Iniciando análisis para: {dominio}\n")
                resultados = analizar_dominio(dominio)
                duracion = round(time.time() - inicio, 2)
                consola.insert(tk.END, f"\n✅ Análisis finalizado en {duracion} segundos. Tecnologías detectadas: {len(resultados)}\n")
            except Exception as e:
                consola.insert(tk.END, f"❌ Error en el análisis: {str(e)}\n")
        threading.Thread(target=tarea).start()

def generar_pdf():
    dominio = simpledialog.askstring("Exportar PDF", "📄 Ingrese el dominio para exportar informe:")
    if dominio:
        ok = exportar_pdf(dominio)
        if ok:
            messagebox.showinfo("Éxito", f"📁 PDF generado exitosamente para {dominio}.")
        else:
            messagebox.showerror("Error", "No se encontró el análisis para ese dominio.")

def mostrar_tratamiento():
    try:
        valor = float(simpledialog.askstring("Tratamiento de Riesgo", "🎯 Ingrese el valor del riesgo (0-100):"))
        decision = determinar_tratamiento(valor)
        messagebox.showinfo("Tratamiento recomendado", f"🔐 Riesgo: {valor} → {decision}")
    except:
        messagebox.showerror("Error", "⚠️ Ingrese un número válido.")

def mostrar_kpis_gui():
    dominio = simpledialog.askstring("Monitoreo KPIs", "📊 Ingrese el dominio:")
    if dominio:
        kpis = calcular_kpis(dominio)
        if kpis:
            resumen = f"\n📊 KPIs de Riesgo para: {dominio}\n"
            for clave, valor in kpis.items():
                if isinstance(valor, dict):
                    resumen += f"- {clave.replace('_', ' ').title()}: {valor['cantidad']} ({valor['porcentaje']}%)\n"
                else:
                    resumen += f"- {clave.replace('_', ' ').title()}: {valor}\n"
            consola.insert(tk.END, resumen + "\n")
        else:
            messagebox.showerror("Error", "❌ No se encontraron datos para ese dominio.")

# =====================
# Pantalla de bienvenida
# =====================
def mostrar_bienvenida():
    bienvenida = tk.Toplevel(root)
    bienvenida.title("Bienvenida a SECUREVAL")
    bienvenida.geometry("600x400")

    tk.Label(bienvenida, text="Bienvenido a SECUREVAL", font=("Arial", 16, "bold")).pack(pady=10)
    mensaje = (
        "Esta herramienta guía paso a paso la gestión de riesgos cibernéticos.\n\n"
        "1. ➕ Registrar activos de tu organización.\n"
        "2. 🔍 Analizar un dominio para detectar tecnologías y vulnerabilidades.\n"
        "3. 📄 Exportar un reporte PDF con los riesgos identificados.\n"
        "4. 🎯 Determinar el tratamiento más adecuado según el nivel de riesgo.\n"
        "5. 📊 Monitorear indicadores clave (KPIs) para priorizar acciones.\n\n"
        "Utiliza los botones de la izquierda para navegar por las funciones."
    )
    tk.Label(bienvenida, text=mensaje, justify="left", wraplength=560).pack(padx=20, pady=10)

    ttk.Button(bienvenida, text="Comenzar", command=bienvenida.destroy).pack(pady=10)

# =====================
# Ventana Principal
# =====================
if __name__ == "__main__":
    root = tk.Tk()
    root.title("🔐 SECUREVAL - Evaluación de Riesgos Cibernéticos")
    root.geometry("700x600")

    estilo = ttk.Style()
    estilo.configure("TButton", font=("Arial", 11), padding=8)

    frame_botones = ttk.Frame(root, padding=10)
    frame_botones.pack(fill="x")

    frame_consola = ttk.LabelFrame(root, text="📺 Consola de Proceso", padding=10)
    frame_consola.pack(fill="both", expand=True, padx=10, pady=10)

    consola = tk.Text(frame_consola, height=18, wrap="word")
    consola.pack(fill="both", expand=True)

    sys.stdout = ConsoleRedirect(consola)

    opciones = [
        ("❓ ¿Qué hace cada módulo?", lambda: messagebox.showinfo("Módulos", 
            "➕ Registrar Activo: Carga activos con su valoración CIA.\n"
            "🔍 Analizar Dominio: Detecta tecnologías y CVEs de un dominio.\n"
            "📄 Exportar a PDF: Genera un reporte de riesgos en PDF.\n"
            "🎯 Tratamiento: Sugiere acciones según el nivel de riesgo.\n"
            "📊 KPIs: Muestra estadísticas de riesgo agrupado.")),
        ("➕ Registrar Activo", registrar_activo_gui),
        ("🔍 Analizar Dominio", ejecutar_analisis),
        ("📄 Exportar a PDF", generar_pdf),
        ("🎯 Tratamiento de Riesgo", mostrar_tratamiento),
        ("📊 Monitoreo de KPIs", mostrar_kpis_gui),
        ("❌ Salir", root.destroy)
    ]

    for texto, accion in opciones:
        ttk.Button(frame_botones, text=texto, command=accion).pack(fill="x", pady=3)

    footer = ttk.Label(root, text="👩‍💻 Desarrollado por Bonilla, Camacho, Morales, Paqui", font=("Arial", 9))
    footer.pack(pady=5)

    root.after(200, mostrar_bienvenida)
    root.mainloop()
