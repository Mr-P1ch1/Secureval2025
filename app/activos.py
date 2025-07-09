# app/activos.py (versión mejorada e integrada con exportación y estructura unificada)
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

ACTIVOS_FILE = os.path.join("resultados", "activos.json")
os.makedirs("resultados", exist_ok=True)
if not os.path.exists(ACTIVOS_FILE):
    with open(ACTIVOS_FILE, "w") as f:
        json.dump([], f, indent=4)

def calcular_valor_activo(c, i, d):
    return round((c + i + d) / 3, 2)

def registrar_activo_gui():
    def guardar_activo():
        nombre = entry_nombre.get().strip()
        tipo = combo_tipo.get().strip()
        descripcion = entry_desc.get().strip()
        estado = combo_estado.get().strip()
        ubicacion = entry_ubicacion.get().strip()
        procesos = entry_proceso.get().strip()
        propietario = entry_prop.get().strip()

        try:
            c = int(combo_c.get())
            i = int(combo_i.get())
            d = int(combo_d.get())
        except:
            messagebox.showerror("Error", "Confidencialidad, Integridad y Disponibilidad deben ser números entre 1 y 5")
            return

        va = calcular_valor_activo(c, i, d)

        with open(ACTIVOS_FILE, "r") as f:
            activos = json.load(f)

        codigo = f"{nombre[:2].upper()}-{len(activos)+1:03}"

        activos.append({
            "id": len(activos)+1,
            "codigo": codigo,
            "nombre": nombre,
            "tipo": tipo,
            "descripcion": descripcion,
            "estado": estado,
            "ubicacion": ubicacion,
            "procesos": procesos,
            "propietario": propietario,
            "confidencialidad": c,
            "integridad": i,
            "disponibilidad": d,
            "valor": va,
            "impacto_empresa": f"C:{c} I:{i} D:{d}"
        })

        with open(ACTIVOS_FILE, "w") as f:
            json.dump(activos, f, indent=4)

        messagebox.showinfo("Éxito", f"Activo '{nombre}' registrado con VA = {va}")
        ventana.destroy()

    ventana = tk.Tk()
    ventana.title("Registrar Activo SECUREVAL")
    ventana.geometry("500x500")

    campos = [
        ("Nombre del Activo:", "entry_nombre"),
        ("Tipo (Primario/Secundario/Soporte):", "combo_tipo", ["Primario", "Secundario", "Soporte"]),
        ("Descripción:", "entry_desc"),
        ("Estado:", "combo_estado", ["En uso", "Vigente", "No vigente", "Eliminado"]),
        ("Ubicación:", "entry_ubicacion"),
        ("Procesos vinculados:", "entry_proceso"),
        ("Propietario:", "entry_prop"),
        ("Confidencialidad (1-5):", "combo_c", list(range(1, 6))),
        ("Integridad (1-5):", "combo_i", list(range(1, 6))),
        ("Disponibilidad (1-5):", "combo_d", list(range(1, 6)))
    ]

    entries = {}
    for texto, nombre, *valores in campos:
        ttk.Label(ventana, text=texto).pack()
        if "combo" in nombre:
            combo = ttk.Combobox(ventana, values=valores[0])
            combo.pack()
            entries[nombre] = combo
        else:
            entry = ttk.Entry(ventana)
            entry.pack()
            entries[nombre] = entry

    entry_nombre = entries["entry_nombre"]
    combo_tipo = entries["combo_tipo"]
    entry_desc = entries["entry_desc"]
    combo_estado = entries["combo_estado"]
    entry_ubicacion = entries["entry_ubicacion"]
    entry_proceso = entries["entry_proceso"]
    entry_prop = entries["entry_prop"]
    combo_c = entries["combo_c"]
    combo_i = entries["combo_i"]
    combo_d = entries["combo_d"]

    ttk.Button(ventana, text="Guardar Activo", command=guardar_activo).pack(pady=10)
    ventana.mainloop()

def listar_activos():
    with open(ACTIVOS_FILE, "r") as f:
        activos = json.load(f)
    print("\n📋 Inventario de Activos:")
    for a in activos:
        print(f"- [{a['codigo']}] {a['nombre']} | Tipo: {a['tipo']} | VA: {a['valor']}")

def obtener_activos():
    with open(ACTIVOS_FILE, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    registrar_activo_gui()
