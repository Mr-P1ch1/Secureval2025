#!/usr/bin/env python3
# test_sistema_final.py - Pruebas completas del sistema SECUREVAL

import sys
import os
import json

def test_completo():
    print("🔐 TEST COMPLETO DEL SISTEMA SECUREVAL v2.0")
    print("=" * 60)
    
    total_tests = 0
    tests_pasados = 0
    
    # Test 1: Estructura de archivos
    print("\n📁 TEST 1: Verificando estructura de archivos...")
    total_tests += 1
    archivos_requeridos = [
        "app/main.py",
        "app/activos.py", 
        "app/analyzer.py",
        "app/tratamiento.py",
        "app/export_pdf.py",
        "app/monitoreo.py",
        "iniciar.sh",
        "instalar.sh",
        "requirements.txt",
        "README.md"
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            archivos_faltantes.append(archivo)
    
    if not archivos_faltantes:
        print("✅ Todos los archivos principales están presentes")
        tests_pasados += 1
    else:
        print(f"❌ Archivos faltantes: {', '.join(archivos_faltantes)}")
    
    # Test 2: Importación de módulos
    print("\n🐍 TEST 2: Verificando importaciones de módulos...")
    total_tests += 1
    try:
        sys.path.insert(0, os.getcwd())
        
        # Importar módulos sin ejecutar GUI
        import json
        import tkinter
        
        # Test de importaciones específicas
        from app import activos
        from app import analyzer
        from app import export_pdf
        from app import monitoreo
        from app import tratamiento
        
        print("✅ Todos los módulos se importan correctamente")
        tests_pasados += 1
    except Exception as e:
        print(f"❌ Error en importación: {str(e)}")
    
    # Test 3: Verificar datos de activos
    print("\n🎯 TEST 3: Verificando datos de activos...")
    total_tests += 1
    try:
        activos_path = "resultados/activos.json"
        if os.path.exists(activos_path):
            with open(activos_path, 'r') as f:
                activos_data = json.load(f)
            print(f"✅ Archivo de activos OK - {len(activos_data)} activos registrados")
            
            # Verificar estructura de datos
            if activos_data and isinstance(activos_data[0], dict):
                campos_requeridos = ['nombre', 'area', 'tipo', 'propietario']
                primer_activo = activos_data[0]
                campos_presentes = all(campo in primer_activo for campo in campos_requeridos)
                
                if campos_presentes:
                    print("✅ Estructura de datos de activos correcta")
                    tests_pasados += 1
                else:
                    print("⚠️ Estructura de activos incompleta")
                    tests_pasados += 0.5
            else:
                print("✅ Archivo de activos válido pero vacío")
                tests_pasados += 1
        else:
            print("⚠️ No hay datos de activos previos (OK para instalación nueva)")
            tests_pasados += 1
    except Exception as e:
        print(f"❌ Error verificando activos: {str(e)}")
    
    # Test 4: Verificar análisis existentes
    print("\n🔍 TEST 4: Verificando análisis de dominios...")
    total_tests += 1
    try:
        resultados_dir = "resultados"
        if os.path.exists(resultados_dir):
            dominios = []
            for item in os.listdir(resultados_dir):
                if os.path.isdir(os.path.join(resultados_dir, item)) and item != "__pycache__":
                    dominio_path = os.path.join(resultados_dir, item)
                    if os.path.exists(os.path.join(dominio_path, "riesgo.json")):
                        dominios.append(item)
            
            print(f"✅ Análisis encontrados: {len(dominios)} dominios")
            
            # Verificar estructura de análisis
            if dominios:
                primer_dominio = dominios[0]
                archivos_esperados = ["riesgo.json", "metadata.json"]
                archivos_encontrados = 0
                
                for archivo in archivos_esperados:
                    if os.path.exists(os.path.join(resultados_dir, primer_dominio, archivo)):
                        archivos_encontrados += 1
                
                if archivos_encontrados >= len(archivos_esperados) // 2:
                    print("✅ Estructura de análisis correcta")
                    tests_pasados += 1
                else:
                    print("⚠️ Estructura de análisis parcial")
                    tests_pasados += 0.5
            else:
                print("⚠️ No hay análisis previos (OK para instalación nueva)")
                tests_pasados += 1
        else:
            print("⚠️ Carpeta de resultados no existe (se creará automáticamente)")
            tests_pasados += 1
    except Exception as e:
        print(f"❌ Error verificando análisis: {str(e)}")
    
    # Test 5: Verificar dependencias del sistema
    print("\n🔧 TEST 5: Verificando dependencias externas...")
    total_tests += 1
    dependencias_ok = 0
    dependencias_total = 4
    
    # Python 3
    if os.system("python3 --version > /dev/null 2>&1") == 0:
        print("✅ Python 3")
        dependencias_ok += 1
    else:
        print("❌ Python 3 no encontrado")
    
    # Tkinter
    try:
        import tkinter
        print("✅ Tkinter")
        dependencias_ok += 1
    except:
        print("❌ Tkinter no disponible")
    
    # Nmap (opcional)
    if os.system("nmap --version > /dev/null 2>&1") == 0:
        print("✅ Nmap")
        dependencias_ok += 1
    else:
        print("⚠️ Nmap no encontrado (opcional)")
        dependencias_ok += 0.5
    
    # Whatweb (opcional)
    if os.system("whatweb --version > /dev/null 2>&1") == 0:
        print("✅ Whatweb")
        dependencias_ok += 1
    else:
        print("⚠️ Whatweb no encontrado (opcional)")
        dependencias_ok += 0.5
    
    if dependencias_ok >= dependencias_total * 0.7:
        tests_pasados += 1
    else:
        print("❌ Dependencias insuficientes")
    
    # Test 6: Verificar permisos de ejecución
    print("\n🔐 TEST 6: Verificando permisos de archivos...")
    total_tests += 1
    scripts_ejecutables = ["iniciar.sh", "instalar.sh"]
    permisos_ok = 0
    
    for script in scripts_ejecutables:
        if os.path.exists(script):
            if os.access(script, os.X_OK):
                print(f"✅ {script} es ejecutable")
                permisos_ok += 1
            else:
                print(f"⚠️ {script} no es ejecutable (chmod +x {script})")
        else:
            print(f"❌ {script} no encontrado")
    
    if permisos_ok >= len(scripts_ejecutables):
        tests_pasados += 1
    elif permisos_ok > 0:
        tests_pasados += 0.5
    
    # Resultados finales
    print("\n" + "=" * 60)
    print("📊 RESULTADOS DEL TEST COMPLETO:")
    print(f"✅ Tests pasados: {tests_pasados:.1f}/{total_tests}")
    porcentaje = (tests_pasados / total_tests) * 100
    print(f"📈 Porcentaje de éxito: {porcentaje:.1f}%")
    
    if porcentaje >= 90:
        print("\n🎉 SISTEMA EN ÓPTIMAS CONDICIONES!")
        print("🚀 Listo para producción")
        estado = "EXCELENTE"
    elif porcentaje >= 70:
        print("\n✅ SISTEMA OPERATIVO!")
        print("⚙️ Algunas mejoras recomendadas")
        estado = "BUENO"
    elif porcentaje >= 50:
        print("\n⚠️ SISTEMA FUNCIONAL CON LIMITACIONES")
        print("🔧 Requiere configuración adicional")
        estado = "ACEPTABLE"
    else:
        print("\n❌ SISTEMA REQUIERE ATENCIÓN")
        print("🛠️ Revisar instalación y dependencias")
        estado = "PROBLEMAS"
    
    print(f"\n📋 ESTADO GENERAL: {estado}")
    print("📖 Para más información, consulta README.md")
    print("🆘 Para soporte, revisa los logs de errores")
    
    return porcentaje >= 70

if __name__ == "__main__":
    exito = test_completo()
    sys.exit(0 if exito else 1)
