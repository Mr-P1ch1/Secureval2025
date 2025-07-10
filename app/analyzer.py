# app/analyzer.py (versión final ultra integrada con herramientas offline)
import os
import json
import subprocess
import requests
import socket
import ssl
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
from .activos import obtener_activos

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
# Usar ruta absoluta para resultados
RESULTADOS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resultados")
os.makedirs(RESULTADOS_DIR, exist_ok=True)

def clasificar_servicio(tech, url):
    tech_lower = tech.lower()
    url_lower = url.lower()
    if any(x in tech_lower for x in ["smtp", "mail", "roundcube"]):
        return "Servidor de Correo"
    if any(x in tech_lower for x in ["ftp", "sftp"]):
        return "Servidor FTP"
    if any(x in tech_lower for x in ["mysql", "postgres", "mongodb", "mariadb"]):
        return "Base de Datos"
    if any(x in tech_lower for x in ["wordpress", "joomla", "cms", "drupal"]):
        return "Gestor de Contenidos"
    if "login" in url_lower:
        return "Portal de Acceso"
    if "api" in url_lower or "swagger" in url_lower:
        return "API Web"
    if "admin" in url_lower or "cpanel" in url_lower:
        return "Panel Administrativo"
    return "Otro"

def detectar_sistema_operativo(subdominio):
    try:
        result = subprocess.check_output(["curl", "-sI", f"http://{subdominio}"], timeout=10).decode()
        headers = result.lower()
        if "x-aspnet-version" in headers or "iis" in headers:
            return "Windows/IIS"
        elif "x-powered-by: php" in headers:
            return "Linux/PHP"
        elif "ubuntu" in headers or "linux" in headers:
            return "Linux"
        elif "windows" in headers:
            return "Windows"
        elif "cloudflare" in headers:
            return "Proxy/CDN"
        else:
            return "Desconocido"
    except:
        return "Desconocido"

