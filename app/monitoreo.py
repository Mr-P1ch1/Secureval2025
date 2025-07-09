# app/monitoreo.py (versión final mejorada con selección activa de dominios o activos)
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.activos import obtener_activos

RESULTADOS_DIR = "resultados"

# ========================
# Funciones de utilidades
# ========================

def listar_dominios():
    """Lista los dominios que han sido escaneados y tienen carpeta de resultados."""
    if not os.path.exists(RESULTADOS_DIR):
        return []
    return [d for d in os.listdir(RESULTADOS_DIR) if os.path.isdir(os.path.join(RESULTADOS_DIR, d))]

def calcular_kpis(dominio):
    """Calcula los indicadores de riesgo (KPIs) para un dominio específico."""
    ruta_json = os.path.join(RESULTADOS_DIR, dominio, "riesgo.json")
    if not os.path.exists(ruta_json):
        return None

    with open(ruta_json, "r") as f:
        datos = json.load(f)

    total = len(datos)
    if total == 0:
        return None

    bajos = sum(1 for r in datos if r["riesgo"] < 10)
    medios = sum(1 for r in datos if 10 <= r["riesgo"] < 25)
    mitigables = sum(1 for r in datos if 25 <= r["riesgo"] < 80)
    criticos = sum(1 for r in datos if r["riesgo"] >= 80)

    return {
        "fecha_analisis": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_amenazas": total,
        "riesgo_bajo": (bajos, round(bajos * 100 / total, 2)),
        "riesgo_medio": (medios, round(medios * 100 / total, 2)),
        "riesgo_mitigable": (mitigables, round(mitigables * 100 / total, 2)),
        "riesgo_critico": (criticos, round(criticos * 100 / total, 2))
    }

def mostrar_kpis_en_gui(kpis):
    texto.delete(1.0, tk.END)
    if not kpis:
        texto.insert(tk.END, "❌ No se encontraron datos para mostrar.\n")
        return

    texto.insert(tk.END, f"\n📊 Indicadores Clave de Riesgo - SECUREVAL\n")
    texto.insert(tk.END, f"🗓 Fecha del análisis: {kpis['fecha_analisis']}\n")
    texto.insert(tk.END, f"🔎 Total amenazas detectadas: {kpis['total_amenazas']}\n")
    texto.insert(tk.END, "-" * 50 + "\n")
    texto.insert(tk.END, f"✅ Riesgo Bajo: {kpis['riesgo_bajo'][0]} ({kpis['riesgo_bajo'][1]}%)\n")
    texto.insert(tk.END, f"🟡 Riesgo Medio: {kpis['riesgo_medio'][0]} ({kpis['riesgo_medio'][1]}%)\n")
    texto.insert(tk.END, f"🟠 Riesgo Mitigable: {kpis['riesgo_mitigable'][0]} ({kpis['riesgo_mitigable'][1]}%)\n")
    texto.insert(tk.END, f"🔴 Riesgo Crítico: {kpis['riesgo_critico'][0]} ({kpis['riesgo_critico'][1]}%)\n")

def mostrar_activos():
    texto.delete(1.0, tk.END)
    activos = obtener_activos()
    if not activos:
        texto.insert(tk.END, "📭 No hay activos registrados.\n")
        return

    texto.insert(tk.END, "📦 Lista de Activos Registrados:\n")
    texto.insert(tk.END, "-" * 50 + "\n")
    for a in activos:
        texto.insert(tk.END, f"🛠️ [{a['codigo']}] {a['nombre']} | Tipo: {a['tipo']} | VA: {a['valor_activo']}\n")

def actualizar_opciones(event=None):
    modo = combo_modo.get()
    if modo == "Dominios escaneados":
        combo_items['values'] = listar_dominios()
    elif modo == "Activos registrados":
        combo_items['values'] = [a["codigo"] for a in obtener_activos()]
    combo_items.set("")
    texto.delete(1.0, tk.END)

def ejecutar_monitoreo():
    modo = combo_modo.get()
    valor = combo_items.get()
    if modo == "Dominios escaneados":
        if not valor:
            messagebox.showwarning("Aviso", "Selecciona un dominio para analizar.")
            return
        kpis = calcular_kpis(valor)
        if kpis:
            mostrar_kpis_en_gui(kpis)
        else:
            messagebox.showerror("Error", "❌ No se pudo calcular los KPIs para ese dominio.")
    elif modo == "Activos registrados":
        mostrar_activos()

# ==========================
# GUI Principal del módulo
# ==========================
ventana = tk.Tk()
ventana.title("📊 Monitoreo de Riesgos - SECUREVAL")
ventana.geometry("750x480")

frame_top = ttk.Frame(ventana)
frame_top.pack(pady=10)

combo_modo = ttk.Combobox(frame_top, values=["Dominios escaneados", "Activos registrados"], state="readonly")
combo_modo.set("Dominios escaneados")
combo_modo.grid(row=0, column=0, padx=5)
combo_modo.bind("<<ComboboxSelected>>", actualizar_opciones)

combo_items = ttk.Combobox(frame_top, values=[], state="readonly", width=45)
combo_items.grid(row=0, column=1, padx=5)

btn_analizar = ttk.Button(frame_top, text="🔎 Mostrar", command=ejecutar_monitoreo)
btn_analizar.grid(row=0, column=2, padx=5)

texto = tk.Text(ventana, height=22, wrap="word")
texto.pack(padx=10, pady=10, fill="both", expand=True)

actualizar_opciones()
ventana.mainloop()
