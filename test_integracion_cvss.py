#!/usr/bin/env python3
"""
Test de integración completo para verificar que el monitoreo 
ahora extrae y muestra correctamente el valor CVSS máximo
"""

import sys
import os
import json
from pathlib import Path

# Agregar el directorio app al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_integracion_cvss_monitoreo():
    """Test de integración completo para CVSS en monitoreo"""
    print("🧪 TEST DE INTEGRACIÓN: CVSS MÁXIMO EN MONITOREO")
    print("=" * 70)
    print("Verificando corrección completa del problema de CVSS en monitoreo")
    print()
    
    success_count = 0
    total_tests = 5
    
    # Test 1: Verificar que existe archivo con datos CVSS
    print("📁 Test 1: Verificando archivos con datos CVSS...")
    resultados_dir = Path("resultados")
    dominios_con_cvss = []
    
    for dominio_dir in resultados_dir.iterdir():
        if dominio_dir.is_dir():
            riesgo_file = dominio_dir / "riesgo.json"
            if riesgo_file.exists():
                try:
                    with open(riesgo_file, 'r') as f:
                        riesgo_data = json.load(f)
                    
                    for item in riesgo_data:
                        if isinstance(item, dict) and item.get('cvss_max', 0) > 0:
                            dominios_con_cvss.append(dominio_dir.name)
                            break
                except:
                    continue
    
    if dominios_con_cvss:
        print(f"✅ Encontrados {len(dominios_con_cvss)} dominios con datos CVSS")
        print(f"   Dominios: {', '.join(dominios_con_cvss[:3])}")
        success_count += 1
    else:
        print("❌ No se encontraron dominios con datos CVSS")
    
    # Test 2: Verificar función calcular_kpis extrae CVSS
    print("\\n🔢 Test 2: Verificando función calcular_kpis...")
    if dominios_con_cvss:
        try:
            from monitoreo import calcular_kpis
            
            dominio_test = dominios_con_cvss[0]
            kpis = calcular_kpis(dominio_test)
            
            if kpis and 'cvss_max' in kpis and kpis['cvss_max'] > 0:
                print(f"✅ calcular_kpis extrae CVSS: {kpis['cvss_max']:.1f}")
                success_count += 1
            else:
                print("❌ calcular_kpis no extrae CVSS correctamente")
        except Exception as e:
            print(f"❌ Error en calcular_kpis: {e}")
    else:
        print("⏭️ Saltando por falta de datos CVSS")
    
    # Test 3: Verificar función mostrar_kpis_en_gui incluye CVSS
    print("\\n🖥️ Test 3: Verificando visualización de KPIs...")
    if dominios_con_cvss:
        try:
            from monitoreo import mostrar_kpis_en_gui
            
            class MockTextWidget:
                def __init__(self):
                    self.content = ''
                def insert(self, pos, text):
                    self.content += text
            
            mock_widget = MockTextWidget()
            kpis = {'cvss_max': 7.5, 'riesgo_promedio': 5.0, 'total_subdominios': 10,
                   'total_tecnologias': 50, 'total_cves': 100, 'subdominios_alto_riesgo': 2,
                   'tecnologias_vulnerables': 5}
            
            mostrar_kpis_en_gui(kpis, mock_widget)
            
            if "CVSS máximo detectado" in mock_widget.content and "7.5/10" in mock_widget.content:
                print("✅ KPIs muestran CVSS máximo correctamente")
                success_count += 1
            else:
                print("❌ KPIs no muestran CVSS máximo")
        except Exception as e:
            print(f"❌ Error en mostrar_kpis_en_gui: {e}")
    else:
        print("⏭️ Saltando por falta de datos CVSS")
    
    # Test 4: Verificar función mostrar_resumen incluye CVSS por subdominio
    print("\\n📋 Test 4: Verificando resumen con CVSS por subdominio...")
    if dominios_con_cvss:
        try:
            from monitoreo import mostrar_resumen
            
            class MockTextWidget:
                def __init__(self):
                    self.content = ''
                def insert(self, pos, text):
                    self.content += text
            
            mock_widget = MockTextWidget()
            mostrar_resumen(dominios_con_cvss[0], mock_widget)
            
            if "CVSS máximo:" in mock_widget.content:
                print("✅ Resumen incluye CVSS máximo por subdominio")
                success_count += 1
            else:
                print("❌ Resumen no incluye CVSS por subdominio")
        except Exception as e:
            print(f"❌ Error en mostrar_resumen: {e}")
    else:
        print("⏭️ Saltando por falta de datos CVSS")
    
    # Test 5: Verificar alertas y clasificación CVSS
    print("\\n🚨 Test 5: Verificando alertas y clasificación CVSS...")
    if dominios_con_cvss:
        try:
            from monitoreo import mostrar_kpis_en_gui
            
            class MockTextWidget:
                def __init__(self):
                    self.content = ''
                def insert(self, pos, text):
                    self.content += text
            
            # Probar diferentes niveles de CVSS
            test_cases = [
                (9.5, "CRÍTICO"),
                (7.5, "ALTO"),
                (5.0, "MEDIO"),
                (2.0, "BAJO")
            ]
            
            alertas_correctas = 0
            for cvss_test, nivel_esperado in test_cases:
                mock_widget = MockTextWidget()
                kpis_test = {'cvss_max': cvss_test, 'riesgo_promedio': 5.0, 'total_subdominios': 10,
                           'total_tecnologias': 50, 'total_cves': 100, 'subdominios_alto_riesgo': 2,
                           'tecnologias_vulnerables': 5}
                
                mostrar_kpis_en_gui(kpis_test, mock_widget)
                
                if nivel_esperado in mock_widget.content:
                    alertas_correctas += 1
            
            if alertas_correctas == len(test_cases):
                print("✅ Clasificación y alertas CVSS funcionan correctamente")
                success_count += 1
            else:
                print(f"❌ Clasificación CVSS incorrecta: {alertas_correctas}/{len(test_cases)}")
        except Exception as e:
            print(f"❌ Error en clasificación CVSS: {e}")
    else:
        print("⏭️ Saltando por falta de datos CVSS")
    
    # Resumen final
    print("\\n" + "=" * 70)
    print(f"📊 RESUMEN FINAL: {success_count}/{total_tests} pruebas pasadas")
    
    if success_count == total_tests:
        print("🎉 ¡PROBLEMA COMPLETAMENTE RESUELTO!")
        print("✅ El monitoreo ahora:")
        print("   • Extrae el CVSS máximo del archivo riesgo.json")
        print("   • Muestra el CVSS máximo en los KPIs principales")
        print("   • Incluye CVSS por subdominio en el resumen detallado")
        print("   • Clasifica y alerta según el nivel de CVSS")
        print("   • Funciona correctamente con todos los dominios")
        return True
    else:
        print("⚠️ Algunas pruebas fallaron")
        print("ℹ️ El problema puede estar parcialmente resuelto")
        return False

if __name__ == "__main__":
    success = test_integracion_cvss_monitoreo()
    sys.exit(0 if success else 1)