def verificar_tls(subdominio):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((subdominio, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=subdominio) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                version = ssock.version()
                return {
                    "tls_version": version,
                    "cifrado": cipher[0],
                    "valido_hasta": cert.get("notAfter", "")
                }
    except:
        return {"tls_version": "No disponible", "cifrado": "-", "valido_hasta": "-"}

def escanear_puertos_nmap(url):
    """Escanea puertos usando nmap, extrayendo el hostname de la URL"""
    try:
        # Extraer hostname de la URL
        if "://" in url:
            hostname = url.split("://")[1].split("/")[0].split(":")[0]
        else:
            hostname = url.split("/")[0].split(":")[0]
        
        print(f"🛡️ Escaneando puertos para hostname: {hostname}")
        
        # Verificar si el hostname se puede resolver antes de escanear
        try:
            import socket
            socket.gethostbyname(hostname)
        except socket.gaierror:
            print(f"❌ No se puede resolver DNS para {hostname}")
            return [f"DNS no resuelve: {hostname}"]
        
        # Ejecutar nmap con configuración optimizada
        cmd = ["nmap", "-T4", "-F", "--max-retries", "1", hostname]
        resultado = subprocess.check_output(cmd, timeout=45, stderr=subprocess.DEVNULL).decode()
        
        # Extraer solo las líneas con puertos abiertos
        lineas = []
        for line in resultado.splitlines():
            if "/tcp" in line and "open" in line:
                # Limpiar y formatear la línea
                puerto_info = line.strip().split()
                if len(puerto_info) >= 3:
                    puerto = puerto_info[0]
                    estado = puerto_info[1] 
                    servicio = puerto_info[2] if len(puerto_info) > 2 else "unknown"
                    lineas.append(f"{puerto} {estado} {servicio}")
        
        if lineas:
            print(f"✅ Puertos abiertos encontrados para {hostname}: {len(lineas)} puertos")
            return lineas
        else:
            print(f"🔒 No se encontraron puertos abiertos para {hostname}")
            return ["No hay puertos abiertos"]
            
    except subprocess.TimeoutExpired:
        print(f"⏱️ Timeout en escaneo de puertos para {hostname} (45s)")
        return ["Timeout en escaneo (45s)"]
    except FileNotFoundError:
        print("❌ Nmap no está instalado o no está en PATH")
        return ["Nmap no disponible"]
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en comando nmap para {hostname}: código {e.returncode}")
        return ["Error en comando nmap"]
    except Exception as e:
        print(f"❌ Error inesperado al escanear {hostname}: {e}")
        return [f"Error: {str(e)[:50]}..."]

def ejecutar_assetfinder(dominio):
    salida = os.path.join(RESULTADOS_DIR, dominio, "subdominios.txt")
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    with open(salida, "w") as f:
        subprocess.run(["assetfinder", "--subs-only", dominio], stdout=f, check=True)
    return salida

def ejecutar_whatweb(file_subdominios, dominio):
    salida = os.path.join(RESULTADOS_DIR, dominio, "tecnologias.json")
    subprocess.run(["whatweb", "-i", file_subdominios, "--log-json", salida], check=True)
    return salida

cve_cache = {}
def buscar_cves(tecnologia):
    if tecnologia in cve_cache:
        return cve_cache[tecnologia]
    url = f"{NVD_API_URL}?keywordSearch={tecnologia}&resultsPerPage=3"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            datos = response.json().get("vulnerabilities", [])
            cve_cache[tecnologia] = datos
            return datos
    except:
        pass
    return []

def evaluar_riesgo_secureval(va, cvss):
    if cvss >= 9.0:
        prob = 5
        vul = 5
    elif cvss >= 7.0:
        prob = 4
        vul = 4
    elif cvss >= 4.0:
        prob = 3
        vul = 3
    elif cvss >= 0.1:
        prob = 2
        vul = 2
    else:
        prob = 1
        vul = 1
    riesgo = round(va * prob * vul, 2)
    return prob, vul, riesgo

def analizar_dominio(dominio, opciones=None):
    """
    Analiza un dominio con las opciones especificadas
    
    Args:
        dominio: Dominio a analizar
        opciones: Diccionario con las opciones habilitadas:
                 {'subdominios': bool, 'tecnologias': bool, 'puertos': bool, 
                  'tls': bool, 'cves': bool}
    """
    if opciones is None:
        opciones = {
            'subdominios': True,
            'tecnologias': True, 
            'puertos': True,
            'tls': True,
            'cves': True
        }
    
    print(f"🔍 Analizando dominio: {dominio}")
    print(f"📋 Opciones habilitadas: {opciones}")
    carpeta = os.path.join(RESULTADOS_DIR, dominio)
    os.makedirs(carpeta, exist_ok=True)

    subdominios_txt = ejecutar_assetfinder(dominio) if opciones.get('subdominios', True) else None
    tecnologias_json = ejecutar_whatweb(subdominios_txt, dominio) if opciones.get('tecnologias', True) else None

    if not tecnologias_json or not os.path.exists(tecnologias_json):
        print("❌ No se pudo obtener información de tecnologías")
        return []

    activos = obtener_activos()
    resultados = []
    errores = []
    resumen = {}
    puertos_totales_detectados = 0
    hosts_con_puertos = 0

    print(f"📄 Procesando archivo de tecnologías: {tecnologias_json}")
    
    with open(tecnologias_json, "r") as f:
        lineas_procesadas = 0
        for line in f:
            try:
                lineas_procesadas += 1
                data = json.loads(line)
                url = data.get("target")
                plugins = data.get("plugins", {})
                
                if not url:
                    continue
                    
                print(f"🔍 Procesando {lineas_procesadas}: {url}")
                
                sistema_operativo = detectar_sistema_operativo(url)
                
                # Solo verificar TLS si la opción está habilitada
                info_tls = verificar_tls(url) if opciones.get('tls', True) else "No verificado"
                
                # Solo escanear puertos si la opción está habilitada
                if opciones.get('puertos', True):
                    print(f"🛡️ Iniciando escaneo de puertos para {url}")
                    puertos = escanear_puertos_nmap(url)
                    
                    # Contar puertos abiertos reales para estadísticas
                    puertos_abiertos = [p for p in puertos if not any(x in p.lower() for x in 
                                       ["dns no resuelve", "timeout", "error", "no hay puertos", "nmap no disponible"])]
                    
                    if puertos_abiertos:
                        print(f"✅ {len(puertos_abiertos)} puertos abiertos detectados en {url}")
                        puertos_totales_detectados += len(puertos_abiertos)
                        hosts_con_puertos += 1
                    else:
                        print(f"🔒 Sin puertos abiertos detectados en {url}")
                else:
                    print(f"⏭️ Saltando escaneo de puertos para {url} (opción deshabilitada)")
                    puertos = ["Escaneo de puertos deshabilitado"]

                for tech in plugins:
                    tipo_servicio = clasificar_servicio(tech, url)
                    
                    # Solo buscar CVEs si la opción está habilitada
                    if opciones.get('cves', True):
                        print(f"⚠️ Buscando CVEs para tecnología {tech} (opción habilitada)")
                        cves = buscar_cves(tech)
                        cvss_scores = [
                            cve["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]
                            for cve in cves if "cvssMetricV31" in cve["cve"]["metrics"]
                        ]
                        max_cvss = max(cvss_scores) if cvss_scores else 0.0
                    else:
                        print(f"⏭️ Saltando búsqueda de CVEs para {tech} (opción deshabilitada)")
                        cves = []
                        max_cvss = 0.0

                    va = 2.0
                    for a in activos:
                        if a["nombre"].lower() in url.lower():
                            va = a.get("valor", 2.0)
                            break

                    prob, vul, riesgo = evaluar_riesgo_secureval(va, max_cvss)
                    criticidad = "Bajo"
                    if riesgo >= 80:
                        criticidad = "Crítico"
                    elif riesgo >= 50:
                        criticidad = "Alto"
                    elif riesgo >= 25:
                        criticidad = "Medio"

                    resultados.append({
                        "subdominio": url,
                        "tecnologia": tech,
                        "tipo_servicio": tipo_servicio,
                        "sistema_operativo": sistema_operativo,
                        "puertos": puertos,
                        "tls": info_tls,
                        "cvss_max": max_cvss,
                        "valor_activo": va,
                        "probabilidad": prob,
                        "vulnerabilidad": vul,
                        "riesgo": riesgo,
                        "criticidad": criticidad,
                        "cves": [cve["cve"]["id"] for cve in cves]
                    })

                    if url not in resumen:
                        resumen[url] = {"tecnologias": set(), "cves": set(), "riesgos": []}
                    resumen[url]["tecnologias"].add(tech)
                    resumen[url]["cves"].update([cve["cve"]["id"] for cve in cves])
                    resumen[url]["riesgos"].append(riesgo)

            except json.JSONDecodeError as e:
                error_msg = f"Error JSON en línea {lineas_procesadas}: {str(e)[:100]}"
                print(f"❌ {error_msg}")
                errores.append(error_msg)
                continue
            except Exception as e:
                error_msg = f"Error procesando línea {lineas_procesadas} ({url}): {str(e)[:100]}"
                print(f"❌ {error_msg}")
                errores.append(error_msg)
                continue

    # Guardar resultados con metadatos adicionales
    metadata = {
        "dominio": dominio,
        "total_resultados": len(resultados),
        "total_errores": len(errores),
        "opciones_utilizadas": opciones,
        "estadisticas_puertos": {
            "total_puertos_detectados": puertos_totales_detectados,
            "hosts_con_puertos": hosts_con_puertos,
            "total_hosts_escaneados": lineas_procesadas
        } if opciones.get('puertos', True) else "Escaneo de puertos deshabilitado"
    }
    
    # Guardar archivo principal de resultados
    ruta_riesgo = os.path.join(carpeta, "riesgo.json")
    with open(ruta_riesgo, "w") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)
    
    # Guardar metadatos del análisis
    ruta_metadata = os.path.join(carpeta, "metadata.json")
    with open(ruta_metadata, "w") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    resumen_final = {
        s: {
            "tecnologias": list(v["tecnologias"]),
            "total_tecnologias": len(v["tecnologias"]),
            "total_cves": len(v["cves"]),
            "riesgo_max": max(v["riesgos"]),
            "riesgo_promedio": round(sum(v["riesgos"]) / len(v["riesgos"]), 2)
        } for s, v in resumen.items()
    }
    with open(os.path.join(carpeta, "resumen.json"), "w") as f:
        json.dump(resumen_final, f, indent=4)

    if errores:
        ruta_errores = os.path.join(carpeta, "errores.log")
        with open(ruta_errores, "w") as f:
            f.write("\n".join(errores))
        print(f"⚠️ Se registraron {len(errores)} errores en: {ruta_errores}")

    # Mostrar estadísticas finales
    print(f"\n📊 RESUMEN DEL ANÁLISIS:")
    print(f"✅ Resultados procesados: {len(resultados)}")
    print(f"❌ Errores encontrados: {len(errores)}")
    
    if opciones.get('puertos', True):
        print(f"🛡️ Estadísticas de puertos:")
        print(f"   • Total puertos abiertos: {puertos_totales_detectados}")
        print(f"   • Hosts con puertos: {hosts_con_puertos}/{lineas_procesadas}")
        if hosts_con_puertos > 0:
            promedio = puertos_totales_detectados / hosts_con_puertos
            print(f"   • Promedio puertos por host: {promedio:.1f}")
    
    print(f"📁 Resultados guardados en: {ruta_riesgo}")
    return resultados

def lanzar_analyzer_gui():
    """Interfaz moderna para análisis de dominios con configuración avanzada."""
    ventana = tk.Toplevel()
    ventana.title("🔍 Análisis de Dominio - SECUREVAL")
    ventana.geometry("700x600")
    ventana.configure(bg='#f0f0f0')
    ventana.resizable(False, False)
    
    # Frame principal con padding
    main_frame = tk.Frame(ventana, bg='#f0f0f0')
    main_frame.pack(fill='both', expand=True, padx=25, pady=25)
    
    # Header moderno
    header_frame = tk.Frame(main_frame, bg='#e74c3c', relief='solid', borderwidth=1)
    header_frame.pack(fill='x', pady=(0, 20))
    
    titulo_header = tk.Label(header_frame, 
                            text="🔍 ANÁLISIS DE SEGURIDAD", 
                            font=("Helvetica", 18, "bold"), 
                            bg='#e74c3c', fg='#ecf0f1')
    titulo_header.pack(pady=15)
    
    subtitulo = tk.Label(header_frame, 
                        text="Evaluación Integral de Vulnerabilidades y Tecnologías", 
                        font=("Helvetica", 10), 
                        bg='#e74c3c', fg='#f8f9fa')
    subtitulo.pack(pady=(0, 15))
    
    # Frame de contenido con scroll
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
    
    # Mensaje de bienvenida inicial
    welcome_frame = tk.Frame(inner_frame, bg='white')
    welcome_frame.pack(fill='both', expand=True)
    
    welcome_text = tk.Label(welcome_frame, 
                           text="¡Bienvenido al Módulo de Análisis de Seguridad!", 
                           font=("Helvetica", 16, "bold"), 
                           bg='white', fg='#e74c3c')
    welcome_text.pack(pady=(20, 15))
    
    desc_text = tk.Label(welcome_frame, 
                        text="Este módulo realizará un análisis exhaustivo de seguridad en el dominio especificado.", 
                        font=("Helvetica", 12), 
                        bg='white', fg='#34495e')
    desc_text.pack(pady=(0, 20))
    
    # Información introductoria
    info_frame = tk.Frame(welcome_frame, bg='#ecf0f1', relief='solid', borderwidth=1)
    info_frame.pack(fill='x', pady=(0, 30))
    
    info_header = tk.Label(info_frame, 
                          text="📋 Proceso de Análisis Automatizado", 
                          font=("Helvetica", 12, "bold"), 
                          bg='#ecf0f1', fg='#2c3e50')
    info_header.pack(pady=(15, 10))
    
    procesos = [
        "🔎 Detección de subdominios con AssetFinder",
        "🛠️ Identificación de tecnologías con WhatWeb", 
        "🛡️ Escaneo de puertos con Nmap",
        "🔒 Verificación de certificados TLS/SSL",
        "⚠️ Búsqueda de CVEs en base NIST NVD",
        "📊 Evaluación de riesgos según metodología SECUREVAL"
    ]
    
    for proceso in procesos:
        tk.Label(info_frame, text=proceso, 
                font=("Helvetica", 10), 
                bg='#ecf0f1', fg='#34495e').pack(anchor='w', padx=20, pady=2)
    
    tk.Label(info_frame, text=" ", bg='#ecf0f1').pack(pady=10)
    
    # Nota importante
    nota_frame = tk.Frame(welcome_frame, bg='#fff3cd', relief='solid', borderwidth=1)
    nota_frame.pack(fill='x', pady=(0, 20))
    
    tk.Label(nota_frame, text="⚠️ Nota Importante", 
            font=("Helvetica", 11, "bold"), 
            bg='#fff3cd', fg='#856404').pack(pady=(10, 5))
    
    tk.Label(nota_frame, text="Asegúrese de tener permisos para analizar el dominio objetivo.", 
            font=("Helvetica", 10), 
            bg='#fff3cd', fg='#856404').pack(pady=(0, 10))
    
    def mostrar_formulario():
        # Ocultar frame de bienvenida
        welcome_frame.pack_forget()
        
        # Mostrar formulario de análisis
        form_frame = tk.Frame(inner_frame, bg='white')
        form_frame.pack(fill='both', expand=True)
        
        # Frame para entrada de dominio
        dominio_frame = tk.Frame(form_frame, bg='white')
        dominio_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(dominio_frame, text="🌐 Dominio objetivo:", 
                font=("Helvetica", 12, "bold"), 
                bg='white', fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        
        entry_dominio = tk.Entry(dominio_frame, 
                               font=("Helvetica", 11),
                               bg='white',
                               fg='#2c3e50',
                               relief='solid',
                               borderwidth=2,
                               highlightthickness=2,
                               highlightcolor='#e74c3c')
        entry_dominio.pack(fill='x', ipady=8)
        
        # Tip para el usuario
        tip_label = tk.Label(dominio_frame, 
                           text="💡 Presione Enter para iniciar el análisis", 
                           font=("Helvetica", 9, "italic"), 
                           bg='white', fg='#7f8c8d')
        tip_label.pack(anchor='w', pady=(3, 0))
        
        # Placeholder y efectos
        placeholder_text = "Ej: ejemplo.com, empresa.org, banco.fin.ec"
        entry_dominio.insert(0, placeholder_text)
        entry_dominio.configure(fg='#7f8c8d')
        
        def on_focus_in_dominio(event):
            if entry_dominio.get() == placeholder_text:
                entry_dominio.delete(0, tk.END)
                entry_dominio.configure(fg='#2c3e50', bg='#f8f9fa')
        
        def on_focus_out_dominio(event):
            if not entry_dominio.get():
                entry_dominio.insert(0, placeholder_text)
                entry_dominio.configure(fg='#7f8c8d', bg='white')
            else:
                entry_dominio.configure(bg='white')
        
        entry_dominio.bind('<FocusIn>', on_focus_in_dominio)
        entry_dominio.bind('<FocusOut>', on_focus_out_dominio)
        
        # Funcionalidad Enter para iniciar análisis
        def on_enter_key(event):
            ejecutar_analisis_completo()
        
        entry_dominio.bind('<Return>', on_enter_key)
        
        # Opciones de configuración
        config_frame = tk.Frame(form_frame, bg='white')
        config_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(config_frame, text="⚙️ Configuración del Análisis:", 
                font=("Helvetica", 12, "bold"), 
                bg='white', fg='#2c3e50').pack(anchor='w', pady=(0, 10))
        
        # Checkboxes con estilo
        check_frame = tk.Frame(config_frame, bg='white')
        check_frame.pack(fill='x')
        
        var_subdominios = tk.BooleanVar(value=True)
        var_tecnologias = tk.BooleanVar(value=True)
        var_puertos = tk.BooleanVar(value=True)
        var_tls = tk.BooleanVar(value=True)
        var_cves = tk.BooleanVar(value=True)
        
        opciones = [
            (var_subdominios, "🔎 Descubrir subdominios"),
            (var_tecnologias, "🛠️ Detectar tecnologías"),
            (var_puertos, "🛡️ Escanear puertos"),
            (var_tls, "🔒 Verificar TLS/SSL"),
            (var_cves, "⚠️ Buscar vulnerabilidades (CVEs)")
        ]
        
        for i, (var, texto) in enumerate(opciones):
            check = tk.Checkbutton(check_frame, text=texto, variable=var,
                                  font=("Helvetica", 10),
                                  bg='white', fg='#34495e',
                                  selectcolor='#e74c3c',
                                  activebackground='white',
                                  activeforeground='#2c3e50')
            check.grid(row=i//2, column=i%2, sticky='w', padx=(0, 20), pady=2)
        
        # Área de progreso y resultados
        progress_frame = tk.Frame(form_frame, bg='#2c3e50', relief='solid', borderwidth=1)
        progress_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        tk.Label(progress_frame, text="📊 Monitor de Progreso", 
                font=("Helvetica", 11, "bold"), 
                bg='#2c3e50', fg='#ecf0f1').pack(pady=(10, 5))
        
        # Progress bar
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, 
                                      maximum=100, length=300)
        progress_bar.pack(pady=5)
        
        # Área de texto para el log
        log_text = tk.Text(progress_frame, height=6, width=60,
                          bg='#34495e', fg='#ecf0f1',
                          font=("Consolas", 9),
                          relief='flat')
        log_text.pack(fill='both', expand=True, padx=10, pady=(5, 10))
        
        # Scrollbar para el log
        log_scroll = ttk.Scrollbar(progress_frame, orient="vertical", command=log_text.yview)
        log_text.configure(yscrollcommand=log_scroll.set)
        
        def log_mensaje(mensaje):
            log_text.insert(tk.END, f"{mensaje}\n")
            log_text.see(tk.END)
            ventana.update_idletasks()
        
        def ejecutar_analisis_completo():
            dominio = entry_dominio.get().strip()
            if not dominio or dominio == placeholder_text:
                messagebox.showerror("Error de Validación", 
                                   "❌ Debe ingresar un dominio válido para analizar.")
                return
            
            # Deshabilitar botón durante análisis
            analizar_btn.configure(state='disabled', text="🔄 Analizando...", bg='#95a5a6')
            log_text.delete(1.0, tk.END)
            progress_var.set(0)
            
            def tarea_analisis():
                try:
                    log_mensaje(f"🚀 Iniciando análisis para: {dominio}")
                    progress_var.set(10)
                    
                    if var_subdominios.get():
                        log_mensaje("🔎 Descubriendo subdominios...")
                        progress_var.set(20)
                    
                    if var_tecnologias.get():
                        log_mensaje("🛠️ Identificando tecnologías...")
                        progress_var.set(40)
                    
                    if var_puertos.get():
                        log_mensaje("🛡️ Escaneando puertos...")
                        progress_var.set(60)
                    
                    if var_tls.get():
                        log_mensaje("🔒 Verificando certificados TLS...")
                        progress_var.set(75)
                    
                    if var_cves.get():
                        log_mensaje("⚠️ Buscando vulnerabilidades...")
                        progress_var.set(85)
                    
                    # Crear diccionario de opciones basado en las selecciones del usuario
                    opciones = {
                        'subdominios': var_subdominios.get(),
                        'tecnologias': var_tecnologias.get(),
                        'puertos': var_puertos.get(),
                        'tls': var_tls.get(),
                        'cves': var_cves.get()
                    }
                    
                    # Ejecutar análisis real con las opciones seleccionadas
                    resultados = analizar_dominio(dominio, opciones)
                    progress_var.set(100)
                    
                    log_mensaje(f"✅ Análisis completado exitosamente")
                    log_mensaje(f"📊 Tecnologías detectadas: {len(resultados)}")
                    log_mensaje(f"📁 Resultados guardados en: resultados/{dominio}/")
                    
                    messagebox.showinfo("✅ Análisis Completado", 
                                       f"Análisis de '{dominio}' finalizado exitosamente.\n\n"
                                       f"📊 Tecnologías encontradas: {len(resultados)}\n"
                                       f"📁 Resultados disponibles en la carpeta de resultados.")
                    
                except Exception as e:
                    log_mensaje(f"❌ Error durante el análisis: {str(e)}")
                    messagebox.showerror("Error de Análisis", 
                                       f"❌ Error durante el análisis:\n{str(e)}")
                finally:
                    # Rehabilitar botón
                    analizar_btn.configure(state='normal', text="🚀 Iniciar Análisis", bg='#e74c3c')
            
            # Ejecutar en hilo separado
            threading.Thread(target=tarea_analisis, daemon=True).start()
        
        # Actualizar botones para el formulario
        btn_container.pack_forget()
        
        # Nuevo contenedor de botones para formulario
        form_btn_container = tk.Frame(btn_frame, bg='#f0f0f0')
        form_btn_container.pack()
        
        # Botón Analizar
        nonlocal analizar_btn
        analizar_btn = tk.Button(form_btn_container, text="🚀 Iniciar Análisis", 
                               command=ejecutar_analisis_completo,
                               font=("Helvetica", 12, "bold"),
                               bg='#e74c3c', fg='white',
                               relief='flat', padx=30, pady=12,
                               cursor='hand2',
                               activebackground='#c0392b',
                               activeforeground='white')
        analizar_btn.pack(side='left', padx=5)
        
        # Efectos hover para botón analizar
        def on_enter_analizar(event):
            if analizar_btn['state'] != 'disabled':
                analizar_btn.configure(bg='#c0392b')
        
        def on_leave_analizar(event):
            if analizar_btn['state'] != 'disabled':
                analizar_btn.configure(bg='#e74c3c')
        
        analizar_btn.bind("<Enter>", on_enter_analizar)
        analizar_btn.bind("<Leave>", on_leave_analizar)
        
        # Botón Volver
        volver_btn = tk.Button(form_btn_container, text="⬅️ Volver", 
                              command=lambda: [form_frame.pack_forget(), welcome_frame.pack(fill='both', expand=True), form_btn_container.pack_forget(), btn_container.pack()],
                              font=("Helvetica", 12),
                              bg='#95a5a6', fg='white',
                              relief='flat', padx=25, pady=12,
                              cursor='hand2',
                              activebackground='#7f8c8d',
                              activeforeground='white')
        volver_btn.pack(side='left', padx=5)
        
        # Efectos hover para botón volver
        def on_enter_volver(event):
            volver_btn.configure(bg='#7f8c8d')
        
        def on_leave_volver(event):
            volver_btn.configure(bg='#95a5a6')
        
        volver_btn.bind("<Enter>", on_enter_volver)
        volver_btn.bind("<Leave>", on_leave_volver)
        
        # Focus inicial en el campo de dominio
        entry_dominio.focus_set()
        entry_dominio.select_range(0, tk.END)
    
    # Frame de botones inicial
    btn_frame = tk.Frame(main_frame, bg='#f0f0f0')
    btn_frame.pack(fill='x')
    
    # Crear frame interno para centrar los botones
    btn_container = tk.Frame(btn_frame, bg='#f0f0f0')
    btn_container.pack()
    
    # Variable para el botón de análisis (se usará en el formulario)
    analizar_btn = None
    
    # Botón Comenzar Análisis
    comenzar_btn = tk.Button(btn_container, text="🚀 Comenzar Análisis", 
                           command=mostrar_formulario,
                           font=("Helvetica", 12, "bold"),
                           bg='#e74c3c', fg='white',
                           relief='flat', padx=30, pady=15,
                           cursor='hand2',
                           activebackground='#c0392b',
                           activeforeground='white')
    comenzar_btn.pack(side='left', padx=5)
    
    # Efectos hover para botón comenzar
    def on_enter_comenzar(event):
        comenzar_btn.configure(bg='#c0392b')
    
    def on_leave_comenzar(event):
        comenzar_btn.configure(bg='#e74c3c')
    
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
    
    # Efectos hover para botón cerrar
    def on_enter_cerrar(event):
        cerrar_btn.configure(bg='#7f8c8d')
    
    def on_leave_cerrar(event):
        cerrar_btn.configure(bg='#95a5a6')
    
    cerrar_btn.bind("<Enter>", on_enter_cerrar)
    cerrar_btn.bind("<Leave>", on_leave_cerrar)
    
    # Centrar ventana
    ventana.transient()
    ventana.grab_set()
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (700 // 2)
    y = (ventana.winfo_screenheight() // 2) - (600 // 2)
    ventana.geometry(f"700x600+{x}+{y}")
    
    # Configurar scroll con mouse wheel
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _bind_to_mousewheel(event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def _unbind_from_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")
    
    canvas.bind('<Enter>', _bind_to_mousewheel)
    canvas.bind('<Leave>', _unbind_from_mousewheel)
    
    # Focus inicial en el botón comenzar
    comenzar_btn.focus_set()
    
    # Asegurar que el canvas se actualice después de crear todos los widgets
    ventana.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
