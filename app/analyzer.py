# app/analyzer.py (versión ampliada con detección de OS y clasificación avanzada)
import os
import json
import subprocess
import requests
from app.activos import obtener_activos

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
RESULTADOS_DIR = "resultados"
os.makedirs(RESULTADOS_DIR, exist_ok=True)

# Clasificación por servicio
def clasificar_servicio(tech, url):
    tech_lower = tech.lower()
    url_lower = url.lower()
    if any(x in tech_lower for x in ["smtp", "mail", "roundcube"]):
        return "Servidor de Correo"
    if any(x in tech_lower for x in ["ftp", "sftp"]):
        return "Servidor FTP"
    if any(x in tech_lower for x in ["mysql", "postgres", "mongodb"]):
        return "Base de Datos"
    if any(x in tech_lower for x in ["wordpress", "joomla", "cms"]):
        return "Gestor de Contenidos"
    if "login" in url_lower:
        return "Portal de Acceso"
    return "Otro"

# Detección de sistema operativo por WhatWeb o cabecera curl
def detectar_sistema_operativo(subdominio):
    try:
        result = subprocess.check_output(["curl", "-sI", f"http://{subdominio}"], timeout=10).decode()
        server_header = next((line for line in result.split("\n") if "Server:" in line), "").lower()
        if "windows" in server_header:
            return "Windows"
        elif "ubuntu" in server_header or "linux" in server_header:
            return "Linux"
        elif "nginx" in server_header:
            return "Linux/Unix"
        elif "iis" in server_header:
            return "Windows/IIS"
        elif "cloudflare" in server_header:
            return "Proxy/CDN"
        else:
            return "Desconocido"
    except:
        return "Desconocido"

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

def buscar_cves(tecnologia):
    url = f"{NVD_API_URL}?keywordSearch={tecnologia}&resultsPerPage=3"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.json().get("vulnerabilities", [])
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

def analizar_dominio(dominio):
    print(f"🔍 Analizando dominio: {dominio}")
    carpeta = os.path.join(RESULTADOS_DIR, dominio)
    os.makedirs(carpeta, exist_ok=True)

    subdominios_txt = ejecutar_assetfinder(dominio)
    tecnologias_json = ejecutar_whatweb(subdominios_txt, dominio)

    activos = obtener_activos()
    resultados = []

    with open(tecnologias_json, "r") as f:
        for line in f:
            try:
                data = json.loads(line)
                url = data.get("target")
                plugins = data.get("plugins", {})
                sistema_operativo = detectar_sistema_operativo(url)
                for tech in plugins:
                    tipo_servicio = clasificar_servicio(tech, url)
                    cves = buscar_cves(tech)
                    cvss_scores = [
                        cve["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]
                        for cve in cves if "cvssMetricV31" in cve["cve"]["metrics"]
                    ]
                    max_cvss = max(cvss_scores) if cvss_scores else 0.0

                    va = 2.0  # Default
                    for a in activos:
                        if a["nombre"].lower() in url.lower():
                            va = a.get("valor", 2.0)
                            break

                    prob, vul, riesgo = evaluar_riesgo_secureval(va, max_cvss)
                    resultados.append({
                        "subdominio": url,
                        "tecnologia": tech,
                        "tipo_servicio": tipo_servicio,
                        "sistema_operativo": sistema_operativo,
                        "cvss_max": max_cvss,
                        "valor_activo": va,
                        "probabilidad": prob,
                        "vulnerabilidad": vul,
                        "riesgo": riesgo,
                        "cves": [cve["cve"]["id"] for cve in cves]
                    })
            except:
                continue

    output_file = os.path.join(carpeta, "riesgo.json")
    with open(output_file, "w") as f:
        json.dump(resultados, f, indent=4)

    print(f"✅ Análisis completado. Resultados guardados en {output_file}")
    return resultados
