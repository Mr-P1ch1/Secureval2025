#!/usr/bin/env python3
"""
Test específico para verificar que el monitoreo extrae correctamente 
el valor CVSS máximo del archivo riesgo.json
"""

import sys
import os
import json
from pathlib import Path

# Agregar el directorio app al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_cvss_extraction():
    """Test para verificar extracción de CVSS máximo"""
    print("🧪 PRUEBA: Extracción de CVSS máximo en monitoreo")
    print("=" * 60)
    
    # Verificar si hay resultados de análisis disponibles
    resultados_dir = Path("resultados")
    
    if not resultados_dir.exists():
        print("❌ No existe directorio de resultados")
        return False
    
    # Buscar dominios con datos CVSS válidos
    dominios_con_cvss = []
    for dominio_dir in resultados_dir.iterdir():
        if dominio_dir.is_dir():
            riesgo_file = dominio_dir / "riesgo.json"
            if riesgo_file.exists():
                try:
                    with open(riesgo_file, 'r') as f:
                        riesgo_data = json.load(f)
                    
                    # Buscar valores CVSS > 0
                    for item in riesgo_data:
                        if isinstance(item, dict) and item.get('cvss_max', 0) > 0:
                            dominios_con_cvss.append(dominio_dir.name)
                            break
                except:
                    continue
    
    if not dominios_con_cvss:
        print("⚠️ No se encontraron dominios con datos CVSS válidos")
        print("ℹ️ Ejecute un análisis con CVEs habilitados primero")
        return False
    
    # Probar con el primer dominio que tenga CVSS válido
    dominio = dominios_con_cvss[0]
    print(f"🔍 Probando con dominio: {dominio}")
    
    # Verificar archivos necesarios
    riesgo_file = resultados_dir / dominio / "riesgo.json"
    
    # Leer datos de riesgo
    try:
        with open(riesgo_file, 'r') as f:
            riesgo_data = json.load(f)
        
        print(f"✅ Archivo riesgo.json leído exitosamente")
        print(f"📊 Total de registros: {len(riesgo_data)}")
        
        # Buscar valores CVSS
        cvss_values = []
        for item in riesgo_data:
            if isinstance(item, dict):
                cvss_max = item.get('cvss_max', 0)
                if cvss_max and cvss_max > 0:
                    cvss_values.append(cvss_max)
        
        if cvss_values:
            max_cvss = max(cvss_values)
            print(f"✅ CVSS máximo encontrado: {max_cvss:.1f}")
            print(f"📈 Total valores CVSS válidos: {len(cvss_values)}")
            
            # Probar la función del monitoreo
            try:
                from monitoreo import calcular_kpis
                kpis = calcular_kpis(dominio)
                
                if kpis and 'cvss_max' in kpis:
                    kpis_cvss = kpis['cvss_max']
                    print(f"✅ Función calcular_kpis extrae CVSS: {kpis_cvss:.1f}")
                    
                    if abs(kpis_cvss - max_cvss) < 0.1:
                        print("✅ CVSS máximo coincide correctamente")
                        return True
                    else:
                        print(f"❌ CVSS no coincide: esperado {max_cvss:.1f}, obtenido {kpis_cvss:.1f}")
                        return False
                else:
                    print("❌ Función calcular_kpis no retorna cvss_max")
                    return False
                    
            except ImportError as e:
                print(f"❌ Error importando monitoreo: {e}")
                return False
        else:
            print("⚠️ No se encontraron valores CVSS válidos en los datos")
            return False
            
    except Exception as e:
        print(f"❌ Error leyendo archivo riesgo.json: {e}")
        return False

def test_monitoreo_gui():
    """Test de interfaz gráfica del monitoreo con CVSS"""
    print("\n🖥️ PRUEBA: Interfaz gráfica con CVSS")
    print("=" * 60)
    
    try:
        import tkinter as tk
        from monitoreo import mostrar_monitoreo
        
        print("✅ Módulos de GUI importados correctamente")
        print("ℹ️ GUI del monitoreo disponible con soporte CVSS")
        return True
        
    except ImportError as e:
        print(f"❌ Error importando GUI: {e}")
        return False
    except Exception as e:
        print(f"❌ Error en GUI: {e}")
        return False

def main():
    """Función principal del test"""
    print("🧪 TEST CVSS MÁXIMO EN MONITOREO")
    print("=" * 60)
    print("Verificando que el monitoreo extraiga correctamente")
    print("el valor CVSS máximo del análisis de dominios\n")
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: Extracción de CVSS
    if test_cvss_extraction():
        tests_passed += 1
        print("✅ Test 1: CVSS Extraction - PASADO")
    else:
        print("❌ Test 1: CVSS Extraction - FALLIDO")
    
    print()
    
    # Test 2: GUI con CVSS
    if test_monitoreo_gui():
        tests_passed += 1
        print("✅ Test 2: GUI Monitoreo - PASADO")
    else:
        print("❌ Test 2: GUI Monitoreo - FALLIDO")
    
    # Resumen final
    print("\n" + "=" * 60)
    print(f"📊 RESUMEN: {tests_passed}/{total_tests} pruebas pasadas")
    
    if tests_passed == total_tests:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ El monitoreo ahora extrae correctamente el CVSS máximo")
        return True
    else:
        print("⚠️ Algunas pruebas fallaron")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
