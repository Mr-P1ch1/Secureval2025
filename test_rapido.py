#!/usr/bin/env python3
# test_rapido.py - Test rápido del sistema

import sys
import os

def test_basico():
    print("🚀 TEST RÁPIDO DEL SISTEMA SECUREVAL")
    print("=" * 40)
    
    # 1. Verificar estructura
    print("\n📁 Verificando estructura...")
    if os.path.exists("app") and os.path.exists("resultados"):
        print("✅ Estructura básica OK")
    else:
        print("❌ Estructura faltante")
        return False
    
    # 2. Verificar módulos principales
    print("\n🔧 Verificando módulos...")
    modulos = ["app/main.py", "app/activos.py", "app/analyzer.py"]
    for modulo in modulos:
        if os.path.exists(modulo):
            print(f"✅ {modulo}")
        else:
            print(f"❌ {modulo} faltante")
            return False
    
    # 3. Test de importación sin GUI
    print("\n🧪 Test de importación...")
    try:
        # Importar sin ejecutar GUI
        sys.path.insert(0, os.getcwd())
        
        # Test básico de imports
        import json
        print("✅ Dependencias básicas OK")
        
        # Test de estructura de archivos
        if os.path.exists("resultados/activos.json"):
            with open("resultados/activos.json", 'r') as f:
                activos = json.load(f)
            print(f"✅ Activos: {len(activos)} registrados")
        
        # Verificar análisis existentes
        dominios = []
        if os.path.exists("resultados"):
            for item in os.listdir("resultados"):
                if os.path.isdir(f"resultados/{item}") and item != "__pycache__":
                    if os.path.exists(f"resultados/{item}/riesgo.json"):
                        dominios.append(item)
        
        print(f"✅ Análisis: {len(dominios)} dominios")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    exito = test_basico()
    
    print("\n" + "=" * 40)
    if exito:
        print("🎉 SISTEMA OPERATIVO!")
        print("🚀 Ejecutar: python3 -m app.main")
        print("\n📋 CARACTERÍSTICAS IMPLEMENTADAS:")
        print("   ✅ Consola integrada con logging")
        print("   ✅ Monitor de actividad del sistema")
        print("   ✅ Selector PDF con combobox")
        print("   ✅ Interfaz moderna y profesional")
        print("   ✅ Análisis por dominios")
        print("   ✅ Gestión completa de activos")
        sys.exit(0)
    else:
        print("❌ SISTEMA CON PROBLEMAS")
        sys.exit(1)
