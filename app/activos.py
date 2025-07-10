# app/activos.py (versión mejorada e integrada con GUI intuitiva)
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Usar ruta absoluta para el archivo de activos
ACTIVOS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resultados", "activos.json")
resultados_dir = os.path.dirname(ACTIVOS_FILE)
os.makedirs(resultados_dir, exist_ok=True)

if not os.path.exists(ACTIVOS_FILE):
    with open(ACTIVOS_FILE, "w") as f:
        json.dump([], f, indent=4)

def calcular_valor_activo(c, i, d):
    return round((c + i + d) / 3, 2)

def registrar_activo_gui():
    """Muestra ventana de registro de activos con diseño moderno y profesional."""
    ventana = tk.Toplevel()
    ventana.title("➕ Registrar Activo - SECUREVAL")
    ventana.geometry("650x650")
    ventana.configure(bg='#f0f0f0')
    ventana.resizable(False, False)
    
    # Frame principal con padding
    main_frame = tk.Frame(ventana, bg='#f0f0f0')
    main_frame.pack(fill='both', expand=True, padx=25, pady=25)
    
    # Header moderno
    header_frame = tk.Frame(main_frame, bg='#2c3e50', relief='solid', borderwidth=1)
    header_frame.pack(fill='x', pady=(0, 20))
    
    titulo_header = tk.Label(header_frame, 
                            text="🔐 REGISTRO DE ACTIVOS", 
                            font=("Helvetica", 18, "bold"), 
                            bg='#2c3e50', fg='#ecf0f1')
    titulo_header.pack(pady=15)
    
    subtitulo = tk.Label(header_frame, 
                        text="Gestión Integral del Inventario de Activos Organizacionales", 
                        font=("Helvetica", 10), 
                        bg='#2c3e50', fg='#bdc3c7')
    subtitulo.pack(pady=(0, 15))
    
    # Frame contenedor para el scroll
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
    
    # Padding interno para el contenido scrollable
    inner_frame = tk.Frame(scrollable_frame, bg='white')
    inner_frame.pack(fill='both', expand=True, padx=30, pady=25)
    
    # Información introductoria
    info_text = tk.Label(inner_frame, 
                        text="Complete los siguientes campos para registrar un nuevo activo en el inventario:", 
                        font=("Helvetica", 11), 
                        bg='white', fg='#34495e')
    info_text.pack(pady=(0, 20), anchor='w')

    # Campos dinámicos con estilo moderno
    campos = [
        ("📝 Nombre del Activo:", "entry_nombre"),
        ("🏷️ Tipo de Activo:", "combo_tipo", ["Primario", "Secundario", "Soporte"]),
        ("📄 Descripción:", "entry_desc"),
        ("📊 Estado:", "combo_estado", ["En uso", "Vigente", "No vigente", "Eliminado"]),
        ("🏢 Área:", "entry_ubicacion"),
        ("🔄 Procesos vinculados:", "entry_proceso"),
        ("👤 Propietario:", "entry_prop"),
        ("🔒 Confidencialidad (1-5):", "combo_c", list(range(1, 6))),
        ("🛡️ Integridad (1-5):", "combo_i", list(range(1, 6))),
        ("⚡ Disponibilidad (1-5):", "combo_d", list(range(1, 6)))
    ]

    widgets = {}
    
    # Crear campos con estilo moderno
    for i, (texto, clave, *valores) in enumerate(campos):
        # Frame para cada campo
        campo_frame = tk.Frame(inner_frame, bg='white')
        campo_frame.pack(fill='x', pady=8)
        
        # Label con estilo moderno
        label = tk.Label(campo_frame, text=texto, 
                        font=("Helvetica", 10, "bold"), 
                        bg='white', fg='#2c3e50')
        label.pack(anchor='w', pady=(0, 3))
        
        if "combo" in clave:
            # Combobox con estilo
            combo = ttk.Combobox(campo_frame, values=valores[0], state="readonly",
                               font=("Helvetica", 10), height=8)
            combo.pack(fill='x', ipady=3)
            widgets[clave] = combo
            
            # Agregar efecto focus
            def on_combo_focus(event, combo=combo):
                combo.configure(style='Focus.TCombobox')
            combo.bind('<FocusIn>', on_combo_focus)
        else:
            # Entry con estilo moderno
            entry = tk.Entry(campo_frame, 
                           font=("Helvetica", 10),
                           bg='white',
                           fg='#2c3e50',
                           relief='solid',
                           borderwidth=1,
                           highlightthickness=2,
                           highlightcolor='#3498db')
            entry.pack(fill='x', ipady=5)
            widgets[clave] = entry
            
            # Efectos focus para entries
            def on_focus_in(event, entry=entry):
                entry.configure(bg='#f8f9fa', highlightbackground='#3498db')
            
            def on_focus_out(event, entry=entry):
                entry.configure(bg='white', highlightbackground='#bdc3c7')
            
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)

    # Sección CIA (Confidencialidad, Integridad, Disponibilidad) destacada
    cia_frame = tk.Frame(inner_frame, bg='#ecf0f1', relief='solid', borderwidth=1)
    cia_frame.pack(fill='x', pady=(15, 0))
    
    cia_header = tk.Label(cia_frame, 
                         text="🎯 Evaluación CIA (Confidencialidad, Integridad, Disponibilidad)", 
                         font=("Helvetica", 11, "bold"), 
                         bg='#ecf0f1', fg='#2c3e50')
    cia_header.pack(pady=10)
    
    cia_info = tk.Label(cia_frame, 
                       text="Valore cada criterio del 1 (Muy bajo) al 5 (Crítico)", 
                       font=("Helvetica", 9), 
                       bg='#ecf0f1', fg='#7f8c8d')
    cia_info.pack(pady=(0, 10))

    # Extraer referencias a los widgets
    entry_nombre = widgets["entry_nombre"]
    combo_tipo = widgets["combo_tipo"]
    entry_desc = widgets["entry_desc"]
    combo_estado = widgets["combo_estado"]
    entry_ubicacion = widgets["entry_ubicacion"]
    entry_proceso = widgets["entry_proceso"]
    entry_prop = widgets["entry_prop"]
    combo_c = widgets["combo_c"]
    combo_i = widgets["combo_i"]
    combo_d = widgets["combo_d"]

    def guardar_activo():
        try:
            nombre = entry_nombre.get().strip()
            tipo = combo_tipo.get()
            descripcion = entry_desc.get().strip()
            estado = combo_estado.get()
            ubicacion = entry_ubicacion.get().strip()
            procesos = entry_proceso.get().strip()
            propietario = entry_prop.get().strip()
            c = int(combo_c.get())
            i = int(combo_i.get())
            d = int(combo_d.get())
            
            # Validaciones mejoradas
            if not all([nombre, tipo, descripcion, estado, ubicacion, propietario]):
                messagebox.showerror("Error de Validación", 
                                   "❌ Todos los campos obligatorios deben ser completados.")
                return
                
        except Exception:
            messagebox.showerror("Error de Validación", 
                               "❌ Revisa todos los campos. Los valores CIA deben estar entre 1 y 5.")
            return

        va = calcular_valor_activo(c, i, d)
        
        # Cargar activos existentes
        try:
            with open(ACTIVOS_FILE, "r", encoding='utf-8') as f:
                activos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            activos = []
        
        # Crear el nuevo activo con toda la información del formulario
        nuevo_activo = {
            "nombre": nombre,
            "tipo": tipo,
            "descripcion": descripcion,
            "estado": estado,
            "area": ubicacion,
            "procesos": procesos,
            "propietario": propietario,
            "confidencialidad": c,
            "integridad": i,
            "disponibilidad": d,
            "valor": va,
            "impacto_cia": f"C:{c} I:{i} D:{d}"
        }
        
        activos.append(nuevo_activo)

        # Guardar con encoding UTF-8
        with open(ACTIVOS_FILE, "w", encoding='utf-8') as f:
            json.dump(activos, f, indent=4, ensure_ascii=False)
            
        print(f"✅ Activo guardado: {nombre} con valor {va}")

        # Mensaje de éxito mejorado
        messagebox.showinfo("✅ Registro Exitoso", 
                           f"Activo '{nombre}' registrado exitosamente\n\n"
                           f"📊 Valor del Activo: {va}\n"
                           f"🎯 Impacto CIA: C:{c} I:{i} D:{d}")
        ventana.destroy()

    # Frame de botones
    btn_frame = tk.Frame(main_frame, bg='#f0f0f0')
    btn_frame.pack(fill='x', pady=(0, 0))
    
    # Crear frame interno para centrar los botones
    btn_container = tk.Frame(btn_frame, bg='#f0f0f0')
    btn_container.pack()
    
    # Botón Guardar con estilo moderno
    guardar_btn = tk.Button(btn_container, text="💾 Registrar Activo", 
                           command=guardar_activo,
                           font=("Helvetica", 12, "bold"),
                           bg='#27ae60', fg='white',
                           relief='flat', padx=30, pady=12,
                           cursor='hand2',
                           activebackground='#219a52',
                           activeforeground='white')
    guardar_btn.pack(side='left', padx=5)
    
    # Efectos hover para botón guardar
    def on_enter_guardar(event):
        guardar_btn.configure(bg='#219a52')
    
    def on_leave_guardar(event):
        guardar_btn.configure(bg='#27ae60')
    
    guardar_btn.bind("<Enter>", on_enter_guardar)
    guardar_btn.bind("<Leave>", on_leave_guardar)
    
    # Botón Cancelar
    cancelar_btn = tk.Button(btn_container, text="❌ Cancelar", 
                            command=ventana.destroy,
                            font=("Helvetica", 12),
                            bg='#95a5a6', fg='white',
                            relief='flat', padx=25, pady=12,
                            cursor='hand2',
                            activebackground='#7f8c8d',
                            activeforeground='white')
    cancelar_btn.pack(side='left', padx=5)
    
    # Efectos hover para botón cancelar
    def on_enter_cancelar(event):
        cancelar_btn.configure(bg='#7f8c8d')
    
    def on_leave_cancelar(event):
        cancelar_btn.configure(bg='#95a5a6')
    
    cancelar_btn.bind("<Enter>", on_enter_cancelar)
    cancelar_btn.bind("<Leave>", on_leave_cancelar)
    
    # Centrar ventana
    ventana.transient()
    ventana.grab_set()
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (650 // 2)
    y = (ventana.winfo_screenheight() // 2) - (650 // 2)
    ventana.geometry(f"650x650+{x}+{y}")
    
    # Configurar scroll con mouse wheel
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _bind_to_mousewheel(event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def _unbind_from_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")
    
    canvas.bind('<Enter>', _bind_to_mousewheel)
    canvas.bind('<Leave>', _unbind_from_mousewheel)
    
    # Focus inicial en el primer campo
    entry_nombre.focus_set()
    
    # Asegurar que el canvas se actualice después de crear todos los widgets
    ventana.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def obtener_activos():
    """Obtiene la lista de activos desde el archivo JSON"""
    try:
        if not os.path.exists(ACTIVOS_FILE):
            print(f"⚠️ Archivo de activos no encontrado: {ACTIVOS_FILE}")
            # Crear archivo con activos por defecto
            activos_default = [
                {
                    "nombre": "general",
                    "tipo": "Activo por defecto",
                    "valor": 2.0,
                    "descripcion": "Valor por defecto para activos no especificados"
                }
            ]
            with open(ACTIVOS_FILE, "w", encoding='utf-8') as f:
                json.dump(activos_default, f, indent=4, ensure_ascii=False)
            return activos_default
        
        with open(ACTIVOS_FILE, "r", encoding='utf-8') as f:
            activos = json.load(f)
            
        # Validar que todos los activos tengan las claves mínimas necesarias
        activos_validos = []
        for activo in activos:
            # Los campos mínimos necesarios para el analyzer son 'nombre' y 'valor'
            if 'valor' in activo and 'nombre' in activo:
                activos_validos.append(activo)
            else:
                print(f"⚠️ Activo incompleto encontrado: {activo.get('nombre', 'Sin nombre')}")
                
        print(f"✅ Cargados {len(activos_validos)} activos válidos desde {ACTIVOS_FILE}")
        return activos_validos
        
    except json.JSONDecodeError as e:
        print(f"❌ Error al leer JSON de activos: {e}")
        return [{"nombre": "general", "tipo": "Default", "valor": 2.0}]
    except Exception as e:
        print(f"❌ Error al cargar activos: {e}")
        return [{"nombre": "general", "tipo": "Default", "valor": 2.0}]

def listar_activos():
    """Lista todos los activos registrados en el sistema"""
    activos = obtener_activos()
    print("\n📋 Inventario de Activos:")
    print("=" * 50)
    
    if not activos:
        print("No hay activos registrados.")
        return
        
    for i, activo in enumerate(activos, 1):
        nombre = activo.get('nombre', 'Sin nombre')
        tipo = activo.get('tipo', 'N/A')
        valor = activo.get('valor', 0.0)
        estado = activo.get('estado', 'N/A')
        
        print(f"{i:2d}. {nombre}")
        print(f"    📋 Tipo: {tipo}")
        print(f"    📊 Valor: {valor}")
        print(f"    🔄 Estado: {estado}")
        
        # Mostrar información adicional si está disponible
        if 'propietario' in activo:
            print(f"    👤 Propietario: {activo['propietario']}")
        if 'area' in activo:
            print(f"    🏢 Área: {activo['area']}")
        if 'impacto_cia' in activo:
            print(f"    🎯 CIA: {activo['impacto_cia']}")
        print()

if __name__ == "__main__":
    registrar_activo_gui()