# app/tratamiento.py (versión final mejorada con GUI interactiva)
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox

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

def actualizar_riesgos(event=None):
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
    texto.delete(1.0, tk.END)

def analizar_tratamiento():
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

    texto.delete(1.0, tk.END)
    texto.insert(tk.END, "📝 Evaluación de Tratamiento:\n")
    texto.insert(tk.END, "-" * 50 + "\n")
    texto.insert(tk.END, f"🌐 Subdominio: {item['subdominio']}\n")
    texto.insert(tk.END, f"🔧 Tecnología detectada: {item['tecnologia']}\n")
    texto.insert(tk.END, f"⚠️ Nivel de riesgo calculado: {riesgo}\n")
    texto.insert(tk.END, f"🛡️ Estrategia recomendada: {estrategia}\n")

# ============================
# Interfaz gráfica
# ============================
ventana = tk.Tk()
ventana.title("🎯 Tratamiento de Riesgos - SECUREVAL")
ventana.geometry("780x460")

frame_top = ttk.Frame(ventana)
frame_top.pack(pady=15)

ttk.Label(frame_top, text="🌐 Selecciona un dominio:").grid(row=0, column=0, padx=5, sticky="e")
combo_dom = ttk.Combobox(frame_top, values=listar_dominios(), state="readonly", width=35)
combo_dom.grid(row=0, column=1, padx=5)
combo_dom.bind("<<ComboboxSelected>>", actualizar_riesgos)

ttk.Label(frame_top, text="📦 Selecciona un riesgo a tratar:").grid(row=1, column=0, padx=5, pady=10, sticky="e")
combo_riesgos = ttk.Combobox(frame_top, values=[], state="readonly", width=60)
combo_riesgos.grid(row=1, column=1, padx=5, pady=10)

btn_tratar = ttk.Button(frame_top, text="🧪 Evaluar Tratamiento", command=analizar_tratamiento)
btn_tratar.grid(row=1, column=2, padx=5)

texto = tk.Text(ventana, height=18, wrap="word")
texto.pack(padx=15, pady=10, fill="both", expand=True)

ventana.mainloop()
